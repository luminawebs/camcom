"""Arma las descargas de Llévatelo (HTML -> PDF A5) con el logo de edunest.
Uso: python3 armar_descargas.py && node ../guias-pdf/renderizar_pdf.mjs descargas"""
import pathlib

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "IA para tu negocio desde el celular"
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
.tarj .caja{min-height:34mm}
.sem{display:grid;gap:3mm}.sem .caja{border-width:.6mm}
.mini{gap:2mm}.mini .caja{padding:2mm 3mm}.mini .caja p{font-size:8.7pt;line-height:1.3}
.r{border-color:#c8102e}.r small{color:#c8102e}.a{border-color:#d9a400}.a small{color:#8a6a00}.v{border-color:#2e9d5b}.v small{color:#1f7a45}"""


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



# ---- Unidad 1: fórmula del pedido
partes = [("1. Quién eres", "Tu negocio, qué vendes y dónde.", "Tengo una ferretería en Quintanares, Soacha."),
          ("2. Qué necesitas", "Un aviso, un mensaje, una idea, una lista.", "Escribe un aviso para el grupo de WhatsApp del barrio."),
          ("3. Para quién", "Quién lo va a leer.", "Para vecinos que arreglan la casa el fin de semana."),
          ("4. Cómo lo quieres", "Largo, tono, datos que no pueden faltar.", "Corto, 4 líneas, amable, con el horario del sábado de 7 a. m. a 6 p. m.")]
ajustes = [("«Más corto»", "o «en 4 líneas»"), ("«Más cercano»", "«como hablamos en Soacha», «tuteando»"), ("«Dame 3 opciones»", "y eliges la que más te guste"),
           ("«Ahora para Facebook»", "o para un letrero, un correo, un volante"), ("«Revisa la ortografía»", "de un texto que escribiste tú")]
doc("u1-formula-pedido", "Tu fórmula para pedirle a la IA", [pagina(
    "Unidad 1 · Llévatelo", "Tu fórmula para pedirle a la IA", "Un buen pedido tiene 4 partes. Escribe las tuyas una vez y guárdalas en las notas del celular.",
    "<div class='cajas'>" + "".join(caja(a, f"<span style='color:#6b6b72;font-size:8.4pt'>{b}</span><br>Ejemplo: «{c}»", 1) for a, b, c in partes) + "</div>", 1, 2),
    pagina("Unidad 1 · Llévatelo", "Conversa: pídele ajustes", "La primera respuesta no es la última. Marca los ajustes que más usas.",
    "<table><tr><th class='c'>✓</th><th>Pídele</th></tr>" + "".join(fila(a, b) for a, b in ajustes) + "</table>"
    "<h2>Tu pedido de esta semana</h2>" + caja("Escríbelo aquí con las 4 partes", "", 4) +
    "<p class='nota'>Asistentes con versión gratis para el celular: ChatGPT, Gemini, Copilot y Meta AI dentro de WhatsApp. Todos se pueden equivocar: revisa siempre.</p>", 2, 2)])

# ---- Unidad 2: 10 pedidos listos
pedidos = [("Descripción de producto", "Vendo [qué vendes] en Soacha. Escribe la descripción de [producto] para mi catálogo: [material, tamaño o tallas], [precio]. Para [cliente]. Tono cálido, 3 líneas, sin inventar datos."),
           ("Nombre de producto", "Dame 5 nombres cortos para [producto] que digan qué es y para cuántos o qué talla."),
           ("Promoción", "Escribe un mensaje para mis clientes: esta semana [promoción] hasta el [día]. Corto, tuteando, con un emoji."),
           ("Recordar un pago", "Escribe un mensaje amable para recordarle a un cliente que tiene pendiente [valor] del pedido de [producto]. Sin sonar a cobro brusco."),
           ("Responder un reclamo", "Un cliente dice que [qué pasó]. Escríbele una respuesta amable: le pido disculpas y [qué vas a hacer tú]. Corto."),
           ("Avisar un cambio", "Escribe un aviso para mis clientes: [cambio de horario, de precio o cierre] desde el [fecha]. Claro y corto."),
           ("Publicación para redes", "Escribe una publicación para Instagram de [producto] para [cliente]. Máximo 4 líneas y 3 etiquetas con #."),
           ("Responder preguntas frecuentes", "Mis clientes siempre preguntan [pregunta]. Escribe una respuesta corta y amable con estos datos: [datos]."),
           ("Ideas de venta", "Tengo [negocio] en [barrio]. Dame 5 ideas sencillas y baratas para vender más en [temporada o fecha]."),
           ("Mejorar tu texto", "Mejora este texto sin cambiar los datos ni agregar nada nuevo: [pega tu texto].")]
doc("u2-pedidos-listos", "10 pedidos listos para tu negocio", [pagina(
    "Unidad 2 · Llévatelo", "10 pedidos listos para tu negocio", "Copia el pedido, cambia lo que está entre [ ] por tus datos reales y revisa lo que te responda antes de usarlo.",
    "<div class='cajas mini'>" + "".join(caja(a, b) for a, b in pedidos[:5]) + "</div>", 1, 2),
    pagina("Unidad 2 · Llévatelo", "Más pedidos y tu revisión", "Antes de publicar, marca cada punto de la lista.",
    "<div class='cajas mini'>" + "".join(caja(a, b) for a, b in pedidos[5:]) + "</div>"
    "<h2>Antes de publicar</h2><table>" + "".join(fila(a, b) for a, b in [("Precio y condiciones", "Son los tuyos, no los que inventó la IA."), ("Datos del producto", "Material, tallas, garantía: nada inventado."), ("Suena a ti", "Si no, pídele «más cercano» o cámbialo tú.")]) + "</table>", 2, 2)])

# ---- Unidad 3: semáforo de datos
rojo = ["Cédulas y números de documento", "Claves, códigos y contraseñas", "Números de cuenta o de tarjeta", "Fotos de documentos, facturas o comprobantes con datos", "Datos de salud de tus clientes (alergias, tratamientos)"]
amarillo = ["Nombres completos de clientes → «Clienta 1» o [nombre]", "Celulares y correos → quítalos", "Direcciones → solo el barrio, si hace falta"]
verde = ["Lo que vendes y tus precios", "Tu horario y tu barrio", "Cómo atiendes y cómo pagan tus clientes"]
li = lambda xs: "<p>" + "<br>".join("• " + x for x in xs) + "</p>"
doc("u3-semaforo-datos", "Semáforo de datos para usar la IA", [pagina(
    "Unidad 3 · Llévatelo", "Semáforo de datos para usar la IA", "Lo que escribes en la IA puede quedar guardado. Antes de enviar un pedido, pásalo por el semáforo.",
    "<div class='sem'>" + f"<div class='caja r'><small>Rojo · nunca</small>{li(rojo)}</div><div class='caja a'><small>Amarillo · quítalos antes</small>{li(amarillo)}</div><div class='caja v'><small>Verde · tranquilo</small>{li(verde)}</div>" + "</div>", 1, 2),
    pagina("Unidad 3 · Llévatelo", "Revisa tu asistente y a tus clientes", "Una vez al mes, revisa esta lista.",
    "<table><tr><th class='c'>✓</th><th>Qué</th></tr>" + "".join(fila(a, b) for a, b in [
        ("Ajustes de privacidad", "Apaga el uso de tus chats para entrenar el modelo (en cada app se llama distinto)."),
        ("Chats viejos", "Borra los que tengan datos de clientes."),
        ("Cuenta con clave", "Tu asistente con una clave que solo tú sepas."),
        ("Permiso de tus clientes", "Pregúntales antes de mandarles saludos o promociones."),
        ("Para lo que te autorizaron", "Usa sus datos solo para eso.")]) + "</table>"
    "<h2>Reescribe un pedido sin datos</h2>" + caja("Antes", "", 2) + caja("Después", "", 2) +
    "<p class='nota'>La Ley 1581 de 2012 protege los datos personales en Colombia; los de salud son datos sensibles. Si tienes dudas, pregunta en la Cámara de Comercio.</p>", 2, 2)])
