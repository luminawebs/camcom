"""Arma las guías de estudio de cada unidad (HTML listo para PDF A5).
Uso: python3 armar_guias.py && node renderizar_pdf.mjs
El contenido sale de los guiones de notebooklm/fuentes/. Si cambia un guion, cambia aquí también."""
import pathlib, re

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "Formaliza tu negocio paso a paso"

GUIAS = {
 "u1-guia": dict(
  n=1, titulo="Formal no es pagar más: es poder crecer",
  pregunta="¿Qué necesita tu negocio para estar formal y qué ganas con eso?",
  idea="Estar formal es tener tres cosas: RUT, matrícula mercantil y el local en regla. El RUT es gratis y no es un impuesto.",
  caso="Un distribuidor le ofrece a Édgar surtir su tienda de Compartir a crédito, pero le pide RUT y matrícula. Édgar cree que registrarse es pagar más impuestos.",
  bloques=[
   ("Los 3 pasos", "pasos", [
     ("RUT, en la DIAN", "Dice quién eres para los impuestos y a qué te dedicas. Es gratis."),
     ("Matrícula mercantil, en la Cámara de Comercio", "Registra a la persona y a su negocio. Se renueva cada año."),
     ("Requisitos del local", "Uso de suelo, aviso de apertura a la Policía y, si pones música, derechos de autor."),
   ]),
  ],
  etiqueta="La ruta", formula=("Formal", "RUT + matrícula mercantil + local en regla"),
  ejemplo_titulo="Lo que ganas",
  ejemplo=[("Comprar a crédito", "proveedores", ""), ("Venderle a empresas", "piden RUT", ""), ("Crédito en un banco", "no gota a gota", ""),
           ("Programas de la Cámara", "ferias y cursos", "total")],
  errores=["Creer que el RUT es un impuesto: es un registro gratis.",
           "Pensar que formalizarse es una sola cosa: son tres pasos.",
           "Esperar a tener más ventas: formal es más fácil crecer."],
  preguntas=["¿Qué venta, crédito o cliente perdiste por no tener un papel?",
             "¿En qué paso de la ruta está tu negocio hoy?",
             "¿Qué te frena más para dar el siguiente paso?"],
  dato="Solo el 22,4 % de los micronegocios de Colombia tenía RUT en 2024 (DANE, 2025).",
  fuentes="DANE (2025). Encuesta de Micronegocios (EMICRON) 2024: boletín técnico. · Decreto 2210 de 2023 (Cámara de Comercio de Soacha).",
 ),
 "u2-guia": dict(
  n=2, titulo="El RUT, gratis y desde el celular",
  pregunta="¿Cómo sacas tu RUT sin pagar ni hacer filas?",
  idea="El RUT se saca gratis en la página de la DIAN, en unos 15 minutos. No vence: solo se actualiza cuando cambian tus datos.",
  caso="Un salón le ofrece a Yuli trabajo fijo si saca el RUT. Le dijeron que cuesta plata y que hay que hacer fila. No es así.",
  bloques=[
   ("Lo que necesitas", "lista", [
     ("Tu cédula", "Fotos claras de las dos caras."),
     ("Una selfie", "Con buena luz, sin gafas ni gorra."),
     ("Correo y celular", "Te llega un código para terminar."),
     ("Dirección y actividad", "Donde trabajas y el código CIIU de tu negocio."),
   ]),
  ],
  etiqueta="La regla", formula=("RUT", "gratis + en línea + no vence (solo se actualiza)"),
  ejemplo_titulo="Paso a paso en línea",
  ejemplo=[("1. DIAN → Inscripción en el RUT", "", ""), ("2. Persona natural y tu cédula", "", ""), ("3. Datos, dirección y CIIU", "", ""),
           ("4. Fotos y selfie", "", ""), ("5. Código del correo", "", ""), ("6. Descarga el PDF", "listo", "total")],
  nota_ejemplo="Tu NIT es tu número de cédula con un dígito de verificación al final.",
  errores=["Pagarle a alguien por sacarlo: la DIAN no cobra.",
           "Sacar un RUT nuevo en vez de actualizar el que tienes.",
           "Poner una actividad que no es la de tu negocio."],
  extra=("¿Y las responsabilidades?", "En el RUT aparece lo que la DIAN espera de ti. Muchos negocios pequeños quedan como no responsables de IVA. Si tienes dudas, muéstrale tu RUT a un contador."),
  preguntas=["¿Tienes RUT? Si no sabes, ¿cómo lo vas a averiguar?",
             "¿Cuál es el código de actividad (CIIU) de tu negocio?",
             "¿Qué datos de tu RUT tienes que actualizar?"],
  dato="El 77,6 % de los micronegocios de Colombia no tenía RUT en 2024 (DANE, 2025).",
  fuentes="DANE (2025). EMICRON 2024: boletín técnico. · DIAN. Inscripción en el RUT. · El Cronista (2026). RUT 2026 paso a paso.",
 ),
 "u3-guia": dict(
  n=3, titulo="Matrícula mercantil y tu local en regla",
  pregunta="¿Qué papeles le piden a tu local y cada cuánto se renuevan?",
  idea="La matrícula mercantil se renueva cada año antes del 31 de marzo. Tu local necesita uso de suelo, matrícula al día y avisar la apertura a la Policía.",
  caso="Wilson no renueva la matrícula de su taller en El Danubio hace tres años. Pasó la Policía y le preguntó por los papeles y la música.",
  bloques=[
   ("Lo que le piden a tu local", "lista", [
     ("Uso de suelo", "Que tu actividad esté permitida en esa dirección (Alcaldía)."),
     ("Matrícula al día", "Renovada este año en la Cámara de Comercio."),
     ("Aviso de apertura", "A la estación de Policía de tu zona."),
     ("Seguridad, sanidad y música", "Bomberos; salud si vendes comida; derechos de autor si pones música."),
   ]),
  ],
  etiqueta="La fecha", formula=("Renovar", "cada año, del 1 de enero al 31 de marzo"),
  ejemplo_titulo="Tu calendario",
  ejemplo=[("Enero a marzo", "renovar matrícula", ""), ("Si cambias de local", "nuevo uso de suelo", ""), ("Si cambias de datos", "actualizar RUT", ""),
           ("Cinco años sin renovar", "se cancela", "total")],
  nota_ejemplo="Antes de matricularte, consulta en el RUES que nadie tenga el nombre que quieres.",
  errores=["Dejar de renovar: la matrícula no se renueva sola.",
           "Abrir el local sin revisar el uso de suelo.",
           "Poner música para los clientes sin pagar derechos de autor."],
  preguntas=["¿Cuándo renovaste por última vez tu matrícula?",
             "¿Qué papel de tu local no podrías mostrar hoy?",
             "¿Qué pendiente vas a resolver primero y en qué fecha?"],
  dato="El 65,6 % de las panaderías y tiendas de barrio del país no estaba registrado en Cámara de Comercio en 2024 (DANE, 2026).",
  fuentes="Ley 1801 de 2016, art. 87. · Mincomercio (2025). Por qué renovar oportunamente su matrícula mercantil. · DANE (2026). EMICRON panaderías y tiendas de barrio 2024.",
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
    pct, resto = re.search(r"\d+(?:,\d+)? %", g["dato"]).group().replace(" ", "&nbsp;"), g["dato"]
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
