"""Configuración del conector del Pase Empresario, leída de variables de entorno.

Las llaves de ePayco y el token de Moodle viven SOLO en el entorno del servidor.
Nada de esto se guarda en archivos del repositorio.
"""
import os
from dataclasses import dataclass, field

# ePayco usa las mismas llaves en pruebas y en producción: lo que cambia es la marca
# test=TRUE de cada transacción. Por eso el candado no puede mirar prefijos de llaves.
ENTORNOS = ("sandbox", "produccion")
API_EPAYCO = "https://api.secure.payco.co"
VALIDACION_EPAYCO = "https://secure.epayco.co"
APIFY_EPAYCO = "https://apify.epayco.co"  # sesiones del Smart Checkout
CHECKOUT_JS = "https://checkout.epayco.co/checkout-v2.js"
TOKEN_JS = "https://checkout.epayco.co/epayco.min.js"


@dataclass
class Config:
    entorno: str = "sandbox"
    api_epayco: str = API_EPAYCO
    validacion_epayco: str = VALIDACION_EPAYCO
    apify_epayco: str = APIFY_EPAYCO
    checkout_js: str = CHECKOUT_JS
    token_js: str = TOKEN_JS
    cliente_id: str = ""        # P_CUST_ID_CLIENTE
    p_key: str = ""             # P_KEY: firma de las confirmaciones
    llave_publica: str = ""     # PUBLIC_KEY
    llave_privada: str = ""     # PRIVATE_KEY
    secreto_sesion: str = ""
    precio_centavos: int = 2_900_000  # $29.000 COP, cuota de referencia del Pase
    moneda: str = "COP"
    url_publica: str = "http://localhost:8080"
    base_datos: str = "pase.db"
    moodle_url: str = ""
    moodle_token: str = ""
    moodle_simulado: bool = True
    cohorte_gratis: str = "registro-gratis"
    cohorte_pase: str = "pase-empresario"
    reintentos_dias: list = field(default_factory=lambda: [0, 3, 7])
    avisos_correo: list = field(default_factory=list)
    puerto: int = 8080

    @property
    def pruebas(self) -> bool:
        return self.entorno == "sandbox"

    @classmethod
    def desde_entorno(cls) -> "Config":
        e = os.environ.get
        c = cls(
            entorno=e("EPAYCO_ENTORNO", "sandbox"),
            api_epayco=e("EPAYCO_API_URL", API_EPAYCO).rstrip("/"),
            validacion_epayco=e("EPAYCO_VALIDACION_URL", VALIDACION_EPAYCO).rstrip("/"),
            apify_epayco=e("EPAYCO_APIFY_URL", APIFY_EPAYCO).rstrip("/"),
            checkout_js=e("EPAYCO_CHECKOUT_JS", CHECKOUT_JS),
            token_js=e("EPAYCO_TOKEN_JS", TOKEN_JS),
            cliente_id=e("EPAYCO_CLIENTE", ""),
            p_key=e("EPAYCO_P_KEY", ""),
            llave_publica=e("EPAYCO_LLAVE_PUBLICA", ""),
            llave_privada=e("EPAYCO_LLAVE_PRIVADA", ""),
            secreto_sesion=e("PASE_SECRETO_SESION", ""),
            precio_centavos=int(e("PASE_PRECIO_CENTAVOS", "2900000")),
            url_publica=e("PASE_URL_PUBLICA", "http://localhost:8080").rstrip("/"),
            base_datos=e("PASE_BASE_DATOS", "pase.db"),
            moodle_url=e("PASE_MOODLE_URL", "").rstrip("/"),
            moodle_token=e("PASE_MOODLE_TOKEN", ""),
            moodle_simulado=e("PASE_MOODLE_SIMULADO", "1") == "1",
            reintentos_dias=[int(x) for x in e("PASE_REINTENTOS_DIAS", "0,3,7").split(",")],
            avisos_correo=[x for x in e("PASE_AVISOS_CORREO", "").split(",") if x],
            puerto=int(e("PASE_PUERTO", "8080")),
        )
        c.validar()
        return c

    def validar(self):
        """Candado: nada de producción por accidente."""
        if self.entorno not in ENTORNOS:
            raise ValueError(f"EPAYCO_ENTORNO debe ser sandbox o produccion, no {self.entorno!r}")
        if self.precio_centavos % 100:
            raise ValueError("PASE_PRECIO_CENTAVOS debe ser pesos enteros (ePayco cobra en pesos)")
        if not self.pruebas:
            if os.environ.get("PASE_PERMITIR_PRODUCCION") != "1":
                raise ValueError("Producción bloqueada: falta PASE_PERMITIR_PRODUCCION=1")
            if not all((self.cliente_id, self.p_key, self.llave_publica, self.llave_privada)):
                raise ValueError("Producción necesita EPAYCO_CLIENTE, EPAYCO_P_KEY y las dos llaves")
            if not self.url_publica.startswith("https://"):
                raise ValueError("Producción necesita PASE_URL_PUBLICA con https://")
        if not self.moodle_simulado and not (self.moodle_url and self.moodle_token):
            raise ValueError("Moodle real necesita PASE_MOODLE_URL y PASE_MOODLE_TOKEN")
