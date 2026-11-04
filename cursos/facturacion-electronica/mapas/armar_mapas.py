"""Arma los mapas mentales del curso (HTML) a partir del contenido de abajo.
Uso: python3 armar_mapas.py  -> genera mapas/<id>.html; luego renderizar.mjs los pasa a PNG."""
import html, pathlib

AQUI = pathlib.Path(__file__).parent
CURSO = "Facturación electrónica sin miedo"

MAPAS = {
 "mapa-curso": ("Mapa del curso", CURSO, [
   ("Unidad 1 · ¿Me toca facturar?", [
     "La factura electrónica la valida la DIAN y llega al correo del cliente",
     "Facturar no es pagar más impuestos: es dejar constancia de la venta",
     "Comerciantes y responsables de IVA: sí, salvo excepciones"]),
   ("Unidad 2 · Habilítate gratis en la DIAN", [
     "RUT al día y acceso al correo del RUT",
     "Registro con el servicio gratuito y firma digital sin costo",
     "Pruebas, numeración y prefijo: listo para facturar"]),
   ("Unidad 3 · Tu primera factura, sin errores", [
     "Nombre, NIT o cédula y correo del cliente",
     "Sin datos: <b>consumidor final</b> y 222222222222",
     "Error = <b>nota crédito</b> + factura nueva"]),
 ]),
 "u1-mapa": ("Unidad 1", "¿Le toca facturar a tu negocio?", [
   ("Qué es", [
     "La factura de siempre, hecha en el celular o el computador",
     "La DIAN la valida antes de que le llegue al cliente",
     "Lleva un código único (CUFE) y un QR"]),
   ("No es pagar más", [
     "Es una constancia de lo que vendes",
     "Tus impuestos dependen de tu RUT y de cuánto vendes"]),
   ("A quién le toca", [
     "Comerciantes",
     "Responsables de IVA y del Régimen Simple",
     "Profesionales que cobran honorarios"]),
   ("Excepciones", [
     "Los no obligados a facturar que dice la ley",
     "Si no sabes, tu RUT + un contador o la Cámara"]),
   ("Lo que ganas", [
     "Venderle a empresas, colegios y al Estado",
     "Tus ventas en orden para pedir un crédito"]),
 ]),
 "u2-mapa": ("Unidad 2", "¿Cómo te habilitas para facturar sin pagar un programa?", [
   ("Antes de empezar", [
     "RUT al día: dirección, celular, correo y actividad",
     "Usuario de la DIAN y acceso al correo del RUT"]),
   ("Los pasos", [
     "<b>1.</b> Regístrate como facturador con el servicio gratuito",
     "<b>2.</b> Pide tu certificado de firma (gratis)",
     "<b>3.</b> Haz las facturas de prueba y escoge tu fecha de inicio",
     "<b>4.</b> Pide tu numeración, con prefijo y rango de contingencia"]),
   ("En tu RUT", [
     "Quedas como facturador electrónico (responsabilidad 52)",
     "No te cambia los impuestos"]),
   ("Errores comunes", [
     "Pagar un programa sin saber que hay uno gratis",
     "Usar un correo que ya no revisas",
     "Olvidar el rango de contingencia"]),
 ]),
 "u3-mapa": ("Unidad 3", "¿Qué datos lleva tu factura y qué haces si te equivocas?", [
   ("Pide antes de facturar", [
     "Nombre completo o razón social",
     "NIT o cédula (revísalo contra el RUT)",
     "Correo del cliente"]),
   ("Lo que lleva la factura", [
     "Tus datos y tu número autorizado con prefijo",
     "Fecha y hora, lo que vendiste, cantidad y valor",
     "Forma de pago, impuestos si aplican, CUFE y QR"]),
   ("Consumidor final", [
     "Si el cliente no da sus datos: <b>222222222222</b>",
     "Nunca inventes datos"]),
   ("Si te equivocas", [
     "La factura no se borra",
     "<b>Nota crédito</b> + factura nueva, apenas te des cuenta",
     "Si ya fue aceptada: pide ayuda a un contador"]),
   ("Si se cae el sistema", [
     "Factura de contingencia con su rango",
     "Después la pasas a la DIAN"]),
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
