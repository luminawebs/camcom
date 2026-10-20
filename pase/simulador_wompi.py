"""Simulador local del sandbox de Wompi, para probar el conector sin red ni llaves.

Imita los endpoints que usa el conector y envía eventos `transaction.updated`
firmados al webhook, igual que Wompi. Reglas del sandbox real que se copian:
  tarjeta 4242 4242 4242 4242 → APPROVED · 4111 1111 1111 1111 → DECLINED
  Nequi 3991111111 → APPROVED · 3992222222 → DECLINED
  PSE en el Web Checkout: el simulador muestra botones Aprobar / Rechazar.

    python -m pase.simulador_wompi    (puerto 8090; webhook en SIM_WEBHOOK)
"""
import html
import itertools
import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import wompi as w

LLAVE_PUBLICA = "pub_test_simulador"
LLAVE_PRIVADA = "prv_test_simulador"
SECRETO_INTEGRIDAD = "test_integrity_simulador"
SECRETO_EVENTOS = "test_events_simulador"


class Simulador:
    def __init__(self, webhook, demora=0.2):
        self.webhook, self.demora = webhook, demora
        self.ids = itertools.count(1000)
        self.tokens, self.fuentes, self.transacciones = {}, {}, {}
        self.aceptaciones_usadas = set()  # en Wompi cada token de aceptación sirve una sola vez
        self.forzado = {}           # payment_source_id -> estado forzado para el próximo cobro
        self.eventos_enviados = []
        self.candado = threading.Lock()

    def _id(self, prefijo):
        return f"{prefijo}{next(self.ids)}"

    def comercio(self):
        return {"data": {
            "name": "EduNest (simulador)",
            "presigned_acceptance": {"acceptance_token": self._id("acept_sim_"),
                                     "permalink": "https://wompi.com/assets/terminos-sandbox.pdf",
                                     "type": "END_USER_POLICY"},
            "presigned_personal_data_auth": {"acceptance_token": self._id("datos_sim_"),
                                             "permalink": "https://wompi.com/assets/datos-sandbox.pdf",
                                             "type": "PERSONAL_DATA_AUTH"},
        }}

    def token_tarjeta(self, d):
        num = str(d.get("number", "")).replace(" ", "")
        if len(num) < 13 or not d.get("cvc"):
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR", "messages": {"number": ["Inválido"]}}}
        tid = self._id("tok_test_")
        self.tokens[tid] = {"tipo": "CARD", "aprueba": num != "4111111111111111", "ultimos": num[-4:]}
        return 201, {"status": "CREATED", "data": {"id": tid, "last_four": num[-4:], "brand": "VISA"}}

    def token_nequi(self, d):
        tid = self._id("nequi_test_")
        cel = str(d.get("phone_number", ""))
        self.tokens[tid] = {"tipo": "NEQUI", "aprueba": cel != "3992222222", "estado": "PENDING",
                            "creado": time.time()}
        return 200, {"data": {"id": tid, "status": "PENDING", "phone_number": cel}}

    def ver_token_nequi(self, tid):
        t = self.tokens.get(tid)
        if not t:
            return 404, {"error": {"type": "NOT_FOUND_ERROR"}}
        if t["estado"] == "PENDING" and time.time() - t["creado"] > self.demora:
            t["estado"] = "APPROVED" if t["aprueba"] else "DECLINED"
        return 200, {"data": {"id": tid, "status": t["estado"]}}

    def _usar_aceptacion(self, d):
        usados = [d[k] for k in ("acceptance_token", "accept_personal_auth") if d.get(k)]
        if any(u in self.aceptaciones_usadas for u in usados):
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR",
                                   "messages": {"acceptance_token": ["El token de aceptación ya fue usado"]}}}
        self.aceptaciones_usadas.update(usados)

    def fuente_pago(self, d):
        t = self.tokens.get(d.get("token"))
        if not t or not d.get("acceptance_token"):
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR", "reason": "token o aceptación"}}
        if (error := self._usar_aceptacion(d)):
            return error
        if t["tipo"] == "NEQUI" and t.get("estado") != "APPROVED":
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR", "reason": "token Nequi no aprobado"}}
        fid = next(self.ids)
        self.fuentes[fid] = {"id": fid, "type": t["tipo"], "aprueba": t["aprueba"],
                             "customer_email": d.get("customer_email"), "status": "AVAILABLE"}
        return 201, {"data": {"id": fid, "type": t["tipo"], "status": "AVAILABLE"}}

    def _nueva_tx(self, referencia, monto, moneda, correo, metodo, final):
        tid = self._id("15113-")
        tx = {"id": tid, "reference": referencia, "amount_in_cents": monto, "currency": moneda,
              "customer_email": correo, "payment_method_type": metodo, "status": "PENDING",
              "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        self.transacciones[tid] = tx
        threading.Timer(self.demora, self.cambiar_estado, (tid, final)).start()
        return tx

    def transaccion(self, d):
        firma = w.firma_integridad(d.get("reference", ""), d.get("amount_in_cents", 0),
                                   d.get("currency", ""), SECRETO_INTEGRIDAD)
        if d.get("signature") != firma:
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR", "messages": {"signature": ["Firma inválida"]}}}
        if not d.get("acceptance_token"):
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR",
                                   "messages": {"acceptance_token": ["Requerido"]}}}
        if any(t["reference"] == d["reference"] for t in self.transacciones.values()):
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR", "messages": {"reference": ["Ya existe"]}}}
        if (error := self._usar_aceptacion(d)):
            return error
        f = self.fuentes.get(d.get("payment_source_id"))
        if not f or f["status"] != "AVAILABLE":
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR", "reason": "fuente de pago"}}
        if ("payment_method" in d) != (f["type"] == "CARD"):
            return 422, {"error": {"type": "INPUT_VALIDATION_ERROR",
                                   "messages": {"payment_method": ["Solo para tarjeta"]}}}
        final = self.forzado.pop(f["id"], None) or ("APPROVED" if f["aprueba"] else "DECLINED")
        tx = self._nueva_tx(d["reference"], d["amount_in_cents"], d["currency"],
                            d.get("customer_email"), f["type"], final)
        return 201, {"data": dict(tx)}

    def cambiar_estado(self, tid, estado):
        with self.candado:
            tx = self.transacciones[tid]
            tx["status"] = estado
        self.enviar_evento(tx)

    def evento(self, tx):
        ts = int(time.time())
        ev = {"event": "transaction.updated", "data": {"transaction": dict(tx)},
              "environment": "test", "sent_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "timestamp": ts,
              "signature": {"properties": ["transaction.id", "transaction.status",
                                           "transaction.amount_in_cents"]}}
        ev["signature"]["checksum"] = w.checksum_evento(ev, SECRETO_EVENTOS)
        return ev

    def enviar_evento(self, tx, ev=None):
        ev = ev or self.evento(tx)
        self.eventos_enviados.append(ev)
        if not self.webhook:
            return None
        cuerpo = json.dumps(ev).encode()
        req = urllib.request.Request(self.webhook, cuerpo, {"Content-Type": "application/json",
                                                             "X-Event-Checksum": ev["signature"]["checksum"]})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except OSError:
            return None

    def pagina_checkout(self, q):
        firma = w.firma_integridad(q.get("reference", ""), q.get("amount-in-cents", ""),
                                   q.get("currency", ""), SECRETO_INTEGRIDAD)
        if q.get("signature:integrity") != firma:
            return "<h1>Firma de integridad inválida</h1>"
        datos = html.escape(urllib.parse.urlencode(q))
        monto = int(q["amount-in-cents"]) // 100
        return (f"<h1>Web Checkout (simulador)</h1><p>Referencia {html.escape(q['reference'])} · "
                f"${monto:,} COP · PSE</p>"
                f"<form method='post' action='/p/pagar?{datos}'>"
                f"<button name='r' value='APPROVED'>Aprobar en el banco</button> "
                f"<button name='r' value='DECLINED'>Rechazar</button></form>")

    def pagar_checkout(self, q, resultado):
        tx = self._nueva_tx(q["reference"], int(q["amount-in-cents"]), q["currency"],
                            q.get("customer-data:email"), "PSE", resultado)
        return f"{q['redirect-url']}?id={tx['id']}&env=test"


def manejador(sim: Simulador):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def enviar(self, codigo, datos, tipo="application/json", extra=None):
            cuerpo = datos if isinstance(datos, bytes) else json.dumps(datos).encode()
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
            self.send_header("Content-Length", str(len(cuerpo)))
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(cuerpo)

        def llave(self):
            return self.headers.get("Authorization", "").removeprefix("Bearer ")

        def do_OPTIONS(self):
            self.enviar(204, b"")

        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            q = dict(urllib.parse.parse_qsl(u.query))
            p = u.path
            if p == "/v1/merchants/info":
                if self.headers.get("x-merchant-public-key") != LLAVE_PUBLICA:
                    return self.enviar(401, {"error": {"type": "INVALID_ACCESS_TOKEN"}})
                return self.enviar(200, sim.comercio())
            if p.startswith("/v1/tokens/nequi/"):
                return self.enviar(*sim.ver_token_nequi(p.rsplit("/", 1)[1]))
            if p.startswith("/v1/transactions/"):
                if self.llave() != LLAVE_PRIVADA:  # con llave pública Wompi responde 404
                    return self.enviar(404, {"error": {"type": "NOT_FOUND_ERROR"}})
                tx = sim.transacciones.get(p.rsplit("/", 1)[1])
                return self.enviar(200, {"data": tx}) if tx else self.enviar(404, {"error": {"type": "NOT_FOUND_ERROR"}})
            if p == "/v1/transactions":
                if self.llave() != LLAVE_PRIVADA:
                    return self.enviar(401, {"error": {"type": "INVALID_ACCESS_TOKEN"}})
                lista = [t for t in sim.transacciones.values() if t["reference"] == q.get("reference")]
                return self.enviar(200, {"data": lista})
            if p == "/p/":
                return self.enviar(200, sim.pagina_checkout(q).encode(), "text/html; charset=utf-8")
            self.enviar(404, {"error": {"type": "NOT_FOUND_ERROR"}})

        def do_POST(self):
            u = urllib.parse.urlparse(self.path)
            crudo = self.rfile.read(int(self.headers.get("Content-Length") or 0))
            p = u.path
            if p == "/p/pagar":
                q = dict(urllib.parse.parse_qsl(u.query))
                r = dict(urllib.parse.parse_qsl(crudo.decode())).get("r", "DECLINED")
                return self.enviar(302, b"", extra={"Location": sim.pagar_checkout(q, r)})
            d = json.loads(crudo or b"{}")
            if p.startswith("/control/"):
                return self.enviar(200, control(sim, p, d))
            if p == "/v1/tokens/cards":
                return self.enviar(*sim.token_tarjeta(d)) if self.llave() == LLAVE_PUBLICA else self.enviar(401, {})
            if p == "/v1/tokens/nequi":
                return self.enviar(*sim.token_nequi(d)) if self.llave() == LLAVE_PUBLICA else self.enviar(401, {})
            if self.llave() != LLAVE_PRIVADA:
                return self.enviar(401, {"error": {"type": "INVALID_ACCESS_TOKEN"}})
            if p == "/v1/payment_sources":
                return self.enviar(*sim.fuente_pago(d))
            if p == "/v1/transactions":
                return self.enviar(*sim.transaccion(d))
            if p == "/v1/payment_links":
                return self.enviar(201, {"data": {"id": sim._id("link_"), **d}})
            self.enviar(404, {"error": {"type": "NOT_FOUND_ERROR"}})

        def do_PUT(self):
            p = urllib.parse.urlparse(self.path).path
            if self.llave() != LLAVE_PRIVADA:
                return self.enviar(401, {"error": {"type": "INVALID_ACCESS_TOKEN"}})
            if p.startswith("/v1/payment_sources/") and p.endswith("/void"):
                f = sim.fuentes.get(int(p.split("/")[3]))
                if not f:
                    return self.enviar(404, {"error": {"type": "NOT_FOUND_ERROR"}})
                f["status"] = "VOIDED"
                return self.enviar(200, {"data": {"id": f["id"], "type": f["type"], "status": "VOIDED"}})
            self.enviar(404, {"error": {"type": "NOT_FOUND_ERROR"}})

    return H


def control(sim, ruta, d):
    """Atajos de prueba que el sandbox real no tiene."""
    if ruta == "/control/forzar":           # el próximo cobro a esta fuente queda así
        sim.forzado[int(d["payment_source_id"])] = d["estado"]
    elif ruta == "/control/anular":
        sim.cambiar_estado(d["transaction_id"], "VOIDED")
    elif ruta == "/control/reenviar":       # mismo evento otra vez (prueba de idempotencia)
        return {"http": sim.enviar_evento(None, sim.eventos_enviados[-1])}
    return {"ok": True}


def arrancar(puerto=8090, webhook=None, demora=0.2):
    sim = Simulador(webhook, demora)
    srv = ThreadingHTTPServer(("127.0.0.1", puerto), manejador(sim))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return sim, srv


if __name__ == "__main__":
    puerto = int(os.environ.get("SIM_PUERTO", "8090"))
    _, srv = arrancar(puerto, os.environ.get("SIM_WEBHOOK", "http://localhost:8080/webhooks/wompi"))
    print(f"Simulador Wompi en http://127.0.0.1:{puerto}/v1  (llave pública {LLAVE_PUBLICA})")
    threading.Event().wait()
