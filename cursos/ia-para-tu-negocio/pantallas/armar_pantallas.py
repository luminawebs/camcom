"""Arma las pantallas simplificadas de un asistente de IA genérico (HTML) y la especificación de cada simulador.
Uso: python3 armar_pantallas.py && node renderizar.mjs
- practica/uN-K.html  -> pantallas del simulador (9:19). El elemento con id="objetivo" es la zona que se toca;
  renderizar.mjs la mide y escribe piezas/uN-practica/contenido.js con las zonas en porcentaje.
- vistas/<id>.html    -> imágenes 4:3 para las lecciones Aprende (piezas/uN-aprende/medios/ilustracion-K.jpg).
No son capturas reales ni de una app en particular: es un asistente sin marca («Asistente») con los botones
que tienen casi todos (nuevo chat, adjuntar, enviar, copiar, ajustes › controles de datos). Los nombres de los menús
cambian en cada app y versión: [VERIFICAR] con el asesor. Hecho a partir de pantallas/ del curso de WhatsApp Business.
"""
import html, json, pathlib

AQUI = pathlib.Path(__file__).parent
TINTA, ACENTO, GRIS = "#141414", "#c8102e", "#f2f2f4"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:360px;height:760px;overflow:hidden;font-family:Roboto,Inter,'DejaVu Sans',sans-serif;background:#fff;color:#111;position:relative}}
.est{{height:24px;background:#fff;color:#333;font-size:11px;display:flex;justify-content:space-between;align-items:center;padding:0 12px}}
.est i{{font-style:normal;background:#ececef;border-radius:8px;padding:1px 7px;font-size:9.5px;letter-spacing:.04em;color:#555}}
.cab{{height:54px;display:flex;align-items:center;gap:8px;padding:0 8px;border-bottom:1px solid #eee}}
.cab h1{{font-size:18px;font-weight:600;flex:1;display:flex;align-items:center;gap:6px}}
.cab h1 .lg{{color:{ACENTO};font-size:18px}}
.cab .ic{{width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-size:20px;border-radius:50%;color:#333}}
.vacio{{position:absolute;top:150px;left:0;right:0;text-align:center;padding:0 30px}}
.vacio .lg{{font-size:40px;color:{ACENTO}}}
.vacio h2{{font-size:22px;font-weight:600;margin-top:10px}}
.vacio p{{font-size:13.5px;color:#777;margin-top:6px}}
.conv{{position:absolute;top:78px;bottom:70px;left:0;right:0;padding:14px 14px;display:flex;flex-direction:column;gap:12px;overflow:hidden}}
.yo{{align-self:flex-end;max-width:84%;background:{GRIS};border-radius:18px 18px 4px 18px;padding:10px 13px;font-size:14px;line-height:1.38}}
.yo .adj{{display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:12px;color:#555}}
.yo .adj b{{width:44px;height:44px;border-radius:8px;background:linear-gradient(135deg,#ffe9a8,#f5c84c);display:flex;align-items:center;justify-content:center;font-size:22px}}
.ia{{align-self:stretch;display:flex;gap:10px;font-size:14px;line-height:1.42}}
.ia .lg{{flex:none;width:26px;height:26px;border-radius:50%;background:#fde8eb;color:{ACENTO};display:flex;align-items:center;justify-content:center;font-size:14px;margin-top:1px}}
.ia .tx{{flex:1;min-width:0}}
.ia .tx p+p{{margin-top:7px}}
.ia .acc{{display:flex;gap:4px;margin-top:8px;color:#666}}
.ia .acc span{{width:34px;height:30px;display:flex;align-items:center;justify-content:center;font-size:15px;border-radius:8px}}
.inv{{background:#fde8eb;text-decoration:underline wavy {ACENTO};text-underline-offset:3px;border-radius:3px;padding:0 2px}}
.chips{{position:absolute;left:0;right:0;bottom:72px;display:flex;gap:8px;padding:0 12px;overflow:hidden}}
.chip{{border:1px solid #d6d6db;border-radius:16px;font-size:13px;padding:7px 12px;white-space:nowrap;background:#fff}}
.entrada{{position:absolute;left:0;right:0;bottom:0;padding:10px 10px 14px;background:#fff}}
.entrada .caja{{display:flex;align-items:flex-end;gap:6px;border:1px solid #d6d6db;border-radius:24px;padding:6px;min-height:48px}}
.entrada .mas{{flex:none;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;color:#444}}
.entrada .txt{{flex:1;min-width:0;font-size:14px;color:#999;padding:8px 2px;line-height:1.35}}
.entrada .txt.esc{{color:#111;max-height:96px;overflow:hidden}}
.entrada .env{{flex:none;width:36px;height:36px;border-radius:50%;background:#e4e4e8;color:#888;display:flex;align-items:center;justify-content:center;font-size:17px}}
.entrada .env.on{{background:{TINTA};color:#fff}}
.velo{{position:absolute;inset:0;background:rgba(0,0,0,.35);z-index:2}}
.hoja{{position:absolute;left:0;right:0;bottom:0;background:#fff;border-radius:18px 18px 0 0;box-shadow:0 -4px 16px rgba(0,0,0,.2);padding:8px 0 16px;z-index:3}}
.hoja .asa{{width:40px;height:4px;border-radius:2px;background:#ccc;margin:2px auto 6px}}
.hoja h3{{font-size:16.5px;font-weight:600;padding:8px 18px 4px}}
.hoja .sub{{font-size:12.5px;color:#777;padding:0 18px 6px}}
.nota{{margin:8px 14px 0;border:1px solid #e2e2e5;border-radius:12px;padding:10px 12px;font-size:13px;line-height:1.38}}
.nota small{{display:block;font-size:11px;color:#888;margin-bottom:3px;text-transform:uppercase;letter-spacing:.05em}}
.gal{{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding:8px 14px}}
.gal div{{aspect-ratio:1;border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:30px;gap:2px}}
.gal small{{font-size:10px;color:#444;background:rgba(255,255,255,.75);border-radius:6px;padding:0 4px}}
.cajon{{position:absolute;top:0;bottom:0;left:0;width:280px;background:#fff;z-index:3;box-shadow:4px 0 16px rgba(0,0,0,.2);padding-top:24px}}
.cajon .tit{{display:flex;align-items:center;gap:8px;padding:16px 18px;font-size:18px;font-weight:600}}
.cajon .tit .lg{{color:{ACENTO}}}
.cajon .op{{display:flex;align-items:center;gap:14px;padding:12px 18px;font-size:15px}}
.cajon .op .ic{{width:22px;text-align:center;color:#555}}
.cajon .sec{{font-size:12px;color:#888;padding:14px 18px 4px;text-transform:uppercase;letter-spacing:.05em}}
.cajon .pie{{position:absolute;left:0;right:0;bottom:16px;border-top:1px solid #eee}}
.item{{display:flex;gap:14px;align-items:center;padding:14px 18px;border-bottom:1px solid #f2f2f2}}
.item .ic{{flex:none;width:28px;text-align:center;font-size:19px;color:#444}}
.item b{{display:block;font-size:15.5px;font-weight:500}}
.item small{{display:block;font-size:12.5px;color:#777;margin-top:2px;line-height:1.3}}
.item .sw{{margin-left:auto;flex:none;width:46px;height:26px;border-radius:13px;background:{TINTA};position:relative}}
.item .sw:after{{content:"";position:absolute;right:3px;top:3px;width:20px;height:20px;border-radius:50%;background:#fff}}
.item .sw.off{{background:#c9c9ce}}.item .sw.off:after{{right:auto;left:3px}}
.aviso{{margin:14px 16px;font-size:12.5px;color:#666;line-height:1.4}}
"""

LG = "✦"


def est():
    return '<div class="est"><span>9:41</span><i>PANTALLA DE PRÁCTICA</i><span>▮▮▮ 76%</span></div>'


def cab(obj=None):
    o = lambda k: ' id="objetivo"' if obj == k else ""
    return (f'<div class="cab"><span class="ic"{o("menu")}>☰</span><h1><span class="lg">{LG}</span>Asistente</h1>'
            f'<span class="ic"{o("nuevo")}>✎</span></div>')


def cab_simple(titulo):
    return f'<div class="cab"><span class="ic">←</span><h1>{titulo}</h1></div>'


def entrada(texto="", obj=None):
    o = lambda k: ' id="objetivo"' if obj == k else ""
    t = f'<div class="txt esc">{html.escape(texto)}</div>' if texto else '<div class="txt">Pregunta lo que quieras</div>'
    env = f'<div class="env{" on" if texto else ""}"{o("enviar")}>{"↑" if texto else "🎤"}</div>'
    return f'<div class="entrada"><div class="caja"><span class="mas"{o("mas")}>＋</span>{t}{env}</div></div>'


def yo(texto, adjunto=None):
    a = f'<div class="adj"><b>{adjunto[0]}</b>{adjunto[1]}</div>' if adjunto else ""
    return f'<div class="yo">{a}{html.escape(texto)}</div>'


def ia(parrafos, obj_copiar=False, crudo=False):
    ps = "".join(f"<p>{p if crudo else html.escape(p)}</p>" for p in parrafos)
    acc = f'<div class="acc"><span{" id=objetivo" if obj_copiar else ""}>⧉</span><span>↻</span><span>👍</span><span>👎</span></div>'
    return f'<div class="ia"><span class="lg">{LG}</span><div class="tx">{ps}{acc}</div></div>'


def conv(*burbujas):
    return f'<div class="conv">{"".join(burbujas)}</div>'


def doc(cuerpo, titulo):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title><style>{CSS}</style></head><body>{cuerpo}</body></html>'


def inicio(obj=None, texto="", obj_ent=None):
    return (est() + cab(obj) + f'<div class="vacio"><div class="lg">{LG}</div><h2>¿En qué te ayudo hoy?</h2>'
            '<p>Escribe o háblale. Revisa siempre lo que te responde.</p></div>' + entrada(texto, obj_ent))


def hoja_notas(titulo, sub, notas, obj):
    filas = "".join(f'<div class="nota"{" id=objetivo" if k == obj else ""}><small>Pedido {k + 1}</small>{html.escape(n)}</div>' for k, n in enumerate(notas))
    return f'<div class="velo"></div><div class="hoja"><div class="asa"></div><h3>{titulo}</h3><div class="sub">{sub}</div>{filas}</div>'


# ---------------------------------------------------------------- textos de los casos
FLOJO = "haz un aviso"
FLOJO_R = ["¡Claro! Aquí tienes un aviso:",
           "🔥 ¡GRAN OFERTA EXCLUSIVA! 🔥 Descubre nuestra increíble selección de productos de la más alta calidad a precios inigualables. ¡50 % de descuento en toda la tienda solo por hoy!",
           "No te pierdas esta oportunidad única. ¡Visítanos y vive una experiencia de compra inolvidable!"]
NELSON = ("Tengo una ferretería en Quintanares, Soacha. Escribe un aviso para el grupo de WhatsApp del barrio, para vecinos que arreglan "
          "la casa el fin de semana. Corto, amable, con el horario del sábado de 7 a. m. a 6 p. m.")
NELSON_LARGO = ["¡Hola, vecinos de Quintanares! 👋",
                "¿Este fin de semana toca arreglar algo en la casa? En la Ferretería de Nelson tenemos pintura, tubería, cerraduras, tornillería y la herramienta que necesites para dejar todo listo.",
                "Te asesoramos sin compromiso para que compres solo lo que vas a usar. Abrimos el sábado de 7 a. m. a 6 p. m. ¡Te esperamos aquí en el barrio!"]
NELSON_CORTO = ["🔨 Ferretería de Nelson · Quintanares", "¿Arreglos en casa este fin de semana? Tenemos pintura, tubería y herramienta.",
                "Sábado de 7 a. m. a 6 p. m.", "¡Lo atendemos como vecino!"]
NOTAS_U1 = ["Aviso ferretería", NELSON, "Escribe algo para vender más este fin de semana"]

LEIDY = ("Vendo ropa de bebé por WhatsApp en Soacha. Escribe la descripción de este enterizo para mi catálogo: algodón, tallas 0-3 y "
         "3-6 meses, $38.000. Para mamás primerizas, tono cálido, 3 líneas.")
LEIDY_R = ["Enterizo amarillo de algodón, suavecito para la piel de tu bebé y fácil de poner con sus broches.",
           '<span id="objetivo" class="{c}">Certificado 100 % orgánico y antialérgico.</span>',
           "Tallas 0-3 y 3-6 meses · $38.000. ¡Ideal para sus primeros días en casa! 💛"]
LEIDY_OK = ["Enterizo amarillo de algodón, suavecito para la piel de tu bebé y fácil de poner con sus broches.",
            "Tallas 0-3 y 3-6 meses · $38.000. ¡Ideal para sus primeros días en casa! 💛"]
GALERIA = [("🧸", "Gorro", "#e7e1f6"), ("🧦", "Medias", "#dff0f7"), ("👶", "Enterizo", "#fff1bf"),
           ("🎀", "Body rosado", "#fbe0e8"), ("🧺", "Pedido", "#ece6dc"), ("🏠", "Casa", "#e3efe3")]
RECLAMO = ("Una clienta dice que el body le llegó descosido y está brava. Escríbele una respuesta amable: le pido disculpas, "
           "se lo cambio sin costo y paso a recogerlo mañana. Tuteando, corto.")
RECLAMO_R = ["¡Hola! Qué pena contigo, tienes toda la razón: el body no debió llegarte así. 🙏",
             "Te lo cambio sin ningún costo. Mañana paso a recogerlo y te dejo uno nuevo. ¿A qué hora te queda bien?",
             "Gracias por avisarme y por la paciencia. 💛"]

YANETH_MAL = "Mensajes de cumpleaños para: María Pérez, CC 1.012.345.678, cel. 310 555 0000, alérgica al tinte; Luz Gómez, CC 52.…"
YANETH = ("Tengo una peluquería en Soacha. Escribe un mensaje de cumpleaños corto y cariñoso para una clienta que viene cada mes a "
          "arreglarse las uñas. Que diga que en su mes tiene 20 % en manicure. Deja [nombre] para ponerlo yo.")
YANETH_R = ["¡Feliz cumpleaños, [nombre]! 🎉", "Gracias por dejarnos consentirte cada mes. Este es tu mes: tienes 20 % en tu manicure. 💅",
            "¡Te esperamos para celebrarlo!"]
NOTAS_U3 = [YANETH_MAL, YANETH, "Te paso la lista de todas mis clientas con sus celulares para que les escribas"]


def cajon(obj):
    ops = [("✎", "Nuevo chat"), ("🔍", "Buscar chats")]
    rec = ["Aviso ferretería", "Descripción enterizo", "Mensaje de cumpleaños"]
    return ('<div class="velo"></div><div class="cajon">' + f'<div class="tit"><span class="lg">{LG}</span>Asistente</div>' +
            "".join(f'<div class="op"><span class="ic">{i}</span>{t}</div>' for i, t in ops) +
            '<div class="sec">Chats recientes</div>' + "".join(f'<div class="op"><span class="ic">💬</span>{t}</div>' for t in rec) +
            f'<div class="pie"><div class="op"{" id=objetivo" if obj == "ajustes" else ""}><span class="ic">⚙</span>Ajustes</div></div></div>')


def ajustes(obj):
    filas = [("👤", "Cuenta", "Tu correo y tu plan"), ("🔔", "Notificaciones", ""), ("🎨", "Personalización", "Cómo quieres que te responda"),
             ("🛡", "Controles de datos", "Historial y uso de tus chats"), ("🎙", "Voz", "Habla con el asistente")]
    return est() + cab_simple("Ajustes") + "".join(
        f'<div class="item"{" id=objetivo" if t == obj else ""}><span class="ic">{i}</span><div><b>{t}</b>{f"<small>{s}</small>" if s else ""}</div></div>'
        for i, t, s in filas)


def controles(mejorar_on=True, obj=None):
    sw = f'<span class="sw{"" if mejorar_on else " off"}"{" id=objetivo" if obj == "mejorar" else ""}></span>'
    return (est() + cab_simple("Controles de datos") +
            f'<div class="item"><div><b>Mejorar el modelo para todos</b><small>Permite que tus chats se usen para entrenar el asistente.</small></div>{sw}</div>'
            '<div class="item"><div><b>Historial de chats</b><small>Guarda tus conversaciones en tu cuenta.</small></div><span class="sw"></span></div>'
            '<div class="item"><span class="ic">🗑</span><div><b>Borrar todos los chats</b><small>Elimina tus conversaciones guardadas.</small></div></div>'
            '<p class="aviso">En cada app esta opción se llama distinto. Búscala en Ajustes, en «Datos» o «Privacidad».</p>')


# ---------------------------------------------------------------- simuladores (Practica)
SIMULADORES = {
    1: dict(titulo="Pídele a la IA el aviso de Nelson", final="Ahora hazlo en tu celular con algo que necesites escribir esta semana: eso es el paso Aplica.", pasos=[
        ("Nelson abrió el asistente. Empieza una conversación nueva.", "Busca el lápiz arriba, a la derecha.",
         est() + cab("nuevo") + conv(yo("lista de precios de cemento"), ia(["Claro. Estos son precios de referencia del cemento gris por bulto…"])) + entrada()),
        ("Nelson guardó tres pedidos en sus notas. Pega el que tiene las 4 partes: quién es, qué necesita, para quién y cómo lo quiere.",
         "Es el que dice que es una ferretería en Quintanares.",
         inicio() + hoja_notas("Pegar desde tus notas", "Elige el pedido completo", NOTAS_U1, 1)),
        ("El pedido quedó escrito. Envíalo.", "El botón de enviar es la flecha negra.", inicio(texto=NELSON, obj_ent="enviar")),
        ("El aviso está bien, pero es largo para el grupo del barrio. Pídele un ajuste: toca la sugerencia que lo deja corto.",
         "Busca la sugerencia que habla de 4 líneas.",
         est() + cab() + conv(yo(NELSON), ia(NELSON_LARGO)) +
         '<div class="chips"><span class="chip">Más formal</span><span class="chip" id="objetivo">Más corto, en 4 líneas</span><span class="chip">En inglés</span></div>' + entrada()),
        ("Quedó listo. Copia el aviso para pegarlo en el grupo del barrio.", "El botón de copiar está debajo de la respuesta, a la izquierda.",
         est() + cab() + conv(yo("Más corto, en 4 líneas"), ia(NELSON_CORTO, obj_copiar=True)) + entrada()),
    ]),
    2: dict(titulo="Pide la descripción de un producto y revísala", final="Ahora pide la descripción de 2 de tus productos y revísalas antes de publicar: eso es el paso Aplica.", pasos=[
        ("Leidy quiere la descripción del enterizo amarillo. Adjunta la foto.", "El botón para adjuntar es el «+» de la caja de texto.", inicio(obj_ent="mas")),
        ("Elige la foto del enterizo.", "Es la foto amarilla con el bebé.",
         inicio() + '<div class="velo"></div><div class="hoja"><div class="asa"></div><h3>Fotos</h3><div class="gal">' +
         "".join(f'<div style="background:{c}"{" id=objetivo" if n == "Enterizo" else ""}>{e}<small>{n}</small></div>' for e, n, c in GALERIA) + "</div></div>"),
        ("Ya escribiste el pedido con tus datos reales: material, tallas, precio, para quién y cómo. Envíalo.", "El botón de enviar es la flecha negra.",
         est() + cab() + '<div class="conv"><div class="yo"><div class="adj"><b>👶</b>enterizo.jpg</div></div></div>' + entrada(LEIDY, "enviar")),
        ("Revisa la respuesta antes de usarla: toca el dato que la IA se inventó.", "Leidy nunca dijo que el enterizo fuera orgánico ni antialérgico.",
         est() + cab() + conv(yo(LEIDY, ("👶", "enterizo.jpg")), ia([LEIDY_R[0], LEIDY_R[1].format(c=""), LEIDY_R[2]], crudo=True)) + entrada()),
        ("Le pediste que quitara ese dato y lo corrigió. Copia la descripción para tu catálogo.", "El botón de copiar está debajo de la respuesta, a la izquierda.",
         est() + cab() + conv(yo("Quita lo de orgánico y antialérgico: no es cierto."), ia(LEIDY_OK, obj_copiar=True)) + entrada()),
    ]),
    3: dict(titulo="Cuida tus datos y pide sin datos personales", final="Ahora revisa los ajustes de tu asistente y reescribe un pedido sin datos de clientes: eso es el paso Aplica.", pasos=[
        ("Antes de pedir, Yaneth revisa la privacidad. Abre el menú del asistente.", "El menú son las tres rayas, arriba a la izquierda.", inicio(obj="menu")),
        ("Entra a «Ajustes».", "Está al final del menú.", inicio() + cajon("ajustes")),
        ("Entra a «Controles de datos».", "Es la opción del escudo.", ajustes("Controles de datos")),
        ("Apaga la opción que deja usar tus chats para entrenar el asistente.", "Es el primer interruptor: «Mejorar el modelo para todos».", controles(True, "mejorar")),
        ("Ahora sí: pega el pedido seguro para los mensajes de cumpleaños.", "El seguro no tiene nombres, cédulas, celulares ni datos de salud.",
         inicio() + hoja_notas("Pegar desde tus notas", "Elige el pedido sin datos personales", NOTAS_U3, 1)),
    ]),
}

# ---------------------------------------------------------------- vistas para Aprende (4:3)
VISTAS = {
    "u1-flojo": ("piezas/u1-aprende/medios/ilustracion-2.jpg", est() + cab() + conv(yo(FLOJO), ia(FLOJO_R)) + entrada()),
    "u1-bueno": ("piezas/u1-aprende/medios/ilustracion-3.jpg", est() + cab() + conv(yo(NELSON), ia(NELSON_CORTO)) + entrada()),
    "u2-inventa": ("piezas/u2-aprende/medios/ilustracion-3.jpg",
                   est() + cab() + conv(yo(LEIDY, ("👶", "enterizo.jpg")), ia([LEIDY_R[0], LEIDY_R[1].format(c="inv").replace(' id="objetivo"', ""), LEIDY_R[2]], crudo=True)) + entrada()),
    "u2-reclamo": ("piezas/u2-aprende/medios/ilustracion-4.jpg", est() + cab() + conv(yo(RECLAMO), ia(RECLAMO_R)) + entrada()),
    "u3-seguro": ("piezas/u3-aprende/medios/ilustracion-4.jpg", est() + cab() + conv(yo(YANETH), ia(YANETH_R)) + entrada()),
    "u3-ajustes": ("piezas/u3-aprende/medios/ilustracion-5.jpg", controles(False)),
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
        assert cuerpo.count('id="objetivo"') + cuerpo.count("id=objetivo") == 1, (u, k)
        (AQUI / "practica" / f"u{u}-{k}.html").write_text(doc(cuerpo, f"U{u} paso {k}"), encoding="utf-8")
        pasos.append({"html": f"practica/u{u}-{k}.html", "imagen": f"pantalla-{k}.jpg", "instruccion": ins, "pista": pista})
    spec["simuladores"][u] = {"titulo": s["titulo"], "final": s["final"], "pasos": pasos}
for v, (destino, cuerpo) in VISTAS.items():
    assert "objetivo" not in cuerpo, v
    (AQUI / "vistas" / f"{v}-pantalla.html").write_text(doc(cuerpo, v), encoding="utf-8")
    (AQUI / "vistas" / f"{v}.html").write_text(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{VISTA_CSS}</style></head><body class="v"><div class="tel"><iframe src="{v}-pantalla.html"></iframe></div></body></html>', encoding="utf-8")
    spec["vistas"][v] = {"html": f"vistas/{v}.html", "destino": destino}
(AQUI / "pantallas.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", sum(len(s["pasos"]) for s in SIMULADORES.values()), "pantallas de práctica,", len(VISTAS), "vistas")
