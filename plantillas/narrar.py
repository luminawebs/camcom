#!/usr/bin/env python3
"""Genera las narraciones de un curso con la API de Resemble AI.

Uso: python3 plantillas/narrar.py cursos/<id> [--forzar] [--solo-texto]

Lee "narracion" de curso.json:
    "narracion": {"voz": "a253156d", "secciones": ["entrada", "aprende"]}
y genera, en MP3 mono de 64 kbps:
- entrada  -> <curso>/medios-moodle/uN-entrada-narracion.mp3  (el caso de la Entrada, con su pregunta)
- aprende  -> <curso>/piezas/uN-aprende/medios/narracion-K.mp3  (una por pantalla de la lección;
              el contenido.js de la pieza debe llevar narracion: true para mostrar el reproductor)

No narra el video de bienvenida ni los resúmenes de unidad: esos se hacen a mano en NotebookLM.
La clave va en la variable de entorno RESEMBLE_API_KEY (nunca en el repositorio).
<curso>/narraciones.json guarda el texto leído de cada audio: si el texto no cambió, no se vuelve a generar
(--forzar los rehace todos). --solo-texto escribe narraciones.json sin llamar a la API, para revisar los textos.
Después: python3 plantillas/armar_curso.py cursos/<id> --scorm (pone los reproductores y mete los audios en los SCORM).
"""
import base64, hashlib, json, os, re, subprocess, sys, tempfile, urllib.request
from pathlib import Path

URL = "https://f.cluster.resemble.ai/synthesize"


def leer_contenido(js: Path) -> dict:
    """contenido.js -> dict (lo evalúa node, así se respeta la sintaxis JS de los moldes)."""
    codigo = "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.CONTENIDO))"
    return json.loads(subprocess.run(["node", "-e", codigo, str(js)], capture_output=True, text=True, check=True).stdout)


NUMEROS = dict(zip("123456789", ["Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis", "Siete", "Ocho", "Nueve"]))


def miles(m):
    return m.group(1).replace(".", "") + " pesos"


def limpiar(s: str, datos: dict | None = None) -> str:
    """Texto de pantalla -> texto para leer en voz alta."""
    s = re.sub(r"\{\{(\w+)\}\}", lambda m: str((datos or {}).get(m.group(1), "")), s)
    s = re.sub(r"\s*\[(VERIFICAR|VALIDAR|por definir)[^\]]*\]", "", s)   # marcas de revisión
    s = re.sub(r"\[([^\]]*)\]", r"\1", s)
    s = s.replace("**", "")
    s = re.sub(r"\$\s?(\d{1,3}(?:\.\d{3})+|\d+)", miles, s)                 # $300.000 -> 300000 pesos
    s = re.sub(r"(\d{1,3})\.(\d{3})\b", r"\1\2", s)                     # 3.500 -> 3500 (miles)
    s = re.sub(r"(\d)\s?%", r"\1 por ciento", s)
    s = re.sub(r"(^|\n|[.:]\s)\s*(\d)\.\s", lambda m: m.group(1) + NUMEROS.get(m.group(2), m.group(2)) + ": ", s)  # listas 1. 2. 3.
    s = s.replace(" · ", ", ").replace("→", ":").replace("=", " es igual a ")
    s = re.sub(r"\n+", ". ", s)
    s = re.sub(r"\.\s*\.", ".", s)
    s = re.sub(r":\s*\.", ":", s)
    return re.sub(r"\s+", " ", s).strip()


def textos(curso: Path, c: dict) -> dict:
    """{ruta relativa del mp3: texto a leer}"""
    secs = c["narracion"].get("secciones", ["entrada", "aprende"])
    out = {}
    for i, u in enumerate(c["unidades"], 1):
        if "entrada" in secs:
            e = u["entrada"]
            out[f"medios-moodle/u{i}-entrada-narracion.mp3"] = limpiar(f"{e['titulo']}. {e['texto']} La pregunta de esta unidad: {e['pregunta']}")
        js = curso / "piezas" / f"u{i}-aprende" / "contenido.js"
        if "aprende" in secs and js.exists():
            ct = leer_contenido(js)
            if not ct.get("narracion"):
                print(f"aviso: {js.relative_to(curso)} no tiene narracion: true; el audio se genera pero la lección no lo muestra")
            for k, p in enumerate(ct["pantallas"], 1):
                out[f"piezas/u{i}-aprende/medios/narracion-{k}.mp3"] = limpiar(f"{p['titulo']}. {p['texto']}", ct.get("datos"))
    return out


def sintetizar(texto: str, voz: str, clave: str, destino: Path):
    cuerpo = json.dumps({"voice_uuid": voz, "data": texto, "output_format": "mp3"}).encode("utf-8")
    req = urllib.request.Request(URL, data=cuerpo, method="POST", headers={
        "Authorization": f"Bearer {clave}", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate"})
    with urllib.request.urlopen(req, timeout=180) as r:
        crudo = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            import gzip
            crudo = gzip.decompress(crudo)
    d = json.loads(crudo)
    if not d.get("success"):
        sys.exit(f"Resemble rechazó {destino.name}: {d.get('issues') or d}")
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(base64.b64decode(d["audio_content"]))
    destino.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp.name, "-ac", "1", "-b:a", "64k", str(destino)], check=True)
    os.unlink(tmp.name)
    return round(d.get("duration", 0), 1)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    curso = Path(args[0]).resolve()
    c = json.loads((curso / "curso.json").read_text(encoding="utf-8"))
    if "narracion" not in c:
        sys.exit('curso.json no tiene "narracion": {"voz": "...", "secciones": [...]}')
    voz = c["narracion"]["voz"]
    registro_ruta = curso / "narraciones.json"
    registro = json.loads(registro_ruta.read_text(encoding="utf-8")) if registro_ruta.exists() else {}
    pedidos = textos(curso, c)
    clave = os.environ.get("RESEMBLE_API_KEY")
    if "--solo-texto" not in args and not clave:
        sys.exit("Falta la variable de entorno RESEMBLE_API_KEY")
    hechos = 0
    for ruta, texto in pedidos.items():
        firma = hashlib.sha1(f"{voz}|{texto}".encode("utf-8")).hexdigest()[:12]
        anterior = registro.get(ruta, {})
        if "--solo-texto" in args:
            registro[ruta] = {**anterior, "texto": texto}
            continue
        if anterior.get("firma") == firma and (curso / ruta).exists() and "--forzar" not in args:
            continue
        seg = sintetizar(texto, voz, clave, curso / ruta)
        registro[ruta] = {"texto": texto, "firma": firma, "segundos": seg, "kb": (curso / ruta).stat().st_size // 1024}
        hechos += 1
        print(f"✓ {ruta}  {seg} s")
    for viejo in [r for r in registro if r not in pedidos]:
        del registro[viejo]
    registro_ruta.write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(v.get("segundos", 0) for v in registro.values())
    print(f"{hechos} audios nuevos · {len(pedidos)} narraciones · {total / 60:.1f} min en total · voz {voz}")


if __name__ == "__main__":
    main()
