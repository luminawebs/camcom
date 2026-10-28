"""Arma las descargas de Llévatelo (HTML -> PDF A5) con el logo de edunest.
Uso: python3 armar_descargas.py && node ../guias-pdf/renderizar_pdf.mjs descargas"""
import pathlib

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "Vende más por WhatsApp Business"
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
.pie{position:absolute;left:10mm;right:10mm;bottom:6mm;font-size:7pt;color:#8d8d94;display:flex;justify-content:space-between}
.cajas{display:grid;gap:3mm}
.caja{border:.4mm solid #d4d4d8;border-radius:3mm;padding:2.6mm 3.4mm}
.caja small{display:block;font-size:7.5pt;text-transform:uppercase;letter-spacing:.06em;color:#9e0c24;font-weight:700}
.caja p{font-size:9.6pt;margin-top:1mm;line-height:1.35}
.linea{border-bottom:.3mm dashed #b8b8be;height:6mm}
.tarj{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.tarj .caja{min-height:34mm}"""


def pagina(etiqueta, titulo, sub, cuerpo, n=1, de=1):
    return (f"<section class='pag'><div class='top'>{LOGO}<span>{etiqueta}</span></div>"
            f"<div class='hero'><small>{CURSO}</small><h1>{titulo}</h1><p>{sub}</p></div>{cuerpo}"
            f"<div class='pie'><span>Aula Virtual Empresarial · Cámara de Comercio de Soacha</span><span>{n} / {de}</span></div></section>")


def fila(a, b, fecha=False):
    return f"<tr><td class='c'><i></i></td><td><b>{a}</b><small>{b}</small></td>" + ("<td class='f'><i></i></td>" if fecha else "") + "</tr>"


def doc(nombre, titulo, paginas):
    (AQUI / f"{nombre}.html").write_text(
        f"<!doctype html><html lang='es'><head><meta charset='utf-8'><title>{titulo}</title><style>{CSS}</style></head><body>{''.join(paginas)}</body></html>",
        encoding="utf-8")
    print("ok", nombre)


def caja(et, texto="", lineas=0):
    return f"<div class='caja'><small>{et}</small>" + (f"<p>{texto}</p>" if texto else "") + "<div class='linea'></div>" * lineas + "</div>"


# ---- Unidad 1: ficha para armar el catálogo
perfil = [("Nombre del negocio", "Como te buscan: «Dulce Sandra · Tortas por encargo»."),
          ("Categoría", "La más cercana a lo que vendes."),
          ("Descripción", "Qué vendes y para quién, en una frase."),
          ("Dirección o zona de domicilio", "Barrio o «Domicilio en Soacha»."),
          ("Horario", "Días y horas en que atiendes."),
          ("Foto del perfil", "Tu logo o tu mejor producto, con buena luz.")]
prod = "".join(f"<div class='caja'><small>Producto {i}</small><p style='font-size:8.4pt;color:#6b6b72'>Nombre (con tamaño) · Precio · Descripción (sabor, tamaño, con cuánto pedir, domicilio)</p><div class='linea'></div><div class='linea'></div></div>" for i in range(1, 5))
doc("u1-ficha-catalogo", "Ficha para armar tu catálogo", [pagina(
    "Unidad 1 · Llévatelo", "Ficha para armar tu catálogo", "Llena esta ficha en papel y después pásala a WhatsApp Business. Marca cada parte del perfil cuando la tengas lista.",
    "<h2>Tu perfil de empresa</h2><table><tr><th class='c'>✓</th><th>Qué</th></tr>" + "".join(fila(a, b) for a, b in perfil) + "</table>"
    "<p class='nota'>Ruta en la app: menú ⋮ › Herramientas para la empresa › Perfil de empresa. En tu celular puede llamarse distinto.</p>", 1, 2),
    pagina("Unidad 1 · Llévatelo", "Tus productos que más vendes", "Empieza por los 5 que más vendes. Para cada uno: foto con luz de día y fondo limpio, nombre con tamaño, precio y descripción.",
    f"<div class='tarj'>{prod}</div><p class='nota'>Ejemplo: «Torta de chocolate para 12 · $65.000 · Bizcocho húmedo con ganache. Pídela con 2 días. Domicilio en Soacha».</p>", 2, 2)])

# ---- Unidad 2: rutina diaria de pedidos
etapas = [("Nuevo pedido", "El cliente ya dijo qué quiere."), ("Pago pendiente", "Le mandaste el valor y falta que pague."),
          ("Pagado", "Ya pagó y falta entregar."), ("Entregado", "Listo. Si vuelve a comprar, empieza otra vez.")]
rutina = [("Filtra «Pago pendiente»", "Escríbeles a los que no han pagado. Ahí está tu plata por cobrar."),
          ("Filtra «Pagado»", "Arma los despachos de mañana. Ahí está lo que no se te puede olvidar."),
          ("Cambia las etiquetas", "Al entregar, pasa el chat a «Entregado»."),
          ("Revisa los chats sin etiqueta", "Ponle etiqueta a cada cliente nuevo del día.")]
semana = "<table><tr><th>Día</th><th>Por cobrar</th><th>Por despachar</th><th>Entregados</th></tr>" + "".join(
    f"<tr><td><b>{d}</b></td><td></td><td></td><td></td></tr>" for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]) + "</table>"
doc("u2-rutina-pedidos", "Rutina diaria de pedidos", [pagina(
    "Unidad 2 · Llévatelo", "Rutina diaria de pedidos", "Cuatro etiquetas y diez minutos al cerrar el día. Pega esta hoja donde la veas.",
    "<h2>Tus etiquetas, en orden</h2><table><tr><th class='c'>✓</th><th>Etiqueta</th></tr>" + "".join(fila(a, b) for a, b in etapas) + "</table>"
    "<h2>Al cerrar el día</h2><table><tr><th class='c'>✓</th><th>Qué</th></tr>" + "".join(fila(a, b) for a, b in rutina) + "</table>", 1, 2),
    pagina("Unidad 2 · Llévatelo", "Tu semana de pedidos", "Anota cada noche cuántos chats quedaron en cada etiqueta. Si «Por cobrar» crece, escríbeles antes de despachar más.",
    semana + "<p class='nota'>Para poner una etiqueta: mantén presionado el chat y toca el ícono de etiqueta. En tu celular la ruta puede ser distinta.</p>", 2, 2)])

# ---- Unidad 3: mensajes listos para copiar
mensajes = [("Mensaje de bienvenida", "¡Hola! Soy [tu nombre], de [tu negocio], en [barrio]. Vendemos [qué vendes]. Mira nuestro catálogo y dime qué necesitas. 😊"),
            ("Mensaje de ausencia", "¡Hola! En este momento no puedo responderte. Te escribo desde las [hora]. Mientras tanto, mira el catálogo."),
            ("/domicilio", "Llevamos a domicilio en [zonas] de [hora] a [hora]. El envío vale [valor]. ¿Qué te mandamos hoy?"),
            ("/horario", "Atendemos de [días] de [hora] a [hora]."),
            ("/pagos", "Recibimos efectivo, Nequi y Daviplata al [número]. Cuando pagues, mándame el comprobante por aquí. 🙏"),
            ("/gracias", "¡Gracias por tu compra, [nombre]! Si te gustó, cuéntale a un amigo. Aquí estamos para lo que necesites.")]
doc("u3-mensajes-listos", "Tus mensajes listos para copiar", [pagina(
    "Unidad 3 · Llévatelo", "Tus mensajes listos para copiar", "Cambia lo que está entre [ ] por tus datos y pégalos en WhatsApp Business.",
    "<div class='cajas'>" + "".join(caja(a, b) for a, b in mensajes[:3]) + "</div>", 1, 2),
    pagina("Unidad 3 · Llévatelo", "Más respuestas rápidas", "Una por cada pregunta que te repiten. En el chat escribes / y eliges.",
    "<div class='cajas'>" + "".join(caja(a, b) for a, b in mensajes[3:]) + caja("Tu respuesta rápida", "Atajo: /", 2) + "</div>"
    "<p class='nota'>Antes de mandar promociones a un cliente, pregúntale si quiere recibirlas y respeta si te dice que no.</p>", 2, 2)])
