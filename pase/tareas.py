"""Tareas programadas del conector (cron diario o cada hora).

    python -m pase.tareas cobro       cobro mensual, reintentos y cancelaciones (diario)
    python -m pase.tareas conciliar   recupera confirmaciones perdidas consultando ePayco (diario)
    python -m pase.tareas pendientes  reprocesa confirmaciones guardadas sin procesar (cada hora)
    python -m pase.tareas correos     envía los avisos pendientes por SMTP (cada 5 minutos)
    python -m pase.tareas probar-correo DESTINO   encola un aviso de prueba y lo envía ya
    python -m pase.tareas resumen     cifras rápidas en JSON
"""
import json
import sys

from . import moodle
from .config import Config
from .nucleo import Pase


def main(argv):
    if argv[:1] == ["probar-correo"] and len(argv) == 2:
        pase = Pase(Config.desde_entorno(), moodle.crear(Config.desde_entorno()))
        pase.avisar_con_diseno(argv[1], "prueba")
        print(json.dumps(pase.enviar_avisos(), ensure_ascii=False))
        return 0
    if len(argv) != 1 or argv[0] not in ("cobro", "conciliar", "pendientes", "correos", "resumen"):
        print(__doc__)
        return 2
    c = Config.desde_entorno()
    pase = Pase(c, moodle.crear(c))
    if argv[0] == "cobro":
        r = pase.cobro_mensual()
    elif argv[0] == "conciliar":
        r = pase.conciliar()
    elif argv[0] == "pendientes":
        r = pase.procesar_pendientes()
    elif argv[0] == "correos":
        r = pase.enviar_avisos()
    else:
        r = pase.resumen()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
