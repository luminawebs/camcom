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
