"""Demo local: simulador de ePayco + conector, para probar el flujo en el navegador.

    python -m pase.demo
Abre http://localhost:8080/?c=wa-afiliados y paga con la tarjeta 4575 6231 8229 0326
(cualquier CVC y fecha futura; 4151 6115 2758 3283 rechaza) o con el botón de PSE/Nequi,
que abre un Checkout simulado con Aprobar / Rechazar. Moodle va simulado.
"""
import os
import tempfile
import threading

from . import simulador_epayco as sime
from .config import Config
from .servidor import App


def main():
    puerto = int(os.environ.get("PASE_PUERTO", "8080"))
    _, srv = sime.arrancar(8090, demora=1.5)
    api = "http://127.0.0.1:8090"
    c = Config(api_epayco=api, validacion_epayco=api, checkout_js=f"{api}/checkout.js",
               token_js=f"{api}/epayco.js", cliente_id=sime.CLIENTE_ID, p_key=sime.P_KEY,
               llave_publica=sime.LLAVE_PUBLICA, llave_privada=sime.LLAVE_PRIVADA,
               url_publica=f"http://localhost:{puerto}", puerto=puerto,
               base_datos=os.path.join(tempfile.gettempdir(), "pase-demo-epayco.db"),
               avisos_correo=["camara@ejemplo.co", "pase@edunest.co"])
    print(f"Abre http://localhost:{puerto}/?c=wa-afiliados")
    App(c).servir()


if __name__ == "__main__":
    threading.current_thread().name = "demo"
    main()
