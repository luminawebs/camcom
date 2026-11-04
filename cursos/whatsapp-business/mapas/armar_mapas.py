"""Arma los mapas mentales del curso (HTML) a partir del contenido de abajo.
Uso: python3 armar_mapas.py  -> genera mapas/<id>.html; luego renderizar.mjs los pasa a PNG."""
import html, pathlib

AQUI = pathlib.Path(__file__).parent
CURSO = "Vende más por WhatsApp Business"

MAPAS = {
 "mapa-curso": ("Mapa del curso", CURSO, [
   ("Unidad 1 · Tu vitrina: perfil y catálogo", [
     "WhatsApp Business es gratis y separa tu negocio de lo personal",
     "Perfil completo: qué vendes, dónde y a qué hora",
     "Catálogo con <b>foto, nombre, precio y descripción</b>"]),
   ("Unidad 2 · Ningún pedido se pierde", [
     "Una etiqueta es un color con nombre en cada chat",
     "<b>Nuevo pedido → Pago pendiente → Pagado → Entregado</b>",
     "Cada día: cobra «Pago pendiente» y despacha «Pagado»"]),
   ("Unidad 3 · Responde rápido", [
     "Bienvenida: saluda solo al cliente nuevo",
     "Ausencia: dice cuándo vuelves",
     "Respuestas rápidas: escribes <b>/</b> y eliges"]),
 ]),
 "u1-mapa": ("Unidad 1", "¿Cómo muestras qué vendes y cuánto vale sin que te pregunten?", [
   ("WhatsApp Business", [
     "App gratis, aparte del WhatsApp normal",
     "Número nuevo o el de siempre, con tus chats"]),
   ("Perfil de empresa", [
     "Nombre y foto del negocio",
     "Categoría y descripción corta",
     "Dirección o zona de domicilio, horario y correo"]),
   ("Catálogo", [
     "Un artículo por producto: foto, nombre, precio y descripción",
     "Empieza por tus 5 productos que más vendes",
     "Lo mandas desde el chat con el clip"]),
   ("Fotos y textos que venden", [
     "Luz de día, fondo limpio, un solo producto",
     "Nombre con tamaño: «Torta de chocolate para 12»",
     "Siempre el precio y las condiciones"]),
 ]),
 "u2-mapa": ("Unidad 2", "¿Cómo sabes en un minuto qué pedido falta cobrar o despachar?", [
   ("Qué es una etiqueta", [
     "Un color con nombre que le pones a un chat",
     "La app trae algunas; las cambias o creas las tuyas"]),
   ("Las etapas del pedido", [
     "<b>1.</b> Nuevo pedido: ya dijo qué quiere",
     "<b>2.</b> Pago pendiente: falta que pague",
     "<b>3.</b> Pagado: falta entregar",
     "<b>4.</b> Entregado: listo"]),
   ("Cómo se pone", [
     "Mantén presionado el chat y toca la etiqueta",
     "También a un mensaje, como el comprobante"]),
   ("Tu rutina de 10 minutos", [
     "Filtra «Pago pendiente» y cobra",
     "Filtra «Pagado» y arma los despachos",
     "Al entregar, cambia a «Entregado»"]),
 ]),
 "u3-mapa": ("Unidad 3", "¿Cómo contestas en segundos lo que te preguntan todos los días?", [
   ("Mensaje de bienvenida", [
     "Sale solo con el cliente nuevo",
     "Qué vendes, tu horario y cómo pedir"]),
   ("Mensaje de ausencia", [
     "Sale solo cuando no puedes atender",
     "Dice a qué hora vuelves",
     "Fuera de horario: pon el horario en el perfil"]),
   ("Respuestas rápidas", [
     "Mensajes guardados con atajo: <b>/domicilio</b>",
     "Tú decides cuándo mandarlas",
     "Una por cada pregunta que te repiten"]),
   ("Como en el mostrador", [
     "Corto, amable y con los datos completos",
     "Termina con una pregunta: «¿Te lo llevo hoy?»",
     "Pide permiso antes de mandar promociones"]),
 ]),
}

CSS = """
*{box-sizing:border-box;margin:0}
body{width:1080px;font-family:Inter,'DejaVu Sans',sans-serif;background:#f6f6f7;color:#1a1a1a}
.cab{background:#c8102e;color:#fff;padding:56px 64px 48px}
.cab small{display:block;font-size:26px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;opacity:.85}
.cab h1{font-size:58px;line-height:1.12;font-weight:800;margin-top:14px}
.ramas{position:relative;padding:48px 64px 24px 112px}
.ramas:before{content:"";position:absolute;left:78px;top:0;bottom:64px;width:6px;background:#141414;border-radius:3px}
.rama{position:relative;background:#fff;border-radius:22px;padding:30px 36px;margin-bottom:30px;box-shadow:0 2px 0 #e2e2e5}
.rama:before{content:"";position:absolute;left:-34px;top:48px;width:34px;height:6px;background:#141414}
.rama .n{position:absolute;left:-56px;top:32px;width:38px;height:38px;border-radius:50%;background:#c8102e;border:6px solid #f6f6f7;box-sizing:content-box;margin-left:-8px}
.rama h2{font-size:38px;font-weight:800;color:#9e0c24;line-height:1.2}
.rama ul{list-style:none;padding:0;margin-top:14px}
.rama li{font-size:30px;line-height:1.35;padding:8px 0 8px 30px;position:relative;color:#2a2a2e}
.rama li:before{content:"";position:absolute;left:4px;top:24px;width:12px;height:12px;border-radius:50%;background:#8d8d94}
.rama b{color:#141414}
.pie{padding:8px 64px 48px;font-size:22px;color:#6b6b72;display:flex;justify-content:space-between}
"""

for ident, (etiqueta, titulo, ramas) in MAPAS.items():
    cuerpo = "".join(
        f'<div class="rama"><span class="n"></span><h2>{html.escape(t)}</h2><ul>'
        + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>"
        for t, items in ramas)
    pagina = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title><style>{CSS}</style></head>
<body><div class="cab"><small>{html.escape(etiqueta)} · {html.escape(CURSO) if ident!='mapa-curso' else 'Aula Virtual Empresarial Soacha'}</small><h1>{html.escape(titulo)}</h1></div>
<div class="ramas">{cuerpo}</div><div class="pie"><span>Aula Virtual Empresarial · Cámara de Comercio de Soacha</span></div></body></html>"""
    (AQUI / f"{ident}.html").write_text(pagina, encoding="utf-8")
    print("ok", ident)
