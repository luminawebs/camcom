"""Arma las guías de estudio de cada unidad (HTML listo para PDF A5).
Uso: python3 armar_guias.py && node renderizar_pdf.mjs
El contenido sale de los guiones de notebooklm/fuentes/. Si cambia un guion, cambia aquí también."""
import pathlib, re

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "Vende más por WhatsApp Business"
GUIAS = {
 "u1-guia": dict(
  n=1, titulo="Tu vitrina: perfil y catálogo",
  pregunta="¿Cómo muestras qué vendes y cuánto vale sin que te tengan que preguntar?",
  idea="WhatsApp Business es gratis. Con un perfil de empresa completo y un catálogo con foto, nombre, precio y descripción, el cliente compra sin preguntarte.",
  caso="A Sandra le escriben todos los días para preguntar qué tortas tiene y cuánto valen. Manda las fotos una por una desde su WhatsApp personal y una clienta se le fue por responder tarde.",
  bloques=[
   ("Tu perfil de empresa", "lista", [
     ("Nombre y foto", "El nombre del negocio y tu logo o tu mejor producto."),
     ("Categoría y descripción", "Qué vendes y para quién, en una frase."),
     ("Dónde y cuándo", "Dirección o zona de domicilio, y tu horario."),
     ("Contacto", "Un correo o tu página, si tienes."),
   ]),
  ],
  etiqueta="La regla", formula=("Perfil completo + catálogo", "el cliente compra sin preguntar"),
  ejemplo_titulo="Un artículo bien hecho",
  ejemplo=[("Foto", "luz de día, fondo limpio", ""), ("Nombre", "Torta de chocolate para 12", ""), ("Descripción", "Pídela con 2 días", ""),
           ("Domicilio", "en Soacha", ""), ("Precio", "$65.000", "total")],
  nota_ejemplo="Empieza por tus 5 productos que más vendes. Desde un chat mandas el catálogo o un producto con el clip de adjuntar.",
  errores=["Vender desde el WhatsApp personal, mezclado con la familia.",
           "Subir fotos oscuras o con cosas alrededor.",
           "Dejar el producto sin precio: el cliente igual te va a preguntar."],
  preguntas=["¿Qué es lo que más te preguntan tus clientes?",
             "¿Cuáles son tus 5 productos que más se venden?",
             "¿Qué dice la descripción de tu perfil, en una frase?"],
  dato=("$0", "cuesta WhatsApp Business: se descarga gratis en la tienda de apps del celular."),
  fuentes="WhatsApp. Servicio de ayuda: catálogo. · WhatsApp Business app (business.whatsapp.com). · Tiendanube. Cómo hacer un catálogo en WhatsApp.",
 ),
 "u2-guia": dict(
  n=2, titulo="Ningún pedido se pierde",
  pregunta="¿Cómo sabes en un minuto qué pedido falta cobrar o despachar?",
  idea="Ponle a cada chat de cliente una etiqueta con la etapa de su pedido. Al cerrar el día, filtra y sabrás a quién cobrar y qué despachar.",
  caso="Camilo vende accesorios para celular a domicilio en Ducales y tiene más de 200 chats. Un viernes se le olvidó despachar tres pedidos que ya estaban pagos.",
  bloques=[
   ("Las etapas del pedido", "pasos", [
     ("Nuevo pedido", "El cliente ya dijo qué quiere."),
     ("Pago pendiente", "Le mandaste el valor y falta que pague."),
     ("Pagado", "Ya pagó y falta entregar."),
     ("Entregado", "Listo. Si vuelve a comprar, empieza otra vez."),
   ]),
  ],
  etiqueta="La ruta", formula=("Pedido", "nuevo → pago pendiente → pagado → entregado"),
  ejemplo_titulo="Tu rutina de 10 minutos",
  ejemplo=[("1. Filtra «Pago pendiente»", "y cobra", ""), ("2. Filtra «Pagado»", "y arma despachos", ""), ("3. Al entregar", "cambia la etiqueta", ""),
           ("Ningún pedido perdido", "✓", "total")],
  nota_ejemplo="Para poner una etiqueta: mantén presionado el chat y toca el ícono de etiqueta. También sirve en un mensaje, como el del comprobante.",
  errores=["Crear muchas etiquetas que después nadie usa.",
           "Olvidar cambiar la etiqueta cuando el cliente avanza.",
           "Revisar los pedidos solo cuando un cliente reclama."],
  preguntas=["¿Qué etiquetas vas a usar en tu negocio?",
             "¿Cuántos clientes tienes hoy en «Pago pendiente»?",
             "¿A qué hora vas a hacer tu rutina de cada día?"],
  dato=("4", "etiquetas bastan para la mayoría de negocios pequeños: una por cada etapa del pedido."),
  fuentes="WhatsApp. Servicio de ayuda: etiquetas. · Leadsales. Cómo usar etiquetas en WhatsApp Business. · Platzi. Maneja el caos con etiquetas.",
 ),
 "u3-guia": dict(
  n=3, titulo="Responde rápido sin vivir pegado al celular",
  pregunta="¿Cómo contestas en segundos lo que te preguntan todos los días?",
  idea="La bienvenida y la ausencia salen solas; las respuestas rápidas las mandas tú con un atajo. Con las tres respondes en segundos y no pierdes clientes.",
  caso="Esperanza vende frutas y verduras a domicilio en El Altico. Le llegan 40 mensajes al día con las mismas preguntas y en la madrugada, en la plaza, no alcanza a contestar.",
  bloques=[
   ("Tus tres herramientas", "lista", [
     ("Mensaje de bienvenida", "Sale solo con el cliente nuevo: qué vendes y cómo pedir."),
     ("Mensaje de ausencia", "Sale solo cuando no puedes atender: a qué hora vuelves."),
     ("Respuestas rápidas", "Mensajes guardados: escribes / y eliges."),
     ("Horario en el perfil", "Para que la ausencia salga fuera de horario."),
   ]),
  ],
  etiqueta="La regla", formula=("Bienvenida + ausencia + 3 respuestas rápidas", "respondes en segundos"),
  ejemplo_titulo="Respuestas rápidas de Esperanza",
  ejemplo=[("/domicilio", "zonas, horario y valor", ""), ("/horario", "lunes a sábado", ""), ("/pagos", "efectivo, Nequi, Daviplata", ""),
           ("Respuesta en segundos", "✓", "total")],
  nota_ejemplo="Escribe como en el mostrador: saluda, da los datos completos y termina con una pregunta, como «¿Te lo llevo hoy?».",
  errores=["Escribir en mayúsculas o con respuestas de una palabra.",
           "Poner un mensaje de ausencia sin decir cuándo vuelves.",
           "Mandar promociones a quien no te ha dado permiso."],
  extra=("¿Y las promociones?", "El número y el nombre de tu cliente son datos personales. Antes de mandarle ofertas, pregúntale si quiere recibirlas y respeta si te dice que no (Ley 1581 de 2012)."),
  preguntas=["¿Cuáles son las 3 preguntas que más te hacen?",
             "¿Qué dice tu mensaje de bienvenida?",
             "¿En qué horario no puedes contestar?"],
  dato=("/", "es la tecla de tus respuestas rápidas: la escribes en el chat y eliges el mensaje guardado."),
  fuentes="WhatsApp. Servicio de ayuda: respuestas rápidas y mensaje de ausencia. · Leadsales. Mensajes automáticos en WhatsApp Business. · Ley 1581 de 2012.",
 ),
}
CSS = """
@page{size:148mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,'DejaVu Sans',sans-serif;color:#1a1a1a;font-size:9.6pt;line-height:1.42;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pag{width:148mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.pag:last-child{page-break-after:auto}
.top{display:flex;justify-content:space-between;align-items:center;padding:7mm 10mm 4mm}
.top svg{height:7mm;width:auto}
.top span{font-size:7.4pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b6b72}
.hero{background:#c8102e;color:#fff;padding:4.5mm 10mm 5mm;position:relative}
.hero .u{display:inline-block;background:#fff;color:#c8102e;font-weight:800;font-size:7.6pt;letter-spacing:.08em;text-transform:uppercase;padding:1mm 2.6mm;border-radius:1.2mm}
.hero h1{font-size:16.5pt;line-height:1.12;font-weight:800;margin-top:2.4mm}
.hero p{font-size:9.4pt;margin-top:2mm;opacity:.92}
.cuerpo{padding:4mm 10mm 0}
.idea{border-left:1.4mm solid #c8102e;background:#f6f6f7;padding:2.6mm 4mm;border-radius:0 2mm 2mm 0;font-size:9.8pt;font-weight:600;line-height:1.38}
.idea small{display:block;font-size:7pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#9e0c24;margin-bottom:1mm}
.caso{margin-top:2.4mm;font-size:8.8pt;color:#45454c}
.caso b{color:#1a1a1a}
h2{font-size:10.6pt;font-weight:800;color:#141414;margin:3.6mm 0 1.8mm;display:flex;align-items:center;gap:2mm}
h2:before{content:"";width:2.4mm;height:2.4mm;background:#c8102e;border-radius:.6mm;flex:none}
.lista{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm}
.lista div{background:#f6f6f7;border-radius:2mm;padding:2.2mm 3mm;font-size:8.2pt;line-height:1.32;color:#45454c}
.lista b{display:block;font-size:9pt;color:#141414;margin-bottom:.6mm}
.lista i{font-style:normal;color:#c8102e;font-weight:800;margin-right:1mm}
.pasos{display:grid;gap:1.6mm}
.pasos div{display:flex;gap:3mm;align-items:flex-start;font-size:8.4pt;line-height:1.32;color:#45454c}
.pasos .num{flex:none;width:6.4mm;height:6.4mm;border-radius:50%;background:#141414;color:#fff;font-weight:800;font-size:9pt;display:flex;align-items:center;justify-content:center}
.pasos b{display:block;color:#141414;font-size:9.2pt}
.barra .t{font-size:8.6pt;color:#45454c;margin-bottom:1.6mm}
.barra .b{display:flex;height:9mm;border-radius:2mm;overflow:hidden;font-size:8pt;font-weight:700}
.barra .b div{display:flex;align-items:center;justify-content:center;color:#fff}
.barra .b div:first-child{background:#8d8d94}.barra .b div:last-child{background:#c8102e}
.cols{display:grid;grid-template-columns:repeat(5,1fr);border:.3mm solid #d4d4d8;border-radius:2mm;overflow:hidden;font-size:8pt;text-align:center}
.cols div{padding:2mm 0;font-weight:700;background:#141414;color:#fff;border-right:.3mm solid #444}
.cols span{padding:3.5mm 0;border-right:.3mm solid #e2e2e5}
.formula{background:#141414;color:#fff;border-radius:2.4mm;padding:3.6mm 4.4mm;font-size:10.2pt;line-height:1.35}
.formula small{display:block;font-size:7pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#ff8a9c;margin-bottom:1mm}
.formula b{color:#fff;font-weight:800}
.ej{margin-top:3mm;border:.3mm solid #e2e2e5;border-radius:2.4mm;overflow:hidden}
.ej .cab{background:#f6f6f7;padding:1.8mm 4mm;font-size:7.4pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6b6b72}
.ej .f{display:flex;justify-content:space-between;padding:1.3mm 4mm;font-size:9pt;border-top:.3mm solid #f0f0f2}
.ej .sub{font-weight:700;background:#fbfbfc}
.ej .total{background:#c8102e;color:#fff;font-weight:800;font-size:10pt}
.nota{font-size:8pt;color:#6b6b72;margin-top:2mm}
.err div{display:flex;gap:2.4mm;font-size:8.6pt;margin-bottom:1.1mm;line-height:1.3;color:#2a2a2e}
.err div:before{content:"✕";flex:none;width:4.8mm;height:4.8mm;border-radius:50%;background:#fde7ea;color:#c8102e;font-weight:800;font-size:7pt;display:flex;align-items:center;justify-content:center;margin-top:.3mm}
.extra{background:#f6f6f7;border-radius:2.4mm;padding:2.4mm 4mm;font-size:8.4pt;line-height:1.35;color:#45454c;margin-top:3mm}
.extra b{display:block;color:#141414;font-size:9.4pt;margin-bottom:.6mm}
.preg div{margin-bottom:2.2mm;font-size:9pt;font-weight:600}
.preg div span{color:#c8102e;font-weight:800;margin-right:1.4mm}
.preg i{display:block;border-bottom:.3mm dashed #b8b8be;height:5mm}
.dato{display:flex;gap:3mm;align-items:center;border:.3mm solid #e2e2e5;border-radius:2.4mm;padding:2.2mm 4mm;font-size:8pt;line-height:1.3;color:#45454c;margin-top:3mm}
.dato b{font-size:15pt;color:#c8102e;font-weight:800;flex:none}
.pie{position:absolute;left:10mm;right:10mm;bottom:6mm;display:flex;justify-content:space-between;font-size:6.8pt;color:#8d8d94;border-top:.3mm solid #e2e2e5;padding-top:2mm}
.fuentes{position:absolute;left:10mm;right:10mm;bottom:12.5mm;font-size:6.6pt;color:#8d8d94;line-height:1.35}
"""

def bloque(t, tipo, d):
    if tipo == "lista":
        h = "".join(f"<div><b><i>{i}.</i>{a}</b>{b}</div>" for i, (a, b) in enumerate(d, 1))
        return f"<h2>{t}</h2><div class='lista'>{h}</div>"
    if tipo == "pasos":
        h = "".join(f"<div><span class='num'>{i}</span><p><b>{a}</b>{b}</p></div>" for i, (a, b) in enumerate(d, 1))
        return f"<h2>{t}</h2><div class='pasos'>{h}</div>"
    if tipo == "barra":
        tit, partes = d
        h = "".join(f"<div style='width:{p}%'>{a} · {v}</div>" for a, v, p in partes)
        return f"<h2>{t}</h2><div class='barra'><p class='t'>{tit}</p><div class='b'>{h}</div></div>"
    if tipo == "columnas":
        return f"<h2>{t}</h2><div class='cols'>{''.join(f'<div>{c}</div>' for c in d)}</div>"

for ident, g in GUIAS.items():
    n = g["n"]
    top = f"<div class='top'>{LOGO}<span>Guía de estudio · Unidad {n}</span></div>"
    pie = lambda p: f"<div class='pie'><span>{CURSO} · Aula Virtual Empresarial Soacha</span><span>{p} / 2</span></div>"
    ej = "".join(f"<div class='f {c}'><span>{a}</span><span>{v}</span></div>" for a, v, c in g["ejemplo"])
    nota = f"<p class='nota'>{g['nota_ejemplo']}</p>" if g.get("nota_ejemplo") else ""
    extra = f"<div class='extra'><b>{g['extra'][0]}</b>{g['extra'][1]}</div>" if g.get("extra") else ""
    pct, resto = (g["dato"][0].replace(" ", "&nbsp;"), g["dato"][1]) if isinstance(g["dato"], tuple) else (re.search(r"\d+(?:,\d+)? %", g["dato"]).group().replace(" ", "&nbsp;"), g["dato"])
    p1 = f"""<section class='pag'>{top}
<div class='hero'><span class='u'>Unidad {n}</span><h1>{g['titulo']}</h1><p>{g['pregunta']}</p></div>
<div class='cuerpo'>
<div class='idea'><small>La idea en una frase</small>{g['idea']}</div>
<p class='caso'><b>El caso:</b> {g['caso']}</p>
{''.join(bloque(*b) for b in g['bloques'])}
<h2>Errores comunes</h2><div class='err'>{''.join(f'<div>{e}</div>' for e in g['errores'])}</div>
{extra if g.get('extra_p1') else ''}
</div>{pie(1)}</section>"""
    p2 = f"""<section class='pag'>{top}
<div class='cuerpo' style='padding-top:2mm'>
<h2>{g.get('etiqueta', 'La fórmula')}</h2>
<div class='formula'><small>Apréndetela</small><b>{g['formula'][0]}</b> = {g['formula'][1]}</div>
<div class='ej'><div class='cab'>{g.get('ejemplo_titulo', 'Ejemplo')}</div>{ej}</div>{nota}
{'' if g.get('extra_p1') else extra}
<h2>Piensa en tu negocio</h2><div class='preg'>{''.join(f'<div><span>{i}.</span>{q}<i></i></div>' for i, q in enumerate(g['preguntas'], 1))}</div>
<div class='dato'><b>{pct}</b><span>{resto}</span></div>
</div>
<p class='fuentes'>Fuentes: {g['fuentes']}</p>{pie(2)}</section>"""
    html = f"<!doctype html><html lang='es'><head><meta charset='utf-8'><title>Guía de estudio · Unidad {n}</title><style>{CSS}</style></head><body>{p1}{p2}</body></html>"
    (AQUI / f"{ident}.html").write_text(html, encoding="utf-8")
    print("ok", ident)
