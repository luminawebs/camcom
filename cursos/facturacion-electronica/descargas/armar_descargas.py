"""Arma las descargas de Llévatelo (HTML -> PDF A5) con el logo de edunest.
Uso: python3 armar_descargas.py && node ../guias-pdf/renderizar_pdf.mjs descargas"""
import pathlib

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "Facturación electrónica sin miedo"
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
.pie{position:absolute;left:10mm;right:10mm;bottom:6mm;font-size:7pt;color:#8d8d94;display:flex;justify-content:space-between}"""


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


antes = [("RUT al día", "Dirección, celular, correo y actividad de tu negocio correctos."),
         ("Acceso al correo del RUT", "Ahí te llegan los códigos de la DIAN."),
         ("Usuario y contraseña de la DIAN", "Si no la recuerdas, recupérala con el correo del RUT.")]
pasos = [("Registro como facturador", "Con el servicio gratuito de la DIAN."),
         ("Certificado de firma digital", "Gratis. Sirve para firmar tus facturas."),
         ("Facturas de prueba", "Hasta quedar habilitado; escoge tu fecha de inicio."),
         ("RUT con la responsabilidad 52", "Facturador electrónico. No cambia tus impuestos."),
         ("Numeración y prefijo", "Un rango, por ejemplo del 1 al 1.000, con un prefijo como FE."),
         ("Rango de contingencia", "Para cuando se caiga el sistema o no haya internet.")]
doc("u2-lista-habilitacion", "Lista para habilitarte en la DIAN", [pagina(
    "Unidad 2 · Llévatelo", "Lista para habilitarte en la DIAN", "Marca lo que ya tienes y ponle fecha a lo que falta. El servicio de la DIAN es gratis: no tienes que comprar un programa.",
    "<h2>Antes de empezar</h2><table><tr><th class='c'>✓</th><th>Qué</th><th class='f'>Fecha</th></tr>" + "".join(fila(a, b, True) for a, b in antes) + "</table>"
    "<h2>Los pasos (1 a 3)</h2><table><tr><th class='c'>✓</th><th>Qué</th><th class='f'>Fecha</th></tr>" + "".join(fila(a, b, True) for a, b in pasos[:3]) + "</table>", 1, 2),
    pagina("Unidad 2 · Llévatelo", "Lista para habilitarte en la DIAN", "Sigue con los pasos que faltan. Cuando termines, ya puedes facturar.",
    "<h2>Los pasos (4 a 6)</h2><table><tr><th class='c'>✓</th><th>Qué</th><th class='f'>Fecha</th></tr>" + "".join(fila(a, b, True) for a, b in pasos[3:]) + "</table>"
    "<p class='nota'>Los nombres de los botones del portal de la DIAN cambian con el tiempo. Si te pierdes, pregunta en la Cámara de Comercio o a un contador.</p>", 2, 2)])

datos = [("Nombre completo o razón social del cliente", ""),
         ("NIT o cédula, revisado contra su RUT", "Número por número, con el dígito de verificación."),
         ("Correo del cliente", "Si es empresa, el correo de facturación."),
         ("Sin datos: «consumidor final» y 222222222222", "Nunca inventes datos.")]
factura = [("Dice «factura electrónica de venta»", ""),
           ("Tu nombre, tu NIT y tu número autorizado con prefijo", ""),
           ("Fecha y hora", ""),
           ("Qué vendiste, cuántos y el valor de cada uno", ""),
           ("Impuestos, solo si te toca cobrarlos", "Pregúntale a tu contador."),
           ("Forma de pago: contado o crédito", ""),
           ("Código único (CUFE) y código QR", "Los pone el sistema al generarla.")]
error = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in [
    ("Te equivocaste y no la han aceptado", "Nota crédito que la anula + factura nueva con los datos bien"),
    ("El cliente ya la aceptó", "Pide ayuda a un contador"),
    ("Se cayó el sistema o no hay internet", "Factura de contingencia y después la pasas a la DIAN"),
    ("El cliente no quiere dar sus datos", "Consumidor final, 222222222222")])
doc("u3-chequeo-factura", "Lista de chequeo de tu factura", [
    pagina("Unidad 3 · Llévatelo", "Lista de chequeo de tu factura", "Revísala antes de generar cada factura. Un minuto de revisión te ahorra una nota crédito.",
           "<h2>Pide antes de facturar</h2><table><tr><th class='c'>✓</th><th>Qué</th></tr>" + "".join(fila(a, b) for a, b in datos) + "</table>"
           "<h2>Lo que lleva la factura</h2><table><tr><th class='c'>✓</th><th>Qué</th></tr>" + "".join(fila(a, b) for a, b in factura[:3]) + "</table>", 1, 2),
    pagina("Unidad 3 · Llévatelo", "Si algo sale mal", "Termina de revisar la factura. Y si algo sale mal, esto es lo que haces.",
           "<table><tr><th class='c'>✓</th><th>Qué</th></tr>" + "".join(fila(a, b) for a, b in factura[3:]) + "</table><h2>Si algo sale mal</h2><table><tr><th>Si…</th><th>Haces</th></tr>" + error + "</table>"
           "<p class='nota'>Fuentes: Estatuto Tributario, art. 617; DIAN, Oficio 900223 de 2022; Decreto 1074 de 2015, art. 2.2.2.5.4. Las reglas de tu caso las confirma un contador o la Cámara de Comercio.</p>", 2, 2)])
