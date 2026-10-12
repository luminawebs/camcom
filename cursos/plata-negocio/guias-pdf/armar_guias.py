"""Arma las guías de estudio de cada unidad (HTML listo para PDF A5).
Uso: python3 armar_guias.py && node renderizar_pdf.mjs
El contenido sale de los guiones de notebooklm/fuentes/. Si cambia un guion, cambia aquí también."""
import pathlib, re

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "La plata del negocio no es la de la casa"

GUIAS = {
 "u1-guia": dict(
  n=1, titulo="Por qué se mezcla la plata",
  pregunta="¿Por dónde se va la plata del negocio?",
  idea="La plata del negocio tiene dueño: el negocio. Lo que vendes no es todo tuyo, una parte es para volver a surtir.",
  caso="Luz Dary vende cerca de $300.000 al día en su miscelánea de León XIII, pero el día 30 no tiene para surtir.",
  bloques=[
   ("Las 4 fugas", "lista", [
     ("El cajón para la casa", "Sacas para el mercado, el arriendo o las onces sin anotarlo."),
     ("Los pagos cruzados", "Pagas la luz de la casa con plata del negocio, o la mercancía con tu tarjeta."),
     ("Lo que consumes", "El cuaderno, la gaseosa o el regalo que tomas del negocio."),
     ("El celular personal", "Los clientes te pagan al mismo Nequi o Daviplata de la familia."),
   ]),
   ("Una venta no es una ganancia", "barra", ("Cuaderno vendido en $5.000", [("Para volver a surtir", "$3.500", 70), ("Ganancia", "$1.500", 30)])),
  ],
  formula=("Se fue", "caja inicial + ventas − pagos del negocio − caja final"),
  ejemplo=[("Caja del lunes", "$200.000", ""), ("+ Ventas de la semana", "$1.800.000", ""), ("− Pagos del negocio", "$1.100.000", ""),
           ("= Debería haber", "$900.000", "sub"), ("− Hay el domingo", "$350.000", ""), ("Se fue sin anotar", "$550.000", "total")],
  errores=["Olvidar la caja del lunes: la plata con la que empezaste también es del negocio.",
           "No restar los pagos del negocio: esa plata salió, pero está anotada; no es una fuga.",
           "Quedarse en lo que «debería haber» y no restarle lo que de verdad hay."],
  preguntas=["¿Cuál de las 4 fugas pasa más en tu negocio?",
             "¿Cuánto sacaste esta semana para cosas de la casa sin anotarlo?",
             "Del producto que más vendes, ¿cuánto es ganancia y cuánto es para volver a surtir?"],
  dato="El 68,2 % de los micronegocios en Colombia no lleva ningún registro contable (DANE, 2025).",
  fuentes="DANE (2025). Encuesta de Micronegocios (EMICRON) 2024: boletín técnico.",
 ),
 "u2-guia": dict(
  n=2, titulo="Págate un sueldo",
  pregunta="¿Cuánto te puedes pagar sin dejar sin plata al negocio?",
  idea="Si atiendes tu negocio, eres su trabajadora más importante: págate un sueldo fijo, en una fecha fija, no «lo que necesites».",
  caso="En octubre Luz Dary sacó $2.500.000 del negocio; en noviembre, $600.000. En enero no tuvo para surtir los útiles escolares.",
  bloques=[
   ("Tu sueldo en 3 pasos", "pasos", [
     ("Ganancia del mes", "Ventas − todo lo que pagaste para el negocio: mercancía, arriendo y servicios del local, transporte."),
     ("Promedio de 3 meses", "Un solo mes engaña: hay meses buenos y malos."),
     ("Deja un colchón", "Una parte se queda en el negocio para los meses malos y para crecer. En el curso usamos el 20 %."),
   ]),
  ],
  formula=("Sueldo", "promedio de ganancia de 3 meses × 0,80"),
  ejemplo=[("Mes 1", "$2.400.000", ""), ("Mes 2", "$1.800.000", ""), ("Mes 3", "$2.100.000", ""),
           ("Promedio (suma ÷ 3)", "$2.100.000", "sub"), ("× 0,80 (colchón del 20 %)", "", ""), ("Sueldo al mes", "$1.680.000", "total")],
  nota_ejemplo="Por quincenas: $840.000 el 15 y $840.000 el 30. El colchón del 20 % es una regla práctica del curso, no una norma: tu contador puede ajustarla.",
  errores=["Usar el mejor mes en lugar del promedio.",
           "Sacar el promedio y olvidar el colchón.",
           "Sumar los tres meses y no dividir entre 3."],
  extra_p1=True,
  extra=("¿Y si no alcanza para la casa?", "No es culpa tuya: es una señal, y ahora la ves con números. Hay tres caminos: vender más, revisar precios o bajar costos."),
  preguntas=["¿Cuánto ganó tu negocio en cada uno de los últimos tres meses?",
             "¿Qué fechas fijas vas a usar para pagarte?",
             "Si tu sueldo no alcanza para la casa, ¿qué camino probarías primero?"],
  dato="El 75,1 % de los micronegocios que ahorraron lo hicieron para gastos del hogar, frente al 35 % para gastos del negocio (Banca de las Oportunidades, 2021).",
  fuentes="Banca de las Oportunidades (2021). Reporte de micronegocios. · Leal, A. C. (s. f.). 7 tips para separar tu dinero del de tu negocio. Siigo.",
 ),
 "u3-guia": dict(
  n=3, titulo="Una cuenta y un registro para el negocio",
  pregunta="¿Cómo separar la plata del negocio sin complicarte?",
  idea="Una cuenta solo para el negocio: todo entra ahí y todo sale de ahí; a la casa va solo tu sueldo. Cinco minutos al día de registro te dicen si estás ganando.",
  caso="A Luz Dary los clientes le pagan al mismo Nequi donde su hija le manda para el arriendo. No puede saber cuánto vendió en la semana.",
  bloques=[
   ("Las 3 reglas de la plata", "pasos", [
     ("Todo entra ahí", "Todo lo que vendes entra a la cuenta del negocio, también el efectivo al final del día."),
     ("Todo sale de ahí", "Todo gasto del negocio sale de esa cuenta."),
     ("A la casa, solo tu sueldo", "Por transferencia, en tu fecha fija."),
   ]),
   ("El registro: 5 columnas", "columnas", ["Fecha", "Qué fue", "Entró", "Salió", "Saldo"]),
  ],
  formula=("Saldo de hoy", "saldo de ayer + lo que entró − lo que salió"),
  ejemplo=[("Empezó el día con", "$400.000", ""), ("+ Vendió", "$350.000", ""), ("− Pagó al proveedor", "$120.000", ""),
           ("Saldo al cerrar", "$630.000", "total")],
  nota_ejemplo="Si el saldo del cuaderno no cuadra con la cuenta y el cajón, algo se fue sin anotar.",
  errores=["Olvidar el sueldo: también sale de la cuenta del negocio y se anota.",
           "Olvidar las ventas en efectivo.",
           "No arrancar del saldo de ayer."],
  extra=("Tu registro abre puertas", "Con una cuenta y un registro ordenados puedes mostrar cuánto vende tu negocio cuando pidas un crédito en un banco, y no en el gota a gota."),
  preguntas=["¿Qué cuenta o billetera vas a usar solo para el negocio?",
             "¿A qué hora del día vas a hacer tu registro de 5 minutos?",
             "¿Qué pagos de la casa salen hoy de la plata del negocio?"],
  dato="En 2024, el 22,9 % de los micronegocios que pidieron crédito acudió a prestamistas gota a gota (DANE, 2025).",
  fuentes="DANE (2025). Encuesta de Micronegocios (EMICRON) 2024: boletín técnico. · Banca de las Oportunidades (2021). Reporte de micronegocios.",
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
<h2>La fórmula</h2>
<div class='formula'><small>Apréndetela</small><b>{g['formula'][0]}</b> = {g['formula'][1]}</div>
<div class='ej'><div class='cab'>Ejemplo</div>{ej}</div>{nota}
{'' if g.get('extra_p1') else extra}
<h2>Piensa en tu negocio</h2><div class='preg'>{''.join(f'<div><span>{i}.</span>{q}<i></i></div>' for i, q in enumerate(g['preguntas'], 1))}</div>
<div class='dato'><b>{pct}</b><span>{resto}</span></div>
</div>
<p class='fuentes'>Fuentes: {g['fuentes']}</p>{pie(2)}</section>"""
    html = f"<!doctype html><html lang='es'><head><meta charset='utf-8'><title>Guía de estudio · Unidad {n}</title><style>{CSS}</style></head><body>{p1}{p2}</body></html>"
    (AQUI / f"{ident}.html").write_text(html, encoding="utf-8")
    print("ok", ident)
