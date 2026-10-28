"""Simulador local de ePayco en modo prueba, para probar el conector sin red ni llaves.

Imita lo que usa el conector y manda las confirmaciones firmadas (campos x_…) a la URL
de confirmación, como ePayco:
  - POST /v1/auth/login, /payment/v1/customer/create, /payment/v1/charge/create,
    GET /payment/v1/customer/{llave}/{id}, POST /v1/remove/token
  - GET /validation/v1/reference/{ref_payco} (Smart Checkout) y
    /restpagos/transaction/response.json (cobros con token)
  - POST /login y /payment/session/create (Apify, sesiones del Smart Checkout v2)
  - /epayco.js (tokenización en el navegador) y /checkout-v2.js (Smart Checkout con botones
    Aprobar / Rechazar, que reemplaza a PSE, Nequi o Daviplata)
Tarjetas: 4575 6231 8229 0326 aprueba, 4151 6115 2758 3283 rechaza.

    python -m pase.simulador_epayco    (puerto 8090)
"""
import base64
import html
import itertools
import json
import os
import secrets
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import epayco as ep

CLIENTE_ID = "900001"
P_KEY = "pkey_simulador"
LLAVE_PUBLICA = "pub_simulador"
LLAVE_PRIVADA = "prv_simulador"
TARJETA_APRUEBA = "4575623182290326"
TARJETA_RECHAZA = "4151611527583283"

CODIGO = {"APPROVED": "1", "DECLINED": "2", "PENDING": "3", "ERROR": "4", "VOIDED": "6"}
TEXTO = {"1": "Aceptada", "2": "Rechazada", "3": "Pendiente", "4": "Fallida", "6": "Reversada"}


class Simulador:
    def __init__(self, demora=0.2):
        self.demora = demora
        self.ids = itertools.count(91000)
        self.jwts = set()
        self.tokens, self.clientes, self.transacciones, self.sesiones = {}, {}, {}, {}
        self.forzado = {}           # token_card -> estado forzado para el próximo cobro
        self.confirmaciones = []    # (url, datos) enviadas
        self.avisar = True          # False: ePayco "no logra" llamar a la URL de confirmación
        self.candado = threading.Lock()

    def _id(self):
        return str(next(self.ids))

    def login(self, d):
        if (d.get("public_key"), d.get("private_key")) != (LLAVE_PUBLICA, LLAVE_PRIVADA):
            return 401, {"status": False, "message": "Credenciales inválidas"}
        jwt = f"jwt-{self._id()}"
        self.jwts.add(jwt)
        return 200, {"token": jwt}

    def login_apify(self, autorizacion):
        esperado = base64.b64encode(f"{LLAVE_PUBLICA}:{LLAVE_PRIVADA}".encode()).decode()
        if autorizacion != f"Basic {esperado}":
            return 401, {"error": "Credenciales inválidas"}
        jwt = f"apify-{self._id()}"
        self.jwts.add(jwt)
        return 200, {"token": jwt}

    def crear_sesion(self, d):
        faltan = [k for k in ("checkout_version", "name", "currency", "amount") if not d.get(k)]
        if faltan or d.get("checkout_version") != "2":
            return 400, {"success": False, "textResponse": f"Faltan {faltan}"}
        sid = secrets.token_hex(12)
        self.sesiones[sid] = d
        return 200, {"success": True, "titleResponse": "Session created successfully",
                     "data": {"sessionId": sid, "token": f"tok-{sid}"}}

    def token_tarjeta(self, d):
        num = str(d.get("card[number]", "")).replace(" ", "")
        if d.get("public_key") != LLAVE_PUBLICA or len(num) < 13 or not d.get("card[cvc]"):
            return 200, {"status": False, "message": "Datos de la tarjeta inválidos"}
        tok = f"tok{self._id()}"
        self.tokens[tok] = {"aprueba": num != TARJETA_RECHAZA, "mask": f"{num[:6]}******{num[-4:]}",
                            "franchise": "visa"}
        return 200, {"status": True, "id": tok, "data": {"id": tok}}

    def crear_cliente(self, d):
        t = self.tokens.get(d.get("token_card"))
        if not t or not d.get("email"):
            return 200, {"status": False, "message": "token_card no válido"}
        cid = f"cus{self._id()}"
        self.clientes[cid] = {"email": d["email"], "cards": [{"token": d["token_card"], **t}]}
        return 200, {"status": True, "success": True,
                     "data": {"status": "exitoso", "customerId": cid}}

    def ver_cliente(self, cid):
        c = self.clientes.get(cid)
        if not c:
            return 200, {"status": False, "message": "No existe"}
        cards = [{"token": x["token"], "franchise": x["franchise"], "mask": x["mask"]} for x in c["cards"]]
        return 200, {"status": True, "data": {"id_customer": cid, "email": c["email"], "cards": cards}}

    def quitar_token(self, d):
        c = self.clientes.get(d.get("customer_id"))
        if not c:
            return 200, {"status": False, "message": "No existe"}
        antes = len(c["cards"])
        c["cards"] = [x for x in c["cards"] if not (x["mask"] == d.get("mask") and x["franchise"] == d.get("franchise"))]
        return 200, {"status": len(c["cards"]) < antes}

    def cobrar(self, d):
        c = self.clientes.get(d.get("customer_id"))
        tarjeta = next((x for x in (c or {}).get("cards", []) if x["token"] == d.get("token_card")), None)
        faltan = [k for k in ("bill", "value", "currency", "doc_number", "email", "ip") if not d.get(k)]
        if not tarjeta or faltan:
            return 200, {"status": False, "message": f"Cobro no válido {faltan}"}
        final = self.forzado.pop(d["token_card"], None) or ("APPROVED" if tarjeta["aprueba"] else "DECLINED")
        tx = self._nueva_tx(d["bill"], d["value"], d["currency"], "VS", final, d.get("test") == "TRUE",
                            d.get("url_confirmation"))
        return 200, {"success": True, "data": {"ref_payco": int(tx["x_ref_payco"]), "factura": d["bill"],
                                               "valor": d["value"], "estado": "Pendiente", "cod_respuesta": 3}}

    def _nueva_tx(self, factura, valor, moneda, franquicia, final, prueba, confirmacion, ref=None):
        ref = ref or self._id()
        tx = {"x_cust_id_cliente": CLIENTE_ID, "x_ref_payco": ref, "x_id_invoice": factura,
              "x_amount": str(valor), "x_currency_code": moneda.upper(), "x_franchise": franquicia,
              "x_transaction_id": f"{ref}{int(time.time())}", "x_test_request": "TRUE" if prueba else "FALSE",
              "x_extra1": factura, "x_cod_response": "3", "x_cod_transaction_state": "3",
              "x_transaction_state": "Pendiente", "x_respuesta": "Pendiente",
              "x_fecha_transaccion": time.strftime("%Y-%m-%d %H:%M:%S")}
        self.transacciones[ref] = tx
        threading.Timer(self.demora, self.cambiar_estado, (ref, final, confirmacion)).start()
        return tx

    def cambiar_estado(self, ref, estado, confirmacion=None):
        with self.candado:
            tx = self.transacciones[ref]
            cod = CODIGO[estado]
            tx.update({"x_cod_response": cod, "x_cod_transaction_state": cod,
                       "x_transaction_state": TEXTO[cod], "x_respuesta": TEXTO[cod]})
            tx["_confirmacion"] = confirmacion or tx.get("_confirmacion")
        self.confirmar(ref)

    def confirmacion(self, ref):
        datos = {k: v for k, v in self.transacciones[ref].items() if not k.startswith("_")}
        datos["x_signature"] = ep.firma_confirmacion(CLIENTE_ID, P_KEY, datos["x_ref_payco"],
                                                     datos["x_transaction_id"], datos["x_amount"],
                                                     datos["x_currency_code"])
        return datos

    def confirmar(self, ref, datos=None):
        datos = datos or self.confirmacion(ref)
        url = self.transacciones[ref].get("_confirmacion")
        self.confirmaciones.append((url, datos))
        if not (url and self.avisar):
            return None
        req = urllib.request.Request(url, urllib.parse.urlencode(datos).encode(),
                                     {"Content-Type": "application/x-www-form-urlencoded"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except OSError:
            return None

    def validacion(self, ref):
        """Como en ePayco real: /validation/v1/reference solo encuentra los ref_payco
        alfanuméricos del Smart Checkout v2; los numéricos (cobros con token) dan error."""
        if ref not in self.transacciones or ref.isdigit():
            return 200, {"status": False, "message": "Error de datos o conexión."}
        return 200, {"success": True, "data": self.confirmacion(ref)}

    def restpagos(self, q):
        ref = q.get("ref_payco", "")
        if q.get("public_key") != LLAVE_PUBLICA or ref not in self.transacciones:
            return 200, {"success": False, "title_response": "Error", "data": {}}
        return 200, {"success": True, "title_response": "Correcto", "data": self.confirmacion(ref)}

    def pagina_checkout(self, q):
        d = self.sesiones.get(q.get("session", ""))
        if not d:
            return "<h1>Sesión no válida</h1>"
        datos = html.escape(urllib.parse.urlencode(q))
        return (f"<h1>Smart Checkout ePayco (simulador)</h1><p>Factura {html.escape(d.get('invoice', ''))} · "
                f"${d.get('amount')} {html.escape(d.get('currency', '').upper())}"
                f"{' · PRUEBA' if q.get('test') == 'true' else ''}</p>"
                f"<form method='post' action='/checkout/pagar?{datos}'>"
                f"<button name='r' value='APPROVED'>Aprobar (PSE / Nequi)</button> "
                f"<button name='r' value='DECLINED'>Rechazar</button></form>")

    def pagar_checkout(self, q, resultado):
        d = self.sesiones[q["session"]]
        # El Smart Checkout v2 devuelve ref_payco alfanuméricos (p. ej. 68fb83729d094878e015be00)
        tx = self._nueva_tx(d["invoice"], d["amount"], d["currency"], "PSE", resultado,
                            q.get("test") == "true", d.get("confirmation"), secrets.token_hex(12))
        sep = "&" if "?" in d["response"] else "?"
        return f"{d['response']}{sep}ref_payco={tx['x_ref_payco']}"


def js_checkout(base):
    return f"""window.ePayco=window.ePayco||{{}};ePayco.checkout={{configure:function(o){{return{{setHooks:function(){{}},
open:function(){{location.href='{base}/checkout?'+new URLSearchParams({{session:o.sessionId,test:String(!!o.test)}})}}}}}}}};"""


def js_token(base):
    return f"""window.ePayco=window.ePayco||{{}};(function(){{var pk='';ePayco.setPublicKey=function(k){{pk=k}};
ePayco.token={{create:function(f,cb){{f=f&&f.jquery?f[0]:f;var d={{public_key:pk}};
f.querySelectorAll('[data-epayco]').forEach(function(e){{d[e.getAttribute('data-epayco')]=e.value}});
fetch('{base}/v1/tokens/navegador',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}})
.then(function(r){{return r.json()}}).then(function(j){{j.status?cb(null,j.id):cb(j.message||'error')}},function(e){{cb(String(e))}})}}}}}})();"""


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

        def base(self):
            return f"http://{self.headers.get('Host')}"

        def autorizado(self):
            return self.headers.get("Authorization", "").removeprefix("Bearer ") in sim.jwts

        def do_OPTIONS(self):
            self.enviar(204, b"")

        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            q = dict(urllib.parse.parse_qsl(u.query))
            p = u.path
            if p == "/checkout-v2.js":
                return self.enviar(200, js_checkout(self.base()).encode(), "application/javascript")
            if p == "/epayco.js":
                return self.enviar(200, js_token(self.base()).encode(), "application/javascript")
            if p == "/checkout":
                return self.enviar(200, sim.pagina_checkout(q).encode(), "text/html; charset=utf-8")
            if p == "/restpagos/transaction/response.json":
                return self.enviar(*sim.restpagos(q))
            if p.startswith("/validation/v1/reference/"):
                return self.enviar(*sim.validacion(p.rsplit("/", 1)[1]))
            if p.startswith("/payment/v1/customer/"):
                if not self.autorizado():
                    return self.enviar(401, {"status": False})
                return self.enviar(*sim.ver_cliente(p.rsplit("/", 1)[1]))
            self.enviar(404, {"status": False})

        def do_POST(self):
            u = urllib.parse.urlparse(self.path)
            crudo = self.rfile.read(int(self.headers.get("Content-Length") or 0))
            p = u.path
            if p == "/checkout/pagar":
                q = dict(urllib.parse.parse_qsl(u.query))
                r = dict(urllib.parse.parse_qsl(crudo.decode())).get("r", "DECLINED")
                return self.enviar(302, b"", extra={"Location": sim.pagar_checkout(q, r)})
            d = json.loads(crudo or b"{}")
            if p.startswith("/control/"):
                return self.enviar(200, control(sim, p, d))
            if p == "/login":
                return self.enviar(*sim.login_apify(self.headers.get("Authorization", "")))
            if p == "/v1/auth/login":
                return self.enviar(*sim.login(d))
            if p == "/v1/tokens/navegador":
                return self.enviar(*sim.token_tarjeta(d))
            if not self.autorizado():
                return self.enviar(401, {"status": False, "message": "Token inválido"})
            if p == "/payment/session/create":
                return self.enviar(*sim.crear_sesion(d))
            if p == "/payment/v1/customer/create":
                return self.enviar(*sim.crear_cliente(d))
            if p == "/payment/v1/charge/create":
                return self.enviar(*sim.cobrar(d))
            if p == "/v1/remove/token":
                return self.enviar(*sim.quitar_token(d))
            self.enviar(404, {"status": False})

    return H


def control(sim, ruta, d):
    """Atajos de prueba que ePayco no tiene."""
    if ruta == "/control/forzar":           # el próximo cobro a este token queda así
        sim.forzado[d["token"]] = d["estado"]
    elif ruta == "/control/reversar":
        sim.cambiar_estado(d["ref_payco"], "VOIDED")
    return {"ok": True}


def arrancar(puerto=8090, demora=0.2):
    sim = Simulador(demora)
    srv = ThreadingHTTPServer(("127.0.0.1", puerto), manejador(sim))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return sim, srv


if __name__ == "__main__":
    puerto = int(os.environ.get("SIM_PUERTO", "8090"))
    _, srv = arrancar(puerto)
    print(f"Simulador ePayco en http://127.0.0.1:{puerto}  (llave pública {LLAVE_PUBLICA})")
    threading.Event().wait()
