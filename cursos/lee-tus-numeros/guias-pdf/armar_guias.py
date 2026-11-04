"""Arma las guías de estudio de cada unidad (HTML listo para PDF A5).
Uso: python3 armar_guias.py && node renderizar_pdf.mjs
El contenido sale de los guiones de notebooklm/fuentes/. Si cambia un guion, cambia aquí también."""
import pathlib, re

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "Lee tus números"

GUIAS = {
 "u1-guia": dict(
  n=1, titulo="Ingresos, costos y gastos",
  pregunta="¿Qué parte de lo que mueve tu negocio es ingreso, qué es costo y qué es gasto?",
  idea="Para saber cuánto gana tu negocio, primero pon cada peso en su lugar: lo que vendes, lo que te cuesta lo que vendes y lo que pagas por estar abierto.",
  caso="La cooperativa le pide a Patricia el estado de resultados de su negocio de comidas rápidas en La Despensa para prestarle para una plancha. En su Nequi está todo mezclado.",
  bloques=[
   ("Las cuatro preguntas", "pasos", [
     ("¿Lo vendí?", "Es un ingreso. Un préstamo no lo es."),
     ("¿Lo necesito para hacer lo que vendo?", "Es un costo: insumos, mercancía, empaques."),
     ("¿Lo pago aunque no venda?", "Es un gasto: arriendo, servicios, sueldos."),
     ("¿Es de la casa?", "No va en las cuentas del negocio."),
   ]),
  ],
  etiqueta="La regla", formula=("Cada peso", "ingreso, costo, gasto o «no es del negocio»"),
  ejemplo_titulo="Un mes de Patricia (cifras de ejemplo)",
  ejemplo=[("Ventas", "ingreso", ""), ("Salchichas, pan, papa, empaques", "costo", ""), ("Arriendo, gas, luz", "gasto", ""),
           ("Préstamo de la cooperativa", "no es ingreso", ""), ("Mercado de la casa", "no va", "total")],
  nota_ejemplo="Tu sueldo sí es un gasto del negocio. Lo que sacas para la casa sale de tu sueldo.",
  errores=["Contar un préstamo como si fuera una venta.",
           "Meter el mercado de la casa en los gastos del negocio.",
           "Olvidar tu propio sueldo: el negocio parece ganar más de lo que gana."],
  preguntas=["¿Qué pagaste ayer en tu negocio? ¿Era costo o gasto?",
             "¿Qué plata de la casa sale hoy de la cuenta del negocio?",
             "¿Te pagas un sueldo fijo? ¿De cuánto?"],
  dato=("1,5 %", "de los micronegocios usa el balance general o el estado de resultados como su registro principal; el 67,3 % no lleva registros (DANE, EMICRON 2024, microdatos) [VERIFICAR cifra ponderada]."),
  fuentes="DANE (2025). EMICRON 2024. · INCP (2023). La contabilidad como herramienta estratégica para los microempresarios. · Alegra. Cómo leer el estado de resultados.",
 ),
 "u2-guia": dict(
  n=2, titulo="El mes en números",
  pregunta="¿Cómo juntas las ventas y los gastos de un mes sin contar nada dos veces?",
  idea="Junta todo lo del mes en una sola hoja, cuenta cada venta una sola vez y deja por fuera lo que entra pero no es venta.",
  caso="Óscar tiene una tienda de mascotas en Ciudad Verde. Anota en un cuaderno, recibe por Nequi y les fía a los vecinos. No sabe cuánto vendió en septiembre.",
  bloques=[
   ("Tus fuentes", "lista", [
     ("Cuaderno o libreta", "Las ventas en efectivo."),
     ("Nequi, Daviplata o banco", "El historial del mes."),
     ("Datáfono y facturas", "Pagos con tarjeta y compras a proveedores."),
     ("Lista de fiados", "Lo que vendiste y te pagan después."),
   ]),
  ],
  etiqueta="La fórmula", formula=("Ventas del mes", "efectivo + transferencias + fiado del mes − lo que no es venta"),
  ejemplo_titulo="Septiembre de Óscar (cifras de ejemplo)",
  ejemplo=[("Efectivo del cuaderno", "$3.000.000", ""), ("Nequi: todo lo que entró", "$2.000.000", ""), ("− Pasado de la caja al Nequi", "−$500.000", ""),
           ("+ Fiados de septiembre", "$200.000", ""), ("Ventas del mes", "$4.700.000", "total")],
  nota_ejemplo="Cuando el vecino pague el fiado en octubre, no lo vuelvas a sumar: ya está en septiembre.",
  errores=["Sumar el cuaderno y todo el Nequi sin quitar lo que pasaste de la caja.",
           "Contar un préstamo o la plata de tu bolsillo como venta.",
           "Sumar el fiado dos veces: cuando lo vendes y cuando te pagan."],
  preguntas=["¿En cuántos lugares queda registro de lo que vendes?",
             "¿Qué mes vas a juntar primero?",
             "¿Qué vas a anotar distinto desde hoy?"],
  dato=("1 hoja", "con el mes completo es el punto de partida de tu estado de resultados."),
  fuentes="Banca de las Oportunidades (2021). Reporte de micronegocios. · Banca de las Oportunidades (2025). Panorama de la exclusión financiera y el crédito informal en los micronegocios.",
 ),
 "u3-guia": dict(
  n=3, titulo="Tu estado de resultados del mes",
  pregunta="¿Cuánto ganó de verdad tu negocio el mes pasado y cómo lo muestras en una hoja?",
  idea="El estado de resultados resta, de arriba hacia abajo, el costo de lo vendido y los gastos a las ventas. Lo que queda es la utilidad del mes.",
  caso="Marisol tiene una papelería en León XIII. En febrero vendió el doble que en un mes normal, pero casi no le quedó plata.",
  bloques=[
   ("Las líneas", "pasos", [
     ("Ventas del mes", "Todo lo que vendiste, cobrado o fiado."),
     ("− Costo de lo vendido = utilidad bruta", "Lo que te costó la mercancía que vendiste."),
     ("− Gastos = utilidad del mes", "Arriendo, servicios, sueldos (el tuyo también)."),
   ]),
  ],
  etiqueta="La fórmula", formula=("Utilidad del mes", "ventas − costo de lo vendido − gastos"),
  ejemplo_titulo="Un mes normal de Marisol (cifras de ejemplo)",
  ejemplo=[("Ventas", "$4.500.000", ""), ("− Costo de lo vendido", "−$2.250.000", ""), ("Utilidad bruta", "$2.250.000", "sub"),
           ("− Gastos (con su sueldo de $800.000)", "−$1.800.000", ""), ("Utilidad del mes · margen 10 %", "$450.000", "total")],
  nota_ejemplo="Margen = utilidad ÷ ventas × 100. En febrero vendió $9.000.000 y le quedaron $270.000: margen del 3 %.",
  errores=["Decir cuánto vendiste cuando te preguntan cuánto ganaste.",
           "Dejar tu sueldo por fuera de los gastos.",
           "Mirar solo las ventas y no el margen."],
  extra=("¿Y el banco?", "Cada entidad pide cosas distintas. Si eres comerciante, la ley te pide llevar contabilidad, y una microempresa prepara su estado de resultados y su estado de situación financiera. Un contador te ayuda a dejarlos oficiales."),
  preguntas=["¿Cuál fue tu utilidad del mes pasado?",
             "¿Cuál es tu margen? ¿Es mejor o peor que el mes anterior?",
             "¿Qué precio o qué gasto vas a revisar?"],
  dato=("3.8", "es el párrafo del Anexo 3 del Decreto 2420 de 2015 que dice qué estados prepara una microempresa [VERIFICAR con el contador]."),
  fuentes="Decreto 2420 de 2015, Anexo 3, párr. 3.8. · CTCP (2019). Concepto 676. · Código de Comercio, art. 19. · Alegra. Cómo leer el estado de resultados.",
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
