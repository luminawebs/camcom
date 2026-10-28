"""Cliente mínimo de la API de ePayco (Colombia) y verificación de confirmaciones.

Fuentes: docs.epayco.com (consultado el 28-oct-2026: Smart Checkout v2, páginas de respuesta y
confirmación, tokenización con epayco.min.js, medios de prueba) y, para cliente, cobro con
token y borrar token, el SDK oficial epayco-sdk-node 1.4.4 (septiembre de 2025). Se verifica
con `python -m pase.probar_sandbox` antes de pasar a producción.

El resto del conector no conoce los campos `x_…` de ePayco: este módulo convierte cada
transacción a la forma interna {id, reference, amount_in_cents, currency, status,
payment_method_type, prueba}, con los estados APPROVED, DECLINED, PENDING, ERROR y VOIDED.
"""
import base64
import hashlib
import hmac
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation

# x_cod_transaction_state / x_cod_response de ePayco → estado interno
ESTADOS = {
    "1": "APPROVED",   # Aceptada
    "2": "DECLINED",   # Rechazada
    "3": "PENDING",    # Pendiente
    "4": "ERROR",      # Fallida
    "6": "VOIDED",     # Reversada
    "7": "PENDING",    # Retenida
    "8": "PENDING",    # Iniciada
    "9": "DECLINED",   # Expirada
    "10": "DECLINED",  # Abandonada
    "11": "DECLINED",  # Cancelada
    "12": "DECLINED",  # Antifraude
}


def sha256(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def firma_confirmacion(cliente_id, p_key, ref_payco, transaction_id, monto, moneda) -> str:
    """x_signature = SHA-256 de p_cust_id_cliente^p_key^x_ref_payco^x_transaction_id^x_amount^x_currency_code."""
    return sha256("^".join(str(v) for v in (cliente_id, p_key, ref_payco, transaction_id, monto, moneda)))


def confirmacion_valida(datos: dict, cliente_id: str, p_key: str) -> bool:
    try:
        esperado = firma_confirmacion(cliente_id, p_key, datos["x_ref_payco"], datos["x_transaction_id"],
                                      datos["x_amount"], datos["x_currency_code"])
    except KeyError:
        return False
    recibido = str(datos.get("x_signature", "")).lower()
    return bool(cliente_id and p_key and recibido) and hmac.compare_digest(esperado, recibido)


def a_centavos(valor) -> int:
    try:
        return int((Decimal(str(valor).replace(",", "")) * 100).to_integral_value())
    except InvalidOperation:
        raise ValueError(f"Monto no válido: {valor!r}") from None


def pesos(centavos: int) -> str:
    return str(centavos // 100)


def es_prueba(valor) -> bool:
    return str(valor).strip().upper() in ("TRUE", "1", "SI", "SÍ", "YES")


def normalizar(d: dict) -> dict:
    """Confirmación o respuesta de la API de validación (campos x_…) → transacción interna."""
    codigo = str(d.get("x_cod_transaction_state") or d.get("x_cod_response") or "")
    return {
        "id": str(d["x_ref_payco"]),
        "reference": d.get("x_id_invoice") or d.get("x_extra1") or "",
        "amount_in_cents": a_centavos(d["x_amount"]),
        "currency": str(d.get("x_currency_code", "")).upper(),
        "status": ESTADOS.get(codigo, "PENDING"),
        "payment_method_type": d.get("x_franchise") or "",
        "transaction_id": str(d.get("x_transaction_id", "")),
        "prueba": es_prueba(d.get("x_test_request", "")),
    }


class ErrorEpayco(Exception):
    def __init__(self, estado, cuerpo):
        super().__init__(f"ePayco respondió {estado}: {cuerpo}")
        self.estado, self.cuerpo = estado, cuerpo


def partir_nombre(nombre: str):
    partes = (nombre or "").split()
    return (partes[0] if partes else ""), " ".join(partes[1:]) or "-"


class Epayco:
    def __init__(self, config):
        self.c = config
        self._jwt, self._jwt_hasta = None, 0.0
        self._apify, self._apify_hasta = None, 0.0
        self._candado = threading.Lock()

    # --- HTTP ---
    def _http(self, metodo, url, cuerpo=None, cabeceras=None):
        datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
        req = urllib.request.Request(url, data=datos, method=metodo)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        for k, v in (cabeceras or {}).items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            raise ErrorEpayco(e.code, e.read().decode(errors="replace")[:500]) from None

    def _token_api(self, renovar=False):
        """POST /v1/auth/login con las dos llaves → JWT (se guarda unos minutos)."""
        with self._candado:
            if renovar or not self._jwt or time.time() > self._jwt_hasta:
                r = self._http("POST", f"{self.c.api_epayco}/v1/auth/login",
                               {"public_key": self.c.llave_publica, "private_key": self.c.llave_privada})
                jwt = r.get("bearer_token") or r.get("token")
                if not jwt:
                    raise ErrorEpayco(401, "sin token de acceso: revisa EPAYCO_LLAVE_PUBLICA y PRIVADA")
                self._jwt, self._jwt_hasta = jwt, time.time() + 600
            return self._jwt

    def _token_apify(self, renovar=False):
        """POST apify.epayco.co/login con Basic PUBLIC_KEY:PRIVATE_KEY → token (dura unos 20 min)."""
        with self._candado:
            if renovar or not self._apify or time.time() > self._apify_hasta:
                basico = base64.b64encode(f"{self.c.llave_publica}:{self.c.llave_privada}".encode()).decode()
                r = self._http("POST", f"{self.c.apify_epayco}/login", {},
                               {"Authorization": f"Basic {basico}"})
                if not r.get("token"):
                    raise ErrorEpayco(401, "Apify sin token: revisa EPAYCO_LLAVE_PUBLICA y PRIVADA")
                self._apify, self._apify_hasta = r["token"], time.time() + 600
            return self._apify

    def _api(self, metodo, ruta, cuerpo=None):
        for renovar in (False, True):
            try:
                r = self._http(metodo, f"{self.c.api_epayco}{ruta}", cuerpo,
                               {"Authorization": f"Bearer {self._token_api(renovar)}", "type": "sdk-jwt"})
            except ErrorEpayco as e:
                if e.estado == 401 and not renovar:
                    continue
                raise
            if r.get("status") is False or r.get("success") is False:
                raise ErrorEpayco(422, json.dumps(r, ensure_ascii=False)[:500])
            return r
        raise ErrorEpayco(401, "no autorizado")

    # --- Lecturas ---
    def transaccion(self, ref_payco):
        """Doble verificación: estado real de la transacción en ePayco por su x_ref_payco."""
        r = self._http("GET", f"{self.c.validacion_epayco}/validation/v1/reference/"
                              f"{urllib.parse.quote(str(ref_payco))}")
        if not r.get("success") or not r.get("data"):
            raise ErrorEpayco(404, f"ref_payco {ref_payco} no encontrada")
        return normalizar(r["data"])

    # --- Tarjeta guardada (cobro mensual) ---
    def crear_cliente(self, token_tarjeta, persona):
        """Cliente de ePayco con la tarjeta tokenizada en el navegador; devuelve la «fuente»
        que guarda el conector: solo ids, nunca datos de la tarjeta."""
        nombre, apellido = partir_nombre(persona["nombre"])
        r = self._api("POST", "/payment/v1/customer/create", {
            "token_card": token_tarjeta, "name": nombre, "last_name": apellido,
            "email": persona["correo"], "default": True,
            "cell_phone": persona.get("whatsapp") or "", "city": persona.get("municipio") or "",
        })
        d = r.get("data") or {}
        cliente = d.get("customerId") or d.get("customer_id") or d.get("id_customer")
        if not cliente:
            raise ErrorEpayco(422, f"ePayco no devolvió el id del cliente: {json.dumps(r)[:300]}")
        return {"cliente": str(cliente), "token": token_tarjeta}

    def cobrar_tarjeta(self, fuente, referencia, persona, ip, monto_centavos=None):
        """POST /payment/v1/charge/create con el cliente y su token. El resultado final llega
        por la URL de confirmación; aquí solo se guarda el x_ref_payco."""
        monto = monto_centavos or self.c.precio_centavos
        nombre, apellido = partir_nombre(persona["nombre"])
        r = self._api("POST", "/payment/v1/charge/create", {
            "token_card": fuente["token"], "customer_id": fuente["cliente"],
            "doc_type": persona.get("tipo_doc") or "CC", "doc_number": persona["documento"],
            "name": nombre, "last_name": apellido, "email": persona["correo"],
            "cell_phone": persona.get("whatsapp") or "", "city": persona.get("municipio") or "",
            "bill": referencia, "description": "Pase Empresario (mensual)",
            "value": pesos(monto), "tax": "0", "tax_base": "0", "currency": self.c.moneda,
            "dues": "1", "ip": ip or "127.0.0.1",
            "url_response": f"{self.c.url_publica}/retorno?ref={urllib.parse.quote(referencia)}",
            "url_confirmation": f"{self.c.url_publica}/webhooks/epayco",
            "method_confirmation": "POST",
            "test": "TRUE" if self.c.pruebas else "FALSE",
            "extras": {"extra1": referencia},
        })
        d = r.get("data") or {}
        ref_payco = d.get("ref_payco") or d.get("x_ref_payco")
        if not ref_payco:
            raise ErrorEpayco(422, f"ePayco no devolvió ref_payco: {json.dumps(r)[:300]}")
        return {"id": str(ref_payco),
                "status": ESTADOS.get(str(d.get("cod_respuesta") or d.get("x_cod_response") or ""), "PENDING")}

    def quitar_tarjeta(self, fuente):
        """Al cancelar se borra el token del cliente en ePayco para no volver a cobrarle.
        ePayco pide franquicia y máscara: se leen del cliente."""
        r = self._api("GET", f"/payment/v1/customer/{self.c.llave_publica}/{fuente['cliente']}")
        datos = r.get("data") or {}
        tarjetas = datos.get("cards") or (datos.get("data") or {}).get("cards") or []
        tarjeta = next((t for t in tarjetas if t.get("token") == fuente["token"]), None)
        if not tarjeta:
            return {"ya_no_existe": True}
        return self._api("POST", "/v1/remove/token", {
            "franchise": tarjeta.get("franchise"), "mask": tarjeta.get("mask"),
            "customer_id": fuente["cliente"]})

    # --- Smart Checkout v2 (PSE, Nequi, Daviplata, tarjeta sin guardar) ---
    def datos_checkout(self, referencia, persona, monto_centavos=None):
        """Crea la sesión del Smart Checkout en el backend (POST /payment/session/create) y
        devuelve lo que necesita ePayco.checkout.configure() en el navegador."""
        monto = monto_centavos or self.c.precio_centavos
        cuerpo = {
            "checkout_version": "2", "name": "Pase Empresario",
            "description": "Pase Empresario · Aula Virtual Empresarial",
            "currency": self.c.moneda, "amount": monto // 100, "invoice": referencia,
            "lang": "ES", "country": "CO", "taxBase": 0, "tax": 0, "taxIco": 0,
            "response": f"{self.c.url_publica}/retorno?ref={urllib.parse.quote(referencia)}",
            "confirmation": f"{self.c.url_publica}/webhooks/epayco", "method": "POST",
            "extras": {"extra1": referencia},
            "billing": {"email": persona["correo"], "name": persona["nombre"],
                        "typeDoc": persona.get("tipo_doc") or "CC", "numberDoc": persona["documento"],
                        "callingCode": "+57", "mobilePhone": persona.get("whatsapp") or ""},
        }
        for renovar in (False, True):
            try:
                r = self._http("POST", f"{self.c.apify_epayco}/payment/session/create", cuerpo,
                               {"Authorization": f"Bearer {self._token_apify(renovar)}"})
                break
            except ErrorEpayco as e:
                if e.estado != 401 or renovar:
                    raise
        sesion = (r.get("data") or {}).get("sessionId")
        if not r.get("success") or not sesion:
            raise ErrorEpayco(422, f"ePayco no creó la sesión: {json.dumps(r, ensure_ascii=False)[:300]}")
        return {"sessionId": sesion, "type": "standard", "test": self.c.pruebas}
