"""Cliente mínimo de la API de Wompi (Colombia) y cálculo de firmas.

Referencias (docs.wompi.co): «Widget y Web Checkout», «Firma de integridad»,
«Eventos», «Fuentes de pago y tokenización», «Enlaces de pago».
Los nombres de campos se tomaron de esa documentación y se deben verificar
contra la versión vigente antes de pasar a producción.
"""
import hashlib
import hmac
import json
import urllib.error
import urllib.parse
import urllib.request


def sha256(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def firma_integridad(referencia: str, monto_centavos: int, moneda: str, secreto: str,
                     expiracion: str = "") -> str:
    """SHA-256 de referencia + monto + moneda [+ fecha de expiración] + secreto de integridad."""
    return sha256(f"{referencia}{monto_centavos}{moneda}{expiracion}{secreto}")


def _valor(datos: dict, ruta: str):
    actual = datos
    for parte in ruta.split("."):
        actual = actual[parte]
    return actual


def checksum_evento(evento: dict, secreto_eventos: str) -> str:
    """Valores de signature.properties (dentro de data) + timestamp + secreto de eventos."""
    props = evento["signature"]["properties"]
    concatenado = "".join(str(_valor(evento["data"], p)) for p in props)
    return sha256(f"{concatenado}{evento['timestamp']}{secreto_eventos}")


def evento_valido(evento: dict, secreto_eventos: str, checksum_cabecera: str = "") -> bool:
    try:
        esperado = checksum_evento(evento, secreto_eventos)
    except (KeyError, TypeError):
        return False
    recibido = (checksum_cabecera or evento.get("signature", {}).get("checksum", "")).lower()
    return bool(recibido) and hmac.compare_digest(esperado, recibido)


class ErrorWompi(Exception):
    def __init__(self, estado, cuerpo):
        super().__init__(f"Wompi respondió {estado}: {cuerpo}")
        self.estado, self.cuerpo = estado, cuerpo


class Wompi:
    def __init__(self, config):
        self.c = config

    def _llamar(self, metodo, ruta, cuerpo=None, privada=False):
        llave = self.c.llave_privada if privada else self.c.llave_publica
        datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
        req = urllib.request.Request(f"{self.c.api_wompi}{ruta}", data=datos, method=metodo)
        req.add_header("Content-Type", "application/json")
        if llave:
            req.add_header("Authorization", f"Bearer {llave}")
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            raise ErrorWompi(e.code, e.read().decode(errors="replace")) from None

    # --- Lecturas ---
    def comercio(self):
        """Tokens de aceptación (términos y tratamiento de datos) que el usuario debe aceptar."""
        d = self._llamar("GET", f"/merchants/{self.c.llave_publica}")["data"]
        return {
            "nombre": d.get("name"),
            "aceptacion": d["presigned_acceptance"],
            "datos_personales": d.get("presigned_personal_data_auth"),
        }

    def transaccion(self, transaccion_id):
        return self._llamar("GET", f"/transactions/{transaccion_id}")["data"]

    def transacciones_por_referencia(self, referencia):
        q = urllib.parse.urlencode({"reference": referencia})
        return self._llamar("GET", f"/transactions?{q}", privada=True)["data"]

    # --- Escrituras (requieren llave privada) ---
    def crear_fuente_pago(self, tipo, token, correo, token_aceptacion, token_datos=None):
        cuerpo = {"type": tipo, "token": token, "customer_email": correo,
                  "acceptance_token": token_aceptacion}
        if token_datos:
            cuerpo["accept_personal_auth"] = token_datos
        return self._llamar("POST", "/payment_sources", cuerpo, privada=True)["data"]

    def cobrar_fuente(self, fuente_id, referencia, correo, monto_centavos=None, recurrente=True):
        monto = monto_centavos or self.c.precio_centavos
        cuerpo = {
            "amount_in_cents": monto,
            "currency": self.c.moneda,
            "signature": firma_integridad(referencia, monto, self.c.moneda, self.c.secreto_integridad),
            "customer_email": correo,
            "payment_method": {"installments": 1},
            "reference": referencia,
            "payment_source_id": int(fuente_id),
            "recurrent": recurrente,
        }
        return self._llamar("POST", "/transactions", cuerpo, privada=True)["data"]

    def crear_enlace_pago(self, nombre, descripcion, referencia, monto_centavos=None, expira=None):
        cuerpo = {
            "name": nombre, "description": descripcion, "single_use": True,
            "collect_shipping": False, "currency": self.c.moneda,
            "amount_in_cents": monto_centavos or self.c.precio_centavos,
            "redirect_url": f"{self.c.url_publica}/retorno",
            "sku": referencia,
        }
        if expira:
            cuerpo["expires_at"] = expira
        return self._llamar("POST", "/payment_links", cuerpo, privada=True)["data"]

    def url_web_checkout(self, referencia, correo, nombre, monto_centavos=None):
        """Web Checkout (redirección): sirve para PSE y otros medios no recurrentes."""
        monto = monto_centavos or self.c.precio_centavos
        q = urllib.parse.urlencode({
            "public-key": self.c.llave_publica,
            "currency": self.c.moneda,
            "amount-in-cents": monto,
            "reference": referencia,
            "signature:integrity": firma_integridad(referencia, monto, self.c.moneda,
                                                    self.c.secreto_integridad),
            "redirect-url": f"{self.c.url_publica}/retorno",
            "customer-data:email": correo,
            "customer-data:full-name": nombre,
        })
        return f"{self.c.checkout_wompi}?{q}"
