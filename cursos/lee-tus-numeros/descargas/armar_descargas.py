"""Arma las descargas de Llévatelo (HTML -> PDF A5) con el logo de edunest.
Uso: python3 armar_descargas.py && node ../guias-pdf/renderizar_pdf.mjs descargas"""
import pathlib

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "Lee tus números"
CSS = """@page{size:A5;margin:0}*{box-sizing:border-box;margin:0}
body{font-family:Inter,'DejaVu Sans',sans-serif;color:#1a1a1a;font-size:10.5pt}
.pag{width:148mm;height:210mm;padding:9mm 10mm;position:relative;page-break-after:always}
.top{display:flex;justify-content:space-between;align-items:center;font-size:7.5pt;color:#6b6b72;text-transform:uppercase;letter-spacing:.06em}
.top svg{height:6mm;width:auto}
.hero{background:#c8102e;color:#fff;border-radius:4mm;padding:6mm;margin:5mm 0}
.hero small{font-size:8pt;text-transform:uppercase;letter-spacing:.08em;opacity:.85}
.hero h1{font-size:17pt;line-height:1.15;margin-top:1.5mm}
.hero p{font-size:9.5pt;margin-top:2mm}
table{width:100%;border-collapse:collapse}
th{font-size:7.5pt;text-transform:uppercase;letter-spacing:.06em;color:#6b6b72;text-align:left;padding:1.5mm;border-bottom:.6mm solid #141414}
td{padding:2.4mm 1.5mm;border-bottom:.3mm solid #e2e2e5;vertical-align:top;font-size:9.5pt}
td b{display:block}
td small{color:#6b6b72;font-size:8pt}
.c{width:9mm;text-align:center}.c i{display:inline-block;width:4.5mm;height:4.5mm;border:.5mm solid #141414;border-radius:1mm}
.f{width:24mm}.f i{display:block;border-bottom:.3mm solid #8d8d94;height:5mm}
h2{font-size:10pt;color:#9e0c24;margin:4mm 0 1mm}
.nota{font-size:8pt;color:#6b6b72;margin-top:3mm}
.w{width:22mm}.w i{display:block;border-bottom:.3mm solid #8d8d94;height:5mm}
.lin td{height:8.4mm}
.tot td{background:#141414;color:#fff;font-weight:800}
.sub td{background:#f6f6f7;font-weight:700}
.pie{position:absolute;left:10mm;right:10mm;bottom:6mm;font-size:7pt;color:#8d8d94;display:flex;justify-content:space-between}"""


def pagina(etiqueta, titulo, sub, cuerpo, n=1, de=1):
    return (f"<section class='pag'><div class='top'>{LOGO}<span>{etiqueta}</span></div>"
            f"<div class='hero'><small>{CURSO}</small><h1>{titulo}</h1><p>{sub}</p></div>{cuerpo}"
            f"<div class='pie'><span>Aula Virtual Empresarial · Cámara de Comercio de Soacha</span><span>{n} / {de}</span></div></section>")



def doc(nombre, titulo, paginas):
    (AQUI / f"{nombre}.html").write_text(
        f"<!doctype html><html lang='es'><head><meta charset='utf-8'><title>{titulo}</title><style>{CSS}</style></head><body>{''.join(paginas)}</body></html>",
        encoding="utf-8")
    print("ok", nombre)


def blanco(n):
    return "<td class='w'><i></i></td>" * n


# Unidad 1 · tabla para clasificar
cab = "<tr><th>Movimiento</th><th class='w'>Valor</th><th class='c'>Ingreso</th><th class='c'>Costo</th><th class='c'>Gasto</th><th class='c'>No va</th></tr>"
ej = [("Venta del día (ejemplo)", "$250.000", 0), ("Compra de pan y salchichas (ejemplo)", "$80.000", 1), ("Arriendo del local (ejemplo)", "$900.000", 2), ("Mercado de la casa (ejemplo)", "$120.000", 3)]
filas_ej = "".join(f"<tr><td>{a}</td><td>{v}</td>" + "".join(f"<td class='c'>{'✓' if i == k else ''}</td>" for i in range(4)) + "</tr>" for a, v, k in ej)
vacias = lambda n: "".join("<tr class='lin'><td></td>" + blanco(1) + "<td class='c'><i></i></td>" * 4 + "</tr>" for _ in range(n))
preg = ("<p class='nota'><b>¿Lo vendí?</b> Ingreso · <b>¿Lo necesito para hacer lo que vendo?</b> Costo · "
        "<b>¿Lo pago aunque no venda?</b> Gasto · <b>¿Es de la casa?</b> No va. Un préstamo o la plata que pones de tu bolsillo no son ingresos.</p>")
doc("u1-clasifica-movimientos", "Tabla para clasificar tus movimientos", [
    pagina("Unidad 1 · Llévatelo", "Clasifica tus movimientos", "Anota 10 movimientos de tu negocio de esta semana y marca en qué columna va cada uno.",
           f"<table>{cab}{filas_ej}{vacias(4)}</table>{preg}", 1, 2),
    pagina("Unidad 1 · Llévatelo", "Clasifica tus movimientos", "Sigue con los que faltan. Al final suma cada columna.",
           f"<table>{cab}{vacias(6)}<tr class='sub'><td>Total de la semana</td>" + blanco(1) + "<td class='c'></td>" * 4 + "</tr></table>"
           "<h2>Tus totales</h2><table><tr><td>Ingresos</td><td class='w'><i></i></td></tr><tr><td>Costos</td><td class='w'><i></i></td></tr>"
           "<tr><td>Gastos</td><td class='w'><i></i></td></tr><tr><td>No va (de la casa, préstamos)</td><td class='w'><i></i></td></tr></table>", 2, 2)])

# Unidad 2 · hoja para juntar el mes
lin = lambda a, b="": f"<tr class='lin'><td><b>{a}</b><small>{b}</small></td><td class='w'><i></i></td></tr>"
doc("u2-hoja-del-mes", "Hoja para juntar el mes", [
    pagina("Unidad 2 · Llévatelo", "Junta el mes en una hoja", "Mes: ______________ (del 1 al último día). Ten a la mano el cuaderno, el historial de Nequi o el banco, los recibos y la lista de fiados.",
           "<h2>Ventas del mes</h2><table><tr><th>Qué</th><th class='w'>Valor</th></tr>"
           + lin("Ventas en efectivo", "Del cuaderno o la libreta.") + lin("Todo lo que entró por Nequi, Daviplata o el banco")
           + lin("− Plata que tú pasaste de la caja", "Ya estaba en el efectivo.") + lin("− Préstamos y plata de tu bolsillo", "Entran, pero no son ventas.")
           + lin("+ Ventas con datáfono", "Si no las sumaste ya en el banco.") + lin("+ Fiados que hiciste este mes", "Aunque te paguen después.")
           + "<tr class='tot'><td>VENTAS DEL MES</td><td></td></tr></table>"
           "<p class='nota'>Si te pagan un fiado de un mes anterior, no lo sumes: ya estaba contado ese mes.</p>", 1, 2),
    pagina("Unidad 2 · Llévatelo", "Costos y gastos del mes", "Con las facturas y los recibos del mes. Deja por fuera lo de la casa.",
           "<h2>Costos (lo que te costó lo que vendiste)</h2><table><tr><th>Qué</th><th class='w'>Valor</th></tr>"
           + lin("Mercancía o insumos") + lin("Empaques") + lin("Otro costo") + "<tr class='sub'><td>Total costos</td><td></td></tr></table>"
           "<h2>Gastos (lo que pagas por estar abierto)</h2><table><tr><th>Qué</th><th class='w'>Valor</th></tr>"
           + lin("Arriendo") + lin("Servicios e internet") + lin("Sueldos de quien te ayuda") + lin("Tu sueldo") + lin("Otros gastos")
           + "<tr class='sub'><td>Total gastos</td><td></td></tr></table>"
           "<p class='nota'>Si pagaste algo de dos meses de una vez, pon en este mes solo lo que le toca.</p>", 2, 2)])

# Unidad 3 · plantilla del estado de resultados
fila3 = lambda a, b="", c="": f"<tr class='lin {c}'><td><b>{a}</b><small>{b}</small></td><td class='w'><i></i></td></tr>"
doc("u3-estado-de-resultados", "Plantilla del estado de resultados", [
    pagina("Unidad 3 · Llévatelo", "Estado de resultados", "Negocio: ______________________ · Mes: ______________. Pasa aquí los números de la hoja del mes.",
           "<table><tr><th>Concepto</th><th class='w'>Valor</th></tr>"
           + fila3("Ventas del mes") + fila3("− Costo de lo vendido", "Mercancía o insumos de lo que vendiste.")
           + "<tr class='sub'><td>= UTILIDAD BRUTA</td><td></td></tr>"
           + fila3("− Arriendo") + fila3("− Servicios e internet") + fila3("− Sueldos de quien te ayuda") + fila3("− Tu sueldo") + fila3("− Otros gastos")
           + "<tr class='sub'><td>= Total gastos</td><td></td></tr><tr class='tot'><td>= UTILIDAD DEL MES</td><td></td></tr></table>"
           "<h2>Margen</h2><p>Utilidad del mes ÷ ventas × 100 = ______ %</p>", 1, 2),
    pagina("Unidad 3 · Llévatelo", "Lee tu estado de resultados", "Contesta estas preguntas antes de mostrarlo.",
           "<table><tr><th>Pregunta</th><th class='w'>Tu respuesta</th></tr>"
           + fila3("¿La utilidad dio positiva o negativa?") + fila3("¿Tu margen es mayor o menor que el mes anterior?")
           + fila3("¿Cuál es tu gasto más grande?") + fila3("¿Qué precio vas a revisar?") + fila3("¿Incluiste tu sueldo?") + "</table>"
           "<p class='nota'>Ejemplo de un mes normal de Marisol (cifras de ejemplo): ventas $4.500.000 − costo $2.250.000 = utilidad bruta $2.250.000 − gastos $1.800.000 = utilidad $450.000. Margen 10 %.</p>"
           "<p class='nota'>Este formato sirve para leer tu negocio. Para un banco o una entidad, un contador te ayuda a dejarlo oficial.</p>", 2, 2)])

# Unidad 4 · hoja del balance
doc("u4-hoja-balance", "Hoja del balance general", [
    pagina("Unidad 4 · Llévatelo", "Tu balance general", "Negocio: ______________________ · Fecha (un solo día): ______________. Solo cosas del negocio.",
           "<h2>Lo que tiene (activos)</h2><table><tr><th>Qué</th><th class='w'>Valor</th></tr>"
           + fila3("Plata en la caja") + fila3("Plata en Nequi, Daviplata o el banco") + fila3("Mercancía e insumos", "Al precio al que los compraste.")
           + fila3("Fiados por cobrar", "Solo los que crees que te van a pagar.") + fila3("Equipos", "Lo que costaron menos el desgaste.")
           + "<tr class='sub'><td>= Total lo que tiene</td><td></td></tr></table>"
           "<h2>Lo que debe (pasivos)</h2><table><tr><th>Qué</th><th class='w'>Valor</th></tr>"
           + fila3("A proveedores") + fila3("Saldo de préstamos del negocio") + fila3("Impuestos o arriendo por pagar")
           + "<tr class='sub'><td>= Total lo que debe</td><td></td></tr><tr class='tot'><td>LO QUE ES TUYO (PATRIMONIO)</td><td></td></tr></table>"
           "<p class='nota'>Patrimonio = lo que tiene − lo que debe. Ejemplo de Patricia (cifras de ejemplo): $6.600.000 − $1.600.000 = $5.000.000.</p>", 1, 1)])

# Unidad 6 · carpeta del crédito
chk = lambda a, b="": f"<tr><td class='c'><i></i></td><td><b>{a}</b><small>{b}</small></td></tr>"
doc("u6-carpeta-del-credito", "Carpeta del crédito", [
    pagina("Unidad 6 · Llévatelo", "Tu carpeta del crédito", "Marca lo que ya tienes. Cada entidad pide distinto: pregunta antes de ir.",
           "<table><tr><th class='c'>✓</th><th>Documento</th></tr>"
           + chk("Cédula") + chk("RUT") + chk("Certificado de matrícula mercantil", "De la Cámara de Comercio, si eres comerciante formal.")
           + chk("Estado de resultados de los últimos meses", "Unidad 3.") + chk("Balance general a la fecha", "Unidad 4.")
           + chk("Flujo de efectivo", "Unidad 5.") + chk("Extractos de Nequi, Daviplata o el banco", "De los últimos 3 a 6 meses.")
           + chk("Facturas o recibos", "De las ventas y las compras grandes.") + "</table>"
           "<p class='nota'>Ordénalos en una carpeta (o una carpeta del celular) con la fecha de cada uno.</p>", 1, 2),
    pagina("Unidad 6 · Llévatelo", "Tus tres frases y tu cuota", "Escríbelas con tus números y llévalas dichas.",
           "<table><tr><th>Frase</th><th class='w'>Tu número</th></tr>"
           + fila3("1. «Mi negocio vende en promedio … al mes»", "Del estado de resultados.")
           + fila3("2. «Después de pagar todo, con mi sueldo, le quedan …»", "La utilidad del mes.")
           + fila3("3. «Cada mes me sobran … para pagar una cuota»", "Del flujo: entradas − salidas, sin la cuota nueva.") + "</table>"
           "<h2>¿Te cabe la cuota?</h2><table><tr><th>Concepto</th><th class='w'>Valor</th></tr>"
           + fila3("Cuota nueva que te ofrecen") + fila3("Lo que te sobra al mes (frase 3)")
           + "<tr class='tot'><td>PESO DE LA CUOTA = cuota ÷ lo que te sobra × 100</td><td>%</td></tr></table>"
           "<h2>Pregunta antes de firmar</h2><p class='nota'>¿Cuál es la tasa efectiva anual? ¿Cuánto voy a pagar en total? ¿Hay seguros o cobros aparte? ¿Qué pasa si me atraso?</p>", 2, 2)])


# Plantillas de Excel (calculan solas): U4 balance, U5 flujo de 4 semanas, U7 tablero de 3 indicadores
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

ROJO, NEGRO, GRIS = "C8102E", "141414", "F6F6F7"
PESOS = '"$"#,##0;[Red]-"$"#,##0'
fino = Side(style="thin", color="E2E2E5")


def libro(titulo, sub):
    wb = Workbook(); ws = wb.active
    ws["A1"] = f"{CURSO} · {titulo}"; ws["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    ws["A2"] = sub; ws["A2"].font = Font(italic=True, size=10, color="FFFFFF")
    for f in (1, 2):
        for col in range(1, 8):
            ws.cell(f, col).fill = PatternFill("solid", fgColor=ROJO)
    ws.column_dimensions["A"].width = 46
    return wb, ws


def fila(ws, f, texto, valor=None, tipo="", formato=PESOS, nota=""):
    ws.cell(f, 1, texto)
    if valor is not None:
        c = ws.cell(f, 2, valor); c.number_format = formato
    if nota:
        ws.cell(f, 3, nota).font = Font(size=9, color="6B6B72")
    for col in (1, 2):
        c = ws.cell(f, col); c.border = Border(bottom=fino)
        if tipo == "sub":
            c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor=GRIS)
        if tipo == "tot":
            c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=NEGRO)
        if tipo == "dato":
            c.fill = PatternFill("solid", fgColor="FFF7E6") if col == 2 else PatternFill()


# U4 · balance general (con el ejemplo de Patricia; cambia los valores amarillos)
wb, ws = libro("Balance general", "Escribe en las celdas amarillas los valores de tu negocio en un solo día. El resto se calcula solo.")
ws.column_dimensions["B"].width = 18; ws.column_dimensions["C"].width = 46
ws["A4"] = "Fecha del balance:"; ws["B4"] = "31/10/2026"; ws["A4"].font = Font(bold=True)
ws["A6"] = "LO QUE TIENE (ACTIVOS)"; ws["A6"].font = Font(bold=True, color=ROJO)
datos = [("Plata en la caja", 300000, ""), ("Plata en Nequi, Daviplata o el banco", 500000, ""), ("Mercancía e insumos", 600000, "Al precio al que los compraste"),
         ("Fiados por cobrar", 0, "Solo los que crees que te van a pagar"), ("Equipos", 5200000, "Lo que costaron menos el desgaste")]
for k, (t, v, n) in enumerate(datos):
    fila(ws, 7 + k, t, v, "dato", nota=n)
fila(ws, 12, "= Total lo que tiene", "=SUM(B7:B11)", "sub")
ws["A14"] = "LO QUE DEBE (PASIVOS)"; ws["A14"].font = Font(bold=True, color=ROJO)
for k, (t, v) in enumerate([("A proveedores", 400000), ("Saldo de préstamos del negocio", 1200000), ("Impuestos o arriendo por pagar", 0)]):
    fila(ws, 15 + k, t, v, "dato")
fila(ws, 18, "= Total lo que debe", "=SUM(B15:B17)", "sub")
fila(ws, 20, "LO QUE ES TUYO (PATRIMONIO)", "=B12-B18", "tot")
ws["A22"] = "Ejemplo con los números de Patricia (cifras de ejemplo). Solo cosas del negocio y todo con la misma fecha."
ws["A22"].font = Font(size=9, italic=True, color="6B6B72")
wb.save(AQUI / "u4-balance-general.xlsx"); print("ok u4-balance-general.xlsx")

# U5 · flujo de las próximas 4 semanas
wb, ws = libro("Flujo de las próximas 4 semanas", "Escribe lo que esperas que entre y lo que tienes que pagar cada semana. El saldo se calcula solo.")
for col, w in zip("BCDE", (16, 16, 16, 16)):
    ws.column_dimensions[col].width = w
cab = ["", "Semana 1", "Semana 2", "Semana 3", "Semana 4"]
for k, t in enumerate(cab):
    c = ws.cell(4, 1 + k, t); c.font = Font(bold=True); c.border = Border(bottom=Side(style="medium", color=NEGRO))
ws.cell(5, 1, "Saldo al empezar la semana").font = Font(bold=True)
ws["B5"] = 500000; ws["B5"].fill = PatternFill("solid", fgColor="FFF7E6")
filas_e = [("Ventas de contado (efectivo y transferencias)", [900000, 1000000, 950000, 950000]), ("Cobros de fiados", [0, 300000, 0, 300000]), ("Otras entradas (no préstamos)", [0, 0, 0, 0])]
filas_s = [("Compras de mercancía o insumos", [600000, 600000, 600000, 600000]), ("Arriendo", [0, 800000, 0, 0]), ("Servicios", [0, 0, 150000, 0]),
           ("Tu sueldo", [225000, 225000, 225000, 225000]), ("Cuota del préstamo", [0, 0, 0, 300000]), ("Otras salidas", [0, 0, 0, 0])]
ws.cell(6, 1, "ENTRADAS").font = Font(bold=True, color=ROJO)
f = 7
for t, vs in filas_e:
    ws.cell(f, 1, t)
    for k, v in enumerate(vs):
        c = ws.cell(f, 2 + k, v); c.number_format = PESOS; c.fill = PatternFill("solid", fgColor="FFF7E6")
    f += 1
fe = f; ws.cell(f, 1, "= Total entradas").font = Font(bold=True)
for k in range(4):
    L = "BCDE"[k]; c = ws.cell(f, 2 + k, f"=SUM({L}7:{L}{f-1})"); c.number_format = PESOS; c.font = Font(bold=True)
f += 1; ws.cell(f, 1, "SALIDAS").font = Font(bold=True, color=ROJO); f += 1; s0 = f
for t, vs in filas_s:
    ws.cell(f, 1, t)
    for k, v in enumerate(vs):
        c = ws.cell(f, 2 + k, v); c.number_format = PESOS; c.fill = PatternFill("solid", fgColor="FFF7E6")
    f += 1
fs = f; ws.cell(f, 1, "= Total salidas").font = Font(bold=True)
for k in range(4):
    L = "BCDE"[k]; c = ws.cell(f, 2 + k, f"=SUM({L}{s0}:{L}{f-1})"); c.number_format = PESOS; c.font = Font(bold=True)
f += 2; ws.cell(f, 1, "SALDO AL TERMINAR LA SEMANA")
for k in range(4):
    L = "BCDE"[k]; c = ws.cell(f, 2 + k, f"={L}5+{L}{fe}-{L}{fs}"); c.number_format = PESOS
for col in range(1, 6):
    c = ws.cell(f, col); c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=NEGRO)
for k in range(1, 4):
    L, P = "BCDE"[k], "BCDE"[k - 1]; ws[f"{L}5"] = f"={P}{f}"
for k in range(4):
    ws.cell(5, 2 + k).number_format = PESOS
ws.cell(f + 2, 1, "Saldo al terminar = saldo al empezar + entradas − salidas. Si una semana da negativo, ahí te va a faltar: cobra antes, pide plazo o mueve una compra.").font = Font(size=9, italic=True, color="6B6B72")
ws.cell(f + 3, 1, "Lo que fiaste no va en entradas hasta que te lo paguen. Cifras de ejemplo: cámbialas por las tuyas.").font = Font(size=9, italic=True, color="6B6B72")
wb.save(AQUI / "u5-flujo-4-semanas.xlsx"); print("ok u5-flujo-4-semanas.xlsx")

# U7 · tablero de 3 indicadores (12 meses)
wb, ws = libro("Tablero de 3 indicadores", "Cada mes escribe tus ventas, costo de lo vendido, gastos fijos y plata disponible. Los 3 indicadores se calculan solos.")
cab = ["Mes", "Ventas", "Costo de lo vendido", "Gastos fijos (con tu sueldo)", "Plata disponible", "Margen", "Punto de equilibrio", "Colchón (meses)"]
anchos = [14, 15, 18, 22, 17, 11, 19, 15]
for k, (t, w) in enumerate(zip(cab, anchos)):
    c = ws.cell(4, 1 + k, t); c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical="center")
    c.border = Border(bottom=Side(style="medium", color=NEGRO)); ws.column_dimensions["ABCDEFGH"[k]].width = w
ws.row_dimensions[4].height = 32
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
for k, m in enumerate(meses):
    r = 5 + k; ws.cell(r, 1, m)
    if k == 0:
        for col, v in zip("BCDE", (4500000, 2250000, 1800000, 900000)):
            ws[f"{col}{r}"] = v
    for col in "BCDE":
        ws[f"{col}{r}"].number_format = PESOS; ws[f"{col}{r}"].fill = PatternFill("solid", fgColor="FFF7E6")
    ws[f"F{r}"] = f'=IF(B{r}>0,(B{r}-C{r}-D{r})/B{r},"")'; ws[f"F{r}"].number_format = "0.0%"
    ws[f"G{r}"] = f'=IF(AND(B{r}>0,C{r}<B{r}),D{r}/(1-C{r}/B{r}),"")'; ws[f"G{r}"].number_format = PESOS
    ws[f"H{r}"] = f'=IF(D{r}>0,E{r}/D{r},"")'; ws[f"H{r}"].number_format = "0.0"
    for col in "FGH":
        ws[f"{col}{r}"].font = Font(bold=True); ws[f"{col}{r}"].fill = PatternFill("solid", fgColor=GRIS)
notas = ["Margen = utilidad ÷ ventas × 100 (utilidad = ventas − costo de lo vendido − gastos fijos).",
         "Punto de equilibrio = gastos fijos ÷ (1 − costo de lo vendido ÷ ventas): lo mínimo que tienes que vender para no perder.",
         "Colchón = plata disponible ÷ gastos fijos: cuántos meses aguantas si un mes no vendes.",
         "Enero tiene el ejemplo de Marisol (cifras de ejemplo): margen 10 %, equilibrio $3.600.000, colchón 0,5 meses. Compara cada mes con el anterior."]
for k, n in enumerate(notas):
    ws.cell(19 + k, 1, n).font = Font(size=9, italic=True, color="6B6B72")
ws.freeze_panes = "B5"
wb.save(AQUI / "u7-tablero-3-indicadores.xlsx"); print("ok u7-tablero-3-indicadores.xlsx")
