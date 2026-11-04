"""Arma las pantallas simplificadas de WhatsApp Business del curso (HTML) y la especificación de cada simulador.
Uso: python3 armar_pantallas.py && node renderizar.mjs
- practica/uN-K.html  -> pantallas del simulador (9:19). El elemento con id="objetivo" es la zona que se toca;
  renderizar.mjs la mide y escribe piezas/uN-practica/contenido.js con las zonas en porcentaje.
- vistas/<id>.html    -> imágenes 4:3 para las lecciones Aprende (piezas/uN-aprende/medios/ilustracion-K.jpg).
No son capturas reales: son pantallas dibujadas para practicar, con los nombres de los menús de la app
(Android, octubre de 2026, [VERIFICAR] con la versión actual). Las marcas y logos de la app no se usan.
"""
import html, json, pathlib

AQUI = pathlib.Path(__file__).parent
VERDE, VERDE_OSC, FONDO_CHAT = "#1f7a5c", "#155c45", "#efe7de"
ETI = {"Nuevo cliente": "#3d8bfd", "Nuevo pedido": "#f2a516", "Pago pendiente": "#c8102e", "Pagado": "#2e9d5b", "Entregado": "#8d8d94"}

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:360px;height:760px;overflow:hidden;font-family:Roboto,Inter,'DejaVu Sans',sans-serif;background:#fff;color:#111;position:relative}}
.est{{height:24px;background:{VERDE_OSC};color:#fff;font-size:11px;display:flex;justify-content:space-between;align-items:center;padding:0 12px}}
.est i{{font-style:normal;background:rgba(255,255,255,.18);border-radius:8px;padding:1px 7px;font-size:9.5px;letter-spacing:.04em}}
.cab{{height:56px;background:{VERDE};color:#fff;display:flex;align-items:center;gap:14px;padding:0 10px 0 14px}}
.cab h1{{font-size:19px;font-weight:600;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.cab .ic{{width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-size:19px;border-radius:50%}}
.cab .av{{width:34px;height:34px;border-radius:50%;background:#d8e8e1;color:{VERDE_OSC};font-weight:700;display:flex;align-items:center;justify-content:center;font-size:14px}}
.cab small{{display:block;font-size:11px;font-weight:400;opacity:.85}}
.chips{{display:flex;gap:8px;padding:10px 12px;overflow:hidden}}
.chip{{border-radius:16px;background:#eef1f0;color:#333;font-size:13px;padding:6px 12px;white-space:nowrap}}
.chip.on{{background:#d6f0e3;color:{VERDE_OSC};font-weight:600}}
.chat{{display:flex;gap:12px;padding:10px 14px;align-items:center}}
.chat .av{{flex:none;width:46px;height:46px;border-radius:50%;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;font-size:17px}}
.chat .tx{{flex:1;min-width:0;border-bottom:1px solid #eee;padding-bottom:10px}}
.chat .f1{{display:flex;justify-content:space-between;font-size:15.5px;font-weight:600}}
.chat .f1 span{{font-size:11.5px;font-weight:400;color:#777}}
.chat .f2{{font-size:13.5px;color:#666;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:3px}}
.chat .et{{display:inline-flex;align-items:center;gap:4px;font-size:11px;color:#444;margin-top:4px}}
.chat .et b{{width:9px;height:9px;border-radius:50%;display:inline-block}}
.chat.sel{{background:#e3f1ea}}
.fab{{position:absolute;right:18px;bottom:22px;width:56px;height:56px;border-radius:16px;background:{VERDE};color:#fff;font-size:26px;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 8px rgba(0,0,0,.25)}}
.menu{{position:absolute;right:8px;top:30px;width:236px;background:#fff;border-radius:6px;box-shadow:0 4px 16px rgba(0,0,0,.28);padding:6px 0;z-index:3}}
.menu div{{padding:13px 18px;font-size:15px}}
.velo{{position:absolute;inset:0;background:rgba(0,0,0,.08);z-index:2}}
.item{{display:flex;gap:16px;align-items:center;padding:13px 18px}}
.item .ic{{flex:none;width:30px;text-align:center;font-size:21px;color:{VERDE}}}
.item b{{display:block;font-size:15.5px;font-weight:500}}
.item small{{display:block;font-size:12.5px;color:#777;margin-top:2px}}
.sec{{font-size:13px;color:{VERDE};font-weight:600;padding:14px 18px 4px}}
.campo{{margin:12px 16px 0;border-bottom:2px solid {VERDE};padding:6px 2px;font-size:15px}}
.campo small{{display:block;font-size:11.5px;color:{VERDE};margin-bottom:3px}}
.campo.gris{{border-color:#ccc}}.campo.gris small{{color:#777}}
.btn{{display:flex;align-items:center;justify-content:center;background:{VERDE};color:#fff;font-weight:600;font-size:15px;border-radius:22px;height:44px;margin:18px 16px 0}}
.btn.lin{{background:#fff;color:{VERDE};border:1.5px solid {VERDE}}}
.foto{{margin:14px 16px 0;height:150px;border-radius:10px;background:radial-gradient(circle at 50% 45%,#fff7ee,#f0dcc8);display:flex;flex-direction:column;align-items:center;justify-content:center;color:#6b4a35;font-size:12px;gap:6px}}.foto span{{font-size:64px}}
.prod{{display:flex;gap:12px;padding:12px 16px;border-bottom:1px solid #eee;align-items:center}}
.prod .im{{flex:none;width:64px;height:64px;border-radius:8px}}
.prod b{{display:block;font-size:15px;font-weight:600}}
.prod small{{display:block;font-size:12.5px;color:#666;margin-top:2px}}
.prod span{{display:block;font-size:14px;font-weight:600;margin-top:4px}}
.fondo{{background:{FONDO_CHAT};position:absolute;top:80px;bottom:62px;left:0;right:0;padding:12px 10px;display:flex;flex-direction:column;gap:8px}}
.bur{{max-width:80%;padding:7px 10px 16px;border-radius:9px;font-size:14px;line-height:1.35;position:relative;box-shadow:0 1px 0 rgba(0,0,0,.08)}}
.bur.el{{background:#fff;align-self:flex-start}}
.bur.yo{{background:#d9fdd3;align-self:flex-end}}
.bur em{{position:absolute;right:8px;bottom:3px;font-size:10px;color:#777;font-style:normal}}
.bur .auto{{display:block;font-size:10.5px;color:{VERDE};font-weight:600;margin-bottom:2px}}
.dia{{align-self:center;background:#fff;border-radius:7px;font-size:11.5px;color:#555;padding:4px 10px}}
.entrada{{position:absolute;left:0;right:0;bottom:0;height:62px;background:{FONDO_CHAT};display:flex;gap:8px;align-items:center;padding:0 8px}}
.entrada .caja{{flex:1;min-width:0;background:#fff;border-radius:24px;height:46px;display:flex;align-items:center;padding:0 16px;font-size:15px;color:#999;gap:10px}}
.entrada .caja.esc{{color:#111}}
.entrada .env{{flex:none;width:46px;height:46px;border-radius:50%;background:{VERDE};color:#fff;display:flex;align-items:center;justify-content:center;font-size:19px}}
.sug{{position:absolute;left:8px;right:8px;bottom:66px;background:#fff;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.2);z-index:2}}
.sug div{{padding:11px 14px;border-bottom:1px solid #f0f0f0;font-size:13.5px;color:#555}}
.sug b{{display:block;color:#111;font-size:14.5px}}
.hoja{{position:absolute;left:0;right:0;bottom:0;background:#fff;border-radius:18px 18px 0 0;box-shadow:0 -4px 16px rgba(0,0,0,.2);padding:8px 0 16px;z-index:3}}
.hoja h3{{font-size:17px;font-weight:600;padding:12px 20px 6px}}
.op{{display:flex;align-items:center;gap:14px;padding:12px 20px;font-size:15.5px}}
.op b{{width:16px;height:16px;border-radius:50%;display:inline-block}}
.op .ck{{margin-left:auto;width:22px;height:22px;border:2px solid #999;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:14px;color:#fff}}
.op .ck.on{{background:{VERDE};border-color:{VERDE}}}
.perfil{{text-align:center;padding:18px 16px 10px}}
.perfil .av{{width:96px;height:96px;border-radius:50%;margin:0 auto;background:radial-gradient(circle at 50% 40%,#f8d7e0,#c8607a);display:flex;align-items:center;justify-content:center;font-size:40px}}
.perfil h2{{font-size:21px;margin-top:10px}}
.perfil small{{display:block;font-size:13px;color:#777;margin-top:3px}}
.dato{{display:flex;gap:16px;padding:11px 18px;font-size:14px;line-height:1.35;border-top:1px solid #f0f0f0}}
.dato .ic{{flex:none;width:24px;text-align:center;color:{VERDE};font-size:17px}}

"""

AV_COL = ["#c8607a", "#3d8bfd", "#f2a516", "#2e9d5b", "#8a5a3c", "#6f42c1", "#20a3a3"]


def est():
    return '<div class="est"><span>9:41</span><i>PANTALLA DE PRÁCTICA</i><span>▮▮▮ 82%</span></div>'


def cab(titulo, iconos=("🔍", "⋮"), atras=False, sub="", av="", obj=None):
    ics = "".join(f'<span class="ic"{" id=objetivo" if obj == k else ""}>{i}</span>' for k, i in enumerate(iconos))
    a = '<span class="ic" style="margin-left:-6px">←</span>' if atras else ""
    avh = f'<span class="av">{av}</span>' if av else ""
    s = f"<small>{sub}</small>" if sub else ""
    return f'<div class="cab">{a}{avh}<h1>{titulo}{s}</h1>{ics}</div>'


def chat(k, nombre, msj, hora, etiqueta=None, obj=False, sel=False):
    e = f'<div class="et"><b style="background:{ETI[etiqueta]}"></b>{etiqueta}</div>' if etiqueta else ""
    return (f'<div class="chat{" sel" if sel else ""}"{" id=objetivo" if obj else ""}><span class="av" style="background:{AV_COL[k % 7]}">{nombre[0]}</span>'
            f'<div class="tx"><div class="f1">{nombre}<span>{hora}</span></div><div class="f2">{html.escape(msj)}</div>{e}</div></div>')


CHATS_CAMILO = [("Laura · Conjunto Ducales", "Ya te pagué por Nequi 👍", "6:12 p. m.", None),
                ("Don Hernán", "¿Tiene cargador tipo C?", "5:40 p. m.", "Nuevo cliente"),
                ("Yesica", "Mándame el forro azul, porfa", "5:02 p. m.", "Nuevo pedido"),
                ("Mamá", "¿Vienes a almorzar el domingo?", "4:15 p. m.", None),
                ("Brayan", "Listo, mañana le consigno", "3:30 p. m.", "Pago pendiente"),
                ("Paola · Torre 4", "Gracias, llegó perfecto", "1:05 p. m.", "Entregado"),
                ("Andrea", "¿Cuánto valen los audífonos?", "12:20 p. m.", None)]


def lista_chats(obj_chat=None, sel=None, etiquetas=True, chips=("Todos", "No leídos", "Pago pendiente", "Pagado"), obj_chip=None, filtro=None, cab_obj=None):
    ch = "".join(f'<span class="chip{" on" if (filtro or "Todos") == c else ""}"{" id=objetivo" if obj_chip == c else ""}>{c}</span>' for c in chips)
    filas = [(k, x) for k, x in enumerate(CHATS_CAMILO) if not filtro or x[3] == filtro]
    if filtro == "Pago pendiente":
        filas = [(4, CHATS_CAMILO[4]), (7, ("Julián", "Dale, ya mismo te transfiero", "Ayer", "Pago pendiente"))]
    cuerpo = "".join(chat(k, n, m, h, e if etiquetas else None, obj=(obj_chat == k), sel=(sel == k)) for k, (n, m, h, e) in filas)
    return est() + cab("Accesorios Camilo", obj=cab_obj) + f'<div class="chips">{ch}</div>' + cuerpo + '<div class="fab">💬</div>'


HERRAMIENTAS = [("🏪", "Perfil de empresa", "Nombre, descripción, horario"), ("🛍", "Catálogo", "Muestra tus productos y servicios"),
                ("🏷", "Etiquetas", "Organiza tus chats y clientes"), ("👋", "Mensaje de bienvenida", "Saluda a quien te escribe por primera vez"),
                ("🌙", "Mensaje de ausencia", "Responde cuando no estás disponible"), ("⚡", "Respuestas rápidas", "Guarda y reutiliza mensajes")]


def herramientas(obj):
    filas = "".join(f'<div class="item"{" id=objetivo" if n == obj else ""}><span class="ic">{i}</span><div><b>{n}</b><small>{s}</small></div></div>'
                    for i, n, s in HERRAMIENTAS)
    return est() + cab("Herramientas para la empresa", iconos=(), atras=True) + '<div class="sec">Administra tu negocio</div>' + filas


def menu(obj):
    ops = ["Herramientas para la empresa", "Nuevo grupo", "Nueva difusión", "Dispositivos vinculados", "Mensajes destacados", "Ajustes"]
    return '<div class="velo"></div><div class="menu">' + "".join(f'<div{" id=objetivo" if o == obj else ""}>{o}</div>' for o in ops) + "</div>"


def chats_sandra(cab_obj=None):
    filas = [("Clienta · Marcela", "¿Tienes torta para el sábado?", "8:05 p. m."), ("Tía Rosa", "Sandrita, ¿cómo va todo?", "7:50 p. m."),
             ("Don Jorge", "¿Cuánto vale la de tres leches?", "7:31 p. m."), ("Grupo Familia 💛", "Carlos: jajaja", "7:20 p. m."),
             ("Natalia", "¿Hace domicilio a Ciudad Verde?", "6:58 p. m."), ("Proveedor harinas", "Mañana le llevo el pedido", "5:12 p. m.")]
    cuerpo = "".join(chat(k, n, m, h) for k, (n, m, h) in enumerate(filas))
    return est() + cab("Dulce Sandra", obj=cab_obj) + '<div class="chips"><span class="chip on">Todos</span><span class="chip">No leídos</span><span class="chip">Grupos</span></div>' + cuerpo + '<div class="fab">💬</div>'


TORTAS = [("Torta de chocolate para 12", "Bizcocho húmedo con ganache. Pídela con 2 días.", "$65.000", "linear-gradient(135deg,#4a2a1a,#7a4a2c)"),
          ("Torta tres leches para 10", "La de siempre, con canela. Pídela con 1 día.", "$55.000", "linear-gradient(135deg,#f6e7c8,#e9cf9a)"),
          ("Cheesecake de maracuyá", "Para 8 porciones. Domicilio en Soacha.", "$60.000", "linear-gradient(135deg,#f7d14a,#f3eccd)"),
          ("Caja de 12 brownies", "Con nueces o sin nueces.", "$36.000", "linear-gradient(135deg,#3b2316,#6a412a)")]


def catalogo(productos, obj=None):
    if not productos:
        cuerpo = ('<div style="text-align:center;padding:40px 30px 0;color:#666;font-size:14px"><div style="font-size:54px">🛍</div>'
                  '<b style="display:block;color:#111;font-size:17px;margin:10px 0 6px">Crea tu catálogo</b>Muestra tus productos para que tus clientes los vean y te pidan.</div>'
                  f'<div class="btn"{" id=objetivo" if obj == "nuevo" else ""}>＋ Añadir artículo nuevo</div>')
    else:
        cuerpo = (f'<div class="item"{" id=objetivo" if obj == "nuevo" else ""}><span class="ic">＋</span><div><b>Añadir artículo nuevo</b></div></div>' +
                  "".join(f'<div class="prod"><span class="im" style="background:{g}"></span><div><b>{n}</b><small>{d}</small><span>{p}</span></div></div>' for n, d, p, g in productos))
    return est() + cab("Catálogo", iconos=("⋮",), atras=True) + cuerpo


def formulario_producto(obj="guardar"):
    return (est() + cab("Añadir artículo", iconos=(), atras=True) +
            '<div class="foto"><span>🎂</span>Foto 1 de 1 · luz de día, fondo limpio</div>' +
            '<div class="campo"><small>Nombre del artículo</small>Torta de chocolate para 12</div>' +
            '<div class="campo"><small>Precio (opcional)</small>$ 65.000</div>' +
            '<div class="campo"><small>Descripción (opcional)</small>Bizcocho húmedo con ganache. Pídela con 2 días. Domicilio en Soacha.</div>' +
            '<div class="campo gris"><small>Código del artículo (opcional)</small>&nbsp;</div>' +
            f'<div class="btn"{" id=objetivo" if obj == "guardar" else ""}>Guardar</div>')


def seleccion_chat(obj="etiqueta"):
    barra = ('<div class="cab" style="background:#155c45"><span class="ic">←</span><h1>1</h1>'
             f'<span class="ic">📌</span><span class="ic"{" id=objetivo" if obj == "etiqueta" else ""}>🏷</span><span class="ic">🗑</span><span class="ic">⋮</span></div>')
    cuerpo = "".join(chat(k, n, m, h, e, sel=(k == 0)) for k, (n, m, h, e) in enumerate(CHATS_CAMILO))
    return est() + barra + '<div class="chips"><span class="chip on">Todos</span><span class="chip">No leídos</span><span class="chip">Pago pendiente</span><span class="chip">Pagado</span></div>' + cuerpo


def hoja_etiquetas(marcada=None, obj=None):
    ops = "".join(f'<div class="op"{" id=objetivo" if obj == n else ""}><b style="background:{c}"></b>{n}<span class="ck{" on" if n == marcada else ""}">{"✓" if n == marcada else ""}</span></div>'
                  for n, c in ETI.items())
    btn = f'<div class="btn"{" id=objetivo" if obj == "guardar" else ""}>Guardar</div>'
    return seleccion_chat(obj=None) + '<div class="velo" style="background:rgba(0,0,0,.35)"></div>' + f'<div class="hoja"><h3>Etiquetar chat</h3>{ops}{btn}</div>'


def chat_vista(nombre, sub, mensajes, entrada="Mensaje", escrito=False, sug=None, obj=None):
    bur = "".join(f'<div class="dia">{t}</div>' if q == "dia" else
                  f'<div class="bur {q}">{"<span class=auto>Mensaje automático</span>" if auto else ""}{html.escape(t)}<em>{h}</em></div>'
                  for q, t, h, auto in mensajes)
    s = ""
    if sug:
        s = '<div class="sug">' + "".join(f'<div{" id=objetivo" if obj == a else ""}><b>/{a}</b>{html.escape(t)}</div>' for a, t in sug) + "</div>"
    caja = f'<div class="caja{" esc" if escrito else ""}">😊 <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{html.escape(entrada)}</span>📎</div>'
    env = f'<div class="env"{" id=objetivo" if obj == "enviar" else ""}>{"➤" if escrito else "🎤"}</div>'
    return est() + cab(nombre, iconos=("📞", "⋮"), atras=True, sub=sub, av=nombre[0]) + f'<div class="fondo">{bur}</div>{s}<div class="entrada">{caja}{env}</div>'


RESPUESTAS = [("gracias", "¡Gracias por tu compra! Que lo disfrutes 🍊"),
              ("domicilio", "¡Hola! Llevamos a domicilio en Soacha de 7 a. m. a 6 p. m. El envío vale $3.000. ¿Qué te mandamos hoy?"),
              ("horario", "Atendemos de lunes a sábado de 7 a. m. a 6 p. m."),
              ("pagos", "Recibimos efectivo, Nequi y Daviplata al 300 000 0000.")]


def respuestas(lista, obj=None):
    filas = "".join(f'<div class="item"><span class="ic">⚡</span><div><b>/{a}</b><small>{html.escape(t)}</small></div></div>' for a, t in lista)
    return est() + cab("Respuestas rápidas", iconos=(), atras=True) + filas + f'<div class="fab"{" id=objetivo" if obj == "mas" else ""}>＋</div>'


def nueva_respuesta(obj="guardar"):
    return (est() + cab("Respuesta rápida", iconos=(), atras=True) +
            '<div class="campo" style="min-height:96px"><small>Mensaje</small>¡Hola! Llevamos a domicilio en Soacha de 7 a. m. a 6 p. m. El envío vale $3.000. ¿Qué te mandamos hoy?</div>' +
            '<div class="campo"><small>Atajo</small>/domicilio</div>' +
            '<p style="font-size:12.5px;color:#777;margin:10px 18px">Escribe / en un chat y elige el atajo para enviar este mensaje.</p>' +
            f'<div class="btn"{" id=objetivo" if obj == "guardar" else ""}>Guardar</div>')


def perfil_sandra():
    datos = [("🏷", "Repostería"), ("📝", "Tortas y postres por encargo para cumpleaños, primeras comuniones y oficinas. Pide con 2 días."),
             ("📍", "Hogares Soacha · Domicilio en Soacha"), ("🕘", "Abierto hoy · 8:00 a. m. a 7:00 p. m."), ("✉", "dulcesandra@correo.com")]
    return (est() + cab("Perfil de empresa", iconos=(), atras=True) +
            '<div class="perfil"><div class="av">🎂</div><h2>Dulce Sandra</h2><small>Cuenta de empresa</small></div>' +
            '<div class="btn lin" style="margin:6px 16px 10px">🛍 Ver catálogo</div>' +
            "".join(f'<div class="dato"><span class="ic">{i}</span><span>{t}</span></div>' for i, t in datos))


def doc(cuerpo, titulo):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title><style>{CSS}</style></head><body>{cuerpo}</body></html>'


# ---------------------------------------------------------------- simuladores (Practica)
CHAT_ESP = [("dia", "HOY", "", False), ("el", "Buenas, ¿hacen domicilio a El Altico?", "6:02 a. m.", False)]
SIMULADORES = {
    1: dict(titulo="Agrega un producto a tu catálogo", final="Ahora hazlo en tu celular con tus 3 productos que más vendes: eso es el paso Aplica.", pasos=[
        ("Abre el menú de la app (los tres puntos de arriba).", "Busca los tres puntos en la esquina de arriba, a la derecha.", chats_sandra(cab_obj=1)),
        ("Entra a «Herramientas para la empresa».", "Es la primera opción del menú.", chats_sandra() + menu("Herramientas para la empresa")),
        ("Abre el «Catálogo».", "Está en la lista, debajo de «Perfil de empresa».", herramientas("Catálogo")),
        ("Agrega tu primer producto.", "Toca el botón verde para añadir un artículo nuevo.", catalogo([], obj="nuevo")),
        ("Ya llenaste foto, nombre, precio y descripción. Guarda el producto.", "El botón para guardar está debajo de los campos.", formulario_producto()),
    ]),
    2: dict(titulo="Ponle la etiqueta a un cliente que ya pagó", final="Ahora ponle etiqueta a todos los chats de clientes de esta semana: eso es el paso Aplica.", pasos=[
        ("Laura ya le pagó a Camilo por Nequi. Selecciona su chat (mantenlo presionado).", "Es el primer chat de la lista: «Ya te pagué por Nequi».", lista_chats(obj_chat=0)),
        ("Toca el ícono de etiqueta.", "Está arriba, en la barra verde, junto al alfiler.", seleccion_chat()),
        ("Elige la etiqueta que va: ya pagó, pero falta entregar.", "Si ya pagó y no le ha entregado, la etapa es «Pagado».", hoja_etiquetas(obj="Pagado")),
        ("Guarda la etiqueta.", "El botón para guardar está al final de la lista.", hoja_etiquetas(marcada="Pagado", obj="guardar")),
        ("Es hora de cobrar. Muestra solo los clientes que todavía no han pagado.", "Busca el filtro arriba de los chats.", lista_chats(obj_chip="Pago pendiente")),
    ]),
    3: dict(titulo="Crea y usa una respuesta rápida", final="Ahora crea tus 3 respuestas rápidas y tu mensaje de bienvenida y de ausencia: eso es el paso Aplica.", pasos=[
        ("Abre «Respuestas rápidas».", "Está al final de la lista de herramientas.", herramientas("Respuestas rápidas")),
        ("Crea una respuesta nueva.", "Toca el botón verde de abajo a la derecha.", respuestas(RESPUESTAS[:1], obj="mas")),
        ("Ya escribiste el mensaje y el atajo /domicilio. Guárdala.", "El botón para guardar está debajo del atajo.", nueva_respuesta()),
        ("Un cliente pregunta por el domicilio. Ya escribiste / : elige la respuesta que va.", "Busca el atajo que habla del domicilio.",
         chat_vista("Julián", "en línea", CHAT_ESP, entrada="/", escrito=True, sug=RESPUESTAS[1:], obj="domicilio")),
        ("La respuesta quedó escrita. Envíala.", "El botón de enviar es el círculo verde.", chat_vista("Julián", "en línea", CHAT_ESP, entrada=RESPUESTAS[1][1], escrito=True, obj="enviar")),
    ]),
}

# ---------------------------------------------------------------- vistas para Aprende (4:3)
VISTAS = {
    "u1-perfil": ("piezas/u1-aprende/medios/ilustracion-3.jpg", perfil_sandra()),
    "u1-catalogo": ("piezas/u1-aprende/medios/ilustracion-4.jpg", catalogo(TORTAS)),
    "u2-etiquetas": ("piezas/u2-aprende/medios/ilustracion-2.jpg", lista_chats()),
    "u3-bienvenida": ("piezas/u3-aprende/medios/ilustracion-2.jpg", chat_vista("Natalia", "en línea", [
        ("dia", "HOY", "", False), ("el", "Buenas", "6:58 p. m.", False),
        ("yo", "¡Hola! Soy Esperanza, frutas y verduras a domicilio en El Altico 🍊🥑 Mira el catálogo y dime qué necesitas.", "6:58 p. m.", True)])),
    "u3-respuestas": ("piezas/u3-aprende/medios/ilustracion-4.jpg", chat_vista("Julián", "en línea", CHAT_ESP, entrada="/", escrito=True, sug=RESPUESTAS[1:])),
}
VISTA_CSS = """html,body{margin:0}body.v{width:800px;height:600px;background:linear-gradient(160deg,#f6f6f7,#e9e9ec);display:flex;align-items:center;justify-content:center;overflow:hidden}
.tel{width:259px;height:547px;border:8px solid #141414;border-radius:30px;overflow:hidden;background:#fff;box-shadow:0 10px 40px rgba(0,0,0,.22)}
.tel iframe{width:360px;height:760px;border:0;display:block;transform:scale(.7208);transform-origin:0 0}"""

(AQUI / "practica").mkdir(exist_ok=True)
(AQUI / "vistas").mkdir(exist_ok=True)
spec = {"simuladores": {}, "vistas": {}}
for u, s in SIMULADORES.items():
    pasos = []
    for k, (ins, pista, cuerpo) in enumerate(s["pasos"], 1):
        assert 'id=objetivo' in cuerpo, (u, k)
        (AQUI / "practica" / f"u{u}-{k}.html").write_text(doc(cuerpo, f"U{u} paso {k}"), encoding="utf-8")
        pasos.append({"html": f"practica/u{u}-{k}.html", "imagen": f"pantalla-{k}.jpg", "instruccion": ins, "pista": pista})
    spec["simuladores"][u] = {"titulo": s["titulo"], "final": s["final"], "pasos": pasos}
for v, (destino, cuerpo) in VISTAS.items():
    (AQUI / "vistas" / f"{v}-pantalla.html").write_text(doc(cuerpo, v), encoding="utf-8")
    (AQUI / "vistas" / f"{v}.html").write_text(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{VISTA_CSS}</style></head><body class="v"><div class="tel"><iframe src="{v}-pantalla.html"></iframe></div></body></html>', encoding="utf-8")
    spec["vistas"][v] = {"html": f"vistas/{v}.html", "destino": destino}
(AQUI / "pantallas.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["pasos"]) for s in SIMULADORES.values()), "pantallas de práctica,", len(VISTAS), "vistas")
