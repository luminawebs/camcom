#!/usr/bin/env python3
"""Arma la versión publicable de un curso y su respaldo .mbz con los medios incluidos.

Uso: python3 moodle/publicar_curso.py cursos/<id> --corto AVS-G01

No toca la carpeta del curso: copia todo a una carpeta temporal y ahí
- cambia los recuadros de medios (as-hueco) por el video o la imagen real de <curso>/medios-moodle/,
- cambia las rutas ../mapas/, ../guias-pdf/ y ../descargas/ por archivos dentro de la página,
- quita las marcas de pendiente ([VERIFICAR …], [por definir], botones sin destino),
- quita las marcas de los SCORM (contenido.js dentro de cada .zip),
y llama a armar_respaldo.py. Lo que se quita queda en <salida>/quitado-al-publicar.txt para el registro del contador.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

VIDEO = ('<video controls preload="metadata" playsinline style="width:100%;max-width:420px;display:block;margin:0 auto;'
         'border-radius:12px;background:#000"><source src="@@PLUGINFILE@@/{0}" type="video/mp4"></video>')
IMG = '<img src="@@PLUGINFILE@@/{0}" alt="{1}" style="display:block;width:100%;height:auto;border-radius:8px">'
HUECO = re.compile(r'<div class="as-hueco[^"]*"><b>[^<]*</b><span>([^<]*)</span></div>')
AVISO_IA = "Resumen generado con inteligencia artificial a partir de los contenidos del curso."
log = []


def quitar(ruta, texto, antes, despues=""):
    if antes in texto:
        log.append(f"{ruta}: «{re.sub('<[^>]+>', '', antes).strip()}»" + (f" → «{re.sub('<[^>]+>', '', despues).strip()}»" if despues else " (quitado)"))
    return texto.replace(antes, despues)


def pagina(ruta, s, medios):
    nombre = ruta.name
    m = re.match(r"(u\d)-(resumen|entrada|llevatelo|cabecera)\.html", nombre)
    u, tipo = (m.group(1), m.group(2)) if m else (None, None)
    for h in HUECO.finditer(s):
        bloque, desc = h.group(0), h.group(1)
        if tipo == "resumen" and f"{u}-resumen.mp4" in medios:
            s = s.replace(bloque, VIDEO.format(f"{u}-resumen.mp4"))
        elif tipo == "entrada" and f"{u}-entrada.jpg" in medios:
            s = s.replace(bloque, IMG.format(f"{u}-entrada.jpg", desc.split(" (")[0]))
        elif nombre == "00-inicio.html" and "bienvenida.mp4" in medios:
            s = s.replace(bloque, VIDEO.format("bienvenida.mp4"))
        else:
            s = quitar(nombre, s, bloque)
    if tipo == "resumen":
        for aviso in re.findall(r"Resumen generado con inteligencia artificial y revisado por [^<]+?\.", s):
            s = quitar(nombre, s, aviso, AVISO_IA)
    # rutas relativas a archivos del curso
    for carpeta in ("mapas", "guias-pdf", "descargas", "medios-moodle"):
        s = re.sub(rf'(src|href|poster)="\.\./{carpeta}/([^"]+)"', r'\1="@@PLUGINFILE@@/\2"', s)
    # descargas que ya existen
    for texto, archivo in (("Plantilla Calcula tu sueldo · Excel 40 KB", "u2-calcula-tu-sueldo.xlsx"),
                           ("Plantilla Registro diario · Excel 40 KB", "u3-registro-diario.xlsx"),
                           ("Hoja para imprimir del cuaderno · PDF 150 KB", "u3-hoja-registro.pdf")):
        viejo = f'<a class="as-btn as-btn--sec" href="#">⬇ <em class="as-ph">[{texto}]</em></a>'
        if viejo in s and archivo in medios:
            kb = max(1, medios[archivo] // 1024)
            nuevo_t = texto.rsplit(" · ", 1)[0] + f" · {texto.rsplit(' · ', 1)[1].split()[0]} {kb} KB"
            s = s.replace(viejo, f'<a class="as-btn as-btn--sec" href="@@PLUGINFILE@@/{archivo}" target="_blank">⬇ {nuevo_t}</a>')
    # botones sin destino con texto pendiente (fichas, descuento) y el botón de resumen de la cabecera
    for a in re.findall(r'<a class="as-btn[^"]*" href="#"[^>]*>(?:(?!</a>).)*<em class="as-ph">(?:(?!</a>).)*</a>', s):
        s = quitar(nombre, s, a)
    if tipo == "cabecera":
        for a in re.findall(r'<a class="as-btn[^"]*" href="#"[^>]*>▶ Resumen[^<]*</a>\s*', s):
            s = quitar(nombre, s, a)
    s = quitar(nombre, s, "Foro Comunidad o WhatsApp de la Cámara", "Foro Comunidad")
    for ph in re.findall(r'\s*<em class="as-ph">\[[^\]]*\]</em>', s):
        s = quitar(nombre, s, ph)
    for v in re.findall(r"\s*\[VERIFICAR[^\]]*\]", s):
        s = quitar(nombre, s, v)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("curso")
    ap.add_argument("--corto", required=True)
    ap.add_argument("--salida")
    a = ap.parse_args()
    curso = (RAIZ / a.curso).resolve() if not os.path.isabs(a.curso) else Path(a.curso)
    info = json.loads((curso / "curso.json").read_text(encoding="utf-8"))
    salida = Path(a.salida) if a.salida else RAIZ / "moodle" / info["id"]
    tmp = Path(tempfile.mkdtemp(prefix="publicar-"))
    pub = tmp / info["id"]
    shutil.copytree(curso, pub, ignore=shutil.ignore_patterns("vista-previa", "notebooklm", "medios", "*.mbz"))

    # todos los archivos que las páginas pueden citar, en un solo lugar
    mm = pub / "medios-moodle"
    mm.mkdir(exist_ok=True)
    for carpeta, patron in (("mapas", "*.png"), ("guias-pdf", "*.pdf"), ("descargas", "*.xlsx"), ("descargas", "*.pdf")):
        for f in (pub / carpeta).glob(patron) if (pub / carpeta).is_dir() else []:
            shutil.copy(f, mm / f.name)
    medios = {f.name: f.stat().st_size for f in mm.iterdir()}

    for ruta in sorted((pub / "paginas").glob("*.html")):
        ruta.write_text(pagina(ruta, ruta.read_text(encoding="utf-8"), medios), encoding="utf-8")

    # SCORM sin marcas: se reescribe contenido.js dentro de cada paquete ya armado
    for z in sorted((pub / "scorm").glob("*.zip")):
        with zipfile.ZipFile(z) as zin:
            entradas = [(i, zin.read(i.filename)) for i in zin.infolist()]
        cambio = False
        for k, (i, data) in enumerate(entradas):
            if i.filename.endswith("contenido.js"):
                t = data.decode("utf-8")
                for v in re.findall(r"\s*\[VERIFICAR[^\]]*\]", t):
                    log.append(f"{z.name}/contenido.js: «{v.strip()}» (quitado)")
                    t = t.replace(v, "")
                    cambio = True
                for bloque, nota in re.findall(r'(,?\s*medio: \{ tipo: "[^"]*", src: "", nota: "([^"]*)" \})', t):
                    log.append(f"{z.name}/contenido.js: imagen pendiente «{nota}» (recuadro quitado)")
                    t = t.replace(bloque, "")
                    cambio = True
                entradas[k] = (i, t.encode("utf-8"))
        if cambio:
            with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zout:
                for i, data in entradas:
                    zout.writestr(i, data)

    # nada pendiente debe quedar a la vista
    restos = []
    for ruta in (pub / "paginas").glob("*.html"):
        frag = ruta.read_text(encoding="utf-8")
        for patron in ("as-hueco", "as-ph", "VERIFICAR", "../mapas/", "../guias-pdf/", "../descargas/", "../medios-moodle/"):
            if patron in frag:
                restos.append(f"{ruta.name}: {patron}")
    if restos:
        sys.exit("Quedan pendientes a la vista:\n" + "\n".join(restos))

    salida.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(RAIZ / "moodle" / "armar_respaldo.py"), str(pub), "--corto", a.corto,
                    "--salida", str(salida)], check=True)
    (salida / "quitado-al-publicar.txt").write_text(
        "Marcas de pendiente quitadas al publicar (van al registro del contador):\n\n" + "\n".join(log) + "\n", encoding="utf-8")
    shutil.rmtree(tmp)
    print(f"{len(log)} cambios de texto · medios incluidos: {', '.join(sorted(medios))}")


if __name__ == "__main__":
    main()
