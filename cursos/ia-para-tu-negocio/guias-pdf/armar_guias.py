"""Arma las guías de estudio de cada unidad (HTML listo para PDF A5).
Uso: python3 armar_guias.py && node renderizar_pdf.mjs
El contenido sale de curso.json y de las lecciones Aprende. Si cambian, cambia aquí también."""
import pathlib, re

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "IA para tu negocio desde el celular"
GUIAS = {
 "u1-guia": dict(
  n=1, titulo="Pídele bien a la IA",
  pregunta="¿Qué le dices a la IA para que te responda algo que de verdad sirva para tu negocio?",
  idea="La IA escribe en segundos, pero solo sabe de tu negocio lo que tú le cuentas. Pídele con 4 partes y conversa hasta que la respuesta te sirva.",
  caso="Nelson tiene una ferretería en Quintanares. Le escribió a la IA «haz un aviso» y le salió un texto largo con una oferta que no tiene. Concluyó que no servía y siguió escribiendo a mano hasta las once de la noche.",
  bloques=[
   ("Las 4 partes de un buen pedido", "pasos", [
     ("Quién eres", "«Tengo una ferretería en Quintanares, Soacha»."),
     ("Qué necesitas", "«Escribe un aviso para el grupo de WhatsApp del barrio»."),
     ("Para quién", "«Para vecinos que arreglan la casa el fin de semana»."),
     ("Cómo lo quieres", "«Corto, 4 líneas, amable, con el horario del sábado»."),
   ]),
  ],
  etiqueta="La fórmula", formula=("Quién soy + qué necesito + para quién + cómo lo quiero", "una respuesta que sirve"),
  ejemplo_titulo="Ajustes que puedes pedir",
  ejemplo=[("«Más corto»", "en 4 líneas", ""), ("«Más cercano»", "como hablamos en Soacha", ""), ("«Dame 3 opciones»", "y eliges", ""),
           ("«Ahora para Facebook»", "mismo aviso, otro lugar", ""), ("Tiempo por ajuste", "segundos", "total")],
  nota_ejemplo="Puedes escribirle o hablarle con el micrófono. Asistentes con versión gratis: ChatGPT, Gemini, Copilot y Meta AI dentro de WhatsApp.",
  errores=["Pedir con dos palabras: «haz un aviso».",
           "Creer que la IA ya conoce tu negocio, tus precios o tu horario.",
           "Borrar todo y empezar de cero en vez de pedir un ajuste."],
  preguntas=["¿Qué escribes cada semana que te quita más tiempo?",
             "Escribe en una frase quién eres: tu negocio y dónde queda.",
             "¿Para quién es tu próximo aviso o mensaje?"],
  dato=("4", "partes tiene un buen pedido: quién eres, qué necesitas, para quién y cómo lo quieres."),
  fuentes="OpenAI. Prompt engineering best practices for ChatGPT. · Google. Prompting guide 101. · DNP (2025). CONPES 4144, Política Nacional de Inteligencia Artificial.",
 ),
 "u2-guia": dict(
  n=2, titulo="Mensajes y descripciones que venden",
  pregunta="¿Cómo usas la IA para escribir tus textos en minutos sin publicar algo que no es cierto?",
  idea="Dale a la IA tus datos reales y pídele tu forma de hablar. Después lee todo y corrige: lo que publicas de tu producto tiene que ser verdad.",
  caso="Leidy vende ropa para bebé en Terreros y se queda hasta tarde escribiendo descripciones. La primera vez copió sin leer lo que dio la IA y publicó que un enterizo era «orgánico y antialérgico». No lo era.",
  bloques=[
   ("Lo que le das a la IA", "lista", [
     ("Qué es", "«Enterizo de algodón para bebé»."),
     ("Los datos reales", "Tallas, material, precio, cuidados."),
     ("Para quién y condiciones", "Mamás primerizas · domicilio en Soacha."),
     ("Cómo lo quieres", "Tono cálido, 3 líneas, tuteando."),
   ]),
  ],
  etiqueta="La regla", formula=("Tus datos reales + un pedido claro + tu revisión", "un texto listo para vender"),
  ejemplo_titulo="Antes de publicar, revisa",
  ejemplo=[("Precio", "¿es el tuyo?", ""), ("Material y tallas", "¿son los reales?", ""), ("Promesas", "garantías, «orgánico», «gratis»", ""),
           ("Tono", "¿suena a ti?", ""), ("Listo para publicar", "✓", "total")],
  nota_ejemplo="Cuando un pedido te funcione, guárdalo en las notas del celular: la próxima vez solo cambias los datos del producto.",
  errores=["Copiar y publicar sin leer lo que escribió la IA.",
           "Dejar que la IA ponga el precio o las condiciones.",
           "Mandar a todos los clientes el mismo texto acartonado."],
  preguntas=["¿Qué producto vas a describir primero?",
             "¿Qué datos reales de ese producto le vas a dar a la IA?",
             "¿Qué mensaje a clientes repites cada semana?"],
  dato=("1 min", "puede tomarte una descripción con un pedido guardado: copias, cambias los datos y revisas."),
  fuentes="Google. Prompting guide 101. · Congreso de Colombia (2011). Ley 1480, Estatuto del Consumidor. · WhatsApp. Acerca de Meta AI en WhatsApp.",
 ),
 "u3-guia": dict(
  n=3, titulo="Lo que no le cuentas a la IA",
  pregunta="¿Qué datos nunca debes poner en la IA y cómo le pides lo mismo sin ellos?",
  idea="Lo que escribes en la IA puede quedar guardado. No pongas nada que no publicarías: cambia los datos de tus clientes por «Clienta 1» o [nombre] y la IA te ayuda igual.",
  caso="Yaneth tiene una peluquería en Rincón de Santa Fe. Iba a pegar en la IA la lista de sus clientas con cédula, celular y alergias para que le escribiera los mensajes de cumpleaños. Su hija la frenó a tiempo.",
  bloques=[
   ("El semáforo de datos", "lista", [
     ("Rojo · nunca", "Cédulas, claves, números de cuenta o tarjeta, fotos de documentos, datos de salud."),
     ("Amarillo · quítalos antes", "Nombres, celulares y direcciones de clientes."),
     ("Verde · tranquilo", "Lo público de tu negocio: productos, precios, horario, barrio."),
   ]),
  ],
  etiqueta="El semáforo", formula=("Rojo: nunca · Amarillo: quita nombres y números", "verde: datos públicos de tu negocio"),
  ejemplo_titulo="El pedido de Yaneth, sin datos",
  ejemplo=[("Antes", "María Pérez, CC…, cel…, alérgica", ""), ("Después", "«una clienta que viene cada mes»", ""), ("Nombre", "deja [nombre] y lo pones tú", ""),
           ("Resultado", "igual de bueno", "total")],
  nota_ejemplo="En los ajustes de tu asistente busca la opción de no usar tus chats para entrenar el modelo (en cada app se llama distinto) y borra los chats con datos de clientes.",
  errores=["Pegar la lista de clientes completa «para que la IA les escriba».",
           "Mandarle a la IA la foto de una cédula o de un comprobante con números de cuenta.",
           "Escribirles promociones a clientes que no dieron permiso."],
  preguntas=["¿Qué datos de clientes guardas y dónde?",
             "¿Qué pedido tuyo tenía datos personales? Reescríbelo.",
             "¿Dónde está la opción de privacidad en tu asistente?"],
  dato=("1581", "es la ley de datos personales de Colombia (2012): los datos de salud son sensibles y tienen protección especial."),
  fuentes="Congreso de Colombia (2012). Ley Estatutaria 1581. · SIC (2024). Circular Externa 002, datos personales en sistemas de IA. · OpenAI. Data controls FAQ.",
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
