"""Demo local: simulador de Wompi + conector, para probar el flujo en el navegador.

    python -m pase.demo
Abre http://localhost:8080/?c=wa-afiliados y paga con la tarjeta 4242 4242 4242 4242
(cualquier CVC y fecha futura) o con Nequi 3991111111. Moodle va simulado.
"""
import os
import tempfile
import threading

from . import simulador_wompi as simw
from .config import Config
from .servidor import App


def main():
    puerto = int(os.environ.get("PASE_PUERTO", "8080"))
    _, srv = simw.arrancar(8090, f"http://127.0.0.1:{puerto}/webhooks/wompi", demora=1.5)
    c = Config(api_wompi="http://127.0.0.1:8090/v1", checkout_wompi="http://127.0.0.1:8090/p/",
               llave_publica=simw.LLAVE_PUBLICA, llave_privada=simw.LLAVE_PRIVADA,
               secreto_integridad=simw.SECRETO_INTEGRIDAD, secreto_eventos=simw.SECRETO_EVENTOS,
               url_publica=f"http://localhost:{puerto}", puerto=puerto,
               base_datos=os.path.join(tempfile.gettempdir(), "pase-demo.db"),
               avisos_correo=["camara@ejemplo.co", "pase@edunest.co"])
    print(f"Abre http://localhost:{puerto}/?c=wa-afiliados")
    App(c).servir()


if __name__ == "__main__":
    threading.current_thread().name = "demo"
    main()
