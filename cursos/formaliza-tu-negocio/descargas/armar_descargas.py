"""Arma las descargas de Llévatelo (HTML -> PDF A5) con el logo de edunest.
Uso: python3 armar_descargas.py && node ../guias-pdf/renderizar_pdf.mjs descargas"""
import pathlib

AQUI = pathlib.Path(__file__).parent
LOGO = (AQUI.parents[2] / "marca" / "edunest-blue.svg").read_text(encoding="utf-8")
CURSO = "Formaliza tu negocio paso a paso"
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


rut = [("Cédula de ciudadanía", "Fotos claras de las dos caras, sin reflejos."),
       ("Una selfie", "Con buena luz, sin gafas ni gorra."),
       ("Correo electrónico que revises", "Ahí te llega el código para terminar."),
       ("Número de celular", ""),
       ("Dirección donde trabajas", "La del local o, si vas a domicilio, la de tu casa."),
       ("Actividad de tu negocio y su código CIIU", "Ejemplo: tienda de barrio 4711. Búscalo en la página de la DIAN."),
       ("15 minutos y buena señal", "Se hace en la página de la DIAN: Inscripción en el RUT, Persona natural.")]
doc("u2-lista-rut", "Lista para sacar el RUT", [pagina(
    "Unidad 2 · Llévatelo", "Lo que necesitas para sacar tu RUT", "Marca cada cosa cuando la tengas lista. El RUT es gratis: nadie te debe cobrar por sacarlo.",
    "<table><tr><th class='c'>✓</th><th>Qué necesitas</th></tr>" + "".join(fila(a, b) for a, b in rut) + "</table>"
    "<h2>Cuando termines</h2><table>" + fila("Descargué mi RUT en PDF", "Guárdalo en el celular y en el correo.") +
    fila("Revisé que la actividad sea la de mi negocio", "Si no, actualízalo en línea, también gratis.") + "</table>"
    "<p class='nota'>Con cédula de extranjería o PPT: pre-RUT en línea y cita en la DIAN. Dudas sobre las responsabilidades del RUT: un contador o la Cámara de Comercio.</p>")])

ruta = [("RUT", "En la DIAN, gratis y en línea (Unidad 2)."),
        ("Matrícula mercantil", "En la Cámara de Comercio: tú y tu establecimiento."),
        ("Matrícula renovada este año", "Del 1 de enero al 31 de marzo.")]
local = [("Concepto de uso de suelo", "En la Alcaldía, con la dirección del local y tu actividad."),
         ("Aviso de apertura a la Policía", "A la estación de tu zona."),
         ("Seguridad", "Extintor, salidas despejadas y la revisión de bomberos."),
         ("Concepto sanitario", "Solo si vendes o preparas alimentos o bebidas."),
         ("Derechos de autor", "Solo si pones música, radio o televisión para tus clientes.")]
cal = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in [
    ("Cada año, de enero a marzo", "Renovar la matrícula mercantil"),
    ("Si cambias de dirección, celular o actividad", "Actualizar el RUT (gratis)"),
    ("Si te pasas de local", "Nuevo uso de suelo y aviso a la Policía"),
    ("Cada año", "Revisar extintor y comprobante de derechos de autor")])
doc("u3-checklist-formal", "Checklist de tu negocio formal", [
    pagina("Unidad 3 · Llévatelo", "Checklist de tu negocio formal",
           "Marca lo que ya tienes. Al frente de cada pendiente escribe la fecha en que lo vas a hacer.",
           "<h2>Tu ruta</h2><table><tr><th class='c'>✓</th><th>Qué</th><th class='f'>Fecha</th></tr>" + "".join(fila(a, b, True) for a, b in ruta) + "</table>"
           "<h2>Tu local (si atiendes al público)</h2><table><tr><th class='c'>✓</th><th>Qué</th><th class='f'>Fecha</th></tr>" + "".join(fila(a, b, True) for a, b in local) + "</table>", 1, 2),
    pagina("Unidad 3 · Llévatelo", "Tu calendario", "Las fechas que se repiten. Pégalas en tu calendario del celular.",
           "<table><tr><th>Cuándo</th><th>Qué haces</th></tr>" + cal + "</table>"
           "<p class='nota'>Requisitos del local: Ley 1801 de 2016, artículo 87. Los trámites y costos en Soacha los confirma la Cámara de Comercio de Soacha y la Alcaldía.</p>", 2, 2)])
