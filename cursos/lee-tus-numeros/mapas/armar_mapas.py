"""Arma los mapas mentales del curso (HTML) a partir del contenido de abajo.
Uso: python3 armar_mapas.py  -> genera mapas/<id>.html; luego renderizar.mjs los pasa a PNG."""
import html, pathlib

AQUI = pathlib.Path(__file__).parent
CURSO = "Lee tus números"

MAPAS = {
 "mapa-curso": ("Mapa del curso", CURSO, [
   ("Unidad 1 · Ingresos, costos y gastos", [
     "Ingreso: lo que vendes (un préstamo no es ingreso)",
     "Costo: lo que te cuesta lo que vendes",
     "Gasto: lo que pagas por estar abierto, también tu sueldo"]),
   ("Unidad 2 · El mes en números", [
     "Junta cuaderno, Nequi o banco, datáfono y fiados",
     "Cada venta se cuenta una sola vez",
     "Fuera traslados, préstamos y lo de la casa"]),
   ("Unidad 3 · Tu estado de resultados del mes", [
     "Ventas − costo de lo vendido = <b>utilidad bruta</b>",
     "Utilidad bruta − gastos = <b>utilidad del mes</b>",
     "<b>Margen</b> = utilidad ÷ ventas × 100"]),
 ]),
 "u1-mapa": ("Unidad 1", "¿Ingreso, costo o gasto?", [
   ("Ingreso", [
     "Lo que entra porque <b>vendiste</b>",
     "No son ingresos: préstamos, plata de tu bolsillo o de la familia"]),
   ("Costo", [
     "Lo que necesitas para <b>hacer o comprar</b> lo que vendes",
     "Insumos, mercancía, empaques",
     "Sube y baja con las ventas"]),
   ("Gasto", [
     "Lo que pagas por <b>tener el negocio abierto</b>",
     "Arriendo, servicios, internet, sueldos",
     "Tu sueldo también es un gasto"]),
   ("No va", [
     "Mercado, colegio y cuentas de la casa",
     "Si sacas para la casa, sale de tu sueldo"]),
   ("La pregunta", [
     "¿Lo vendí? ¿Lo necesito para vender? ¿Lo pago aunque no venda? ¿Es de la casa?"]),
 ]),
 "u2-mapa": ("Unidad 2", "¿Cómo juntas el mes sin contar nada dos veces?", [
   ("Escoge el mes", [
     "Uno que ya terminó, del 1 al último día"]),
   ("Tus fuentes", [
     "Cuaderno o libreta",
     "Historial de Nequi, Daviplata o el banco",
     "Datáfono, facturas, recibos y lista de fiados"]),
   ("Las ventas", [
     "Efectivo + transferencias + fiado del mes",
     "La venta cuenta el mes en que la haces"]),
   ("No cuentes dos veces", [
     "Plata de la caja al Nequi: ya estaba",
     "Préstamos y aportes tuyos: no son ventas",
     "Fiado que te pagan después: ya estaba contado"]),
   ("Costos y gastos", [
     "Con facturas y recibos del mes",
     "Pagos de dos meses: a cada mes lo suyo"]),
 ]),
 "u3-mapa": ("Unidad 3", "¿Cuánto ganó de verdad tu negocio el mes pasado?", [
   ("Estado de resultados", [
     "También se llama <b>P y G</b>",
     "Ventas, costos y gastos de un mes o un año"]),
   ("Las líneas", [
     "<b>Ventas</b> del mes",
     "− Costo de lo vendido = <b>utilidad bruta</b>",
     "− Gastos (con tu sueldo) = <b>utilidad del mes</b>"]),
   ("El margen", [
     "Utilidad ÷ ventas × 100",
     "Cuántos pesos te quedan de cada 100",
     "Compáralo mes a mes"]),
   ("Para qué sirve", [
     "Pedir un crédito con tus números",
     "Revisar un precio que no te deja nada",
     "Vender más no siempre es ganar más"]),
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
