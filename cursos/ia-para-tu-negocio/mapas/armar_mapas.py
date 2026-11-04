"""Arma los mapas mentales del curso (HTML) a partir del contenido de abajo.
Uso: python3 armar_mapas.py  -> genera mapas/<id>.html; luego renderizar.mjs los pasa a PNG."""
import html, pathlib

AQUI = pathlib.Path(__file__).parent
CURSO = "IA para tu negocio desde el celular"

MAPAS = {
 "mapa-curso": ("Mapa del curso", CURSO, [
   ("Unidad 1 · Pídele bien a la IA", [
     "La IA escribe por ti, pero solo sabe lo que tú le cuentas",
     "<b>Quién soy + qué necesito + para quién + cómo lo quiero</b>",
     "Conversa: pídele cambios, no empieces de cero"]),
   ("Unidad 2 · Mensajes y descripciones que venden", [
     "Dale tus datos reales: precio, tallas, material",
     "La IA se puede inventar cosas: <b>lee y corrige</b>",
     "Que suene como tú; guarda los pedidos que funcionan"]),
   ("Unidad 3 · Lo que no le cuentas a la IA", [
     "Lo que escribes puede quedar guardado",
     "<b>Rojo:</b> cédulas, claves, cuentas, salud · <b>Amarillo:</b> nombres y números",
     "Cambia nombres por «Clienta 1» o [nombre]"]),
 ]),
 "u1-mapa": ("Unidad 1", "¿Qué le dices a la IA para que te responda algo que sirva?", [
   ("Un asistente de IA", [
     "App que conversa y escribe, por texto o por voz",
     "Hay versiones gratis para el celular",
     "No conoce tu negocio y se puede equivocar"]),
   ("Por qué sale mal", [
     "«Haz un aviso»: sin datos, la IA adivina",
     "Rellena con palabras grandes y ofertas inventadas"]),
   ("Las 4 partes de un buen pedido", [
     "<b>1.</b> Quién eres: tu negocio y dónde",
     "<b>2.</b> Qué necesitas: aviso, mensaje, idea",
     "<b>3.</b> Para quién: tu cliente",
     "<b>4.</b> Cómo lo quieres: largo, tono, datos"]),
   ("Conversa", [
     "«Más corto», «más cercano», «dame 3 opciones»",
     "Cada ajuste toma segundos"]),
 ]),
 "u2-mapa": ("Unidad 2", "¿Cómo escribes con IA en minutos sin publicar algo que no es cierto?", [
   ("Dale tus datos reales", [
     "Qué es, material, tallas y precio",
     "Para quién es y condiciones (domicilio, cambios)",
     "Si puedes, la foto del producto"]),
   ("La IA se puede inventar cosas", [
     "«Orgánico», «garantía», «envío gratis»…",
     "Lo que publicas tiene que ser verdad",
     "<b>Lee y corrige antes de publicar</b>"]),
   ("Mensajes para clientes", [
     "Promociones, recordar un pago, responder un reclamo",
     "Cuéntale qué pasó y qué vas a hacer tú"]),
   ("Que suene como tú", [
     "Tuteando, cercano, sin palabras rebuscadas",
     "Guarda en tus notas los pedidos que funcionan"]),
 ]),
 "u3-mapa": ("Unidad 3", "¿Qué datos nunca pones en la IA y cómo pides sin ellos?", [
   ("Lo que escribes viaja", [
     "Puede quedar guardado en la empresa del asistente",
     "No escribas nada que no publicarías"]),
   ("El semáforo de datos", [
     "<b>Rojo, nunca:</b> cédulas, claves, cuentas, salud",
     "<b>Amarillo, quítalos:</b> nombres, celulares, direcciones",
     "<b>Verde:</b> productos, precios, horario, barrio"]),
   ("Pide sin datos personales", [
     "«Clienta 1» o [nombre] en vez del nombre real",
     "El resultado es igual de bueno"]),
   ("Ajustes y clientes", [
     "Apaga el uso de tus chats para entrenar",
     "Borra los chats con datos de clientes",
     "Usa sus datos solo para lo que te autorizaron"]),
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
