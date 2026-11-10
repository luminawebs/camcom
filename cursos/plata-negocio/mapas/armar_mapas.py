"""Arma los mapas mentales del curso (HTML) a partir del contenido de abajo.
Uso: python3 armar_mapas.py  -> genera mapas/<id>.html; luego renderizar.mjs los pasa a PNG."""
import html, pathlib

AQUI = pathlib.Path(__file__).parent
CURSO = "La plata del negocio no es la de la casa"

MAPAS = {
 "mapa-curso": ("Mapa del curso", CURSO, [
   ("Unidad 1 · Por dónde se va la plata", [
     "Las 4 fugas: el cajón para la casa, los pagos cruzados, lo que consumes y el celular personal",
     "Una venta no es una ganancia: una parte es para volver a surtir",
     "<b>Se fue</b> = caja inicial + ventas − pagos del negocio − caja final"]),
   ("Unidad 2 · Págate un sueldo", [
     "Sueldo fijo, en fecha fija, no «lo que necesite»",
     "Ganancia del mes = ventas − lo que pagaste para el negocio",
     "<b>Sueldo</b> = promedio de 3 meses × 0,80 (colchón del 20&nbsp;%)"]),
   ("Unidad 3 · Una cuenta y un registro", [
     "Una cuenta o billetera solo para el negocio",
     "3 reglas: todo entra ahí, todo gasto sale de ahí, a la casa solo tu sueldo",
     "<b>Saldo de hoy</b> = saldo de ayer + entró − salió"]),
   ("Unidad 4 · Ventas y gastos por categoría (Pase)", [
     "5 categorías: mercancía, fijos, variables, tu sueldo, deudas e inversiones",
     "El fiado es venta, pero no es plata: va en su lista",
     "<b>Te deben</b> = fiados de antes + nuevos − lo que pagaron"]),
   ("Unidad 5 · Tu libro del mes (Pase)", [
     "7 columnas: fecha, qué fue, categoría, medio, entró, salió, saldo",
     "<b>Total de una categoría</b> = suma de sus líneas del mes"]),
   ("Unidad 6 · Tu utilidad real (Pase)", [
     "<b>Costo de lo vendido</b> = inventario inicial + compras − inventario final",
     "<b>Utilidad real</b> = ventas − costo de lo vendido − gastos − tu sueldo"]),
   ("Unidad 7 · El cierre del mes (Pase)", [
     "Cuadra, suma, cuenta, calcula y decide: 20 minutos",
     "<b>Diferencia</b> = saldo del libro − (cuenta + cajón)"]),
 ]),
 "u1-mapa": ("Unidad 1", "¿Por dónde se va la plata del negocio?", [
   ("Las 4 fugas", [
     "<b>1.</b> El cajón para la casa: mercado, arriendo, onces sin anotar",
     "<b>2.</b> Los pagos cruzados: la luz de la casa con plata del negocio",
     "<b>3.</b> Lo que consumes: el cuaderno, la gaseosa, el regalo",
     "<b>4.</b> El celular personal: los clientes pagan al Nequi de la familia"]),
   ("Una venta no es una ganancia", [
     "Cuaderno vendido en $5.000 que costó $3.500",
     "Ganancia: <b>$1.500</b>. Los $3.500 son para volver a surtir"]),
   ("Mide la fuga de la semana", [
     "<b>Se fue</b> = caja inicial + ventas − pagos del negocio − caja final",
     "$200.000 + $1.800.000 − $1.100.000 = $900.000",
     "En caja hay $350.000: se fueron <b>$550.000</b> sin anotar"]),
   ("Errores comunes", [
     "Olvidar la caja del lunes",
     "No restar los pagos del negocio",
     "No restarle lo que de verdad hay al final"]),
   ("Dato", [
     "El 68,2&nbsp;% de los micronegocios no lleva ningún registro contable (DANE, EMICRON 2024)"]),
 ]),
 "u2-mapa": ("Unidad 2", "¿Cuánto te puedes pagar sin dejar sin plata al negocio?", [
   ("Tú también trabajas en tu negocio", [
     "Sueldo fijo, en fecha fija, como a cualquier trabajadora"]),
   ("Paso 1 · Ganancia del mes", [
     "Ventas − todo lo que pagaste para el negocio (mercancía, arriendo y servicios del local, transporte)"]),
   ("Paso 2 · Promedio de 3 meses", [
     "Un solo mes engaña",
     "($2.400.000 + $1.800.000 + $2.100.000) ÷ 3 = <b>$2.100.000</b>"]),
   ("Paso 3 · Deja un colchón", [
     "20&nbsp;%: regla práctica del curso, el contador puede ajustarla",
     "$2.100.000 × 0,80 = <b>$1.680.000</b> al mes",
     "Por quincenas: $840.000 el 15 y $840.000 el 30"]),
   ("¿Y si no alcanza para la casa?", [
     "Es una señal, no una culpa",
     "Vender más, revisar precios o bajar costos"]),
   ("Errores comunes", [
     "Usar el mejor mes en vez del promedio",
     "Olvidar el colchón",
     "Sumar los tres meses y no dividir entre 3"]),
 ]),
 "u3-mapa": ("Unidad 3", "¿Cómo separar la plata del negocio sin complicarte?", [
   ("Una cuenta solo para el negocio", [
     "Cuenta de ahorros o billetera digital distinta a la personal",
     "No importa en qué banco"]),
   ("Las 3 reglas de la plata", [
     "<b>1.</b> Todo lo que vendes entra ahí, también el efectivo",
     "<b>2.</b> Todo gasto del negocio sale de ahí",
     "<b>3.</b> A la casa solo va tu sueldo, en tu fecha fija"]),
   ("El registro: 5 minutos al día", [
     "Fecha · qué fue · entró · salió · saldo",
     "<b>Saldo de hoy</b> = saldo de ayer + entró − salió",
     "$400.000 + $350.000 − $120.000 = <b>$630.000</b>"]),
   ("Si no cuadra", [
     "Si el cuaderno no cuadra con la cuenta y el cajón, algo se fue sin anotar",
     "No olvides anotar tu sueldo ni las ventas en efectivo"]),
   ("Tu registro abre puertas", [
     "Muestra cuánto vendes para pedir crédito en un banco",
     "En 2024, el 22,9&nbsp;% de los micronegocios que pidieron crédito acudió al gota a gota (DANE, EMICRON 2024)"]),
 ]),
 "u4-mapa": ("Unidad 4", "¿Cómo anoto todo sin enredarme?", [
   ("Cada salida tiene su cajón", [
     "<b>1.</b> Mercancía o insumos: lo que compras para vender o producir",
     "<b>2.</b> Gastos fijos: arriendo y servicios del local, internet, ayudante",
     "<b>3.</b> Gastos variables: bolsas, empaques, transporte, comisiones",
     "<b>4.</b> Tu sueldo, en tu fecha fija",
     "<b>5.</b> Deudas e inversiones: cuotas, vitrina, máquina"]),
   ("Las ventas, en dos", [
     "De contado: efectivo o transferencia, la plata ya está",
     "Fiadas: es venta, pero la plata todavía no está"]),
   ("La lista de fiados", [
     "Fecha · quién · qué llevó · cuánto debe · cuándo paga",
     "<b>Te deben</b> = fiados de antes + nuevos − lo que pagaron",
     "$120.000 + $85.000 − $40.000 = <b>$165.000</b>"]),
   ("El soporte en 1 minuto", [
     "Foto a la factura o al comprobante el mismo día",
     "Una carpeta del celular por mes: «Negocio · noviembre»"]),
 ]),
 "u5-mapa": ("Unidad 5", "¿Cómo junto todo el mes en un solo lugar?", [
   ("Un libro, siete columnas", [
     "Fecha · qué fue · categoría · medio · entró · salió · saldo",
     "Cuaderno, Excel o app: lo importante es que sea uno solo"]),
   ("Una línea por movimiento", [
     "Las ventas del día: una línea por medio de pago",
     "<b>Saldo</b> = saldo de la línea anterior + entró − salió"]),
   ("Los totales del mes", [
     "<b>Total de una categoría</b> = suma de sus líneas del mes",
     "Es la base para la utilidad (U6) y el cierre (U7)"]),
   ("¿Y la ley?", [
     "Comerciante inscrito: contabilidad (Código de Comercio, art. 19)",
     "No responsable de IVA sin contabilidad: libro fiscal (ET, art. 616)",
     "Tu contador te dice cuál aplica"]),
 ]),
 "u6-mapa": ("Unidad 6", "¿Cuánto gana de verdad mi negocio?", [
   ("Lo que compraste no es lo que vendiste", [
     "<b>Costo de lo vendido</b> = inventario al empezar + compras − inventario al terminar",
     "$600.000 + $2.400.000 − $1.200.000 = <b>$1.800.000</b>"]),
   ("La utilidad real", [
     "<b>Utilidad real</b> = ventas − costo de lo vendido − fijos − variables − tu sueldo",
     "$5.000.000 − $1.800.000 − $900.000 − $300.000 − $1.200.000 = <b>$800.000</b>"]),
   ("Lo que va aparte", [
     "Las cuotas de un crédito: es devolver un préstamo",
     "Las máquinas: te sirven muchos meses"]),
   ("El margen", [
     "<b>Margen</b> = utilidad real ÷ ventas × 100",
     "$800.000 ÷ $5.000.000 = <b>16&nbsp;%</b>"]),
   ("Ojo", [
     "Utilidad no es plata en la cuenta: el fiado y el inventario no están en la caja"]),
 ]),
 "u7-mapa": ("Unidad 7", "¿Qué hago el último día del mes?", [
   ("Los 5 pasos del cierre", [
     "<b>1. Cuadra</b> el libro con la cuenta y el cajón (5 min)",
     "<b>2. Suma</b> las categorías y lo que te deben (5 min)",
     "<b>3. Cuenta</b> el inventario a precio de compra (5 min)",
     "<b>4. Calcula</b> la utilidad real y el margen (3 min)",
     "<b>5. Decide</b> una acción para el mes (2 min)"]),
   ("Cuando no cuadra", [
     "<b>Diferencia</b> = saldo del libro − (cuenta + cajón)",
     "Positiva: falta plata. Negativa: sobra plata",
     "Búscala en los movimientos antes de ajustar"]),
   ("Tu hoja de cierre", [
     "Ventas, costo, gastos, sueldo, utilidad, margen, te deben, inventario",
     "Mes a mes: lo que llevas al banco o al contador"]),
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
