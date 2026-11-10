"""Arma las descargas de Llévatelo: plantillas Excel (U2, U3) y la hoja del cuaderno para imprimir (U3, HTML → PDF).
Uso: python3 armar_descargas.py && node ../guias-pdf/renderizar_pdf.mjs descargas"""
import pathlib
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = pathlib.Path(__file__).parent
ROJO, NEGRO, GRIS, SUAVE = "C8102E", "141414", "8D8D94", "F6F6F7"
PESOS = '"$"#,##0;[Red]-"$"#,##0'
fino = Side(style="thin", color="D4D4D8")
borde = Border(left=fino, right=fino, top=fino, bottom=fino)


def cabecera(ws, titulo, sub, ancho):
    ws.sheet_view.showGridLines = False
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ancho)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ancho)
    ws["A1"] = titulo
    ws["A1"].font = Font(bold=True, size=16, color="FFFFFF")
    ws["A2"] = sub
    ws["A2"].font = Font(size=10, color="FFFFFF")
    for r in (1, 2):
        for c in range(1, ancho + 1):
            ws.cell(r, c).fill = PatternFill("solid", fgColor=ROJO)
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 22


def encabezados(ws, fila, nombres):
    for c, n in enumerate(nombres, 1):
        x = ws.cell(fila, c, n)
        x.font = Font(bold=True, color="FFFFFF")
        x.fill = PatternFill("solid", fgColor=NEGRO)
        x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        x.border = borde
    ws.row_dimensions[fila].height = 30


def entrada(c):
    c.fill = PatternFill("solid", fgColor="FFF7D6")
    c.border = borde


def calculo(c, negrita=False):
    c.fill = PatternFill("solid", fgColor=SUAVE)
    c.border = borde
    c.font = Font(bold=negrita)


# ---------- U2: Calcula tu sueldo ----------
wb = Workbook()
for nombre, ejemplo in (("Tu sueldo", False), ("Ejemplo Luz Dary", True)):
    ws = wb.active if not ejemplo else wb.create_sheet(nombre)
    ws.title = nombre
    cabecera(ws, "Calcula tu sueldo", "Unidad 2 · La plata del negocio no es la de la casa · Llena solo las celdas amarillas", 4)
    ws.column_dimensions["A"].width = 30
    for col in "BCD":
        ws.column_dimensions[col].width = 20
    encabezados(ws, 4, ["Mes", "Ventas del mes", "Pagos del negocio\n(mercancía, local, transporte)", "Ganancia del mes"])
    for i in range(3):
        f = 5 + i
        ws.cell(f, 1, f"Mes {i + 1}" if not ejemplo else ["Mes 1", "Mes 2", "Mes 3"][i])
        entrada(ws.cell(f, 1))
        for c in (2, 3):
            entrada(ws.cell(f, c))
            ws.cell(f, c).number_format = PESOS
        g = ws.cell(f, 4)
        if ejemplo:
            g.value = [2400000, 1800000, 2100000][i]
            entrada(g)
        else:
            g.value = f'=IF(AND(B{f}="",C{f}=""),"",B{f}-C{f})'
            calculo(g)
        g.number_format = PESOS
    filas = [("Promedio de 3 meses", "=IFERROR(AVERAGE(D5:D7),\"\")", True),
             ("Colchón (regla práctica del curso)", 0.2, False),
             ("Tu sueldo al mes", "=IFERROR(B9*(1-B10),\"\")", True),
             ("Por quincena", "=IFERROR(B11/2,\"\")", True)]
    for k, (et, v, neg) in enumerate(filas):
        f = 9 + k
        ws.cell(f, 1, et).font = Font(bold=True)
        c = ws.cell(f, 2, v)
        if k == 1:
            entrada(c)
            c.number_format = "0%"
        else:
            calculo(c, neg)
            c.number_format = PESOS
    ws["B11"].fill = PatternFill("solid", fgColor=ROJO)
    ws["B11"].font = Font(bold=True, color="FFFFFF", size=12)
    notas = ["Cómo se usa:",
             "1. Escribe las ventas y lo que pagaste para el negocio en cada uno de los últimos 3 meses.",
             "2. La hoja calcula la ganancia de cada mes, el promedio y tu sueldo con el colchón.",
             "3. El colchón del 20 % es una regla práctica del curso, no una norma: tu contador puede ajustarlo.",
             "4. Escoge tus fechas fijas de pago (por ejemplo, el 15 y el 30) y págate por transferencia.",
             "Si el sueldo no alcanza para la casa, es una señal: vender más, revisar precios o bajar costos."]
    if ejemplo:
        notas[1] = "En este ejemplo solo se conoce la ganancia de cada mes de Luz Dary (Unidad 2)."
    for k, t in enumerate(notas):
        c = ws.cell(14 + k, 1, t)
        c.font = Font(bold=(k == 0), color="45454C" if k else NEGRO, size=10)
        ws.merge_cells(start_row=14 + k, start_column=1, end_row=14 + k, end_column=4)
wb.save(AQUI / "u2-calcula-tu-sueldo.xlsx")

# ---------- U3: Registro diario ----------
wb = Workbook()
for nombre, ejemplo in (("Registro", False), ("Ejemplo", True)):
    ws = wb.active if not ejemplo else wb.create_sheet(nombre)
    ws.title = nombre
    cabecera(ws, "Registro diario del negocio", "Unidad 3 · 5 minutos al cerrar · Saldo de hoy = saldo de ayer + entró − salió", 5)
    for col, w in zip("ABCDE", (14, 36, 16, 16, 18)):
        ws.column_dimensions[col].width = w
    encabezados(ws, 4, ["Fecha", "Qué fue", "Entró", "Salió", "Saldo"])
    ws.cell(5, 2, "Saldo con el que empiezas")
    ws.cell(5, 2).font = Font(italic=True)
    for c in (1, 2, 3, 4):
        entrada(ws.cell(5, c))
    s = ws.cell(5, 5)
    entrada(s)
    s.number_format = PESOS
    datos = []
    if ejemplo:
        s.value = 400000
        ws.cell(5, 1, "Lunes")
        datos = [("Lunes", "Ventas del día", 350000, None), ("Lunes", "Pago al proveedor", None, 120000)]
    total = 40 if not ejemplo else 2
    for i in range(total):
        f = 6 + i
        for c in (1, 2, 3, 4):
            entrada(ws.cell(f, c))
        ws.cell(f, 1).number_format = "dd/mm/yyyy"
        for c in (3, 4):
            ws.cell(f, c).number_format = PESOS
        if i < len(datos):
            for c, v in zip((1, 2, 3, 4), datos[i]):
                if v is not None:
                    ws.cell(f, c, v)
        e = ws.cell(f, 5, f'=IF(AND(C{f}="",D{f}=""),"",LOOKUP(2,1/(E$5:E{f - 1}<>""),E$5:E{f - 1})+N(C{f})-N(D{f}))')
        calculo(e, True)
        e.number_format = PESOS
    if ejemplo:
        f = 6 + total + 1
        ws.cell(f, 2, "Saldo al cerrar (Luz Dary): $630.000").font = Font(bold=True, color=ROJO)
    ws.freeze_panes = "A5"
    fin = 6 + total + (3 if ejemplo else 1)
    for k, t in enumerate(["Si el saldo no cuadra con la cuenta y el cajón, algo se fue sin anotar.",
                           "No olvides anotar tu sueldo (sale de la cuenta del negocio) ni las ventas en efectivo."]):
        ws.cell(fin + k, 1, t).font = Font(size=10, color="45454C")
        ws.merge_cells(start_row=fin + k, start_column=1, end_row=fin + k, end_column=5)
wb.save(AQUI / "u3-registro-diario.xlsx")

# ---------- U3: hoja del cuaderno para imprimir ----------
filas = "".join("<tr><td></td><td></td><td></td><td></td><td></td></tr>" for _ in range(22))
html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Registro diario</title><style>
@page{{size:A4;margin:12mm}}*{{box-sizing:border-box;margin:0}}
body{{font-family:Inter,'DejaVu Sans',sans-serif;color:#1a1a1a;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.cab{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2mm solid #c8102e;padding-bottom:3mm}}
h1{{font-size:20pt;font-weight:800}}.cab small{{font-size:8pt;color:#6b6b72;text-transform:uppercase;letter-spacing:.08em;font-weight:700}}
.f{{margin:4mm 0;background:#141414;color:#fff;border-radius:2mm;padding:3mm 4mm;font-size:11pt}}.f b{{color:#ff8a9c}}
.datos{{display:flex;gap:6mm;font-size:10pt;margin-bottom:3mm}}.datos span{{flex:1;border-bottom:.3mm solid #8d8d94;padding-bottom:1mm}}
table{{width:100%;border-collapse:collapse;font-size:10pt}}th{{background:#141414;color:#fff;padding:2.2mm;font-weight:700}}
td{{border:.3mm solid #b8b8be;height:8.6mm}}th:nth-child(1){{width:16%}}th:nth-child(2){{width:36%}}
tr.ini td{{background:#f6f6f7}}.pie{{margin-top:3mm;font-size:8pt;color:#6b6b72;display:flex;justify-content:space-between}}
</style></head><body>
<div class="cab"><h1>Registro diario del negocio</h1><small>Unidad 3 · La plata del negocio no es la de la casa</small></div>
<div class="f"><b>Saldo de hoy</b> = saldo de ayer + lo que entró − lo que salió</div>
<div class="datos"><span>Negocio:</span><span>Mes:</span><span>Cuenta del negocio:</span></div>
<table><tr><th>Fecha</th><th>Qué fue</th><th>Entró</th><th>Salió</th><th>Saldo</th></tr>
<tr class="ini"><td></td><td><i>Saldo con el que empiezas</i></td><td></td><td></td><td></td></tr>{filas}</table>
<div class="pie"><span>Si el saldo no cuadra con la cuenta y el cajón, algo se fue sin anotar. Anota también tu sueldo.</span><span>Aula Virtual Empresarial Soacha</span></div>
</body></html>"""
(AQUI / "u3-hoja-registro.html").write_text(html, encoding="utf-8")
print("ok")


# ================= Unidades 4 a 7 (tramo del Pase) =================
CATS = ["Venta de contado", "Pago de fiado", "Mercancía o insumos", "Gastos fijos", "Gastos variables", "Tu sueldo", "Deudas e inversiones"]
MEDIOS = ["Efectivo", "Transferencia", "Billetera"]


def lista(ws, rango, opciones):
    dv = DataValidation(type="list", formula1='"' + ",".join(opciones) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rango)


def notas(ws, fila, textos, ancho):
    for k, t in enumerate(textos):
        c = ws.cell(fila + k, 1, t)
        c.font = Font(bold=(k == 0), color="45454C" if k else NEGRO, size=10)
        ws.merge_cells(start_row=fila + k, start_column=1, end_row=fila + k, end_column=ancho)


def libro(ws, titulo, sub, filas_ej, n=60):
    """Libro de 7 columnas con saldo calculado y totales por categoría a la derecha."""
    cabecera(ws, titulo, sub, 10)
    for col, w in zip("ABCDEFGHIJ", (12, 30, 22, 14, 15, 15, 16, 3, 24, 16)):
        ws.column_dimensions[col].width = w
    encabezados(ws, 4, ["Fecha", "Qué fue", "Categoría", "Medio", "Entró", "Salió", "Saldo"])
    ws.cell(5, 2, "Saldo con el que empiezas").font = Font(italic=True)
    for c in range(1, 8):
        entrada(ws.cell(5, c))
    ws.cell(5, 7).number_format = PESOS
    if filas_ej:
        ws.cell(5, 7, filas_ej[0])
    for i in range(n):
        f = 6 + i
        for c in range(1, 7):
            entrada(ws.cell(f, c))
        ws.cell(f, 1).number_format = "dd/mm/yyyy"
        for c in (5, 6):
            ws.cell(f, c).number_format = PESOS
        if filas_ej and i < len(filas_ej) - 1:
            for c, v in zip(range(1, 7), filas_ej[i + 1]):
                if v is not None:
                    ws.cell(f, c, v)
        e = ws.cell(f, 7, f'=IF(AND(E{f}="",F{f}=""),"",LOOKUP(2,1/(G$5:G{f - 1}<>""),G$5:G{f - 1})+N(E{f})-N(F{f}))')
        calculo(e, True)
        e.number_format = PESOS
    lista(ws, f"C6:C{5 + n}", CATS)
    lista(ws, f"D6:D{5 + n}", MEDIOS)
    encabezados_tot = ws.cell(4, 9, "Totales por categoría")
    encabezados_tot.font = Font(bold=True, color="FFFFFF")
    encabezados_tot.fill = PatternFill("solid", fgColor=ROJO)
    ws.cell(4, 10).fill = PatternFill("solid", fgColor=ROJO)
    for k, cat in enumerate(CATS):
        f = 5 + k
        ws.cell(f, 9, cat).border = borde
        col = "E" if cat in ("Venta de contado", "Pago de fiado") else "F"
        t = ws.cell(f, 10, f'=SUMIF($C$6:$C${5 + n},I{f},${col}$6:${col}${5 + n})')
        calculo(t, True)
        t.number_format = PESOS
    ws.freeze_panes = "A5"
    return 6 + n + 1


# ---------- U4: registro con categorías + lista de fiados ----------
wb = Workbook()
for nombre, ej in (("Registro", False), ("Ejemplo Luz Dary", True)):
    ws = wb.active if not ej else wb.create_sheet(nombre)
    ws.title = nombre
    filas = [1200000, ("Lunes", "Ventas del día", "Venta de contado", "Efectivo", 310000, None),
             ("Lunes", "Útiles al proveedor", "Mercancía o insumos", "Transferencia", None, 420000),
             ("Martes", "Bolsas y empaques", "Gastos variables", "Efectivo", None, 45000),
             ("Miércoles", "Arriendo del local", "Gastos fijos", "Transferencia", None, 700000),
             ("Jueves", "Don Jairo pagó su fiado", "Pago de fiado", "Billetera", 40000, None)] if ej else None
    fin = libro(ws, "Registro con categorías", "Unidad 4 · Cada salida con su categoría · Llena solo las celdas amarillas", filas, len(filas) - 1 if ej else 60)
    notas(ws, fin, ["Cómo se usa:", "1. Escoge la categoría y el medio de la lista de cada fila.",
                    "2. El fiado NO se anota aquí cuando lo das: va en la hoja «Fiados». Entra aquí como «Pago de fiado» cuando te pagan.",
                    "3. Toma foto del soporte de cada salida y guárdala en la carpeta del mes."], 7)
ws = wb.create_sheet("Fiados")
cabecera(ws, "Lista de fiados", "Unidad 4 · Te deben = fiados de antes + fiados nuevos − lo que te pagaron", 7)
for col, w in zip("ABCDEFG", (12, 24, 30, 15, 15, 14, 16)):
    ws.column_dimensions[col].width = w
encabezados(ws, 4, ["Fecha", "Quién", "Qué llevó", "Debe", "Pagó", "Paga el", "Le falta"])
for i in range(40):
    f = 5 + i
    for c in range(1, 7):
        entrada(ws.cell(f, c))
    for c in (4, 5):
        ws.cell(f, c).number_format = PESOS
    t = ws.cell(f, 7, f'=IF(D{f}="","",D{f}-N(E{f}))')
    calculo(t)
    t.number_format = PESOS
ws.cell(46, 6, "Te deben").font = Font(bold=True)
t = ws.cell(46, 7, "=SUM(G5:G44)")
t.fill = PatternFill("solid", fgColor=ROJO)
t.font = Font(bold=True, color="FFFFFF")
t.number_format = PESOS
ws.freeze_panes = "A5"
wb.save(AQUI / "u4-registro-categorias-fiados.xlsx")

# ---------- U5: libro del mes ----------
wb = Workbook()
ws = wb.active
ws.title = "Libro del mes"
fin = libro(ws, "Libro del mes", "Unidad 5 · Una línea por movimiento · Los totales por categoría salen solos", None, 120)
notas(ws, fin, ["Cómo se usa:", "1. Una hoja por mes: copia esta hoja el día 1.",
                "2. Las ventas del día pueden ir en una línea por medio de pago.",
                "3. El último día, los totales de la derecha son lo que necesitas para la Unidad 6 y para tu contador."], 7)
wb.save(AQUI / "u5-libro-del-mes.xlsx")

# ---------- U6: utilidad real e inventario ----------
wb = Workbook()
for nombre, ej in (("Tu utilidad", False), ("Ejemplo Marleny", True)):
    ws = wb.active if not ej else wb.create_sheet(nombre)
    ws.title = nombre
    cabecera(ws, "Tu utilidad real del mes", "Unidad 6 · Llena las celdas amarillas con los totales de tu libro", 3)
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 44
    vals = [5000000, 600000, 2400000, 1200000, 900000, 300000, 1200000] if ej else [None] * 7
    filas = [("Ventas del mes", "Del libro: ventas de contado + fiado vendido"),
             ("Inventario al empezar el mes", "A precio de compra"),
             ("Compras de mercancía o insumos", "Del libro"),
             ("Inventario al terminar el mes", "Cuéntalo el último día"),
             ("Gastos fijos", "Del libro"),
             ("Gastos variables", "Del libro"),
             ("Tu sueldo", "Del libro")]
    for k, ((et, ay), v) in enumerate(zip(filas, vals)):
        f = 4 + k
        ws.cell(f, 1, et).font = Font(bold=True)
        c = ws.cell(f, 2, v)
        entrada(c)
        c.number_format = PESOS
        ws.cell(f, 3, ay).font = Font(size=9, color=GRIS)
    res = [("Costo de lo vendido", "=IF(B5&B6&B7=\"\",\"\",N(B5)+N(B6)-N(B7))", "Inventario al empezar + compras − inventario al terminar"),
           ("Utilidad real", "=IF(B4=\"\",\"\",B4-N(B12)-N(B8)-N(B9)-N(B10))", "Ventas − costo de lo vendido − fijos − variables − sueldo"),
           ("Margen", "=IFERROR(B13/B4,\"\")", "Utilidad real ÷ ventas")]
    for k, (et, fo, ay) in enumerate(res):
        f = 12 + k
        ws.cell(f, 1, et).font = Font(bold=True)
        c = ws.cell(f, 2, fo)
        calculo(c, True)
        c.number_format = "0.0%" if et == "Margen" else PESOS
        ws.cell(f, 3, ay).font = Font(size=9, color=GRIS)
    ws["B13"].fill = PatternFill("solid", fgColor=ROJO)
    ws["B13"].font = Font(bold=True, color="FFFFFF", size=12)
    notas(ws, 17, ["Recuerda:", "Las cuotas de un crédito y las máquinas no se restan aquí.",
                   "Utilidad no es plata en la cuenta: el fiado y el inventario no están en la caja."], 3)
wb.save(AQUI / "u6-utilidad-real.xlsx")

# ---------- U7: cierre del mes ----------
wb = Workbook()
ws = wb.active
ws.title = "Cierre"
cabecera(ws, "Cierre del mes en 20 minutos", "Unidad 7 · Cuadra · suma · cuenta · calcula · decide", 4)
for col, w in zip("ABCD", (40, 18, 18, 18)):
    ws.column_dimensions[col].width = w
encabezados(ws, 4, ["Paso 1 · Cuadra", "Valor", "", ""])
cuadre = [("Saldo según el libro", None), ("Saldo de la cuenta o billetera del negocio", None), ("Efectivo en el cajón", None)]
for k, (et, _) in enumerate(cuadre):
    ws.cell(5 + k, 1, et)
    entrada(ws.cell(5 + k, 2))
    ws.cell(5 + k, 2).number_format = PESOS
ws.cell(8, 1, "Diferencia (positiva: falta · negativa: sobra)").font = Font(bold=True)
c = ws.cell(8, 2, '=IF(B5="","",B5-(N(B6)+N(B7)))')
calculo(c, True)
c.number_format = PESOS
encabezados(ws, 10, ["Hoja de cierre", "Mes anterior", "Este mes", "Cambio"])
hoja = ["Ventas", "Costo de lo vendido", "Gastos fijos + variables", "Tu sueldo", "Utilidad real", "Margen", "Te deben (fiados)", "Inventario"]
for k, et in enumerate(hoja):
    f = 11 + k
    ws.cell(f, 1, et).font = Font(bold=et in ("Utilidad real", "Margen"))
    for col in (2, 3):
        x = ws.cell(f, col)
        entrada(x)
        x.number_format = "0.0%" if et == "Margen" else PESOS
    if et == "Utilidad real":
        for col, L in ((2, "B"), (3, "C")):
            x = ws.cell(f, col, f'=IF({L}11="","",{L}11-N({L}12)-N({L}13)-N({L}14))')
            calculo(x, True)
            x.number_format = PESOS
    if et == "Margen":
        for col, L in ((2, "B"), (3, "C")):
            x = ws.cell(f, col, f'=IFERROR({L}15/{L}11,"")')
            calculo(x, True)
            x.number_format = "0.0%"
    d = ws.cell(f, 4, f'=IF(OR(B{f}="",C{f}=""),"",C{f}-B{f})')
    calculo(d)
    d.number_format = "0.0%" if et == "Margen" else PESOS
ws.cell(20, 1, "Paso 5 · Mi acción para el mes que viene").font = Font(bold=True, color=ROJO)
ws.merge_cells("A21:D22")
entrada(ws["A21"])
ws["A21"].alignment = Alignment(wrap_text=True, vertical="top")
notas(ws, 24, ["Una sola acción, concreta y medible:", "Ejemplo: «Cobrar $100.000 de fiados antes del día 15»."], 4)
wb.save(AQUI / "u7-cierre-del-mes.xlsx")


def hoja_pdf(nombre, titulo, unidad, formula, cols, anchos, n, pie, extra=""):
    th = "".join(f"<th style='width:{a}%'>{c}</th>" for c, a in zip(cols, anchos))
    filas = "".join("<tr>" + "<td></td>" * len(cols) + "</tr>" for _ in range(n))
    h = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title><style>
@page{{size:A4;margin:12mm}}*{{box-sizing:border-box;margin:0}}
body{{font-family:Inter,'DejaVu Sans',sans-serif;color:#1a1a1a;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.cab{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2mm solid #c8102e;padding-bottom:3mm}}
h1{{font-size:20pt;font-weight:800}}.cab small{{font-size:8pt;color:#6b6b72;text-transform:uppercase;letter-spacing:.08em;font-weight:700}}
.f{{margin:4mm 0;background:#141414;color:#fff;border-radius:2mm;padding:3mm 4mm;font-size:11pt}}.f b{{color:#ff8a9c}}
.datos{{display:flex;gap:6mm;font-size:10pt;margin-bottom:3mm}}.datos span{{flex:1;border-bottom:.3mm solid #8d8d94;padding-bottom:1mm}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt}}th{{background:#141414;color:#fff;padding:2mm;font-weight:700}}
td{{border:.3mm solid #b8b8be;height:8.2mm;padding:0 2mm}}.pie{{margin-top:3mm;font-size:8pt;color:#6b6b72;display:flex;justify-content:space-between}}
.k td:first-child{{font-weight:700}}
</style></head><body>
<div class="cab"><h1>{titulo}</h1><small>{unidad} · La plata del negocio no es la de la casa</small></div>
<div class="f">{formula}</div>
<div class="datos"><span>Negocio:</span><span>Mes:</span></div>
{extra}<table><tr>{th}</tr>{filas}</table>
<div class="pie"><span>{pie}</span><span>Aula Virtual Empresarial Soacha</span></div>
</body></html>"""
    (AQUI / f"{nombre}.html").write_text(h, encoding="utf-8")


hoja_pdf("u5-hoja-libro", "Libro del mes", "Unidad 5", "<b>Saldo</b> = saldo de la línea anterior + entró − salió",
         ["Fecha", "Qué fue", "Categoría", "Medio", "Entró", "Salió", "Saldo"], [10, 26, 16, 12, 12, 12, 12], 24,
         "Categorías: venta, mercancía, fijos, variables, tu sueldo, deudas. El último día, suma cada categoría.")
cierre_tabla = "".join(f"<tr><td>{x}</td><td></td><td></td></tr>" for x in
                       ["Saldo según el libro", "Cuenta del negocio", "Efectivo en el cajón", "Diferencia (falta / sobra)"])
hoja_tabla = "".join(f"<tr><td>{x}</td><td></td><td></td></tr>" for x in
                     ["Ventas", "Costo de lo vendido", "Gastos fijos + variables", "Tu sueldo", "Utilidad real", "Margen", "Te deben (fiados)", "Inventario"])
(AQUI / "u7-hoja-cierre.html").write_text(f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Hoja de cierre del mes</title><style>
@page{{size:A4;margin:12mm}}*{{box-sizing:border-box;margin:0}}
body{{font-family:Inter,'DejaVu Sans',sans-serif;color:#1a1a1a;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.cab{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2mm solid #c8102e;padding-bottom:3mm}}
h1{{font-size:20pt;font-weight:800}}.cab small{{font-size:8pt;color:#6b6b72;text-transform:uppercase;letter-spacing:.08em;font-weight:700}}
h2{{font-size:12pt;margin:5mm 0 2mm;color:#9e0c24}}
.pasos{{display:flex;gap:2mm;margin-top:4mm}}.pasos div{{flex:1;background:#141414;color:#fff;border-radius:2mm;padding:2.5mm;font-size:9pt}}.pasos b{{display:block;color:#ff8a9c;font-size:10pt}}
.datos{{display:flex;gap:6mm;font-size:10pt;margin:4mm 0 0}}.datos span{{flex:1;border-bottom:.3mm solid #8d8d94;padding-bottom:1mm}}
table{{width:100%;border-collapse:collapse;font-size:10pt}}th{{background:#141414;color:#fff;padding:2mm}}
td{{border:.3mm solid #b8b8be;height:8.6mm;padding:0 2mm}}td:first-child{{width:46%;font-weight:600}}
.accion{{border:.6mm solid #c8102e;border-radius:2mm;height:26mm;padding:2mm;font-size:9pt;color:#6b6b72}}
.pie{{margin-top:3mm;font-size:8pt;color:#6b6b72;display:flex;justify-content:space-between}}
</style></head><body>
<div class="cab"><h1>Hoja de cierre del mes</h1><small>Unidad 7 · La plata del negocio no es la de la casa</small></div>
<div class="pasos"><div><b>1. Cuadra</b>5 min</div><div><b>2. Suma</b>5 min</div><div><b>3. Cuenta</b>5 min</div><div><b>4. Calcula</b>3 min</div><div><b>5. Decide</b>2 min</div></div>
<div class="datos"><span>Negocio:</span><span>Mes:</span></div>
<h2>1. Cuadra · Diferencia = libro − (cuenta + cajón)</h2>
<table><tr><th></th><th>Valor</th><th>Nota</th></tr>{cierre_tabla}</table>
<h2>2 a 4. Tus números del mes</h2>
<table><tr><th></th><th>Mes anterior</th><th>Este mes</th></tr>{hoja_tabla}</table>
<h2>5. Mi acción para el mes que viene</h2>
<div class="accion">Una sola, concreta y medible. Ejemplo: «Cobrar $100.000 de fiados antes del día 15».</div>
<div class="pie"><span>Utilidad real = ventas − costo de lo vendido − gastos − tu sueldo · Margen = utilidad ÷ ventas</span><span>Aula Virtual Empresarial Soacha</span></div>
</body></html>""", encoding="utf-8")
print("ok pase")
