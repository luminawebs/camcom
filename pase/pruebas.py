"""Pruebas de punta a punta contra el simulador de Wompi y un Moodle simulado.

    python -m unittest pase.pruebas -v

Cubren los criterios de aceptación 1 a 5 de requerimientos-tablero-pase.md.
"""
import datetime as dt
import http.client
import json
import os
import tempfile
import threading
import time
import unittest
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer

from . import simulador_wompi as simw
from . import wompi as w
from .config import Config
from .moodle import MoodleSimulado
from .nucleo import Pase
from .servidor import App

os.environ["PASE_LOG"] = "0"


class Reloj:
    def __init__(self, fecha):
        self.fecha = fecha

    def __call__(self):
        return self.fecha


def esperar(condicion, maximo=5.0):
    fin = time.time() + maximo
    while time.time() < fin:
        if condicion():
            return True
        time.sleep(0.05)
    return False


class Escenario(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        srv = ThreadingHTTPServer(("127.0.0.1", 0), None)  # reserva puerto del conector
        self.puerto = srv.server_address[1]
        srv.server_close()
        self.sim, self.srv_sim = simw.arrancar(0, f"http://127.0.0.1:{self.puerto}/webhooks/wompi", 0.1)
        api = f"http://127.0.0.1:{self.srv_sim.server_address[1]}"
        self.c = Config(api_wompi=f"{api}/v1", checkout_wompi=f"{api}/p/",
                        llave_publica=simw.LLAVE_PUBLICA, llave_privada=simw.LLAVE_PRIVADA,
                        secreto_integridad=simw.SECRETO_INTEGRIDAD, secreto_eventos=simw.SECRETO_EVENTOS,
                        url_publica=f"http://127.0.0.1:{self.puerto}",
                        base_datos=os.path.join(self.tmp.name, "pase.db"),
                        avisos_correo=["camara@ejemplo.co", "pase@edunest.co"], puerto=self.puerto)
        self.c.validar()
        self.reloj = Reloj(dt.date(2026, 11, 3))
        self.moodle = MoodleSimulado()
        self.pase = Pase(self.c, self.moodle, hoy=self.reloj)
        self.app = App(self.c, self.pase)
        self.srv = ThreadingHTTPServer(("127.0.0.1", self.puerto), self.app.manejador())
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def tearDown(self):
        self.srv.shutdown()
        self.srv_sim.shutdown()
        self.srv.server_close()
        self.srv_sim.server_close()
        self.pase.bd.close()
        self.tmp.cleanup()

    # ----------------------------------------------------------------- ayudas
    def http(self, metodo, url, cuerpo=None, cabeceras=None):
        u = urllib.parse.urlparse(url)
        con = http.client.HTTPConnection(u.hostname, u.port, timeout=10)
        con.request(metodo, u.path + (f"?{u.query}" if u.query else ""), cuerpo, cabeceras or {})
        r = con.getresponse()
        return r.status, dict(r.getheaders()), r.read()

    def inscribir_por_formulario(self, opcion="pase", correo="dora@tienda.co", doc="52111222"):
        datos = urllib.parse.urlencode({
            "canal": "wa-afiliados", "nombre": "Dora Pérez", "tipo_doc": "CC", "documento": doc,
            "correo": correo, "whatsapp": "3001234567", "negocio": "Tienda Dora",
            "municipio": "Soacha", "acepta_datos": "on", "opcion": opcion})
        return self.http("POST", f"{self.c.url_publica}/inscripcion", datos,
                         {"Content-Type": "application/x-www-form-urlencoded"})

    def tokenizar(self, ruta, cuerpo):
        req = urllib.request.Request(f"{self.c.api_wompi}{ruta}", json.dumps(cuerpo).encode(),
                                     {"Authorization": f"Bearer {self.c.llave_publica}",
                                      "Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req).read())["data"]

    def pagar_tarjeta(self, numero="4242424242424242", correo="dora@tienda.co"):
        status, cab, _ = self.inscribir_por_formulario(correo=correo)
        self.assertEqual(status, 303)
        firma = urllib.parse.parse_qs(urllib.parse.urlparse(cab["Location"]).query)["p"][0]
        _, _, pagina = self.http("GET", f"{self.c.url_publica}/pagar?p={firma}")
        self.assertIn(b"Pase Empresario", pagina)
        tok = self.tokenizar("/tokens/cards", {"number": numero, "cvc": "123", "exp_month": "08",
                                               "exp_year": "28", "card_holder": "Dora Perez"})
        comercio = self.pase.wompi.comercio()
        status, _, cuerpo = self.http("POST", f"{self.c.url_publica}/pagar/token", json.dumps({
            "p": firma, "tipo": "CARD", "token": tok["id"],
            "acept": comercio["aceptacion"]["acceptance_token"],
            "datos": comercio["datos_personales"]["acceptance_token"], "enmascarado": "**** 4242"}),
            {"Content-Type": "application/json"})
        self.assertEqual(status, 200, cuerpo)
        return int(firma.split(".")[0]), json.loads(cuerpo)["referencia"]

    def estado_persona(self, pid):
        return self.pase.persona(pid)["estado"]

    def en_cohorte(self, pid, cohorte):
        uid = self.pase.persona(pid)["moodle_user_id"]
        return uid is not None and uid in self.moodle.cohortes.get(cohorte, set())

    def esperar_estado(self, pid, estado):
        self.assertTrue(esperar(lambda: self.estado_persona(pid) == estado),
                        f"esperaba {estado}, está {self.estado_persona(pid)}")


class PruebasFirmas(unittest.TestCase):
    def test_firma_integridad(self):
        import hashlib
        esperado = hashlib.sha256(b"PASE-1-202611-12900000COPsecreto").hexdigest()
        self.assertEqual(w.firma_integridad("PASE-1-202611-1", 2900000, "COP", "secreto"), esperado)

    def test_checksum_evento(self):
        sim = simw.Simulador(None)
        ev = sim.evento({"id": "1-2", "status": "APPROVED", "amount_in_cents": 2900000})
        self.assertTrue(w.evento_valido(ev, simw.SECRETO_EVENTOS))
        ev["data"]["transaction"]["status"] = "VOIDED"
        self.assertFalse(w.evento_valido(ev, simw.SECRETO_EVENTOS))

    def test_candado_produccion(self):
        os.environ.pop("PASE_PERMITIR_PRODUCCION", None)
        with self.assertRaises(ValueError):
            Config(entorno="produccion", llave_privada="prv_prod_x").validar()
        with self.assertRaises(ValueError):
            Config(entorno="sandbox", llave_privada="prv_prod_x").validar()


class PruebasFlujo(Escenario):
    def test_1_tarjeta_aprobada_matricula_en_menos_de_1_minuto(self):
        inicio = time.time()
        pid, ref = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        self.assertLess(time.time() - inicio, 60)
        self.assertTrue(self.en_cohorte(pid, "pase-empresario"))
        self.assertTrue(self.en_cohorte(pid, "registro-gratis"))
        destinos = {r["para"] for r in self.pase.q("SELECT para FROM avisos")}
        self.assertEqual(destinos, {"dora@tienda.co", "camara@ejemplo.co", "pase@edunest.co"})
        sus = self.pase.suscripcion(pid)
        self.assertEqual((sus["estado"], sus["proximo_corte"], sus["medio_enmascarado"]),
                         ("activa", "2026-12-03", "**** 4242"))
        _, _, est = self.http("GET", f"{self.c.url_publica}/estado-pago?ref={ref}")
        self.assertEqual(json.loads(est)["estado"], "APPROVED")

    def test_2_evento_repetido_no_duplica(self):
        pid, _ = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        antes = (self.pase.uno("SELECT COUNT(*) n FROM historial")["n"], len(self.moodle.llamadas))
        status, _, _ = self.http("POST", f"{self.sim.webhook}", json.dumps(self.sim.eventos_enviados[-1]),
                                 {"Content-Type": "application/json"})
        self.assertEqual(status, 200)
        self.pase.procesar_pendientes()
        despues = (self.pase.uno("SELECT COUNT(*) n FROM historial")["n"], len(self.moodle.llamadas))
        self.assertEqual(antes, despues)
        self.assertEqual(self.pase.uno("SELECT COUNT(*) n FROM eventos_wompi")["n"], 1)

    def test_3_firma_alterada_se_rechaza(self):
        pid, _ = self.pagar_tarjeta("4111111111111111")  # rechazada: sigue interesado
        self.assertTrue(esperar(lambda: self.pase.uno("SELECT estado FROM pagos")["estado"] == "DECLINED"))
        falso = json.loads(json.dumps(self.sim.eventos_enviados[-1]))
        falso["data"]["transaction"]["status"] = "APPROVED"  # alguien intenta aprobarse solo
        status, _, _ = self.http("POST", self.sim.webhook, json.dumps(falso), {"Content-Type": "application/json"})
        self.assertEqual(status, 401)
        self.assertEqual(self.pase.resumen()["eventos_rechazados"], 1)
        self.assertEqual(self.estado_persona(pid), "interesado")
        self.assertFalse(self.en_cohorte(pid, "pase-empresario"))

    def test_3b_retorno_del_navegador_no_activa(self):
        pid, ref = self.pagar_tarjeta("4111111111111111")
        self.http("GET", f"{self.c.url_publica}/retorno?ref={ref}&id=cualquiera")
        time.sleep(0.4)
        self.assertEqual(self.estado_persona(pid), "interesado")

    def test_4_tres_rechazos_cancelan_y_pagar_reactiva(self):
        pid, _ = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        fuente = int(self.pase.suscripcion(pid)["payment_source_id"])
        for dia in ("2026-12-03", "2026-12-06", "2026-12-10"):
            self.reloj.fecha = dt.date.fromisoformat(dia)
            self.sim.forzado[fuente] = "DECLINED"
            self.assertTrue(self.pase.cobro_mensual(), f"no cobró el {dia}")
            self.assertTrue(esperar(lambda: self.pase.uno(
                "SELECT COUNT(*) n FROM pagos WHERE estado='DECLINED'")["n"] == ["2026-12-03", "2026-12-06",
                                                                                  "2026-12-10"].index(dia) + 1))
            time.sleep(0.1)
        self.esperar_estado(pid, "cancelado")
        self.assertFalse(self.en_cohorte(pid, "pase-empresario"))
        self.assertTrue(self.en_cohorte(pid, "registro-gratis"))  # avance y cursos gratis intactos
        # un día sin nada que cobrar
        self.reloj.fecha = dt.date(2026, 12, 11)
        self.assertEqual(self.pase.cobro_mensual(), [])
        # vuelve a pagar con otra tarjeta
        self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        self.assertTrue(self.en_cohorte(pid, "pase-empresario"))
        eventos = [r["evento"] for r in self.pase.q("SELECT evento FROM historial WHERE persona_id=?", pid)]
        self.assertIn("cancelo", eventos)
        self.assertIn("reactivo", eventos)

    def test_4b_cobro_mensual_aprobado_renueva(self):
        pid, _ = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        self.reloj.fecha = dt.date(2026, 12, 2)
        self.assertEqual(self.pase.cobro_mensual(), [])  # aún no es el corte
        self.reloj.fecha = dt.date(2026, 12, 3)
        self.assertEqual(len(self.pase.cobro_mensual()), 1)
        self.esperar_estado(pid, "activo")
        self.assertEqual(self.pase.suscripcion(pid)["proximo_corte"], "2027-01-03")
        self.assertEqual(self.pase.cobro_mensual(), [])  # el mismo día no cobra dos veces

    def test_4c_cancelacion_voluntaria_al_corte(self):
        pid, _ = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        self.pase.pedir_cancelacion(pid)
        self.reloj.fecha = dt.date(2026, 12, 3)
        self.assertEqual(self.pase.cobro_mensual(), [(pid, "cancelada")])
        self.assertEqual(self.pase.uno("SELECT COUNT(*) n FROM pagos")["n"], 1)
        self.assertFalse(self.en_cohorte(pid, "pase-empresario"))

    def test_5_registro_gratis(self):
        status, _, cuerpo = self.inscribir_por_formulario("gratis")
        self.assertEqual(status, 200, cuerpo)
        pid = self.pase.uno("SELECT id FROM personas")["id"]
        self.assertEqual(self.estado_persona(pid), "registro_gratis")
        self.assertTrue(self.en_cohorte(pid, "registro-gratis"))
        self.assertFalse(self.en_cohorte(pid, "pase-empresario"))
        # mismo documento con otro canal: no duplica
        self.inscribir_por_formulario("gratis")
        self.assertEqual(self.pase.uno("SELECT COUNT(*) n FROM personas")["n"], 1)

    def test_nequi(self):
        status, cab, _ = self.inscribir_por_formulario()
        firma = urllib.parse.parse_qs(urllib.parse.urlparse(cab["Location"]).query)["p"][0]
        pid = int(firma.split(".")[0])
        tok = self.tokenizar("/tokens/nequi", {"phone_number": "3991111111"})
        self.assertTrue(esperar(lambda: self.pase.wompi._llamar("GET", f"/tokens/nequi/{tok['id']}")
                                ["data"]["status"] == "APPROVED"))
        acept = self.pase.wompi.comercio()["aceptacion"]["acceptance_token"]
        self.pase.pagar_con_token(pid, "NEQUI", tok["id"], acept)
        self.esperar_estado(pid, "suscrito")
        self.assertEqual(self.pase.suscripcion(pid)["medio"], "nequi")

    def test_pse_web_checkout_y_renovacion_manual(self):
        status, cab, _ = self.inscribir_por_formulario()
        firma = urllib.parse.parse_qs(urllib.parse.urlparse(cab["Location"]).query)["p"][0]
        pid = int(firma.split(".")[0])
        status, cab, _ = self.http("GET", f"{self.c.url_publica}/pagar/pse?p={firma}")
        self.assertEqual(status, 302)
        checkout = cab["Location"]
        _, _, pag = self.http("GET", checkout)
        self.assertIn(b"Aprobar", pag)  # la firma de integridad fue aceptada
        q = urllib.parse.urlparse(checkout).query
        status, cab, _ = self.http("POST", f"{self.c.checkout_wompi}pagar?{q}", "r=APPROVED",
                                   {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertTrue(cab["Location"].startswith(f"{self.c.url_publica}/retorno?id="))
        self.esperar_estado(pid, "suscrito")
        self.assertTrue(self.pase.suscripcion(pid)["renovacion_manual"])
        # 5 días antes del corte llega el enlace; si no paga, se cancela al agotar el plazo
        self.reloj.fecha = dt.date(2026, 11, 28)
        self.assertEqual(len(self.pase.cobro_mensual()), 1)
        self.assertTrue(self.pase.uno("SELECT 1 FROM avisos WHERE asunto LIKE 'Renueva%'"))
        self.reloj.fecha = dt.date(2026, 12, 4)
        self.pase.cobro_mensual()
        self.assertEqual(self.estado_persona(pid), "en_mora")
        self.reloj.fecha = dt.date(2026, 12, 11)
        self.pase.cobro_mensual()
        self.assertEqual(self.estado_persona(pid), "cancelado")

    def test_monto_alterado_no_activa(self):
        pid, ref = self.pagar_tarjeta("4111111111111111")
        with self.assertRaises(ValueError):
            self.pase.aplicar_transaccion({"id": "x", "reference": ref, "amount_in_cents": 100,
                                           "currency": "COP", "status": "APPROVED"})
        self.assertEqual(self.estado_persona(pid), "interesado")

    def test_conciliacion_recupera_evento_perdido(self):
        self.sim.webhook = None  # Wompi no logra avisar
        pid, _ = self.pagar_tarjeta()
        time.sleep(0.3)
        self.assertEqual(self.estado_persona(pid), "interesado")
        self.assertEqual(self.pase.conciliar(), 1)
        self.assertEqual(self.estado_persona(pid), "suscrito")


if __name__ == "__main__":
    unittest.main()
