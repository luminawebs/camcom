"""Arma las guías de estudio de cada unidad (HTML listo para PDF A5).
Uso: python3 armar_guias.py && node renderizar_pdf.mjs
El contenido sale de los guiones de notebooklm/fuentes/. Si cambia un guion, cambia aquí también."""
import pathlib, re

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "Facturación electrónica sin miedo"

GUIAS = {
 "u1-guia": dict(
  n=1, titulo="¿Me toca facturar?",
  pregunta="¿Le toca facturar a tu negocio y qué es de verdad una factura electrónica?",
  idea="La factura electrónica es la factura de siempre, validada por la DIAN y enviada al correo del cliente. Facturar no es pagar más impuestos.",
  caso="Un colegio le quiere comprar a Gloria los refrigerios de todos los días en su panadería de San Mateo, pero le pide factura electrónica. Gloria cree que necesita un programa caro.",
  bloques=[
   ("A quién le toca", "pasos", [
     ("Comerciantes", "Quien compra y vende o presta servicios como negocio."),
     ("Responsables de IVA y del Régimen Simple", "Lo dice tu RUT, en la casilla de responsabilidades."),
     ("Profesionales", "Quien cobra honorarios por su profesión."),
   ]),
  ],
  etiqueta="La regla", formula=("Facturar", "dejar constancia de la venta, no pagar más impuestos"),
  ejemplo_titulo="Lo que ganas",
  ejemplo=[("Venderle a empresas", "pagan con factura", ""), ("Colegios y el Estado", "solo con factura", ""), ("Tus ventas en orden", "para un crédito", ""),
           ("Facturar con la DIAN", "gratis", "total")],
  nota_ejemplo="Si no te toca facturar, la empresa que te compra hace un documento soporte. Confirma tu caso con un contador.",
  errores=["Creer que facturar es pagar más impuestos.",
           "Comprar un programa sin saber que la DIAN tiene uno gratis.",
           "Decidir si te toca sin revisar tu RUT con un contador."],
  preguntas=["¿Qué cliente te ha pedido factura y qué pasó?",
             "¿Qué dice tu RUT en las responsabilidades?",
             "¿Te toca facturar? ¿Qué tienes que confirmar y con quién?"],
  dato=("$52.374", "es el valor de la UVT de 2026, la medida que usa la ley para los topes (DIAN, Resolución 000238 de 2025)."),
  fuentes="DIAN (2023). Resolución 000165, art. 7. · DIAN (2020). Oficio 907979. · DIAN (2025). Resolución 000238 (UVT 2026).",
 ),
 "u2-guia": dict(
  n=2, titulo="Habilítate gratis en la DIAN",
  pregunta="¿Cómo te habilitas para facturar sin pagar un programa?",
  idea="La DIAN tiene un servicio gratuito para facturar. Te registras, pides tu firma, haces las pruebas y pides tu numeración.",
  caso="Un contratista le quiere comprar materiales a Andrés cada semana en su ferretería de Quintanares, pero solo si le factura. Le dijeron que el programa cuesta medio millón al año.",
  bloques=[
   ("Antes de empezar", "lista", [
     ("RUT al día", "Dirección, celular, correo y actividad correctos."),
     ("Correo del RUT", "Ahí te llegan los códigos."),
     ("Usuario de la DIAN", "Y su contraseña; se recupera con el correo."),
     ("Celular o computador", "Con internet. No compras nada."),
   ]),
  ],
  etiqueta="La ruta", formula=("Habilitarte", "registro gratuito + firma + pruebas + numeración"),
  ejemplo_titulo="Los pasos",
  ejemplo=[("1. Registro como facturador", "servicio gratuito", ""), ("2. Certificado de firma", "gratis", ""), ("3. Facturas de prueba", "y fecha de inicio", ""),
           ("4. Numeración y prefijo", "y contingencia", ""), ("A facturar", "listo", "total")],
  nota_ejemplo="Al habilitarte, tu RUT queda con la responsabilidad 52 (facturador electrónico). No te cambia los impuestos.",
  errores=["Pagar un programa sin conocer el servicio gratuito.",
           "Registrarte con un correo que ya no revisas.",
           "Olvidar pedir el rango de contingencia."],
  preguntas=["¿Tu RUT tiene bien tus datos y tu correo?",
             "¿En qué paso de la habilitación vas?",
             "¿Cuál es tu siguiente paso y en qué fecha lo vas a hacer?"],
  dato=("$0", "cuestan el servicio de facturación de la DIAN y el certificado de firma [VERIFICAR con el contador]."),
  fuentes="DIAN. Facturación gratuita. · DIAN. 3 pasos para facturar electrónicamente. · Actualícese. Los 5 pasos para facturar con el servicio gratuito.",
 ),
 "u3-guia": dict(
  n=3, titulo="Tu primera factura, sin errores",
  pregunta="¿Qué datos lleva tu factura y qué haces si te equivocas?",
  idea="Pide los datos completos antes de facturar. Si te equivocas, la factura no se borra: haces una nota crédito y una factura nueva.",
  caso="Doris le hizo su primera factura a una empresa de vigilancia por los almuerzos del mes, pero escribió mal el NIT. La contadora se la devolvió.",
  bloques=[
   ("Lo que lleva tu factura", "lista", [
     ("Tus datos", "Nombre y NIT, y tu número autorizado con prefijo."),
     ("Los del cliente", "Nombre, NIT o cédula y correo."),
     ("La venta", "Fecha y hora, qué vendiste, cantidad, valor y forma de pago."),
     ("El código único", "CUFE y QR, que pone el sistema."),
   ]),
  ],
  etiqueta="La regla", formula=("Error", "nota crédito + factura nueva"),
  ejemplo_titulo="Antes de enviar",
  ejemplo=[("Nombre del cliente", "completo", ""), ("NIT o cédula", "contra el RUT", ""), ("Correo", "el de facturación", ""),
           ("Detalle y valor", "revisado", ""), ("Lista para enviar", "✓", "total")],
  nota_ejemplo="Si el cliente no da sus datos: «consumidor final» con el número 222222222222. Nunca inventes datos.",
  errores=["Escribir el NIT sin revisarlo contra el RUT del cliente.",
           "Intentar borrar una factura en vez de hacer una nota crédito.",
           "Dejar de vender cuando se cae el sistema: usa la contingencia."],
  extra=("¿Y si ya la aceptaron?", "Si el cliente ya aceptó la factura (o pasaron tres días hábiles sin reclamo), ya no se corrige con una nota crédito de la forma normal. Pide ayuda a un contador."),
  preguntas=["¿Qué datos les pides hoy a tus clientes?",
             "¿Cuál es el error que más te preocupa cometer?",
             "¿A quién le vas a hacer tu primera factura?"],
  dato=("3 días", "hábiles tiene tu cliente para reclamar la factura; si no reclama, queda aceptada (Decreto 1074 de 2015) [VERIFICAR]."),
  fuentes="DIAN (2022). Oficio 900223. · Decreto 1074 de 2015, art. 2.2.2.5.4 (aceptación). · Estatuto Tributario, arts. 617 y 652-1.",
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
