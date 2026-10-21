"""Configuración del conector del Pase Empresario, leída de variables de entorno.

Las llaves de Wompi y el token de Moodle viven SOLO en el entorno del servidor.
Nada de esto se guarda en archivos del repositorio.
"""
import os
from dataclasses import dataclass, field

URL_WOMPI = {
    "sandbox": "https://sandbox.wompi.co/v1",
    "produccion": "https://production.wompi.co/v1",
}


@dataclass
class Config:
    entorno: str = "sandbox"
    api_wompi: str = URL_WOMPI["sandbox"]
    checkout_wompi: str = "https://checkout.wompi.co/p/"
    llave_publica: str = ""
    llave_privada: str = ""
    secreto_integridad: str = ""
    secreto_eventos: str = ""
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

    @classmethod
    def desde_entorno(cls) -> "Config":
        e = os.environ.get
        entorno = e("WOMPI_ENTORNO", "sandbox")
        c = cls(
            entorno=entorno,
            api_wompi=e("WOMPI_API_URL", URL_WOMPI.get(entorno, URL_WOMPI["sandbox"])),
            checkout_wompi=e("WOMPI_CHECKOUT_URL", "https://checkout.wompi.co/p/"),
            llave_publica=e("WOMPI_LLAVE_PUBLICA", ""),
            llave_privada=e("WOMPI_LLAVE_PRIVADA", ""),
            secreto_integridad=e("WOMPI_SECRETO_INTEGRIDAD", ""),
            secreto_eventos=e("WOMPI_SECRETO_EVENTOS", ""),
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
        if self.entorno not in URL_WOMPI:
            raise ValueError(f"WOMPI_ENTORNO debe ser sandbox o produccion, no {self.entorno!r}")
        if self.entorno == "sandbox":
            for nombre, valor, prefijo in (
                ("WOMPI_LLAVE_PUBLICA", self.llave_publica, "pub_test_"),
                ("WOMPI_LLAVE_PRIVADA", self.llave_privada, "prv_test_"),
                ("WOMPI_SECRETO_INTEGRIDAD", self.secreto_integridad, "test_integrity_"),
                ("WOMPI_SECRETO_EVENTOS", self.secreto_eventos, "test_events_"),
            ):
                if valor and not valor.startswith(prefijo):
                    raise ValueError(f"{nombre} no es de sandbox (debe empezar por {prefijo})")
        else:
            if os.environ.get("PASE_PERMITIR_PRODUCCION") != "1":
                raise ValueError("Producción bloqueada: falta PASE_PERMITIR_PRODUCCION=1")
            if not self.llave_privada.startswith("prv_prod_"):
                raise ValueError("WOMPI_LLAVE_PRIVADA de producción debe empezar por prv_prod_")
        if not self.moodle_simulado and not (self.moodle_url and self.moodle_token):
            raise ValueError("Moodle real necesita PASE_MOODLE_URL y PASE_MOODLE_TOKEN")
