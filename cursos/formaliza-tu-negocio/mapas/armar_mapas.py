"""Arma los mapas mentales del curso (HTML) a partir del contenido de abajo.
Uso: python3 armar_mapas.py  -> genera mapas/<id>.html; luego renderizar.mjs los pasa a PNG."""
import html, pathlib

AQUI = pathlib.Path(__file__).parent
CURSO = "Formaliza tu negocio paso a paso"

MAPAS = {
 "mapa-curso": ("Mapa del curso", CURSO, [
   ("Unidad 1 · Formal no es pagar más", [
     "Estar formal = RUT + matrícula mercantil + local en regla",
     "El RUT no es un impuesto: es un registro gratis",
     "Ganas: crédito con proveedores, clientes empresa y crédito en el banco"]),
   ("Unidad 2 · El RUT desde el celular", [
     "Gratis, en la página de la DIAN, en unos 15 minutos",
     "Cédula, selfie, correo, dirección y código de actividad (CIIU)",
     "<b>NIT</b> = tu cédula + dígito de verificación. No vence: se actualiza"]),
   ("Unidad 3 · Matrícula y local en regla", [
     "Matrícula mercantil en la Cámara de Comercio: tú y tu establecimiento",
     "<b>Renueva</b> cada año del 1 de enero al 31 de marzo",
     "Local: uso de suelo, matrícula al día, aviso a la Policía y derechos de autor si hay música"]),
 ]),
 "u1-mapa": ("Unidad 1", "¿Qué necesita tu negocio para estar formal?", [
   ("Los 3 pasos", [
     "<b>1.</b> RUT, en la DIAN: quién eres para los impuestos",
     "<b>2.</b> Matrícula mercantil, en la Cámara de Comercio",
     "<b>3.</b> Requisitos del local, ante la Alcaldía y la Policía"]),
   ("El RUT no es un impuesto", [
     "Es gratis y no cobra nada por sí solo",
     "Lo que pagas depende de cuánto vendes y ganas: pregúntale a un contador"]),
   ("Lo que ganas", [
     "Comprar a crédito a distribuidores",
     "Venderle a empresas que piden RUT o factura",
     "Crédito en un banco, no en el gota a gota"]),
   ("¿En qué paso vas?", [
     "Sin RUT: empieza por ahí (Unidad 2)",
     "Con RUT y sin matrícula: sigue con la matrícula (Unidad 3)",
     "Todo al día y con local: revisa los requisitos del local"]),
   ("Dato", [
     "Solo el 22,4&nbsp;% de los micronegocios de Colombia tenía RUT en 2024 (DANE, EMICRON 2024)"]),
 ]),
 "u2-mapa": ("Unidad 2", "¿Cómo sacas tu RUT sin pagar ni hacer filas?", [
   ("Qué es el RUT", [
     "Registro Único Tributario de la DIAN",
     "<b>NIT</b> = tu cédula + dígito de verificación",
     "No vence: se actualiza si cambian tus datos"]),
   ("Lo que necesitas", [
     "Cédula (fotos de las dos caras) y una selfie",
     "Correo y celular",
     "Dirección donde trabajas y código de actividad (CIIU)"]),
   ("Paso a paso en línea", [
     "DIAN → Inscripción en el RUT → Persona natural",
     "Datos, fotos y código que llega al correo",
     "Descarga el PDF y guárdalo en el celular"]),
   ("Las responsabilidades", [
     "Lo que la DIAN espera de ti",
     "Dudas sobre lo que te quedó: muéstrale tu RUT a un contador"]),
   ("Errores comunes", [
     "Pagarle a alguien por sacarlo: es gratis",
     "Sacar un RUT nuevo en vez de actualizar el que tienes",
     "Poner una actividad que no es la de tu negocio"]),
 ]),
 "u3-mapa": ("Unidad 3", "¿Qué papeles le piden a tu local y cada cuánto se renuevan?", [
   ("La matrícula mercantil", [
     "Registro en la Cámara de Comercio: tú y tu establecimiento",
     "Se paga según los activos del negocio",
     "Antes, consulta tu nombre en el RUES"]),
   ("Se renueva cada año", [
     "<b>Del 1 de enero al 31 de marzo</b>",
     "Tarde: te pueden sancionar",
     "Cinco años sin renovar: se cancela"]),
   ("Lo que le piden a tu local", [
     "Uso de suelo (Alcaldía)",
     "Matrícula mercantil al día",
     "Avisar la apertura a la Policía",
     "Seguridad y sanidad (bomberos y, si vendes comida, salud)",
     "Derechos de autor si pones música para los clientes"]),
   ("Sin local", [
     "Si trabajas a domicilio o vendes en línea, no te piden los requisitos del local"]),
   ("Norma", [
     "Ley 1801 de 2016, artículo 87 (Código Nacional de Seguridad y Convivencia Ciudadana)"]),
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
