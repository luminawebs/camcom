#!/usr/bin/env python3
"""Arma un curso completo a partir de su ficha (cursos/<id>/curso.json).

Uso (desde la carpeta del proyecto):
    python3 plantillas/armar_curso.py cursos/plata-negocio            # páginas + estructura + vista previa
    python3 plantillas/armar_curso.py cursos/plata-negocio --scorm    # además, los .zip SCORM

Qué produce dentro de la carpeta del curso:
    estructura.md     árbol del curso: secciones, pasos, actividad de Moodle y minutos
    paginas/*.html    fragmentos llenos para pegar en el editor de Moodle (entre COPIAR DESDE AQUÍ y HASTA AQUÍ)
    vista-previa/     sitio para revisar el curso en tamaño celular (abrir vista-previa/index.html)
    scorm/*.zip       con --scorm: un paquete por pieza interactiva (piezas/<pieza>/contenido.js)

La estructura sale del esqueleto universal y de la receta del perfil (manual de producción):
cada perfil dice qué molde llena Aprende y Practica, y el nivel dice qué pasos van y cuántos minutos.
"""
import html
import json
import re
import shutil
import urllib.parse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))
import empaquetar  # noqa: E402

NIVELES = {"g": "Gancho gratuito", "c": "Certificado asincrónico", "p": "Premium en vivo"}
PASOS = ["entrada", "aprende", "practica", "aplica", "demuestra", "llevatelo", "profundiza"]
NOMBRE_PASO = {"entrada": "Entrada", "aprende": "Aprende", "practica": "Practica", "aplica": "Aplica",
               "demuestra": "Demuestra", "llevatelo": "Llévatelo", "profundiza": "Profundiza"}
PREGUNTA_PASO = {"entrada": "¿Por qué me importa?", "aprende": "¿Qué necesito saber?", "practica": "¿Lo entendí?",
                 "aplica": "¿Me sirve a mí?", "demuestra": "¿Lo logré?", "llevatelo": "¿Qué me llevo?",
                 "profundiza": "¿Dónde aprendo más?"}
# Invitación al Pase al final de la última unidad gratuita (curso.json "pase": {"unidades": [4 títulos de U4-U7]}).
# El canal ?c= le dice al conector de qué curso llegó la persona.
PASE_URL = "https://pase.edunest.co/"
PASE_PRECIO = "$29.000 al mes"

# Receta por perfil: paso -> (formato, actividad de Moodle, min certificado, min gancho, molde HTML5 o None)
# Profundiza es opcional (0 min). En el gancho, Aplica se reemplaza por PEER_G (foro entre pares, sin tutor).
RECETAS = {
    "K": {"nombre": "Cálculo y análisis", "pasos": {
        "entrada": ("Caso con números", "Página", 2, 1, None),
        "aprende": ("Lección interactiva", "SCORM 1.2 · HTML5", 8, 5, "leccion-interactiva"),
        "practica": ("Calculadora con retroalimentación", "SCORM 1.2 · HTML5", 10, 8, "calculadora"),
        "aplica": ("Tus números en la plantilla", "Tarea", 20, 8, None),
        "demuestra": ("Cuestionario calculado", "Cuestionario", 10, 0, None),
        "llevatelo": ("Fórmula + plantilla", "Página + Archivo", 3, 2, None),
        "profundiza": ("Lecturas y guías", "Carpeta + URL", 0, 0, None)}},
    "N": {"nombre": "Normativa y trámites", "pasos": {
        "entrada": ("¿Te pasó?", "Página", 2, 1, None),
        "aprende": ("Lección con cifras editables", "SCORM 1.2 · HTML5", 8, 5, "leccion-interactiva"),
        "practica": ("Árbol de decisión", "SCORM 1.2 · HTML5", 10, 8, "arbol-decision"),
        "aplica": ("Checklist de mi negocio", "Tarea", 15, 8, None),
        "demuestra": ("Cuestionario", "Cuestionario", 10, 0, None),
        "llevatelo": ("Calendario y checklist", "Página + Archivo", 3, 2, None),
        "profundiza": ("Fuentes oficiales", "URL + Página", 0, 0, None)}},
    "P": {"nombre": "Procedimiento en herramienta", "pasos": {
        "entrada": ("Reto del día", "Página", 2, 1, None),
        "aprende": ("Screencast corto", "H5P · Video interactivo", 7, 5, None),
        "practica": ("Simulador de pantalla", "SCORM 1.2 · HTML5", 10, 8, "simulador-pantalla"),
        "aplica": ("Hazlo en tu negocio", "Tarea", 15, 8, None),
        "demuestra": ("Cuestionario", "Cuestionario", 10, 0, None),
        "llevatelo": ("Ficha paso a paso", "Página + Archivo", 3, 2, None),
        "profundiza": ("Ayuda oficial de la herramienta", "URL + Página", 0, 0, None)}},
    "E": {"nombre": "Estrategia", "pasos": {
        "entrada": ("Dos negocios, dos resultados", "Página", 2, 1, None),
        "aprende": ("Pódcast de caso", "Página con audio", 8, 5, None),
        "practica": ("Lienzo interactivo", "SCORM 1.2 · HTML5", 10, 8, "lienzo"),
        "aplica": ("Tu plan", "Tarea con rúbrica", 20, 8, None),
        "demuestra": ("Cuestionario", "Cuestionario", 10, 0, None),
        "llevatelo": ("Plantilla del lienzo", "Página + Archivo", 3, 2, None),
        "profundiza": ("Lecturas y casos", "Carpeta + URL", 0, 0, None)}},
    "H": {"nombre": "Habilidad creativa", "pasos": {
        "entrada": ("Antes y después", "Página", 2, 1, None),
        "aprende": ("Video demostración", "H5P · Video interactivo", 7, 5, None),
        "practica": ("¿Cuál funciona mejor?", "SCORM 1.2 · HTML5", 8, 6, "comparador"),
        "aplica": ("Sube tu trabajo", "Taller (revisión entre pares)", 20, 10, None),
        "demuestra": ("Cuestionario", "Cuestionario", 8, 0, None),
        "llevatelo": ("Checklist de grabación", "Página", 3, 2, None),
        "profundiza": ("Referentes y tutoriales", "URL + Página", 0, 0, None)}},
    "R": {"nombre": "Relacional", "pasos": {
        "entrada": ("El mensaje difícil", "Página", 2, 1, None),
        "aprende": ("Pódcast con diálogos", "Página con audio", 7, 5, None),
        "practica": ("Escenario ramificado", "SCORM 1.2 · HTML5", 10, 8, "escenario-ramificado"),
        "aplica": ("Tus respuestas", "Tarea", 15, 8, None),
        "demuestra": ("Cuestionario situacional", "Cuestionario", 10, 0, None),
        "llevatelo": ("Banco de respuestas", "Página", 3, 2, None),
        "profundiza": ("Lecturas y guías", "Carpeta + URL", 0, 0, None)}},
}

INICIO_GANCHO = [
    ("Bienvenida", "Video vertical de 60 s: qué vas a lograr.", "H5P · Video interactivo", 1),
    ("Datos y perfil del negocio", "Autorización Ley 1581, sector, barrio y necesidad.", "Retroalimentación", 2),
    ("Diagnóstico rápido", "3 preguntas para saber desde dónde arranca.", "Cuestionario", 3),
]
PEER_G = ("Comparte y comenta", "Foro de preguntas y respuestas", 15, 8, None)
# Resumen de unidad: video O audio, nunca los dos. curso.json "resumen_formato" (o unidad.resumen.formato).
RESUMEN = {
    "video": ("Video de 60 s (automático o NotebookLM)", "H5P · Video interactivo", "▶ Resumen en video · 1 min", "Resumen en video"),
    "audio": ("Audio de 5 min (NotebookLM)", "Página con audio", "♪ Resumen en audio · 5 min", "Resumen en audio"),
}


def formato_resumen(c, u):
    f = (u.get("resumen") or {}).get("formato") or c.get("resumen_formato", "audio")
    if f not in RESUMEN:
        raise SystemExit(f"resumen_formato debe ser 'video' o 'audio', no {f!r}")
    return f
CIERRE_GANCHO = [
    ("Reto final entre pares", "Por cohorte mensual: entregas tu resultado y Moodle te asigna dos compañeros para evaluar con una rúbrica de 3 criterios.", "Taller (revisión entre pares)", 15),
    ("Constancia de participación", "Se emite al completar las 3 unidades.", "Certificado personalizado", 1),
    ("Tu siguiente paso", "Invitación al curso certificado con descuento.", "Página", 2),
]


# ---------------------------------------------------------------- utilidades
def t(s):
    """Escapa y resalta [lo que falta] igual que aula.js."""
    s = html.escape(str(s), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"\[([^\]]+)\]", r'<em class="as-ph">[\1]</em>', s)


def hueco(tipo, nombre, nota):
    return f'<div class="as-hueco as-hueco--{tipo}"><b>{nombre}</b><span>{t(nota)}</span></div>'


def pagina(titulo, donde, cuerpo, css):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)}</title>
<link rel="stylesheet" href="{css}">
<style>body{{margin:0;background:#f6f6f7}}.vista{{max-width:760px;margin:0 auto;padding:16px}}</style>
</head>
<body>
<!-- {html.escape(titulo)}
     Dónde va en Moodle: {donde}
     Cómo usarlo: editor de Moodle en "Código HTML" (botón < >), pega SOLO lo que está entre
     COPIAR DESDE AQUÍ y HASTA AQUÍ. Lo resaltado entre [ ] falta validar o producir. -->
<div class="vista">
<!-- ===== COPIAR DESDE AQUÍ ===== -->
<div class="as as-pila">
{cuerpo}
</div>
<!-- ===== HASTA AQUÍ ===== -->
</div>
</body>
</html>
"""


def mapa(c, nombre, que):
    """Mapa mental: lo arma Claude desde los guiones en <curso>/mapas/ (NotebookLM no deja descargarlo)."""
    if nombre in c.get("_mapas", ()):
        return f'<img src="../mapas/{nombre}.png" alt="{html.escape(que)}" style="display:block;width:100%;height:auto;border-radius:8px">'
    return hueco("imagen", "Mapa mental", f"{que}. Lo arma Claude desde los guiones: mapas/{nombre}.png")


def ficha(c, i):
    """Ficha vertical 1080 × 1920 para el celular: la arma plantillas/fichas.py en <curso>/fichas/ (ya no Canva)."""
    kb = c.get("_fichas", {}).get(f"u{i}-ficha")
    if kb:
        return (f'<img src="../fichas/u{i}-ficha.jpg" alt="Ficha de la Unidad {i} para guardar en el celular" '
                f'style="display:block;width:100%;max-width:360px;height:auto;margin:0 auto;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.18)">'
                f'<a class="as-btn" href="../fichas/u{i}-ficha.jpg" download="u{i}-ficha.jpg" target="_blank">⬇ Guarda la ficha en tu celular · JPG {kb} KB</a>')
    return hueco('vertical', 'Ficha vertical', f'Ficha 1080 × 1920 para guardar en el celular. La arma Claude con plantillas/fichas.py en fichas/u{i}-ficha.jpg. Máx. 250 KB.')


def guia(c, i):
    """Guía de estudio en PDF: la arma Claude con el logo en <curso>/guias-pdf/ (ya no NotebookLM)."""
    kb = c.get("_guias", {}).get(f"u{i}-guia")
    if kb:
        return f'<a class="as-btn as-btn--sec" href="../guias-pdf/u{i}-guia.pdf" target="_blank">⬇ Guía de estudio de la Unidad {i} · PDF {kb} KB</a>'
    return f'<a class="as-btn as-btn--sec" href="#">⬇ <em class="as-ph">[Guía de estudio de la Unidad {i} · PDF A5. La arma Claude en guias-pdf/u{i}-guia.pdf]</em></a>'


def video_vertical(c, nombre, alterno):
    """Video vertical hecho con plantillas/video_resumen.py en medios-moodle/<nombre>.mp4 (bienvenida, uN-resumen). Si no existe, el espacio."""
    if f"{nombre}.mp4" not in c.get("_videos", ()):
        return alterno
    pista = f'<track kind="captions" srclang="es" label="Español" src="../medios-moodle/{nombre}.vtt">' if f"{nombre}.vtt" in c["_videos"] else ""
    return (f'<video controls preload="metadata" playsinline style="width:100%;max-width:420px;display:block;margin:0 auto;border-radius:12px;'
            f'background:#000" src="../medios-moodle/{nombre}.mp4">{pista}</video>')


def imagen_entrada(c, i, nota):
    """Ilustración de la Entrada (plantillas/ilustrar.py, Gemini) en medios-moodle/uN-entrada.jpg. Si no existe, deja el espacio."""
    if f"u{i}-entrada.mp4" in c.get("_imagenes", ()):  # video de la Entrada (plantillas/video_entrada.py): imagen + narración
        return (f'<video controls preload="metadata" playsinline poster="../medios-moodle/u{i}-entrada.jpg" style="display:block;width:100%;'
                f'border-radius:8px;background:#000" src="../medios-moodle/u{i}-entrada.mp4">'
                f'<track kind="captions" srclang="es" label="Español" src="../medios-moodle/u{i}-entrada.vtt"></video>')
    if f"u{i}-entrada.jpg" in c.get("_imagenes", ()):
        return f'<img src="../medios-moodle/u{i}-entrada.jpg" alt="{html.escape(nota.split(" (")[0])}" style="display:block;width:100%;height:auto;border-radius:8px">'
    return hueco("imagen", "Imagen", nota)


def narracion(c, nombre, que):
    """Narración de Resemble AI (plantillas/narrar.py) en medios-moodle/<nombre>.mp3. Si no existe, no se muestra nada."""
    if nombre not in c.get("_narraciones", ()):
        return ""
    return (f'\n    <div class="as-pila" style="gap:4px"><audio controls preload="none" src="../medios-moodle/{nombre}.mp3" style="width:100%"></audio>'
            f'<small class="as-sec">🔊 {t(que)} · voz generada con inteligencia artificial</small></div>')


def descarga(c, x):
    """Botón de descarga de Llévatelo. x es texto (pendiente) o {"texto", "archivo"} con el archivo en <curso>/descargas/."""
    if isinstance(x, dict):
        kb = c.get("_descargas", {}).get(x["archivo"])
        if kb:
            return f'<a class="as-btn as-btn--sec" href="../descargas/{html.escape(x["archivo"])}" target="_blank">⬇ {t(x["texto"])} · {kb} KB</a>'
        x = x["texto"]
    return f'<a class="as-btn as-btn--sec" href="#">⬇ <em class="as-ph">[{html.escape(x)}]</em></a>'


def ficha_moodle(eti, titulo, actividad, lineas, extra=""):
    """Tarjeta para piezas que se configuran en Moodle (no llevan plantilla propia)."""
    lis = "".join(f"<li>{t(x)}</li>" for x in lineas)
    return (f'<div class="as-tarjeta as-pila"><span class="as-eti">{t(eti)}</span><h2>{t(titulo)}</h2>'
            f'<span class="as-chip as-chip--gris" style="align-self:flex-start">Actividad de Moodle: {t(actividad)}</span>'
            f'<ul class="as-check">{lis}</ul>{extra}</div>')


def cursos_con_pase():
    """[(canal, título corto)] de los cursos del repo que tienen tramo del Pase, en el orden de su canal (AVS-G01, G02...)."""
    out = []
    for f in sorted((RAIZ.parent / "cursos").glob("*/curso.json")):
        x = json.loads(f.read_text(encoding="utf-8"))
        if x.get("pase"):
            out.append((x["pase"].get("canal", "curso-" + x["id"]), x.get("titulo_corto", x["titulo"])))
    return sorted(out)


def pagina_pase(c, n):
    """Invitación a comprar el Pase al final de la unidad n (la última gratuita). Lo que más resalta es que el Pase
    abre todos los cursos y todos sus certificados; debajo, lo que sigue en este curso (unidades 4 a 7)."""
    pa = c["pase"]
    canal = pa.get("canal", "curso-" + c["id"])
    enlace = f"{PASE_URL}?c={urllib.parse.quote(canal)}"
    todos = cursos_con_pase()
    lista = "".join(
        f'<li class="as-paso"{" style=\"border:2px solid var(--as-rojo)\"" if k == canal else ""}><span class="as-paso__n">📘</span>'
        f'<span class="as-paso__t"><b>{t(x)}</b>{"<small style=\"display:block\">Este curso</small>" if k == canal else ""}</span>'
        f'<span class="as-chip as-chip--ok">🎓 Certificado</span></li>' for k, x in todos)
    filas = "".join(
        f'<li class="as-paso"><span class="as-paso__n">{k}</span><span class="as-paso__t"><b>{t(x)}</b></span>'
        f'<span class="as-chip as-chip--rojo">🔒 Pase</span></li>' for k, x in enumerate(pa["unidades"], n + 1))
    dato = ('style="background:var(--as-rojo-100);border-radius:10px;padding:12px 14px;text-align:center"')
    grande = 'style="display:block;font-size:2rem;font-weight:700;line-height:1.1;color:var(--as-rojo-oscuro)"'
    return {f"paginas/u{n}-pase.html": (f"Unidad {n}: Lo que sigue", f"Página al final de la Unidad {n}, después de Profundiza. Sin finalización.", f"""
  <div class="as-banda as-pila">
    <span class="as-eti">Terminaste la parte gratuita</span>
    <h2>{t(pa.get('titulo', 'Vas muy bien. Sigue con el Pase Empresario'))}</h2>
    <p>{t(pa.get('texto', f'Ya hiciste las {n} unidades gratis de «{c.get("titulo_corto", c["titulo"])}». Con el Pase sigues aquí mismo, en la unidad {n + 1}, sin perder tu avance.'))}</p>
  </div>
  <div class="as-tarjeta as-pila" style="border:3px solid var(--as-rojo)">
    <span class="as-eti">Un solo pago al mes</span>
    <h2>Todos los cursos y todos sus certificados</h2>
    <div {dato}><b {grande}>📚 🎓</b>Todos los cursos del Aula y los nuevos que salgan, con un certificado por cada curso que termines</div>
    <ol class="as-pasos">{lista}</ol>
    <p class="as-sec">Cada certificado lleva tu nombre, el curso, las horas y un código de verificación.</p>
    <div class="as-aviso as-aviso--marca"><b>{PASE_PRECIO}.</b> Pagas con tarjeta, PSE, Nequi o Daviplata.</div>
    <a class="as-btn as-btn--ancho" href="{html.escape(enlace)}" target="_blank" rel="noopener">Quiero el Pase Empresario ›</a>
  </div>
  <div class="as-tarjeta as-pila">
    <h3>Lo que sigue en este curso</h3>
    <ol class="as-pasos">{filas}</ol>
    <p class="as-sec"><small>Usa el mismo correo con el que entras al Aula: así todo se abre solo en tu usuario.
      Si ya tienes el Pase, ya está abierto para ti.</small></p>
  </div>""")}


# ---------------------------------------------------------------- estructura
def estructura(c):
    nivel, receta = c["nivel"], RECETAS[c["perfil"]]
    pasos = [p for p in PASOS if not (nivel == "g" and p == "demuestra")]
    n_u = len(c["unidades"])
    secciones = [{"titulo": "INICIO", "tema": "Bienvenida, datos y diagnóstico", "items": []}]
    for nombre, desc, act, m in INICIO_GANCHO:
        secciones[0]["items"].append({"codigo": "", "nombre": nombre, "formato": desc, "actividad": act, "min": m,
                                      "pagina": "paginas/00-inicio.html" if nombre == "Bienvenida" else f"paginas/00-{slug(nombre)}.html"})
    for i, u in enumerate(c["unidades"], 1):
        r = RESUMEN[formato_resumen(c, u)]
        items = [{"codigo": f"U{i} · Resumen", "paso": "resumen", "nombre": r[3], "formato": r[0],
                  "actividad": r[1], "min": 0, "opcional": True, "pagina": f"paginas/u{i}-resumen.html"}]
        for p in pasos:
            ajuste = c.get("receta", {}).get(p)   # curso.json "receta": {"aprende": [formato, actividad, min c, min g, molde]}
            formato, act, mc, mg, molde = PEER_G if (nivel == "g" and p == "aplica") else (tuple(ajuste) if ajuste else receta["pasos"][p])
            it = {"codigo": f"U{i} · {NOMBRE_PASO[p]}", "paso": p, "formato": formato, "actividad": act,
                  "min": mg if nivel == "g" else mc}
            if p == "profundiza":
                it["opcional"] = True
            if molde:
                it.update(nombre=formato, molde=molde, pieza=f"piezas/u{i}-{p}")
            else:
                it.update(nombre=u[p].get("titulo", formato) if isinstance(u.get(p), dict) else formato, pagina=f"paginas/u{i}-{p}.html")
            items.append(it)
        if nivel == "g" and c.get("pase") and i == n_u:
            items.append({"codigo": f"U{i} · Lo que sigue", "paso": "pase", "nombre": "Unidades 4 a 7 con el Pase Empresario",
                          "formato": "Invitación al Pase", "actividad": "Página", "min": 0, "opcional": True,
                          "pagina": f"paginas/u{i}-pase.html"})
        secciones.append({"titulo": f"UNIDAD {i}", "tema": u["tema"], "objetivo": u["objetivo"], "items": items,
                          "cabecera": f"paginas/u{i}-cabecera.html", "n": i, "de": n_u})
    cierre = {"titulo": "CIERRE", "tema": "Reto, constancia y siguiente paso", "items": []}
    for nombre, desc, act, m in CIERRE_GANCHO:
        cierre["items"].append({"codigo": "", "nombre": nombre, "formato": desc, "actividad": act, "min": m,
                                "pagina": "paginas/99-cierre.html" if nombre == "Tu siguiente paso" else f"paginas/99-{slug(nombre)}.html"})
    secciones.append(cierre)
    for s in secciones:
        s["min"] = sum(x["min"] for x in s["items"])
    return secciones


def corta(actividad):
    """Nombre corto de la actividad de Moodle para chips."""
    a = actividad.split(" · ")[0]
    return a.split(" (")[0].replace("Foro de preguntas y respuestas", "Foro")


def slug(s):
    s = s.lower()
    for a, b in zip("áéíóúñ", "aeioun"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def fmt_min(m):
    return f"{m // 60} h {m % 60:02d} min" if m >= 60 else f"{m} min"


# ---------------------------------------------------------------- páginas
def paginas(c, secs):
    """Devuelve {ruta: (titulo, donde, cuerpo)}."""
    P = {}
    u_secs = [s for s in secs if s.get("n")]
    total = sum(s["min"] for s in secs)
    ini = c["inicio"]

    pasos_li = "".join(
        f'<li class="as-paso"><span class="as-paso__n">{k}</span><span class="as-paso__t"><b>{NOMBRE_PASO[p]}</b>'
        f'<small>{PREGUNTA_PASO[p]}</small></span><span></span></li>'
        for k, p in enumerate([p for p in PASOS if not (c["nivel"] == "g" and p == "demuestra")], 1))
    P["paginas/00-cabecera-curso.html"] = ("Cabecera del curso", "Resumen del curso o sección General.", f"""
  <div class="as-banda as-pila">
    <span class="as-eti">{NIVELES[c['nivel']]} · {len(u_secs)} unidades</span>
    <h1>{t(c['titulo'])}</h1>
    <p>{t(c['promesa'])}</p>
  </div>
  <div class="as-tarjeta as-pila">
    {hueco('video', 'Video', 'Bienvenida de 60 s, vertical, con subtítulos. H5P o MP4 liviano.')}
    <div class="as-fila" style="justify-content:space-between">
      <span class="as-chip">⏱ {t(c['duracion'])}</span>
      <span class="as-chip as-chip--rojo">{t(c['certificado'])}</span>
      <span class="as-chip as-chip--gris">Gratis</span>
    </div>
    <a class="as-btn as-btn--ancho" href="#">Empezar por el Inicio ›</a>
  </div>""")

    fs = {formato_resumen(c, u) for u in c["unidades"]}
    aviso_resumen = ("Cada unidad abre con un resumen en video de 1 minuto" if fs == {"video"} else
                     "Cada unidad abre con un resumen en audio de 5 minutos" if fs == {"audio"} else
                     "Cada unidad abre con un resumen corto, en video o en audio") + ", como adelanto antes de empezar o para repasar."
    P["paginas/00-inicio.html"] = ("Inicio del curso", "Sección INICIO: Página «Bienvenida». Debajo: Datos (Retroalimentación) y Diagnóstico (Cuestionario). Sube mapas/mapa-curso.png a la Página y cambia el src de la imagen.", f"""
  <div class="as-tarjeta as-pila">
    <span class="as-eti">Inicio · Bienvenida</span>
    <h2>{t(ini['bienvenida'])}</h2>
    {video_vertical(c, 'bienvenida', hueco('vertical', 'Video vertical', ini.get('video_nota', 'Bienvenida de 60 s: Luz Dary cuenta su problema y qué vas a lograr. Con subtítulos.')))}
    <p>{t(ini['texto'])}</p>
  </div>
  <div class="as-tarjeta as-pila">
    <h3>Así funciona cada unidad</h3>
    <p class="as-sec">Todas las unidades tienen los mismos pasos, en el mismo orden. Cada paso se desbloquea al terminar el anterior.</p>
    <ol class="as-pasos">{pasos_li}</ol>
  </div>
  <div class="as-tarjeta as-pila">
    <h3>Datos del curso</h3>
    <div>
      <div class="as-dato"><span>Duración</span><b>{t(c['duracion'])}</b></div>
      <div class="as-dato"><span>Unidades</span><b>{len(u_secs)}</b></div>
      <div class="as-dato"><span>Para la constancia</span><b>{t(ini['aprobar'])}</b></div>
      <div class="as-dato"><span>Funciona sin datos</span><b>Descarga en la app de Moodle</b></div>
      <div class="as-dato"><span>Dudas</span><b>{t(ini['dudas'])}</b></div>
    </div>
  </div>
  <div class="as-tarjeta as-pila">
    <h3>Mapa del curso</h3>
    {mapa(c, "mapa-curso", c.get("mapa_curso_nota", "Mapa del curso con las 3 unidades y sus fórmulas"))}
  </div>
  <p class="as-sec">{t(aviso_resumen)}</p>
  <div class="as-aviso as-aviso--marca"><b>Antes de empezar:</b> llena tus datos y responde el diagnóstico (3 preguntas, sin nota).</div>""")

    P["paginas/00-datos-y-perfil-del-negocio.html"] = ("Datos y perfil del negocio", "Descripción de la actividad Retroalimentación del INICIO.", ficha_moodle(
        "Inicio · 2 min", "Datos y perfil del negocio", "Retroalimentación",
        ["Autorización de tratamiento de datos (Ley 1581 de 2012) [VERIFICAR texto con la Cámara]",
         "Tipo de negocio y sector", "Barrio de Soacha", "¿Qué te gustaría resolver con este curso?"]))
    P["paginas/00-diagnostico-rapido.html"] = ("Diagnóstico rápido", "Cuestionario sin nota del INICIO.", ficha_moodle(
        "Inicio · 3 min", "Diagnóstico rápido", "Cuestionario (sin nota)", ini["diagnostico"]))

    for s, u in zip(u_secs, c["unidades"]):
        i = s["n"]
        pasos_u = [x for x in s["items"] if x["paso"] not in ("resumen", "pase")]
        num = {x["paso"]: k for k, x in enumerate(pasos_u, 1)}
        mins = {x["paso"]: x["min"] for x in pasos_u}
        filas = "".join(
            f'<li class="as-paso"><span class="as-paso__n">{k}</span><span class="as-paso__t"><b>{NOMBRE_PASO[x["paso"]]}</b>'
            f'<small>{t(x["formato"])} · {"opcional" if x.get("opcional") else str(x["min"]) + " min"}</small></span><span class="as-chip as-chip--gris">{t(corta(x["actividad"]))}</span></li>'
            for k, x in enumerate(pasos_u, 1))
        fr = formato_resumen(c, u)
        P[f"paginas/u{i}-cabecera.html"] = (f"Unidad {i}: cabecera", f"Resumen de la sección Unidad {i}.", f"""
  <div class="as-banda as-pila">
    <span class="as-eti">Unidad {i} de {s['de']} · ≈ {s['min']} min</span>
    <h2>{t(u['tema'])}</h2>
    <p>Al terminar sabrás {t(u['objetivo'])}.</p>
  </div>
  <a class="as-btn as-btn--sec" href="#" style="align-self:flex-start">{RESUMEN[fr][2]}</a>
  <ol class="as-pasos">{filas}</ol>""")
        if fr == "video":
            cuerpo_res = f"""
  <div class="as-tarjeta as-pila">
    <span class="as-eti">Unidad {i} · Resumen · opcional</span>
    <h2>{t(u['tema'])} en un minuto</h2>
    <p class="as-sec">Míralo antes de empezar como adelanto, o al final para repasar.</p>
    {video_vertical(c, f'u{i}-resumen', hueco('video', 'Video', f'Resumen en video de 60 s (plantillas/video_resumen.py con video/u{i}-resumen.json, o NotebookLM). Con subtítulos.'))}
  </div>"""
        else:
            cuerpo_res = f"""
  <div class="as-tarjeta as-pila">
    <span class="as-eti">Unidad {i} · Resumen · opcional</span>
    <h2>{t(u['tema'])} en 5 minutos</h2>
    <p class="as-sec">Escúchalo antes de empezar como adelanto, o al final para repasar. No necesitas mirar la pantalla.</p>
    {hueco('audio', 'Audio', f'Resumen en audio de 5 min de NotebookLM (solicitud 2B, Unidad {i}). MP3 mono 64 kbps, ≈ 2,4 MB.')}
    <details><summary><b>Leer la transcripción</b></summary><p class="as-sec" style="margin-top:8px"><em class="as-ph">[Transcripción del audio, se genera después de descargarlo]</em></p></details>
  </div>"""
        P[f"paginas/u{i}-resumen.html"] = (f"Unidad {i}: Resumen", f"Arriba de la sección Unidad {i}: {RESUMEN[fr][1]}. No bloquea el avance.", cuerpo_res + f"""
  <p class="as-sec">Resumen generado con inteligencia artificial y revisado por {t(c.get('revisor', 'un contador público'))}.</p>""")
        refs = "".join(
            f'<li><a href="{html.escape(r["url"])}" target="_blank" rel="noopener">{t(r["para"])}</a><br><small class="as-sec">{t(r["apa"])}</small></li>'
            for r in u.get("profundiza", []))
        P[f"paginas/u{i}-profundiza.html"] = (f"Unidad {i}: Profundiza", f"Paso {num['profundiza']} PROFUNDIZA, Unidad {i}: Página con enlaces. Opcional.", f"""
  <div class="as-tarjeta as-pila">
    <span class="as-eti">Paso {num['profundiza']} · Profundiza · opcional</span>
    <h2>Si quieres saber más</h2>
    <p class="as-sec">Lecturas cortas y fuentes oficiales sobre esta unidad. No son obligatorias.</p>
    <ul class="as-check">{refs}</ul>
  </div>""")
        e = u["entrada"]
        P[f"paginas/u{i}-entrada.html"] = (f"Unidad {i}: Entrada", f"Paso 1 ENTRADA de la Unidad {i}: actividad Página.", f"""
  <div class="as-tarjeta as-pila">
    <span class="as-eti">Paso 1 · Entrada · {mins['entrada']} min</span>
    <h2>{t(e['titulo'])}</h2>
    {imagen_entrada(c, i, e['imagen'])}{"" if f"u{i}-entrada.mp4" in c.get("_imagenes", ()) else narracion(c, f"u{i}-entrada-narracion", "Escucha el caso")}
    <p>{t(e['texto'])}</p>
  </div>
  <div class="as-aviso as-aviso--marca as-pila">
    <span class="as-eti">La pregunta de esta unidad</span>
    <h3>{t(e['pregunta'])}</h3>
  </div>
  <div class="as-tarjeta as-pila">
    <h3>¿Y en tu negocio?</h3>
    <p class="as-sec">{t(e['reflexion'])}</p>
  </div>""")
        a = u["aplica"]
        foro = c["nivel"] == "g"
        P[f"paginas/u{i}-aplica.html"] = (f"Unidad {i}: Aplica", (f"Descripción del Foro de preguntas y respuestas del paso APLICA, Unidad {i}. Finalización: publicar 1 y comentar 1." if foro else f"Descripción de la Tarea del paso APLICA, Unidad {i}."), f"""
  <div class="as-tarjeta as-pila">
    <span class="as-eti">Paso {num['aplica']} · Aplica · {mins['aplica']} min</span>
    <h2>{t(a['titulo'])}</h2>
    <p>{t(a['texto'])}</p>
    <div class="as-aviso">{t(a['entrega'])}</div>
  </div>""" + ("""
  <div class="as-tarjeta as-pila">
    <h3>Para comentar a un compañero</h3>
    <ul class="as-check"><li>¿Qué te sirvió de lo que hizo?</li><li>¿Qué le sugieres para la próxima semana?</li></ul>
    <p class="as-sec">Comenta con respeto: todos estamos aprendiendo. Nadie del equipo califica este paso.</p>
  </div>""" if foro else ""))
        L = u["llevatelo"]
        k_ll = num["llevatelo"]
        res = "".join(f"<li>{t(x)}</li>" for x in L["resumen"])
        desc = guia(c, i) + "".join(descarga(c, x) for x in L["descargas"])
        P[f"paginas/u{i}-llevatelo.html"] = (f"Unidad {i}: Llévatelo", f"Paso {k_ll} LLÉVATELO, Unidad {i}: Página + Archivo. Sube mapas/u{i}-mapa.png y guias-pdf/u{i}-guia.pdf a la Página y cambia el src y el href.", f"""
  <div class="as-tarjeta as-pila">
    <span class="as-eti">Paso {k_ll} · Llévatelo · {mins['llevatelo']} min</span>
    <h2>{t(L['titulo'])}</h2>
    {ficha(c, i)}
  </div>
  <div class="as-tarjeta as-pila">
    <h3>En tres frases</h3>
    <ul class="as-check">{res}</ul>
    <div class="as-aviso"><b>{t(L.get('etiqueta_formula', 'La fórmula'))}:</b> {t(L['formula'])}</div>
  </div>
  <div class="as-tarjeta as-pila">
    <h3>El mapa de la unidad</h3>
    {mapa(c, f"u{i}-mapa", f"Mapa de la Unidad {i}: {u['tema']}")}
  </div>
  <div class="as-tarjeta as-pila">
    <h3>Descarga</h3>
    {desc}
  </div>""")

    if c.get("pase") and c["nivel"] == "g":
        P.update(pagina_pase(c, len(u_secs)))

    ci = c["cierre"]
    P["paginas/99-cierre.html"] = ("Cierre del curso", "Resumen de la sección CIERRE.", f"""
  <div class="as-banda as-pila">
    <span class="as-eti">Cierre</span>
    <h2>{t(ci['titulo'])}</h2>
    <p>{t(ci['texto'])}</p>
  </div>
  <ol class="as-pasos">
    <li class="as-paso"><span class="as-paso__n">1</span><span class="as-paso__t"><b>Reto final</b><small>{t(ci['reto'])}</small></span><span class="as-chip as-chip--gris">Taller</span></li>
    <li class="as-paso"><span class="as-paso__n">★</span><span class="as-paso__t"><b>{t(c['certificado'])}</b><small>Se activa al completar las {len(u_secs)} unidades</small></span><span class="as-chip as-chip--ok">PDF</span></li>
  </ol>
  <div class="as-tarjeta as-pila">
    <span class="as-eti">Tu siguiente paso</span>
    <h3>{t(ci['siguiente'])}</h3>
    {hueco('imagen', 'Imagen', 'Portada del siguiente curso (16:9).')}
    <p class="as-sec">{t(ci['siguiente_texto'])}</p>
    <a class="as-btn" href="#">Ver el curso <em class="as-ph">[descuento por definir]</em> ›</a>
  </div>""")
    P["paginas/99-reto-final-entre-pares.html"] = ("Reto final entre pares", "Descripción del Taller del CIERRE. Fases por fecha; una cohorte por mes.", ficha_moodle(
        "Cierre · 15 min", "Reto final: " + ci["reto"].lower(), "Taller (revisión entre pares)",
        ["Entregas: " + c["evidencia"],
         "Moodle te asigna dos compañeros de tu cohorte del mes para revisar con esta rúbrica:",
         *[f"{k}. {x}" for k, x in enumerate(ci.get("rubrica", [
             "¿Calculó su sueldo con el promedio de 3 meses y el colchón?",
             "¿Definió una cuenta o billetera solo para el negocio?",
             "¿Su registro de la semana tiene fecha, qué fue, entró, salió y saldo?"]), 1)],
         "Antes de calificar ves un ejemplo ya evaluado.",
         "Un moderador de la Cámara revisa una vez por semana que los comentarios sean respetuosos."]))
    P["paginas/99-constancia-de-participacion.html"] = ("Constancia", "Configuración del certificado.", ficha_moodle(
        "Cierre · 1 min", c["certificado"], "Certificado personalizado",
        [f"Se emite al completar las {len(u_secs)} unidades (finalización de actividad).",
         "Lleva nombre, curso, fecha, horas y código de verificación.",
         "Diseño en Canva con logo de la Cámara [VERIFICAR logo definitivo]"]))
    return P


# ---------------------------------------------------------------- estructura.md
def arbol(c, secs):
    total = sum(s["min"] for s in secs)
    r = RECETAS[c["perfil"]]
    out = [f"# {c['titulo']}", "",
           f"{NIVELES[c['nivel']]} · Perfil {c['perfil']} ({r['nombre']}) · ≈ {fmt_min(total)} de estudiante · "
           f"{sum(len(s['items']) for s in secs)} piezas", "", f"**Promesa:** {c['promesa']}", "",
           f"**Caso hilo:** {c['caso']}", "", "## Objetivos", ""]
    out += [f"{k}. {x}" for k, x in enumerate(c["objetivos"], 1)]
    out += ["", f"**Evidencia:** {c['evidencia']}", "", "## Estructura", "", "```"]
    for si, s in enumerate(secs):
        last = si == len(secs) - 1
        out.append(("└── " if last else "├── ") + s["titulo"] + (f" · {s['tema']}" if s.get("n") else "") + f"  ({s['min']} min)")
        ch = "    " if last else "│   "
        for ii, x in enumerate(s["items"]):
            fuente = x.get("pieza") and f"{x['pieza']} ({x['molde']})" or x.get("pagina", "")
            out.append(ch + ("└── " if ii == len(s["items"]) - 1 else "├── ") +
                       (x["codigo"] + " | " if x["codigo"] else "") + f"{x['nombre']} [{x['actividad']} · {'opcional' if x.get('opcional') else str(x['min']) + ' min'}] → {fuente}")
        if not last:
            out.append("│")
    out += ["```", ""]
    return "\n".join(out)


# ---------------------------------------------------------------- vista previa
def vista_previa(c, secs, carpeta, pags):
    destino = carpeta / "vista-previa"
    if destino.exists():
        shutil.rmtree(destino)
    (destino / "comun").mkdir(parents=True)
    for f in ("aula.css", "aula.js"):
        shutil.copy(RAIZ / "comun" / f, destino / "comun" / f)
    for ruta, (tit, donde, cuerpo) in pags.items():
        (destino / ruta).parent.mkdir(parents=True, exist_ok=True)
        (destino / ruta).write_text(pagina(tit, donde, cuerpo, "../comun/aula.css"), encoding="utf-8")
    if c.get("_mapas"):
        (destino / "mapas").mkdir()
        for n in c["_mapas"]:
            shutil.copy(carpeta / "mapas" / f"{n}.png", destino / "mapas" / f"{n}.png")
    for carpeta_extra, clave in (("medios-moodle", "_narraciones"), ("medios-moodle", "_imagenes"), ("medios-moodle", "_videos"), ("descargas", "_descargas")):
        if c.get(clave):
            (destino / carpeta_extra).mkdir(exist_ok=True)
            for n in c[clave]:
                n = n if "." in n else n + ".mp3"
                shutil.copy(carpeta / carpeta_extra / n, destino / carpeta_extra / n)
    if c.get("_fichas"):
        (destino / "fichas").mkdir()
        for n in c["_fichas"]:
            shutil.copy(carpeta / "fichas" / f"{n}.jpg", destino / "fichas" / f"{n}.jpg")
    if c.get("_guias"):
        (destino / "guias-pdf").mkdir()
        for n in c["_guias"]:
            shutil.copy(carpeta / "guias-pdf" / f"{n}.pdf", destino / "guias-pdf" / f"{n}.pdf")
    pendientes = []
    for s in secs:
        for x in s["items"]:
            if x.get("pieza"):
                d = destino / x["pieza"]
                d.mkdir(parents=True, exist_ok=True)
                shutil.copy(RAIZ / "componentes" / x["molde"] / "index.html", d / "index.html")
                js = (carpeta / x["pieza"] / "contenido.js").read_text(encoding="utf-8")
                (d / "contenido.js").write_text(js, encoding="utf-8")
                if (carpeta / x["pieza"] / "medios").is_dir():
                    shutil.copytree(carpeta / x["pieza"] / "medios", d / "medios")
                pendientes += [(x["codigo"] or x["nombre"], m) for m in re.findall(r"\[(VERIFICAR[^\]]*|VALIDAR[^\]]*)\]", js)]
                pendientes += [(x["codigo"] or x["nombre"], "Medio por producir: " + m) for m in re.findall(r'src: "", nota: "([^"]+)"', js)]
    for ruta, (tit, d, cuerpo) in pags.items():
        pendientes += [(tit, m) for m in re.findall(r"\[(VERIFICAR[^\]]*|por definir[^\]]*)\]", cuerpo)]
        pendientes += [(tit, "Medio por producir: " + html.unescape(m)) for m in re.findall(r'class="as-hueco[^"]*"><b>[^<]+</b><span>([^<]+)', cuerpo)]
    datos = {"curso": {k: c[k] for k in ("titulo", "promesa", "duracion", "caso", "objetivos", "evidencia", "personas")},
             "nivel": NIVELES[c["nivel"]], "perfil": f"{c['perfil']} · {RECETAS[c['perfil']]['nombre']}",
             "secciones": secs, "pendientes": pendientes, "total": sum(s["min"] for s in secs)}
    plantilla = (RAIZ / "vista_curso.html").read_text(encoding="utf-8")
    (destino / "index.html").write_text(
        plantilla.replace("__TITULO_CORTO__", html.escape(c.get("titulo_corto", c["titulo"]))).replace("__DATOS__", json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")),
        encoding="utf-8")
    return destino, pendientes


# ---------------------------------------------------------------- principal
def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    carpeta = Path(args[0]).resolve()
    c = json.loads((carpeta / "curso.json").read_text(encoding="utf-8"))
    if (carpeta / "mapas").is_dir():
        c["_mapas"] = sorted(p.stem for p in (carpeta / "mapas").glob("*.png"))
    if (carpeta / "guias-pdf").is_dir():
        c["_guias"] = {p.stem: max(1, round(p.stat().st_size / 1024)) for p in sorted((carpeta / "guias-pdf").glob("*.pdf"))}
    if (carpeta / "fichas").is_dir():
        c["_fichas"] = {p.stem: max(1, round(p.stat().st_size / 1024)) for p in sorted((carpeta / "fichas").glob("u*-ficha.jpg"))}
    if (carpeta / "medios-moodle").is_dir():
        c["_narraciones"] = sorted(p.stem for p in (carpeta / "medios-moodle").glob("*-narracion.mp3"))
        c["_videos"] = sorted(p.name for p in (carpeta / "medios-moodle").iterdir() if re.match(r"(bienvenida|u\d+-resumen)\.(mp4|vtt)$", p.name))
        c["_imagenes"] = sorted(p.name for p in (carpeta / "medios-moodle").glob("u*-entrada.*") if p.suffix in (".jpg", ".mp4", ".vtt"))
    if (carpeta / "descargas").is_dir():
        c["_descargas"] = {p.name: max(1, round(p.stat().st_size / 1024)) for p in sorted((carpeta / "descargas").iterdir())
                           if p.suffix in (".pdf", ".xlsx")}
    secs = estructura(c)
    for s in secs:  # el nombre de cada pieza interactiva es el título de su contenido.js
        for x in s["items"]:
            if x.get("pieza") and (carpeta / x["pieza"] / "contenido.js").exists():
                x["nombre"] = empaquetar.titulo_de((carpeta / x["pieza"] / "contenido.js").read_text(encoding="utf-8"), x["nombre"])
    pags = paginas(c, secs)
    for ruta, (tit, donde, cuerpo) in pags.items():
        (carpeta / ruta).parent.mkdir(parents=True, exist_ok=True)
        (carpeta / ruta).write_text(pagina(tit, donde, cuerpo, "../../../plantillas/comun/aula.css"), encoding="utf-8")
    (carpeta / "estructura.md").write_text(arbol(c, secs), encoding="utf-8")
    destino, pend = vista_previa(c, secs, carpeta, pags)
    print(f"✓ {len(pags)} páginas, estructura.md y {destino.name}/ · {len(pend)} pendientes")
    if "--scorm" in args:
        for s in secs:
            for x in s["items"]:
                if x.get("pieza"):
                    z = empaquetar.empaquetar_desde(x["molde"], carpeta / x["pieza"], f"{c['id']}-{Path(x['pieza']).name}", carpeta / "scorm")
                    print(f"✓ {z.relative_to(carpeta)}  ({z.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
