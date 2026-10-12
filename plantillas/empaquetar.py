#!/usr/bin/env python3
"""Empaqueta cada componente de componentes/ como un .zip SCORM 1.2 listo para Moodle.

Uso:
    python3 empaquetar.py                      # todos los componentes
    python3 empaquetar.py calculadora          # solo uno
    python3 empaquetar.py calculadora --curso costos-u2-practica
        # usa componentes/calculadora como molde pero toma contenido.js y medios/
        # de cursos/costos-u2-practica/ (una carpeta por pieza de curso)
    Para un curso completo usa armar_curso.py --scorm, que llama a empaquetar_desde() por cada pieza.

Cada paquete lleva: index.html, contenido.js, comun/aula.css, comun/aula.js,
la carpeta medios/ si existe, e imsmanifest.xml. Resultado en scorm/<nombre>.zip.
En Moodle: Agregar actividad > Paquete SCORM > subir el .zip.
"""
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent
COMUN = RAIZ / "comun"
SALIDA = RAIZ / "scorm"

MANIFIESTO = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="aula-soacha-{id}" version="1.0"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata><schema>ADL SCORM</schema><schemaversion>1.2</schemaversion></metadata>
  <organizations default="org">
    <organization identifier="org">
      <title>{titulo}</title>
      <item identifier="item1" identifierref="rec1" isvisible="true"><title>{titulo}</title></item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="rec1" type="webcontent" adlcp:scormtype="sco" href="index.html">
{archivos}
    </resource>
  </resources>
</manifest>
"""


def titulo_de(contenido_js: str, defecto: str) -> str:
    m = re.search(r'titulo:\s*"([^"]+)"', contenido_js)
    return m.group(1) if m else defecto


def empaquetar(molde: str, curso: str | None = None) -> Path:
    fuente = RAIZ / "cursos" / curso if curso else RAIZ / "componentes" / molde
    return empaquetar_desde(molde, fuente, curso or molde, SALIDA)


def empaquetar_desde(molde: str, fuente: Path, nombre: str, salida: Path) -> Path:
    """Molde de componentes/<molde> + contenido.js y medios/ de la carpeta fuente -> salida/<nombre>.zip"""
    base = RAIZ / "componentes" / molde
    if not (base / "index.html").exists():
        sys.exit(f"No existe el componente: {molde}")
    if not (fuente / "contenido.js").exists():
        sys.exit(f"Falta contenido.js en {fuente}")

    html = (base / "index.html").read_text(encoding="utf-8").replace("../../comun/", "comun/")
    contenido = (fuente / "contenido.js").read_text(encoding="utf-8")
    archivos = {
        "index.html": html.encode("utf-8"),
        "contenido.js": contenido.encode("utf-8"),
        "comun/aula.css": (COMUN / "aula.css").read_bytes(),
        "comun/aula.js": (COMUN / "aula.js").read_bytes(),
    }
    medios = fuente / "medios"
    if medios.is_dir():
        for f in sorted(medios.rglob("*")):
            if f.is_file():
                archivos["medios/" + f.relative_to(medios).as_posix()] = f.read_bytes()

    lista = "\n".join(f'      <file href="{escape(p)}"/>' for p in archivos)
    manifiesto = MANIFIESTO.format(id=nombre, titulo=escape(titulo_de(contenido, nombre)), archivos=lista)

    salida.mkdir(parents=True, exist_ok=True)
    destino = salida / f"{nombre}.zip"
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", manifiesto)
        for ruta, datos in archivos.items():
            z.writestr(ruta, datos)
    return destino


if __name__ == "__main__":
    args = sys.argv[1:]
    curso = None
    if "--curso" in args:
        i = args.index("--curso")
        curso = args[i + 1]
        del args[i:i + 2]
    moldes = args or sorted(p.name for p in (RAIZ / "componentes").iterdir() if (p / "index.html").exists())
    for m in moldes:
        d = empaquetar(m, curso)
        print(f"✓ {d.relative_to(RAIZ)}  ({d.stat().st_size // 1024} KB)")
