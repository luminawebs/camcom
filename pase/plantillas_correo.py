"""Correos del Pase con la marca del portal: Poppins, verde #00806b y el logo de EduNest.

Cada aviso sale en dos versiones (texto y HTML) y el logo va adjunto dentro del mensaje (cid:logo),
así se ve aunque el cliente de correo bloquee las imágenes remotas. El HTML usa tablas y estilos
en línea porque Gmail y Outlook ignoran casi todo el CSS de <style>.

    python -m pase.plantillas_correo CARPETA   escribe una vista previa .html de cada correo
"""
import datetime as dt
import html
import os
import sys

LOGO = os.path.join(os.path.dirname(__file__), "estaticos", "logo-correo.png")
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
         "octubre", "noviembre", "diciembre")

# Los mismos valores del sistema de diseño de las pantallas de pago.
ACENTO, SUAVE, TINTA, TINTA2 = "#00806b", "#e3f6f1", "#14181f", "#4a5260"
FONDO, BORDE = "#f6f7f9", "#dfe2e7"
AVISO = {"exito": (ACENTO, SUAVE), "error": ("#b42318", "#fef3f2"), "alerta": ("#93370d", "#fffaeb")}
LETRA = "Poppins,'Segoe UI',Helvetica,Arial,sans-serif"


def fecha_larga(valor):
    d = valor if isinstance(valor, dt.date) else dt.date.fromisoformat(str(valor)[:10])
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def pesos(centavos):
    return "$" + f"{centavos // 100:,}".replace(",", ".")


def medio_legible(enmascarado):
    """'457562******0326' → 'Tarjeta •••• 0326'; un texto sin números se deja igual."""
    numeros = "".join(ch for ch in (enmascarado or "") if ch.isdigit())
    if len(numeros) >= 4 and "*" in (enmascarado or ""):
        return f"Tarjeta •••• {numeros[-4:]}"
    return (enmascarado or "").strip()


def primer_nombre(nombre):
    return (nombre or "").strip().split(" ")[0].capitalize() or "emprendedor"


# ---------------------------------------------------------------- contenido de cada aviso
def _contenido(tipo, c, d):
    """Devuelve el contenido del aviso como datos; _html y _texto lo visten."""
    nombre = primer_nombre(d.get("nombre"))
    # Mis cursos: si la persona no ha entrado, Moodle le pide el login y luego la deja ahí
    aula = f'{c.moodle_url or "https://portal.edunest.co"}/my/courses.php'
    valor = pesos(c.precio_centavos)
    if tipo == "registro":
        return dict(
            asunto="Bienvenido al Aula Virtual Empresarial",
            previo="Tu registro gratuito está listo. Así entras por primera vez.",
            etiqueta="Registro gratuito", titulo=f"¡Bienvenido, {nombre}!",
            parrafos=["Tu registro en el Aula Virtual Empresarial de edunest.co está "
                      "listo. Ya puedes hacer gratis las tres primeras unidades de cada curso."],
            pasos=["Busca el correo del aula con tu contraseña. Puede tardar unos minutos; si no llega, "
                   "revisa la carpeta de spam o promociones.",
                   f"Entra con tu usuario <b>{html.escape(d.get('usuario') or '')}</b> y esa contraseña.",
                   "Empieza por el curso que más le sirva hoy a tu negocio."],
            boton=("Entrar al aula", aula),
            nota=f"¿Quieres los cursos completos y el certificado? Con el Pase Empresario ({valor} al mes) "
                 "desbloqueas las unidades 4 a 7 de todos los cursos.")
    if tipo == "pase_activo":
        filas = [("Plan", "Pase Empresario mensual"), ("Valor", f"{valor} al mes")]
        if medio_legible(d.get("medio")):
            filas.append(("Medio de pago", medio_legible(d["medio"])))
        if d.get("proximo_corte"):
            filas.append(("Próxima renovación", fecha_larga(d["proximo_corte"])))
        return dict(
            asunto="¡Ya tienes tu Pase Empresario!",
            previo="Tu pago fue aprobado. Ya tienes todos los cursos completos y el certificado.",
            etiqueta="Pago aprobado", estado="exito", titulo=f"¡Listo, {nombre}! Ya tienes tu Pase",
            parrafos=["Tu pago fue aprobado. Desde ahora tienes todas las unidades de todos los cursos y "
                      "puedes obtener tus certificados."],
            resumen=filas, boton=("Ir a mis cursos", aula),
            nota="Puedes cancelar cuando quieras: conservas el acceso hasta tu fecha de renovación y no "
                 "volvemos a cobrarte.",
            enlace=("Ver o cancelar mi Pase", d["enlace_cuenta"]) if d.get("enlace_cuenta") else None)
    if tipo == "pago_rechazado":
        return dict(
            asunto="Tu pago no se aprobó",
            previo="No se hizo ningún cobro. Puedes intentarlo de nuevo con otro medio.",
            etiqueta="Pago no aprobado", estado="error", titulo=f"{nombre}, tu pago no se aprobó",
            parrafos=["El banco o la billetera no aprobó el pago de tu Pase Empresario, así que "
                      "<b>no se hizo ningún cobro</b>. Tu registro gratuito sigue activo."],
            pasos=["Revisa que la tarjeta o la cuenta tenga cupo y esté habilitada para compras en línea.",
                   "Si sigue sin pasar, prueba con PSE, Nequi u otra tarjeta."],
            boton=("Intentar de nuevo", c.url_publica))
    if tipo == "cobro_fallido":
        return dict(
            asunto="No pudimos cobrar tu Pase",
            previo=f"Sigues con acceso. Lo intentaremos de nuevo el {fecha_larga(d['reintento'])}.",
            etiqueta="Renovación pendiente", estado="alerta", titulo=f"{nombre}, no pudimos cobrar tu Pase",
            parrafos=["Intentamos renovar tu Pase Empresario pero el pago no pasó. <b>Mientras tanto "
                      "sigues con acceso a todos tus cursos.</b>"],
            resumen=[("Valor", valor), ("Próximo intento", fecha_larga(d["reintento"]))]
            + ([("Medio de pago", medio_legible(d["medio"]))] if medio_legible(d.get("medio")) else []),
            pasos=["Revisa que tu tarjeta o cuenta tenga cupo antes de esa fecha; volveremos a intentarlo "
                   "solos.",
                   "Si después de los reintentos no logramos cobrar, el Pase se cierra, pero conservas tu "
                   "avance y tus cursos gratuitos."])
    if tipo == "renovar":
        filas = [("Vence el", fecha_larga(d["corte"])), ("Valor", valor)]
        return dict(
            asunto="Renueva tu Pase Empresario",
            previo=f"Tu Pase vence el {fecha_larga(d['corte'])}. Renuévalo en un minuto.",
            etiqueta="Renovación", titulo=f"{nombre}, es hora de renovar tu Pase",
            parrafos=["Tu Pase Empresario se renueva con un pago manual. Hazlo antes de la fecha para no "
                      "perder el acceso a las unidades 4 a 7 y a tus certificados."],
            resumen=filas, boton=("Renovar mi Pase", d["enlace"]),
            nota="El enlace es solo para ti; no lo compartas.")
    if tipo == "pase_termino":
        motivo = d.get("motivo") or ""
        if "reintento" in motivo or "sin pago" in motivo:
            causa = "No logramos renovar el pago, así que tu Pase Empresario se cerró."
        else:
            causa = "Tu Pase Empresario se cerró, como lo pediste."
        return dict(
            asunto="Tu Pase Empresario terminó",
            previo="Conservas tu avance y tus cursos gratuitos. Puedes volver cuando quieras.",
            etiqueta="Pase cerrado", titulo=f"{nombre}, tu Pase Empresario terminó",
            parrafos=[causa + " No volveremos a cobrarte.",
                      "<b>Conservas todo tu avance</b> y sigues teniendo gratis las tres primeras unidades "
                      "de cada curso. Si vuelves al Pase, retomas donde ibas."],
            boton=("Volver al Pase", c.url_publica), boton_secundario=True)
    if tipo == "cancelacion":
        return dict(
            asunto="Cancelaste tu Pase Empresario",
            previo=f"Sigues con todos los cursos hasta el {fecha_larga(d['corte'])}. No volveremos a cobrarte.",
            etiqueta="Cancelación recibida", titulo=f"{nombre}, cancelaste tu Pase",
            parrafos=["Recibimos tu solicitud. <b>No volveremos a cobrarte</b> y conservas todos los cursos "
                      "hasta tu fecha de corte.",
                      "Después de esa fecha sigues con tu avance y con las tres primeras unidades gratis de "
                      "cada curso."],
            resumen=[("Acceso completo hasta", fecha_larga(d["corte"])), ("Próximo cobro", "Ninguno")],
            boton=("Seguir con mi Pase", d["enlace_cuenta"]), boton_secundario=True,
            nota="¿No fuiste tú o cambiaste de opinión? Entra con el botón de arriba y elige «Seguir con mi "
                 "Pase» antes de esa fecha.")
    if tipo == "codigo":
        return dict(
            asunto=f"Tu código para entrar a Mi Pase: {d['codigo']}",
            previo=f"Vence en {d['minutos']} minutos. Si no lo pediste, ignora este correo.",
            etiqueta="Código de acceso", titulo=f"{nombre}, este es tu código",
            parrafos=[f'<span style="display:inline-block;padding:10px 18px;border-radius:12px;background:{SUAVE};'
                      f'color:{TINTA};font-size:30px;font-weight:700;letter-spacing:8px">'
                      f'{html.escape(d["codigo"])}</span>',
                      f"Escríbelo en la página de Mi Pase. Vence en {d['minutos']} minutos y sirve una sola vez.",
                      "Si no lo pediste, ignora este correo: nadie puede entrar sin el código."])
    if tipo == "interno":
        return dict(asunto=d["asunto"], previo=d["texto"], etiqueta="Aviso del Pase", titulo=d["asunto"],
                    parrafos=[html.escape(d["texto"])])
    if tipo == "prueba":
        return dict(asunto="Prueba del Pase Empresario", previo="Si lees esto, los avisos ya salen.",
                    etiqueta="Prueba", estado="exito", titulo="Los avisos del Pase ya salen por correo",
                    parrafos=["Si lees esto, el envío por Brevo funciona y el diseño de los correos se "
                              "ve en tu bandeja."])
    raise ValueError(f"aviso desconocido: {tipo}")


# ---------------------------------------------------------------- vestido
def _p(texto, color=TINTA2, tam=15, extra=""):
    return (f'<p style="margin:0 0 14px;font-family:{LETRA};font-size:{tam}px;line-height:1.6;'
            f'color:{color};{extra}">{texto}</p>')


def _boton(texto, url, secundario=False):
    fondo, color, borde = ("#ffffff", ACENTO, ACENTO) if secundario else (ACENTO, "#ffffff", ACENTO)
    u = html.escape(url, quote=True)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 22px">'
            f'<tr><td align="center" bgcolor="{fondo}" style="border-radius:12px;border:2px solid {borde}">'
            f'<a href="{u}" target="_blank" style="display:inline-block;padding:13px 28px;font-family:{LETRA};'
            f'font-size:16px;font-weight:600;color:{color};text-decoration:none;border-radius:12px">'
            f'{html.escape(texto)}</a></td></tr></table>')


def _html(k, c):
    color, fondo_et = AVISO.get(k.get("estado"), (TINTA2, FONDO))
    partes = [
        f'<div style="margin:0 0 18px"><span style="display:inline-block;padding:5px 12px;border-radius:999px;'
        f'background:{fondo_et};color:{color};font-family:{LETRA};font-size:12px;font-weight:600;'
        f'letter-spacing:.3px">{html.escape(k["etiqueta"])}</span></div>',
        f'<h1 style="margin:0 0 16px;font-family:{LETRA};font-size:24px;line-height:1.3;font-weight:700;'
        f'color:{TINTA}">{html.escape(k["titulo"])}</h1>']
    partes += [_p(t) for t in k["parrafos"]]
    if k.get("resumen"):
        filas = "".join(
            f'<tr><td style="padding:10px 16px;font-family:{LETRA};font-size:14px;color:{TINTA2};width:45%;'
            f'{"border-top:1px solid " + BORDE + ";" if i else ""}">{html.escape(a)}</td>'
            f'<td align="right" style="padding:10px 16px;font-family:{LETRA};font-size:14px;font-weight:600;'
            f'color:{TINTA};{"border-top:1px solid " + BORDE + ";" if i else ""}">{html.escape(b)}</td></tr>'
            for i, (a, b) in enumerate(k["resumen"]))
        partes.append(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
                      f'style="margin:6px 0 22px;background:{FONDO};border:1px solid {BORDE};border-radius:14px">'
                      f'{filas}</table>')
    if k.get("pasos"):
        filas = "".join(
            f'<tr><td valign="top" style="padding:0 12px 12px 0;width:28px"><div style="width:26px;height:26px;'
            f'border-radius:13px;background:{SUAVE};color:{ACENTO};font-family:{LETRA};font-size:13px;'
            f'font-weight:700;line-height:26px;text-align:center">{i}</div></td>'
            f'<td valign="top" style="padding:3px 0 12px;font-family:{LETRA};font-size:15px;line-height:1.55;'
            f'color:{TINTA2}">{t}</td></tr>' for i, t in enumerate(k["pasos"], 1))
        partes.append(f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
                      f'style="margin:4px 0 14px">{filas}</table>')
    if k.get("boton"):
        partes.append(_boton(*k["boton"], secundario=k.get("boton_secundario")))
    if k.get("nota"):
        partes.append(f'<div style="padding:14px 16px;border-radius:12px;background:{SUAVE};font-family:{LETRA};'
                      f'font-size:14px;line-height:1.55;color:{TINTA}">{k["nota"]}</div>')
    if k.get("enlace"):
        partes.append(f'<p style="margin:18px 0 0;font-family:{LETRA};font-size:14px"><a href="'
                      f'{html.escape(k["enlace"][1], quote=True)}" target="_blank" style="color:{ACENTO};'
                      f'font-weight:600;text-decoration:underline">{html.escape(k["enlace"][0])}</a></p>')
    cuerpo = "".join(partes)
    previo = html.escape(k["previo"])
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light">
<title>{html.escape(k["asunto"])}</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>@media (max-width:620px){{.tarjeta{{padding:28px 22px !important}}.marco{{padding:16px 10px !important}}}}</style>
</head><body style="margin:0;padding:0;background:{FONDO}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{previo}&#8199;&#847;&#8199;&#847;&#8199;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{FONDO}">
<tr><td class="marco" align="center" style="padding:32px 16px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px">
<tr><td style="padding:0 4px 18px"><img src="cid:logo" width="150" height="25" alt="edunest.co"
 style="display:block;border:0;width:150px;height:auto"></td></tr>
<tr><td style="background:#ffffff;border:1px solid {BORDE};border-radius:16px;overflow:hidden">
<div style="height:4px;background:{ACENTO};border-radius:16px 16px 0 0;font-size:0;line-height:0">&nbsp;</div>
<div class="tarjeta" style="padding:36px 40px 32px">{cuerpo}</div></td></tr>
<tr><td style="padding:22px 8px 0;font-family:{LETRA};font-size:12px;line-height:1.6;color:{TINTA2}" align="center">
<b style="color:{TINTA}">Aula Virtual Empresarial</b> · edunest.co<br>
Este correo sale de una dirección que no recibe respuestas.{_contacto(c)}
</td></tr></table></td></tr></table></body></html>"""


def _contacto(c):
    soporte = getattr(c, "correo_soporte", "")
    if not soporte:
        return ""
    s = html.escape(soporte)
    return (f'<br>¿Necesitas ayuda? Escríbenos a <a href="mailto:{s}" style="color:{ACENTO};'
            f'text-decoration:underline">{s}</a>.')


def _texto(k, c):
    import re
    limpio = lambda t: html.unescape(re.sub(r"<[^>]+>", "", t))  # noqa: E731
    lineas = [k["titulo"], ""] + [limpio(t) + "\n" for t in k["parrafos"]]
    lineas += [f"{a}: {b}" for a, b in k.get("resumen", [])]
    if k.get("resumen"):
        lineas.append("")
    lineas += [f"{i}. {limpio(t)}" for i, t in enumerate(k.get("pasos", []), 1)]
    if k.get("pasos"):
        lineas.append("")
    if k.get("boton"):
        lineas += [f"{k['boton'][0]}: {k['boton'][1]}", ""]
    if k.get("nota"):
        lineas += [limpio(k["nota"]), ""]
    if k.get("enlace"):
        lineas += [f"{k['enlace'][0]}: {k['enlace'][1]}", ""]
    lineas += ["--", "Aula Virtual Empresarial · edunest.co",
               "Este correo sale de una dirección que no recibe respuestas."]
    if getattr(c, "correo_soporte", ""):
        lineas.append(f"¿Necesitas ayuda? Escríbenos a {c.correo_soporte}.")
    return "\n".join(lineas)


def armar(tipo, config, **datos):
    """(asunto, texto, html) del aviso `tipo` con los datos de la persona."""
    k = _contenido(tipo, config, datos)
    return k["asunto"], _texto(k, config), _html(k, config)


# ---------------------------------------------------------------- vistas previas
EJEMPLOS = {
    "registro": dict(nombre="ana maría rojas", usuario="ana@ejemplo.co"),
    "pase_activo": dict(nombre="Ana María Rojas", medio="457562******4242", proximo_corte="2026-11-30",
                        enlace_cuenta="https://pase.edunest.co/mi-pase?p=1.1798000000.abc"),
    "cancelacion": dict(nombre="Ana María Rojas", corte="2026-11-30",
                        enlace_cuenta="https://pase.edunest.co/mi-pase?p=1.1798000000.abc"),
    "codigo": dict(nombre="Ana María Rojas", codigo="482915", minutos=15),
    "pago_rechazado": dict(nombre="Ana María Rojas"),
    "cobro_fallido": dict(nombre="Ana María Rojas", reintento="2026-12-03", medio="457562******4242"),
    "renovar": dict(nombre="Ana María Rojas", corte="2026-11-30",
                    enlace="https://pase.edunest.co/checkout?r=PASE-123&f=abc"),
    "pase_termino": dict(nombre="Ana María Rojas", motivo="reintentos agotados"),
    "interno": dict(asunto="Nueva suscripción al Pase", texto="Ana María Rojas (Tienda Ana) · canal camara"),
}


def main(argv):
    from .config import Config
    if len(argv) != 1:
        print(__doc__)
        return 2
    os.makedirs(argv[0], exist_ok=True)
    import shutil
    shutil.copy(LOGO, os.path.join(argv[0], "logo-correo.png"))
    c = Config.desde_entorno()
    for tipo, d in EJEMPLOS.items():
        asunto, texto, cuerpo = armar(tipo, c, **d)
        with open(os.path.join(argv[0], f"{tipo}.html"), "w", encoding="utf-8") as f:
            f.write(cuerpo.replace("cid:logo", "logo-correo.png"))
        with open(os.path.join(argv[0], f"{tipo}.txt"), "w", encoding="utf-8") as f:
            f.write(f"Asunto: {asunto}\n\n{texto}\n")
    print(f"{len(EJEMPLOS)} correos en {argv[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
