"""Pruebas de punta a punta contra el simulador de ePayco y un Moodle simulado.

    python -m unittest pase.pruebas -v

Cubren los criterios de aceptación 1 a 5 de requerimientos-tablero-pase.md.
"""
import datetime as dt
import hashlib
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
from unittest import mock

from . import epayco as ep
from . import simulador_epayco as sime
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
        self.sim, self.srv_sim = sime.arrancar(0, 0.1)
        self.api = f"http://127.0.0.1:{self.srv_sim.server_address[1]}"
        self.c = Config(api_epayco=self.api, validacion_epayco=self.api, restpagos_epayco=self.api, apify_epayco=self.api,
                        checkout_js=f"{self.api}/checkout-v2.js", token_js=f"{self.api}/epayco.js",
                        cliente_id=sime.CLIENTE_ID, p_key=sime.P_KEY,
                        llave_publica=sime.LLAVE_PUBLICA, llave_privada=sime.LLAVE_PRIVADA,
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

    def firma_inscripcion(self):
        status, cab, _ = self.inscribir_por_formulario()
        self.assertEqual(status, 303)
        return urllib.parse.parse_qs(urllib.parse.urlparse(cab["Location"]).query)["p"][0]

    def tokenizar(self, numero):
        """Lo que hace epayco.js en el navegador."""
        req = urllib.request.Request(f"{self.api}/v1/tokens/navegador", json.dumps({
            "public_key": self.c.llave_publica, "card[number]": numero, "card[cvc]": "123",
            "card[exp_month]": "08", "card[exp_year]": "2028", "card[name]": "Dora Perez"}).encode(),
            {"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req).read())["id"]

    def pagar_tarjeta(self, numero=sime.TARJETA_APRUEBA):
        firma = self.firma_inscripcion()
        _, _, pagina = self.http("GET", f"{self.c.url_publica}/pagar?p={firma}")
        self.assertIn(b"Pase Empresario", pagina)
        self.assertIn(b'data-epayco="card[number]"', pagina)
        status, _, cuerpo = self.http("POST", f"{self.c.url_publica}/pagar/token", json.dumps({
            "p": firma, "token": self.tokenizar(numero), "enmascarado": "**** " + numero[-4:]}),
            {"Content-Type": "application/json"})
        self.assertEqual(status, 200, cuerpo)
        return int(firma.split(".")[0]), json.loads(cuerpo)["referencia"]

    def pagar_checkout(self, firma, resultado="APPROVED", seguir_retorno=True):
        status, cab, _ = self.http("GET", f"{self.c.url_publica}/pagar/checkout?p={firma}")
        self.assertEqual(status, 302)
        retorno = self.pagar_en_checkout(cab["Location"], resultado)
        self.assertTrue(retorno.startswith(f"{self.c.url_publica}/retorno?ref="))
        if seguir_retorno:
            self.http("GET", retorno)
        return retorno

    def pagar_en_checkout(self, enlace, resultado="APPROVED"):
        """Abre nuestra página /checkout (crea la sesión v2) y paga en el Smart Checkout simulado."""
        status, _, pagina = self.http("GET", enlace)
        self.assertEqual(status, 200)
        self.assertIn(self.c.checkout_js.encode(), pagina)
        datos = json.loads(pagina.split(b"ePayco.checkout.configure(")[1].split(b").open()")[0])
        self.assertEqual((datos["type"], datos["test"]), ("standard", True))
        self.assertIn(datos["sessionId"], self.sim.sesiones)
        q = urllib.parse.urlencode({"session": datos["sessionId"], "test": "true"})
        _, cab, _ = self.http("POST", f"{self.api}/checkout/pagar?{q}", f"r={resultado}",
                              {"Content-Type": "application/x-www-form-urlencoded"})
        return cab["Location"]

    def ultima_confirmacion(self):
        return dict(self.sim.confirmaciones[-1][1])

    def confirmar(self, datos):
        return self.http("POST", f"{self.c.url_publica}/webhooks/epayco", urllib.parse.urlencode(datos),
                         {"Content-Type": "application/x-www-form-urlencoded"})[0]

    def estado_persona(self, pid):
        return self.pase.persona(pid)["estado"]

    def en_cohorte(self, pid, cohorte):
        uid = self.pase.persona(pid)["moodle_user_id"]
        return uid is not None and uid in self.moodle.cohortes.get(cohorte, set())

    def esperar_estado(self, pid, estado):
        self.assertTrue(esperar(lambda: self.estado_persona(pid) == estado),
                        f"esperaba {estado}, está {self.estado_persona(pid)}")

    def fuente(self, pid):
        return json.loads(self.pase.suscripcion(pid)["payment_source_id"])


class PruebasFirmas(unittest.TestCase):
    def test_firma_confirmacion(self):
        esperado = hashlib.sha256(b"900001^pkey^123456^987654321^29000.00^COP").hexdigest()
        self.assertEqual(ep.firma_confirmacion("900001", "pkey", "123456", "987654321", "29000.00", "COP"),
                         esperado)
        datos = {"x_ref_payco": "123456", "x_transaction_id": "987654321", "x_amount": "29000.00",
                 "x_currency_code": "COP", "x_signature": esperado.upper()}
        self.assertTrue(ep.confirmacion_valida(datos, "900001", "pkey"))
        self.assertFalse(ep.confirmacion_valida({**datos, "x_amount": "100.00"}, "900001", "pkey"))
        self.assertFalse(ep.confirmacion_valida(datos, "900001", "otra"))
        self.assertFalse(ep.confirmacion_valida(datos, "", ""))  # sin llaves no se acepta nada

    def test_normalizar(self):
        tx = ep.normalizar({"x_ref_payco": 77, "x_id_invoice": "PASE-1", "x_amount": "29000.00",
                            "x_currency_code": "cop", "x_cod_transaction_state": "1",
                            "x_test_request": "TRUE", "x_franchise": "PSE"})
        self.assertEqual((tx["id"], tx["reference"], tx["amount_in_cents"], tx["currency"], tx["status"],
                          tx["prueba"]), ("77", "PASE-1", 2900000, "COP", "APPROVED", True))
        for codigo, estado in (("2", "DECLINED"), ("3", "PENDING"), ("4", "ERROR"), ("6", "VOIDED"),
                               ("10", "DECLINED"), ("99", "PENDING")):
            self.assertEqual(ep.normalizar({"x_ref_payco": 1, "x_amount": "1", "x_cod_response": codigo})
                             ["status"], estado)

    def test_nombre_usuario_moodle(self):
        from .moodle import nombre_usuario
        self.assertEqual(nombre_usuario(" Dora+Pase1@Tienda.co "), "dora-pase1@tienda.co")

    def test_candado_produccion(self):
        os.environ.pop("PASE_PERMITIR_PRODUCCION", None)
        llaves = dict(cliente_id="1", p_key="k", llave_publica="a", llave_privada="b",
                      url_publica="https://pase.edunest.co")
        with self.assertRaises(ValueError):
            Config(entorno="produccion", **llaves).validar()
        os.environ["PASE_PERMITIR_PRODUCCION"] = "1"
        try:
            Config(entorno="produccion", **llaves).validar()
            with self.assertRaises(ValueError):
                Config(entorno="produccion", **{**llaves, "p_key": ""}).validar()
        finally:
            os.environ.pop("PASE_PERMITIR_PRODUCCION")
        with self.assertRaises(ValueError):
            Config(entorno="pruebas").validar()


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
                         ("activa", "2026-12-03", "**** 0326"))
        self.assertEqual(set(self.fuente(pid)), {"cliente", "token"})  # solo ids, nada de la tarjeta
        _, _, est = self.http("GET", f"{self.c.url_publica}/estado-pago?ref={ref}")
        self.assertEqual(json.loads(est)["estado"], "APPROVED")

    def test_1b_tablero_con_usuario_y_clave(self):
        pid, _ = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        url = f"{self.c.url_publica}/tablero"
        form = {"Content-Type": "application/x-www-form-urlencoded"}
        entrar = lambda u, c, ip="1.1.1.1": self.app.entrar_admin(u, c, ip)
        with mock.patch.dict(os.environ, {"PASE_ADMIN_USUARIO": "", "PASE_ADMIN_CLAVE": ""}):
            self.assertIn("aún no tiene usuario", self.http("GET", url)[2].decode())
        with mock.patch.dict(os.environ, {"PASE_ADMIN_USUARIO": "david", "PASE_ADMIN_CLAVE": "clave-larga-1"}):
            status, _, cuerpo = self.http("GET", url)
            self.assertEqual(status, 200)
            self.assertIn('name="clave"', cuerpo.decode())
            self.assertNotIn("Pases activos", cuerpo.decode())
            self.assertEqual(self.http("GET", url + "/pagos.csv")[0], 303)
            mala = urllib.parse.urlencode({"usuario": "david", "clave": "otra"})
            self.assertEqual(self.http("POST", url + "/entrar", mala, form)[0], 401)
            buena = urllib.parse.urlencode({"usuario": "david", "clave": "clave-larga-1"})
            status, cab, _ = self.http("POST", url + "/entrar", buena, form)
            self.assertEqual(status, 303)
            self.assertIn("HttpOnly", cab["Set-Cookie"])
            galleta = {"Cookie": cab["Set-Cookie"].split(";")[0]}
            texto = self.http("GET", url, cabeceras=galleta)[2].decode()
            for esperado in ("Pases activos", "$29.000", "wa-afiliados", "Dora Pérez", "Modo PRUEBAS"):
                self.assertIn(esperado, texto)
            status, cab, csv_ = self.http("GET", url + "/pagos.csv", cabeceras=galleta)
            self.assertEqual((status, cab["Content-Type"]), (200, "text/csv; charset=utf-8"))
            self.assertIn("52111222", csv_.decode("utf-8-sig"))
            self.assertNotIn("0326", csv_.decode("utf-8-sig"))  # nada de la tarjeta
            falsa = {"Cookie": "pase_admin=9999999999.abc"}
            self.assertNotIn("Pases activos", self.http("GET", url, cabeceras=falsa)[2].decode())
            # 5 fallos bloquean esa IP 15 minutos, aunque luego ponga la clave buena
            for _ in range(5):
                self.assertIsNone(entrar("david", "x", "2.2.2.2"))
            self.assertIsNone(entrar("david", "clave-larga-1", "2.2.2.2"))
            self.assertTrue(entrar("david", "clave-larga-1", "3.3.3.3"))
        # cambiar la contraseña cierra las sesiones abiertas
        with mock.patch.dict(os.environ, {"PASE_ADMIN_USUARIO": "david", "PASE_ADMIN_CLAVE": "otra-clave-22"}):
            self.assertNotIn("Pases activos", self.http("GET", url, cabeceras=galleta)[2].decode())
        d = self.pase.tablero()
        self.assertEqual((d["suscripciones"], d["recaudo_total_cop"]), ({"activa": 1}, 29000))

    def test_2_confirmacion_repetida_no_duplica(self):
        pid, _ = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        antes = (self.pase.uno("SELECT COUNT(*) n FROM historial")["n"], len(self.moodle.llamadas))
        self.assertEqual(self.confirmar(self.ultima_confirmacion()), 200)
        self.pase.procesar_pendientes()
        despues = (self.pase.uno("SELECT COUNT(*) n FROM historial")["n"], len(self.moodle.llamadas))
        self.assertEqual(antes, despues)
        self.assertEqual(self.pase.uno("SELECT COUNT(*) n FROM eventos_pasarela")["n"], 1)

    def test_3_firma_alterada_se_rechaza(self):
        pid, _ = self.pagar_tarjeta(sime.TARJETA_RECHAZA)  # rechazada: sigue interesado
        self.assertTrue(esperar(lambda: self.pase.uno("SELECT estado FROM pagos")["estado"] == "DECLINED"))
        falso = self.ultima_confirmacion()
        falso["x_amount"] = "100"  # alguien cambia el monto sin poder firmar
        self.assertEqual(self.confirmar(falso), 401)
        self.assertEqual(self.pase.resumen()["eventos_rechazados"], 1)
        self.assertEqual(self.estado_persona(pid), "interesado")
        self.assertFalse(self.en_cohorte(pid, "pase-empresario"))

    def test_3a_estado_alterado_no_activa(self):
        # La firma de ePayco no cubre el estado: por eso se consulta siempre la API.
        pid, _ = self.pagar_tarjeta(sime.TARJETA_RECHAZA)
        self.assertTrue(esperar(lambda: self.pase.uno("SELECT estado FROM pagos")["estado"] == "DECLINED"))
        falso = self.ultima_confirmacion()
        falso.update(x_cod_response="1", x_cod_transaction_state="1", x_respuesta="Aceptada")
        self.assertEqual(self.confirmar(falso), 200)
        self.pase.procesar_pendientes()
        self.assertEqual(self.estado_persona(pid), "interesado")
        self.assertFalse(self.en_cohorte(pid, "pase-empresario"))
        self.assertEqual(self.pase.uno("SELECT estado FROM pagos")["estado"], "DECLINED")

    def test_3b_retorno_del_navegador_no_activa(self):
        pid, ref = self.pagar_tarjeta(sime.TARJETA_RECHAZA)
        self.http("GET", f"{self.c.url_publica}/retorno?ref={ref}&ref_payco=123")
        time.sleep(0.4)
        self.assertEqual(self.estado_persona(pid), "interesado")

    def test_3c_transaccion_de_prueba_no_sirve_en_produccion(self):
        pid, ref = self.pagar_tarjeta(sime.TARJETA_RECHAZA)
        self.c.entorno = "produccion"
        with self.assertRaises(ValueError):
            self.pase.aplicar_transaccion({"id": "1", "reference": ref, "amount_in_cents": 2900000,
                                           "currency": "COP", "status": "APPROVED", "prueba": True})
        self.c.entorno = "sandbox"
        self.assertEqual(self.estado_persona(pid), "interesado")

    def test_4_tres_rechazos_cancelan_y_pagar_reactiva(self):
        pid, _ = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        fuente = self.fuente(pid)
        for n, dia in enumerate(("2026-12-03", "2026-12-06", "2026-12-10"), 1):
            self.reloj.fecha = dt.date.fromisoformat(dia)
            self.sim.forzado[fuente["token"]] = "DECLINED"
            self.assertTrue(self.pase.cobro_mensual(), f"no cobró el {dia}")
            self.assertTrue(esperar(lambda: self.pase.uno(
                "SELECT COUNT(*) n FROM pagos WHERE estado='DECLINED'")["n"] == n))
            time.sleep(0.1)
        self.esperar_estado(pid, "cancelado")
        self.assertFalse(self.en_cohorte(pid, "pase-empresario"))
        self.assertTrue(self.en_cohorte(pid, "registro-gratis"))  # avance y cursos gratis intactos
        self.assertEqual(self.sim.clientes[fuente["cliente"]]["cards"], [])  # no se le vuelve a cobrar
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

    def test_4d_reversion_vuelve_a_mora(self):
        pid, _ = self.pagar_tarjeta()
        self.esperar_estado(pid, "suscrito")
        ref_payco = self.pase.uno("SELECT ref_pasarela FROM pagos")["ref_pasarela"]
        self.sim.cambiar_estado(ref_payco, "VOIDED")
        self.esperar_estado(pid, "en_mora")

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

    def test_checkout_y_renovacion_manual(self):
        firma = self.firma_inscripcion()
        pid = int(firma.split(".")[0])
        self.pagar_checkout(firma)
        self.esperar_estado(pid, "suscrito")
        sus = self.pase.suscripcion(pid)
        self.assertEqual((sus["medio"], sus["renovacion_manual"]), ("checkout", 1))
        # 5 días antes del corte llega el enlace; si no paga, se cancela al agotar el plazo
        self.reloj.fecha = dt.date(2026, 11, 28)
        self.assertEqual(len(self.pase.cobro_mensual()), 1)
        aviso = self.pase.uno("SELECT cuerpo FROM avisos WHERE asunto LIKE 'Renueva%'")["cuerpo"]
        enlace = aviso.split("Renovar mi Pase: ")[1].split("\n")[0]
        status, _, pagina = self.http("GET", enlace)
        self.assertEqual(status, 200)
        self.assertIn(b"ePayco.checkout.configure(", pagina)
        sesion = list(self.sim.sesiones.values())[-1]
        self.assertEqual((sesion["amount"], sesion["currency"], sesion["confirmation"]),
                         (29000, "COP", f"{self.c.url_publica}/webhooks/epayco"))
        status, _, _ = self.http("GET", enlace.replace("&f=", "&f=0"))  # enlace adulterado
        self.assertEqual(status, 404)
        self.reloj.fecha = dt.date(2026, 12, 4)
        self.pase.cobro_mensual()
        self.assertEqual(self.estado_persona(pid), "en_mora")
        self.reloj.fecha = dt.date(2026, 12, 11)
        self.pase.cobro_mensual()
        self.assertEqual(self.estado_persona(pid), "cancelado")

    def test_checkout_renovacion_pagada(self):
        firma = self.firma_inscripcion()
        pid = int(firma.split(".")[0])
        self.pagar_checkout(firma)
        self.esperar_estado(pid, "suscrito")
        self.reloj.fecha = dt.date(2026, 11, 29)
        self.pase.cobro_mensual()
        enlace = self.pase.uno("SELECT cuerpo FROM avisos WHERE asunto LIKE 'Renueva%'")["cuerpo"].split(
            "Renovar mi Pase: ")[1].split("\n")[0]
        self.pagar_en_checkout(enlace)
        self.esperar_estado(pid, "activo")
        self.assertEqual(self.pase.suscripcion(pid)["proximo_corte"], "2027-01-03")
        status, _, _ = self.http("GET", enlace)  # ya pagado: el enlace deja de servir
        self.assertEqual(status, 404)

    def test_monto_alterado_no_activa(self):
        pid, ref = self.pagar_tarjeta(sime.TARJETA_RECHAZA)
        with self.assertRaises(ValueError):
            self.pase.aplicar_transaccion({"id": "x", "reference": ref, "amount_in_cents": 100,
                                           "currency": "COP", "status": "APPROVED"})
        self.assertEqual(self.estado_persona(pid), "interesado")

    def test_conciliacion_recupera_confirmacion_perdida(self):
        self.sim.avisar = False  # ePayco no logra llamar a la URL de confirmación
        pid, _ = self.pagar_tarjeta()
        time.sleep(0.3)
        self.assertEqual(self.estado_persona(pid), "interesado")
        self.assertEqual(self.pase.conciliar(), 1)
        self.assertEqual(self.estado_persona(pid), "suscrito")

    def test_conciliacion_checkout_con_ref_del_retorno(self):
        self.sim.avisar = False
        firma = self.firma_inscripcion()
        pid = int(firma.split(".")[0])
        retorno = self.pagar_checkout(firma)
        ref_payco = urllib.parse.parse_qs(urllib.parse.urlparse(retorno).query)["ref_payco"][0]
        self.assertFalse(ref_payco.isdigit())  # formato alfanumérico del Smart Checkout v2
        self.assertEqual(self.pase.uno("SELECT ref_pasarela FROM pagos")["ref_pasarela"], ref_payco)
        time.sleep(0.3)
        self.assertEqual(self.estado_persona(pid), "interesado")
        self.assertEqual(self.pase.conciliar(), 1)
        self.assertEqual(self.estado_persona(pid), "suscrito")

    def test_moodle_caido_no_deja_pago_aprobado_sin_matricula(self):
        original, fallos = self.moodle.agregar_a_cohorte, []

        def caido(uid, cohorte):
            if cohorte == "pase-empresario" and not fallos:
                fallos.append(cohorte)
                raise RuntimeError("Moodle no responde")
            return original(uid, cohorte)
        self.moodle.agregar_a_cohorte = caido
        pid, ref = self.pagar_tarjeta()
        self.assertTrue(esperar(lambda: fallos and self.pase.uno(
            "SELECT error FROM eventos_pasarela")["error"]))
        self.assertEqual(self.estado_persona(pid), "interesado")
        self.assertNotEqual(self.pase.uno("SELECT estado FROM pagos WHERE referencia=?", ref)["estado"],
                            "APPROVED")
        self.assertEqual(self.pase.procesar_pendientes(), 1)  # Moodle volvió
        self.assertEqual(self.estado_persona(pid), "suscrito")
        self.assertTrue(self.en_cohorte(pid, "pase-empresario"))

    def test_base_de_wompi_no_arranca(self):
        import sqlite3
        ruta = os.path.join(self.tmp.name, "vieja.db")
        con = sqlite3.connect(ruta)
        con.execute("CREATE TABLE eventos_wompi (id INTEGER)")
        con.close()  # en Windows un archivo abierto no deja borrar la carpeta temporal
        with self.assertRaises(RuntimeError):
            Pase(Config(base_datos=ruta), self.moodle)


class SmtpFalso:
    """Hace de conexión SMTP: guarda lo enviado y falla con las direcciones de `rechazar`."""

    def __init__(self, rechazar=()):
        self.enviados, self.rechazar, self.abierto = [], set(rechazar), False

    def __enter__(self):
        self.abierto = True
        return self

    def __exit__(self, *_):
        self.abierto = False

    def enviar(self, para, asunto, cuerpo, html=None):
        assert self.abierto
        if para in self.rechazar:
            raise RuntimeError("550 buzón no existe")
        self.enviados.append((para, asunto))


class Correos(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.c = Config(base_datos=os.path.join(self.tmp.name, "pase.db"))
        self.pase = Pase(self.c, MoodleSimulado())

    def tearDown(self):
        self.pase.bd.close()
        self.tmp.cleanup()

    def test_envia_pendientes_y_reintenta_fallidos(self):
        self.pase.avisar(["ana@ejemplo.co", "malo@ejemplo.co"], "Hola", "Cuerpo")
        smtp = SmtpFalso(rechazar={"malo@ejemplo.co"})
        self.assertEqual(self.pase.enviar_avisos(smtp), {"enviados": 1, "fallidos": 1})
        self.assertEqual(smtp.enviados, [("ana@ejemplo.co", "Hola")])
        malo = self.pase.uno("SELECT * FROM avisos WHERE para='malo@ejemplo.co'")
        self.assertIsNone(malo["enviado_en"])
        self.assertIn("550", malo["error"])
        for _ in range(10):
            self.pase.enviar_avisos(smtp)
        self.assertEqual(self.pase.uno("SELECT intentos FROM avisos WHERE id=?", malo["id"])["intentos"], 5)
        self.assertEqual(len(smtp.enviados), 1)  # el bueno no se repite

    def test_dos_corridas_a_la_vez_no_repiten(self):
        self.pase.avisar("ana@ejemplo.co", "Hola", "Cuerpo")
        otra = Pase(self.c, MoodleSimulado())
        smtp = SmtpFalso()

        class SmtpQueCruza(SmtpFalso):
            def enviar(s, para, asunto, cuerpo, html=None):  # mientras esta corrida envía, arranca el timer
                otra.enviar_avisos(smtp)
                super().enviar(para, asunto, cuerpo, html)

        primera = SmtpQueCruza()
        self.assertEqual(self.pase.enviar_avisos(primera)["enviados"], 1)
        self.assertEqual(len(primera.enviados) + len(smtp.enviados), 1)
        otra.bd.close()

    def test_sin_smtp_quedan_guardados(self):
        self.pase.avisar("ana@ejemplo.co", "Hola", "Cuerpo")
        self.assertEqual(self.pase.enviar_avisos()["sin_smtp"], 1)
        self.assertIsNone(self.pase.uno("SELECT enviado_en FROM avisos")["enviado_en"])

    def test_mensaje_por_brevo(self):
        from unittest import mock
        from . import correo
        c = Config(smtp_host="smtp-relay.brevo.com", smtp_usuario="u@smtp-brevo.com", smtp_clave="x")
        with mock.patch.object(correo.smtplib, "SMTP") as SMTP:
            with correo.Smtp(c) as s:
                s.enviar("ana@ejemplo.co", "¡Ya tienes tu Pase!", "Bienvenida")
        SMTP.assert_called_once_with("smtp-relay.brevo.com", 2525, timeout=30)
        conexion = SMTP.return_value
        conexion.starttls.assert_called_once()
        conexion.login.assert_called_once_with("u@smtp-brevo.com", "x")
        m = conexion.send_message.call_args[0][0]
        self.assertEqual(m["From"], "Aula Virtual Empresarial <no-responder@edunest.co>")
        self.assertEqual(m["Subject"], "¡Ya tienes tu Pase!")
        self.assertTrue(m["Message-ID"].endswith("@edunest.co>"))

    def test_correo_con_diseno_lleva_html_y_logo(self):
        from unittest import mock
        from . import correo
        self.pase.avisar_con_diseno("ana@ejemplo.co", "pase_activo", nombre="ana rojas",
                                    medio="457562******4242", proximo_corte="2026-11-30")
        a = self.pase.uno("SELECT * FROM avisos")
        self.assertEqual(a["asunto"], "¡Ya tienes tu Pase Empresario!")
        self.assertIn("Tarjeta •••• 4242", a["cuerpo"])
        self.assertIn("30 de noviembre de 2026", a["html"])
        self.assertIn("#00806b", a["html"])
        c = Config(smtp_host="smtp-relay.brevo.com")
        with mock.patch.object(correo.smtplib, "SMTP") as SMTP:
            self.assertEqual(self.pase.enviar_avisos(correo.Smtp(c))["enviados"], 1)
        m = SMTP.return_value.send_message.call_args[0][0]
        self.assertEqual(m.get_content_type(), "multipart/alternative")
        texto, rico = m.get_payload()
        self.assertEqual(texto.get_content_type(), "text/plain")
        self.assertEqual(rico.get_content_type(), "multipart/related")
        logo = rico.get_payload()[1]
        self.assertEqual((logo.get_content_type(), logo["Content-ID"]), ("image/png", "<logo>"))

    def test_todas_las_plantillas_arman(self):
        from . import plantillas_correo as pc
        for tipo, datos in pc.EJEMPLOS.items():
            asunto, texto, cuerpo = pc.armar(tipo, self.c, **datos)
            self.assertTrue(asunto and texto and cuerpo.startswith("<!doctype html>"), tipo)
            self.assertNotIn("<b>", texto, tipo)

    def test_base_vieja_gana_columnas(self):
        import sqlite3
        ruta = os.path.join(self.tmp.name, "vieja.db")
        b = sqlite3.connect(ruta)
        b.execute("CREATE TABLE avisos (id INTEGER PRIMARY KEY, para TEXT, asunto TEXT, cuerpo TEXT, "
                  "creado TEXT, enviado_en TEXT)")
        b.commit(); b.close()
        p = Pase(Config(base_datos=ruta), MoodleSimulado())
        self.assertIn("intentos", {r[1] for r in p.bd.execute("PRAGMA table_info(avisos)")})
        p.bd.close()


if __name__ == "__main__":
    unittest.main()
