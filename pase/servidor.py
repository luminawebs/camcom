"""Servidor HTTP del conector: formulario, pago, retorno y confirmación de ePayco.

Solo biblioteca estándar de Python 3.9+. Uso:
    python -m pase.servidor          (lee la configuración del entorno)
"""
import datetime as dt
import hashlib
import hmac
import html
import http.cookies
import json
import os
import queue
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import moodle as moodle_mod
from .config import Config
from .nucleo import ENLACE_CODIGO_HORAS, TEXTO_AUTORIZACION_V1, Pase

CSS = """
:root{--acento:#00806b;--acento-2:#006655;--suave:#e3f6f1;--tinta:#14181f;--tinta-2:#4a5260;--fondo:#f6f7f9;
--borde:#dfe2e7;--campo:#c9ced6;--error:#b42318;--error-suave:#fef3f2;--aviso:#93370d;--aviso-suave:#fffaeb;
--azul:var(--tinta);--verde:var(--acento);--sombra:0 1px 2px rgba(16,24,40,.06),0 6px 18px rgba(16,24,40,.06)}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 Poppins,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
background:var(--fondo);color:var(--tinta)}a{color:var(--acento)}a:hover{color:var(--acento-2)}
.cabeza{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;background:#fff;
border-bottom:1px solid var(--borde)}.cabeza img{height:26px;width:auto;display:block}
.banda{margin:0;background:var(--aviso-suave);color:var(--aviso);font-size:12px;font-weight:600;text-align:center;
padding:6px 16px;border-bottom:1px solid #fedf89}
main{max-width:480px;margin:0 auto;padding:20px 16px 40px;display:flex;flex-direction:column;gap:18px}
main>*{margin:0}h1{font-size:1.5rem;line-height:1.25;font-weight:700;margin:0}
.seguro{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;color:var(--tinta-2)}
.pasos{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;font-size:12px;
font-weight:600;color:#6b7280}.pasos li{display:flex;flex-direction:column;gap:6px}
.pasos li::before{content:"";height:4px;border-radius:4px;background:var(--borde)}
.pasos .hecho{color:var(--acento)}.pasos .hecho::before{background:var(--acento)}
.pasos .medio::before{background:linear-gradient(90deg,var(--acento) 50%,var(--borde) 50%)}
.pasos .falla{color:var(--error)}.pasos .falla::before{background:var(--error)}
.antetitulo{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--acento);margin:0 0 4px}
.plan{background:var(--tinta);color:#fff;border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:12px}
.plan .fila-precio{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
.plan strong{font-size:22px}.plan small{font-size:13px;color:#c5cad3}
.plan ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px;font-size:13px;color:#e6e8ec}
.plan li{display:flex;gap:8px}.plan li svg{flex-shrink:0;margin-top:2px}
.resumen{display:flex;align-items:center;justify-content:space-between;gap:12px;background:#fff;border:1px solid var(--borde);
border-radius:14px;padding:14px 16px}.resumen p{margin:0}.resumen .der{text-align:right}
.resumen .precio{font-size:20px;font-weight:700}.chico{font-size:12px;color:var(--tinta-2)}
.caja{background:#fff;border:1px solid var(--borde);border-radius:14px;padding:18px;box-shadow:var(--sombra)}
form.caja{display:flex;flex-direction:column;gap:14px}.campo{display:flex;flex-direction:column;gap:6px}
label{font-size:13px;font-weight:600}.opc{font-weight:400;color:var(--tinta-2)}
input,select{width:100%;height:48px;padding:0 14px;border:1px solid var(--campo);border-radius:10px;font:inherit;
background:#fff;color:var(--tinta)}input:focus,select:focus{outline:none;border:2px solid var(--acento);padding:0 13px}
.fila{display:grid;grid-template-columns:repeat(auto-fit,minmax(0,1fr));gap:10px}.fila.doc{grid-template-columns:96px minmax(0,1fr)}
.check{display:flex;gap:10px;align-items:flex-start;font-size:12px;font-weight:400;color:var(--tinta-2);line-height:1.45}
.check input{width:20px;height:20px;margin:1px 0 0;flex-shrink:0;accent-color:var(--acento);padding:0}
details{border-top:1px solid #eceef1;padding-top:12px}summary{font-size:13px;font-weight:600;color:var(--acento);cursor:pointer}
details[open] summary{margin-bottom:12px}details .campo+.campo{margin-top:12px}
button,.boton{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;min-height:52px;padding:0 18px;
border:0;border-radius:12px;background:var(--acento);color:#fff;font:inherit;font-weight:600;cursor:pointer;
text-decoration:none;text-align:center}button:hover,.boton:hover{background:var(--acento-2);color:#fff}
button:disabled{opacity:.6;cursor:wait}.verde{background:var(--acento)}
.sec,.sec:hover{background:#fff;color:var(--tinta);border:1px solid var(--campo);min-height:48px}
.enlace,.enlace:hover{background:none;color:var(--tinta);font-size:14px;font-weight:500;text-decoration:underline;min-height:44px}
.nota{font-size:12px;color:var(--tinta-2)}.centro{text-align:center}
.aviso{background:var(--aviso-suave);border:1px solid #fedf89;color:var(--aviso);border-radius:10px;padding:10px 12px;font-size:13px}
.pestanas{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px;padding:4px;background:#e9ebef;border-radius:12px}
.pestanas a{display:flex;align-items:center;justify-content:center;gap:8px;min-height:44px;border-radius:9px;color:var(--tinta-2);
font-size:14px;font-weight:600;text-decoration:none}.pestanas a[aria-current]{background:#fff;color:var(--tinta);
box-shadow:0 1px 3px rgba(16,24,40,.12)}
.tarjeta-vista{height:196px;border-radius:16px;padding:20px;background:var(--tinta);color:#fff;display:flex;flex-direction:column;
justify-content:space-between;position:relative;overflow:hidden}.tarjeta-vista::before{content:"";position:absolute;right:-40px;
top:-40px;width:180px;height:180px;border-radius:40px;background:var(--acento);transform:rotate(45deg);opacity:.55}
.tarjeta-vista>*{position:relative}.tarjeta-vista .arriba{display:flex;justify-content:space-between;align-items:center}
.chip{width:40px;height:30px;border-radius:6px;background:#d9c38a}.marca{display:flex;align-items:center;min-height:24px;
background:#fff;border-radius:6px;padding:4px 8px}.marca:empty{visibility:hidden}.marca img{height:16px;width:auto;display:block}
.tarjeta-vista .numero{font-size:20px;letter-spacing:.12em;font-weight:500}.tarjeta-vista .abajo{display:flex;
justify-content:space-between;gap:12px;font-size:12px;text-transform:uppercase}
.con-marca{position:relative}.con-marca input{padding-right:64px}.con-marca img{position:absolute;right:12px;top:17px;height:14px}
input.mal{border:2px solid var(--error);background:var(--error-suave);padding:0 13px}
#msg:empty{display:none}#msg{display:flex;gap:6px;font-size:13px;color:var(--error);margin:-6px 0 0}
#msg.ok{color:var(--tinta-2)}.logos{display:flex;gap:6px;flex-wrap:wrap;justify-content:center}
.logos span{display:flex;align-items:center;justify-content:center;width:52px;height:34px;background:#fff;
border:1px solid var(--borde);border-radius:6px;padding:5px}.logos img{max-width:100%;max-height:100%}
.por{display:flex;align-items:center;justify-content:center;gap:6px;font-size:12px;color:var(--tinta-2)}
.por img{height:20px;width:auto}
.medios{list-style:none;padding:0;display:flex;flex-direction:column;gap:10px}.medios li{display:flex;align-items:center;gap:12px;
min-height:64px;padding:12px 14px;background:#fff;border:1px solid var(--borde);border-radius:12px}
.medios .logo{width:44px;height:32px;flex-shrink:0;display:flex;align-items:center;justify-content:center;border:1px solid
var(--borde);border-radius:6px;padding:3px}.medios .logo img{max-width:100%;max-height:100%}
.medios strong{display:block;font-size:14px}.medios span span{display:block;font-size:12px;line-height:1.4;color:var(--tinta-2)}
.dato{display:flex;gap:10px;align-items:flex-start;background:#fff;border:1px solid var(--borde);border-radius:12px;
padding:12px 14px;font-size:13px;color:var(--tinta-2)}.dato svg{flex-shrink:0;margin-top:1px}.dato strong{color:var(--tinta)}
.estado{background:#fff;border:1px solid var(--borde);border-radius:16px;padding:32px 20px 24px;display:flex;flex-direction:column;
align-items:center;gap:12px;text-align:center}.estado p{margin:0}.estado .chico{max-width:300px}
.icono{width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--suave)}
.icono.falla{background:var(--error-suave)}.icono .lleno{width:52px;height:52px;border-radius:50%;background:var(--acento);
display:flex;align-items:center;justify-content:center}
@keyframes girar{to{transform:rotate(360deg)}}.girando{animation:girar 1.1s linear infinite}
@media (prefers-reduced-motion:reduce){.girando{animation:none}}
.etapas{list-style:none;padding:0;margin:8px 0 0;width:100%;display:flex;flex-direction:column;gap:10px;text-align:left;font-size:14px}
.etapas li{display:flex;align-items:center;gap:10px;color:#6b7280}.etapas li::before{content:"";width:24px;height:24px;
flex-shrink:0;border-radius:50%;border:2px solid var(--borde);box-sizing:border-box}
.etapas .hecho{color:var(--tinta)}.etapas .hecho::before{border:0;background:var(--acento) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12l5 5L20 7'/%3E%3C/svg%3E") center/14px no-repeat}
.etapas .ahora{color:var(--tinta);font-weight:600}.etapas .ahora::before{border-color:var(--acento);background:var(--suave)}
.razones{width:100%;padding:14px;background:var(--fondo);border-radius:12px;text-align:left;font-size:13px;color:var(--tinta-2)}
.salir{align-self:flex-end}.salir button{width:auto;min-height:40px}
.razones ul{margin:6px 0 0;padding-left:18px}.oculto{display:none!important}
.insignia{display:inline-flex;align-items:center;font-size:12px;font-weight:700;border-radius:999px;padding:3px 10px;
background:#2affcd;color:var(--tinta)}.insignia.alerta{background:#fedf89}.insignia.apagada{background:#c5cad3}
.filas{background:#fff;border:1px solid var(--borde);border-radius:14px;padding:4px 16px;box-shadow:var(--sombra)}
.filas div{display:flex;justify-content:space-between;gap:12px;padding:12px 0;font-size:14px}
.filas div+div{border-top:1px solid #eceef1}.filas span{color:var(--tinta-2)}.filas b{text-align:right}
.aparte{display:flex;flex-direction:column;gap:8px;border-top:1px solid var(--borde);padding-top:18px}
.aparte p{margin:0}.aparte form{margin:4px 0 0}
.dos-col{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.dos-col div{background:#fff;
border:1px solid var(--borde);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:4px;font-size:12px;
color:var(--tinta-2)}.dos-col b{font-size:13px;color:var(--acento)}.dos-col div+div b{color:var(--error)}
fieldset{margin:0;border:1px solid var(--borde);border-radius:14px;padding:14px 16px;background:#fff;display:flex;
flex-direction:column;gap:10px}legend{font-size:13px;font-weight:600;padding:0 4px}
.opcion{display:flex;gap:10px;align-items:center;font-size:13px;font-weight:400}.opcion input{width:20px;height:20px;
margin:0;flex-shrink:0;accent-color:var(--acento);padding:0}
.peligro,.peligro:hover{background:var(--error)}
input.codigo{height:56px;font-size:24px;font-weight:600;letter-spacing:.3em;text-align:center}
.ok-suave{display:flex;gap:8px;align-items:center;background:var(--suave);color:var(--acento-2);border-radius:10px;
padding:10px 12px;font-size:13px}
"""

FUENTE = ("<link rel='preconnect' href='https://fonts.googleapis.com'><link rel='preconnect' "
          "href='https://fonts.gstatic.com' crossorigin><link rel='stylesheet' "
          "href='https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&amp;display=swap'>")


def pagina(titulo, cuerpo, sandbox=True):
    banda = '<p class="banda">Modo prueba · no se hacen cobros reales</p>' if sandbox else ""
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(titulo)}</title>{FUENTE}<style>{CSS}</style></head>"
            f"<body><header class='cabeza'><img src='/estaticos/edunest.svg' alt='edunest.co'>"
            f"</header>{banda}<main>{cuerpo}</main></body></html>").encode()


# Logos que sirve /estaticos/ (archivos oficiales de cada marca, ver pase/LEEME.md)
ESTATICOS = {n: os.path.join(os.path.dirname(__file__), "estaticos", n) for n in (
    "edunest.svg", "epayco.svg", "visa.svg", "mastercard.svg", "amex.svg", "pse.svg", "nequi.svg", "daviplata.svg")}

ICONO_CANDADO = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00806b" stroke-width="2.2" '
                 'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" '
                 'height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>')
ICONO_FLECHA = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
ICONO_OK = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2affcd" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>')
ICONO_TARJETA = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                 'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="5" width="20" '
                 'height="14" rx="2"/><path d="M2 10h20"/></svg>')
ICONO_BANCO = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10l9-6 9 6"/>'
               '<path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/></svg>')
ICONO_ALERTA = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
                'stroke-linecap="round" aria-hidden="true" style="flex-shrink:0;margin-top:2px"><circle cx="12" cy="12" '
                'r="9"/><path d="M12 8v5M12 16.5v.5"/></svg>')


def pasos(actual, falla=False):
    """Barra de 3 pasos (datos, pago, listo). actual=2.5: el paso 3 va a medias (confirmando el pago)."""
    items = []
    for n, nombre in enumerate(("1 · Tus datos", "2 · Pago", "3 · Listo"), 1):
        clase = ("falla" if falla and n == actual else "hecho" if n <= actual else
                 "medio" if n - 0.5 == actual else "")
        items.append(f'<li class="{clase}">{nombre}</li>')
    return '<ol class="pasos" aria-label="Pasos del pago">' + "".join(items) + "</ol>"


def pesos_cop(c):
    return f"${c.precio_centavos // 100:,}".replace(",", ".")


def resumen(c, persona=None, detalle="al mes · IVA incluido", plan="Pase Empresario"):
    hola = f'<p class="chico">Hola, {html.escape(persona["nombre"].split()[0])}</p>' if persona else ""
    return (f'<section class="resumen"><div>{hola}<p><b>{plan}</b></p></div><div class="der">'
            f'<p class="precio">{pesos_cop(c)}</p><p class="chico">{detalle}</p></div></section>')


ESTADOS_PAGO = {"APPROVED": "Aprobado", "DECLINED": "Rechazado", "PENDING": "Pendiente", "ERROR": "Error",
                "VOIDED": "Anulado"}
CSS_TABLERO = """
main{max-width:1100px}.cifras{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
.cifra{background:#fff;border:1px solid var(--borde);border-radius:12px;padding:14px}
.cifra b{display:block;font-size:1.6rem;color:var(--azul)}.cifra span{font-size:.85rem;color:#56606b}
h2{font-size:1.1rem;color:var(--azul);margin:28px 0 8px}.tabla{overflow-x:auto;background:#fff;
border:1px solid var(--borde);border-radius:12px}table{border-collapse:collapse;width:100%;font-size:.9rem}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid var(--borde);white-space:nowrap}
th{background:#eef2f7;font-weight:600}tr:last-child td{border-bottom:0}td.n{text-align:right}
.APPROVED{color:var(--verde);font-weight:600}.DECLINED,.ERROR{color:#c0392b;font-weight:600}
.modo{display:inline-block;font-size:.8rem;padding:3px 10px;border-radius:999px;vertical-align:middle;margin-left:8px}
.modo.prueba{background:#fff7e0;color:#8a5a00;border:1px solid #e9c46a}.modo.real{background:#e6f5ec;color:var(--verde);
border:1px solid var(--verde)}.salir{float:right}.salir button{margin-top:0;padding:8px 14px}
.dos{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}.vacio{padding:12px;color:#56606b}
.buscar{display:flex;gap:8px;flex-wrap:wrap}.buscar input{flex:1 1 240px;max-width:420px}.buscar button{width:auto}
.acciones{display:flex;gap:6px}.acciones button{width:auto;min-height:36px;padding:0 12px;font-size:13px}
.rojo,.rojo:hover{color:var(--error);border-color:#f1b8b2}
"""


def pesos(n):
    return "$" + f"{int(n or 0):,}".replace(",", ".")


def tabla(columnas, filas):
    if not filas:
        return '<div class="tabla"><p class="vacio">Nada por ahora.</p></div>'
    cab = "".join(f"<th>{html.escape(c)}</th>" for c in columnas)
    cuerpo = "".join("<tr>" + "".join(c if c.startswith("<td") else f"<td>{c}</td>" for c in f) + "</tr>"
                     for f in filas)
    return f'<div class="tabla"><table><thead><tr>{cab}</tr></thead><tbody>{cuerpo}</tbody></table></div>'


def tablero_html(d, precio_cop, sandbox, soporte=""):
    e = lambda v: html.escape(str(v if v is not None else ""))
    col = dt.timezone(dt.timedelta(hours=-5))
    fecha = lambda v: e(dt.datetime.fromisoformat(v).astimezone(col).strftime("%Y-%m-%d %H:%M") if v else "")
    activos = d["suscripciones"].get("activa", 0)
    cifras = [
        (sum(d["personas"].values()), "Inscritos"),
        (activos, "Pases activos"),
        (pesos(d["recaudo_mes_cop"]), f"Recaudo {d['mes']} ({d['pagos_mes']} pagos)"),
        (pesos(d["recaudo_mes_cop"] * 25 // 100), "25 % Cámara del mes (sobre el bruto)"),
        (pesos(activos * precio_cop), "Ingreso mensual esperado"),
        (d["suscripciones"].get("en_mora", 0), "En mora"),
    ]
    alertas = []
    if d["avisos_en_cola"]:
        alertas.append(f"{d['avisos_en_cola']} correo(s) en cola")
    if d["eventos_pendientes"]:
        alertas.append(f"{d['eventos_pendientes']} confirmación(es) de ePayco sin procesar")
    if d["eventos_rechazados"]:
        alertas.append(f"{d['eventos_rechazados']} confirmación(es) rechazadas por firma")
    modo = ('<span class="modo prueba">Modo PRUEBAS</span>' if sandbox else
            '<span class="modo real">PRODUCCIÓN: cobros reales</span>')
    cuerpo = ['<form method="post" action="/tablero/salir" class="salir"><button class="sec">Salir</button></form>',
              f'<h1>Tablero del Pase Empresario {modo}</h1>',
              f'<p class="nota">Recaudo total aprobado: {pesos(d["recaudo_total_cop"])}. '
              '<a href="/tablero/pagos.csv">Descargar pagos (CSV)</a></p>']
    if alertas:
        cuerpo.append(f'<p class="aviso">{e(" · ".join(alertas))}</p>')
    cuerpo.append(soporte)
    cuerpo.append('<div class="cifras">' + "".join(
        f'<div class="cifra"><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in cifras) + "</div>")
    cuerpo.append('<div class="dos"><div><h2>Personas por estado</h2>' + tabla(
        ["Estado", "Cantidad"], [[e(k), f'<td class="n">{v}</td>'] for k, v in d["personas"].items()]) +
        '</div><div><h2>Por canal</h2>' + tabla(
        ["Canal", "Inscritos", "Pases activos"],
        [[e(c["canal"]), f'<td class="n">{c["inscritos"]}</td>', f'<td class="n">{c["activos"] or 0}</td>']
         for c in d["canales"]]) + "</div></div>")
    cuerpo.append("<h2>Renovaciones de los próximos 7 días</h2>" + tabla(
        ["Corte", "Nombre", "Correo", "Medio", "Nota"],
        [[e(r["proximo_corte"]), e(r["nombre"]), e(r["correo"]),
          e(r["medio_enmascarado"] or r["medio"]),
          "Se cancela al corte" if r["cancelar_al_corte"] else
          ("Renovación manual" if r["renovacion_manual"] else "Cobro automático")]
         for r in d["renovaciones"]]))
    cuerpo.append("<h2>En mora</h2>" + tabla(
        ["Nombre", "Correo", "Corte", "Intento", "Próximo intento"],
        [[e(r["nombre"]), e(r["correo"]), e(r["proximo_corte"]), e(r["intento"]), e(r["proximo_intento"])]
         for r in d["en_mora"]]))
    cuerpo.append("<h2>Últimos pagos</h2>" + tabla(
        ["Fecha", "Nombre", "Tipo", "Periodo", "Monto", "Estado", "Medio"],
        [[fecha(r["aprobado_en"] or r["creado"]), e(r["nombre"]), e(r["tipo"]), e(r["periodo"]),
          f'<td class="n">{pesos((r["monto"] or 0) // 100)}</td>',
          f'<td class="{e(r["estado"])}">{e(ESTADOS_PAGO.get(r["estado"], r["estado"]))}</td>', e(r["metodo"])]
         for r in d["ultimos_pagos"]]))
    if d["avisos_con_error"]:
        cuerpo.append("<h2>Correos con error</h2>" + tabla(
            ["Para", "Asunto", "Intentos", "Error"],
            [[e(r["para"]), e(r["asunto"]), e(r["intentos"]), e((r["error"] or "")[:120])]
             for r in d["avisos_con_error"]]))
    return pagina("Tablero del Pase", "".join(cuerpo), sandbox).replace(
        b"</style>", CSS_TABLERO.encode() + b"</style>", 1)


def login_html(configurado, error=""):
    if not configurado:
        return ("<h1>Tablero del Pase</h1><div class='caja'><p>El tablero aún no tiene usuario. En el servidor, "
                "agrega <code>PASE_ADMIN_USUARIO</code> y <code>PASE_ADMIN_CLAVE</code> (10 caracteres o más) "
                "en /etc/pase/pase.env y reinicia el servicio.</p></div>")
    aviso = f'<p class="aviso">{html.escape(error)}</p>' if error else ""
    return f"""<h1>Tablero del Pase</h1>{aviso}
<form class="caja" method="post" action="/tablero/entrar">
<label>Usuario</label><input name="usuario" required autocomplete="username" autofocus>
<label>Contraseña</label><input name="clave" type="password" required autocomplete="current-password">
<button>Entrar</button>
<p class="nota">Tras 5 intentos fallidos el acceso se bloquea 15 minutos.</p>
</form>"""


def formulario(canal, c=None):
    canal = html.escape(canal)
    precio = pesos_cop(c) if c else "$29.000"
    return f"""
{pasos(1)}
<div><p class="antetitulo">Aula Virtual Empresarial Soacha</p>
<h1>Fortalece tu negocio desde el celular</h1></div>
<section class="plan" aria-label="Pase Empresario">
<div class="fila-precio"><b>Pase Empresario</b><span><strong>{precio}</strong><small> /mes</small></span></div>
<ul><li>{ICONO_OK}Todos los cursos completos, no solo las unidades gratis</li>
<li>{ICONO_OK}Certificado de cada curso que termines</li>
<li>{ICONO_OK}Cursos nuevos cada mes · cancelas cuando quieras</li></ul>
</section>
<form class="caja" method="post" action="/inscripcion">
<input type="hidden" name="canal" value="{canal}">
<div class="campo"><label for="nombre">Nombre completo</label><input id="nombre" name="nombre" required autocomplete="name"></div>
<div class="fila doc"><div class="campo"><label for="tipo">Tipo</label><select id="tipo" name="tipo_doc"><option>CC</option>
<option>CE</option><option>NIT</option><option>PPT</option></select></div>
<div class="campo"><label for="documento">Número de documento</label><input id="documento" name="documento" required
inputmode="numeric" pattern="[0-9A-Za-z\\-]{{5,15}}"></div></div>
<div class="campo"><label for="correo">Correo</label><input id="correo" name="correo" type="email" required autocomplete="email">
<span class="nota">Aquí te llega el acceso al aula.</span></div>
<div class="campo"><label for="whatsapp">WhatsApp <span class="opc">(opcional)</span></label><input id="whatsapp" name="whatsapp"
inputmode="tel" autocomplete="tel" pattern="(\\+?57)?3[0-9]{{9}}" placeholder="3001234567"></div>
<details><summary>Datos de tu negocio (opcional)</summary>
<div class="campo"><label for="negocio">Nombre del negocio</label><input id="negocio" name="negocio"></div>
<div class="campo"><label for="matricula">Matrícula mercantil</label><input id="matricula" name="matricula_mercantil"></div>
<div class="campo"><label for="municipio">Municipio</label><input id="municipio" name="municipio" value="Soacha"></div>
</details>
<label class="check"><input type="checkbox" name="acepta_datos" required>
<span>{html.escape(TEXTO_AUTORIZACION_V1)}</span></label>
<label class="check"><input type="checkbox" name="acepta_whatsapp"><span>Quiero recibir mensajes por WhatsApp.</span></label>
<button name="opcion" value="pase">Continuar al pago {ICONO_FLECHA}</button>
<button name="opcion" value="gratis" class="enlace" formnovalidate>Prefiero solo el registro gratis</button>
</form>"""


def pestanas(firma, activa):
    tarjeta = f'href="/pagar?p={firma}"' + (' aria-current="page"' if activa == "tarjeta" else "")
    otros = f'href="/pagar/checkout?p={firma}"' + (' aria-current="page"' if activa == "otros" else "")
    return (f'<nav class="pestanas" aria-label="Medio de pago"><a {tarjeta}>{ICONO_TARJETA}Tarjeta</a>'
            f'<a {otros}>{ICONO_BANCO}PSE · Nequi</a></nav>')


def pantalla_pago(c, persona, firma):
    precio = pesos_cop(c)
    cfg = json.dumps({"pub": c.llave_publica, "p": firma})
    nombre, correo = html.escape(persona["nombre"]), html.escape(persona["correo"])
    ayuda = ('<p class="aviso">Modo prueba: usa la tarjeta 4575 6231 8229 0326 (aprueba) o 4151 6115 2758 3283 '
             '(rechaza), vence 12/27, CVC 123. Una tarjeta inventada no la acepta ePayco.</p>'
             if c.pruebas else "")
    return f"""
<span class="seguro">{ICONO_CANDADO}Pago seguro</span>
{pasos(2)}
{resumen(c, persona)}
{pestanas(firma, "tarjeta")}
<div class="tarjeta-vista" aria-hidden="true"><div class="arriba"><span class="chip"></span><span class="marca" id="v-marca"></span></div>
<p class="numero" id="v-num">•••• •••• •••• ••••</p>
<div class="abajo"><span>{nombre}</span><span id="v-venc">MM/AA</span></div></div>
<form id="tarjeta" class="caja" onsubmit="return tarjeta(event)" novalidate>
<input type="hidden" data-epayco="card[name]" value="{nombre}">
<input type="hidden" data-epayco="card[email]" value="{correo}">
<input type="hidden" id="mes" data-epayco="card[exp_month]">
<input type="hidden" id="anio" data-epayco="card[exp_year]">
<div class="campo"><label for="num">Número de tarjeta</label><div class="con-marca">
<input id="num" data-epayco="card[number]" inputmode="numeric" autocomplete="cc-number" placeholder="0000 0000 0000 0000" required>
<img id="num-marca" class="oculto" alt=""></div></div>
<div class="fila"><div class="campo"><label for="venc">Vence (MM/AA)</label>
<input id="venc" inputmode="numeric" autocomplete="cc-exp" placeholder="08/28" maxlength="7" required></div>
<div class="campo"><label for="cvc">CVC</label><input id="cvc" data-epayco="card[cvc]" inputmode="numeric"
autocomplete="cc-csc" placeholder="3 dígitos" maxlength="4" required></div></div>
<p id="msg" role="alert"></p>
<label class="check"><input type="checkbox" id="acepto" required><span>Autorizo a EduNest a cobrar {precio}
cada mes a esta tarjeta por medio de ePayco hasta que cancele el Pase.</span></label>
<button id="pagar">{ICONO_CANDADO.replace('#00806b', 'currentColor')}Pagar {precio}</button></form>
{ayuda}
<div class="logos"><span><img src="/estaticos/visa.svg" alt="Visa"></span><span><img src="/estaticos/mastercard.svg"
alt="Mastercard"></span><span><img src="/estaticos/amex.svg" alt="American Express"></span></div>
<p class="por">Procesado por <img src="/estaticos/epayco.svg" alt="ePayco"></p>
<p class="nota centro">Tus datos de tarjeta van directo a ePayco. EduNest no los ve ni los guarda.
Cancelas cuando quieras.</p>
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="{html.escape(c.token_js)}"></script>
<script>
const C={cfg};
const $id=id=>document.getElementById(id);
function msg(t,ok){{const m=$id('msg');m.className=ok?'ok':'';m.innerHTML=t?(ok?'':'{ICONO_ALERTA}')+'<span></span>':'';
 if(t) m.lastChild.textContent=t}}
ePayco.setPublicKey(C.pub);
// Marca de la tarjeta por los primeros dígitos, solo para mostrar el logo
function marca(n){{return /^4/.test(n)?'visa':/^(5[1-5]|2[2-7])/.test(n)?'mastercard':/^3[47]/.test(n)?'amex':''}}
function vista(){{const n=$id('num').value.replace(/\\D/g,''), m=marca(n);
 $id('v-num').textContent=(n+'•'.repeat(Math.max(0,16-n.length))).replace(/(.{{4}})/g,'$1 ').trim();
 $id('v-venc').textContent=$id('venc').value||'MM/AA';
 const i=$id('num-marca'); i.classList.toggle('oculto',!m); if(m) i.src='/estaticos/'+m+'.svg';
 $id('v-marca').innerHTML=m?'<img src="/estaticos/'+m+'.svg" alt="">':''}}
$id('num').addEventListener('input',e=>{{const d=e.target.value.replace(/\\D/g,'').slice(0,19);
 e.target.value=d.replace(/(\\d{{4}})(?=\\d)/g,'$1 ');vista()}});
$id('venc').addEventListener('input',e=>{{let d=e.target.value.replace(/\\D/g,'').slice(0,4);
 if(d.length>2) d=d.slice(0,2)+'/'+d.slice(2); e.target.value=d;vista()}});
$id('cvc').addEventListener('input',e=>{{e.target.value=e.target.value.replace(/\\D/g,'').slice(0,4)}});
// Mensajes en español y el campo marcado (ePayco responde en inglés, p. ej. «…field is empty: number»)
const CAMPO={{number:['num','El número de tarjeta no es válido. Revísalo.'],cvc:['cvc','Escribe los 3 o 4 números del respaldo de tu tarjeta.'],
 exp_month:['venc','El mes de vencimiento debe ser de 01 a 12.'],exp_year:['venc','La tarjeta está vencida o el año no es válido.'],
 date_exp:['venc','La fecha de vencimiento no es válida (MM/AA, sin vencer).'],
 name:['num','Falta el nombre del titular.'],email:['num','Falta un correo válido.'],acepto:['acepto','Marca la autorización de cobro mensual para continuar.']}};
function marcar(clave){{document.querySelectorAll('input.mal').forEach(e=>e.classList.remove('mal'));
 const c=CAMPO[clave]; if(!c) return false; const e=$id(c[0]); if(e.type!=='checkbox') e.classList.add('mal');
 e.focus(); msg(c[1]); return true}}
function luhn(n){{let s=0;for(let i=0;i<n.length;i++){{let d=+n[n.length-1-i];if(i%2){{d*=2;if(d>9)d-=9}}s+=d}}return n.length>=13&&n.length<=19&&s%10===0}}
function revisar(num){{const v=$id('venc').value.split('/'), m=+v[0], hoy=new Date(), cvc=$id('cvc').value;
 if(!luhn(num)) return 'number';
 if(!(m>=1&&m<=12)) return 'exp_month';
 let a=(v[1]||'').trim(); if(a.length===2) a='20'+a;  // ePayco espera el año con 4 dígitos
 if(a.length!==4||+a<hoy.getFullYear()||(+a===hoy.getFullYear()&&m<hoy.getMonth()+1)) return 'exp_year';
 $id('mes').value=String(m).padStart(2,'0'); $id('anio').value=a;
 if(!/^\\d{{3,4}}$/.test(cvc)) return 'cvc';
 if(!$id('acepto').checked) return 'acepto'; return ''}}
function tarjeta(ev){{ev.preventDefault();
 const num=$id('num').value.replace(/\\D/g,'');
 const malo=revisar(num); if(malo) return marcar(malo)&&false;
 marcar('');msg('Procesando tu pago…',true);$id('pagar').disabled=true;
 $id('num').value=num;  // ePayco lee el número sin espacios
 ePayco.token.create(window.jQuery?jQuery('#tarjeta'):$id('tarjeta'),async function(error,token){{
  $id('num').dispatchEvent(new Event('input'));
  if(error){{$id('pagar').disabled=false;const t=String(error.description||error.message||error);
   const clave=Object.keys(CAMPO).find(k=>t.endsWith(': '+k)); if(clave&&marcar(clave)) return;
   return msg('ePayco no aceptó la tarjeta: '+t)}}
  try{{const r=await fetch('/pagar/token',{{method:'POST',headers:{{'Content-Type':'application/json'}},
   body:JSON.stringify({{p:C.p,token:String(token&&token.id||token),enmascarado:'**** '+num.slice(-4)}})}});
   const j=await r.json(); if(!r.ok) throw new Error(j.error||r.status);
   location='/retorno?ref='+encodeURIComponent(j.referencia)}}catch(e){{$id('pagar').disabled=false;msg('No se pudo: '+e.message)}}}});
 return false}}
</script>"""


def pantalla_checkout(c, datos):
    precio = pesos_cop(c)
    medios = (("pse", "PSE", "Débito desde tu cuenta de ahorros o corriente"),
              ("nequi", "Nequi", "Apruebas el pago en tu app"),
              ("daviplata", "Daviplata", "Apruebas el pago en tu app"))
    lista = "".join(f'<li><span class="logo"><img src="/estaticos/{n}.svg" alt=""></span><span><strong>{t}</strong>'
                    f'<span>{d}</span></span></li>' for n, t, d in medios)
    return f"""
<span class="seguro">{ICONO_CANDADO}Pago seguro</span>
{pasos(2)}
{resumen(c, detalle="IVA incluido", plan="Pase Empresario · 1 mes")}
<div><h1>Paga con PSE, Nequi o Daviplata</h1>
<p class="nota">También puedes usar una tarjeta sin guardarla.</p></div>
<ul class="medios">{lista}</ul>
<div class="dato"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00806b" stroke-width="2"
stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/>
<path d="M3 10h18M8 3v4M16 3v4"/></svg><span>Este pago cubre <strong>un mes</strong>. Antes del corte te enviamos
el enlace para renovar.</span></div>
<button onclick="abrir()">Ir a pagar {precio} {ICONO_FLECHA}</button>
<p class="nota centro">Se abre la ventana segura de ePayco. Al terminar vuelves aquí.</p>
<p class="por">Procesado por <img src="/estaticos/epayco.svg" alt="ePayco"></p>
<script src="{html.escape(c.checkout_js)}"></script>
<script>
function abrir(){{ePayco.checkout.configure({json.dumps(datos)}).open()}}
</script>"""


def retorno(c, firma=None):
    aula = html.escape(c.moodle_url or "", quote=True)
    entrar = f'<a class="boton" href="{aula}">Entrar al aula {ICONO_FLECHA}</a>' if aula else ""
    if firma:
        otra_vez = (f'<a class="boton" href="/pagar?p={firma}">Intentar de nuevo</a>'
                    f'<a class="boton sec" href="/pagar/checkout?p={firma}">Pagar con PSE o Nequi</a>')
    else:
        otra_vez = '<p class="chico">Vuelve al enlace de pago que te enviamos para intentarlo de nuevo.</p>'
    return f"""
<span class="seguro">{ICONO_CANDADO}Pago seguro</span>
<div id="pasos">{pasos(2.5)}</div>
<section class="estado" aria-live="polite">
<div id="esperando" style="display:contents">
<svg class="girando" width="56" height="56" viewBox="0 0 48 48" fill="none" aria-hidden="true"><circle cx="24" cy="24" r="20"
stroke="#e3f6f1" stroke-width="5"/><path d="M24 4a20 20 0 0 1 20 20" stroke="#00806b" stroke-width="5" stroke-linecap="round"/></svg>
<h1>Estamos confirmando tu pago</h1>
<p class="chico">Suele tardar menos de un minuto. No cierres esta página.</p>
<ul class="etapas"><li class="hecho">Pago enviado a ePayco</li><li class="ahora">Esperando respuesta del banco</li>
<li>Activando tu acceso al aula</li></ul></div>
<div id="aprobado" class="oculto" style="display:contents">
<span class="icono"><span class="lleno"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3"
stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg></span></span>
<h1>¡Listo! Tu Pase está activo</h1>
<p class="chico">Te enviamos un correo con tu usuario y el enlace al aula.</p>{entrar}</div>
<div id="rechazado" class="oculto" style="display:contents">
<span class="icono falla"><svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#b42318" stroke-width="2.4"
stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5M12 16.5v.5"/></svg></span>
<h1>Tu pago no se aprobó</h1>
<p class="chico">El banco no autorizó el cobro. <strong>No se te descontó nada.</strong></p>
<div class="razones"><b>Suele pasar por:</b><ul><li>Fondos o cupo insuficiente</li>
<li>Compras por internet desactivadas en la tarjeta</li><li>Algún dato mal escrito (vencimiento o CVC)</li></ul></div>
{otra_vez}</div>
</section>
<p class="nota centro" id="ref"></p>
<script>
const q=new URLSearchParams(location.search), ref=q.get('ref')||'', tx=q.get('ref_payco')||'';
const $id=id=>document.getElementById(id);
if(ref) $id('ref').textContent='Referencia '+ref+' · Guárdala si necesitas ayuda';
function ver(id,pasosHtml){{for(const x of ['esperando','aprobado','rechazado']) $id(x).classList.toggle('oculto',x!==id);
 $id('pasos').innerHTML=pasosHtml}}
async function mirar(){{try{{const r=await fetch('/estado-pago?ref='+encodeURIComponent(ref)+'&ref_payco='+encodeURIComponent(tx));
 const j=await r.json();
 if(j.estado==='APPROVED'){{document.title='Pago aprobado';return ver('aprobado',{json.dumps(pasos(3))})}}
 if(j.estado==='DECLINED'||j.estado==='ERROR'||j.estado==='VOIDED'){{document.title='Pago no aprobado';
  return ver('rechazado',{json.dumps(pasos(2, falla=True))})}}}}catch(e){{}}
 setTimeout(mirar,2500)}}
mirar();
</script>"""


# ---------------------------------------------------------------- Mi Pase (cuenta de la persona)
ICONO_CALENDARIO = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00806b" stroke-width="2" '
                    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" '
                    'height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>')
MOTIVOS = ("Ya terminé lo que necesitaba", "Está caro para mí ahora", "No tengo tiempo", "Otro")


def _fecha(valor):
    from .plantillas_correo import fecha_larga
    return fecha_larga(valor) if valor else ""


def _medio(sus):
    from .plantillas_correo import medio_legible
    if sus["renovacion_manual"]:
        return "PSE, Nequi o Daviplata"
    return medio_legible(sus["medio_enmascarado"]) or "Tarjeta"


def pantalla_codigo(correo="", enviado=False, error="", vencido=False):
    """Entrada a Mi Pase sin enlace: correo → código de 6 dígitos (sin contraseñas)."""
    correo = html.escape(correo, quote=True)
    aviso = ('<p class="aviso">Tu enlace venció. Pide un código para entrar.</p>' if vencido else "")
    if error:
        aviso = f'<p class="aviso">{html.escape(error)}</p>'
    if not enviado:
        return f"""
<div><p class="antetitulo">Mi Pase</p><h1>Entra a tu cuenta del Pase</h1>
<p class="nota" style="font-size:14px;margin-top:6px">Te enviamos un código al correo con el que te inscribiste.
Sin contraseñas.</p></div>{aviso}
<form class="caja" method="post" action="/mi-pase/codigo">
<div class="campo"><label for="correo">Correo</label><input id="correo" name="correo" type="email" required
autocomplete="email" value="{correo}"></div>
<button>Enviarme un código</button></form>"""
    return f"""
<div><p class="antetitulo">Mi Pase</p><h1>Escribe tu código</h1>
<p class="nota" style="font-size:14px;margin-top:6px">Si {correo} tiene el Pase, le llegó un código de 6 dígitos.
Revisa también spam o promociones.</p></div>{aviso}
<form class="caja" method="post" action="/mi-pase/entrar">
<input type="hidden" name="correo" value="{correo}">
<div class="campo"><label for="codigo">Código de 6 dígitos</label><input id="codigo" name="codigo" class="codigo"
inputmode="numeric" autocomplete="one-time-code" pattern="[0-9 ]{{6,7}}" maxlength="7" required autofocus></div>
<button>Entrar</button></form>
<form method="post" action="/mi-pase/codigo"><input type="hidden" name="correo" value="{correo}">
<button class="enlace">Enviar otro código</button></form>
<p class="nota centro">El código vence en 15 minutos y sirve una sola vez.</p>"""


def pantalla_mi_pase(c, persona, sus, firma, firma_pago):
    nombre = html.escape(persona["nombre"].split()[0].capitalize())
    aula = html.escape(c.moodle_url or "", quote=True)
    corte = _fecha(sus["proximo_corte"])
    estado = sus["estado"]
    if estado == "activa" and sus["cancelar_al_corte"]:
        insignia = '<span class="insignia alerta">Se cancela</span>'
        filas = [("Acceso completo hasta", corte), ("Próximo cobro", "Ninguno")]
    elif estado == "activa":
        insignia = '<span class="insignia">Activo</span>'
        filas = [("Próxima renovación", corte), ("Medio de pago", _medio(sus))]
    elif estado == "en_mora":
        insignia = '<span class="insignia alerta">Pago pendiente</span>'
        filas = [("Venció el", corte), ("Medio de pago", _medio(sus))]
    else:
        insignia = '<span class="insignia apagada">Cerrado</span>' if estado == "cancelada" else \
            '<span class="insignia apagada">Sin activar</span>'
        filas = [("Cerrado el", _fecha(sus["cancelada_en"]))] if sus["cancelada_en"] else []
    if sus["inicio"] and estado != "cancelada":
        filas.append(("Miembro desde", _fecha(sus["inicio"])))
    tabla_ = ('<section class="filas">' + "".join(f"<div><span>{html.escape(a)}</span><b>{html.escape(b)}</b></div>"
                                                 for a, b in filas) + "</section>") if filas else ""
    cursos = f'<a class="boton" href="{aula}">Ir a mis cursos {ICONO_FLECHA}</a>' if aula else ""
    if estado == "activa" and sus["cancelar_al_corte"]:
        abajo = f"""<div class="aparte"><p><b>¿Cambiaste de opinión?</b></p>
<p class="nota" style="font-size:13px">Hasta el {corte} puedes seguir con el Pase sin volver a pagar ni poner la
tarjeta.</p><form method="post" action="/mi-pase/seguir"><input type="hidden" name="p" value="{firma}">
<button class="sec">Seguir con mi Pase</button></form></div>"""
    elif estado in ("activa", "en_mora"):
        texto = (f"Puedes cancelar cuando quieras. Sigues con acceso hasta el {corte} y no te volvemos a cobrar."
                 if estado == "activa" else "Si cancelas ahora, el Pase se cierra hoy y no intentamos cobrarte "
                                            "de nuevo.")
        abajo = f"""<div class="aparte"><p><b>¿Ya no lo necesitas?</b></p>
<p class="nota" style="font-size:13px">{texto}</p>
<a class="boton sec" href="/mi-pase/cancelar?p={firma}">Cancelar mi Pase</a></div>"""
    else:
        abajo = (f'<a class="boton sec" href="/pagar?p={firma_pago}">Volver al Pase</a>'
                 '<p class="nota centro">Conservas tu avance y las tres primeras unidades gratis de cada curso.</p>')
    return f"""
<div><p class="antetitulo">Mi cuenta</p><h1>Hola, {nombre}</h1></div>
<section class="plan" aria-label="Pase Empresario">
<div class="fila-precio"><b>Pase Empresario</b>{insignia}</div>
<p style="margin:0"><strong>{pesos_cop(c)}</strong><small> /mes · IVA incluido</small></p>
<p style="margin:0;font-size:13px;color:#e6e8ec">Todos los cursos completos y tus certificados.</p></section>
{tabla_}{cursos}{abajo}"""


def pantalla_confirmar_cancelacion(c, sus, firma):
    corte = _fecha(sus["proximo_corte"])
    if sus["estado"] == "en_mora":
        dato = "Tu último pago no pasó, así que <strong>el Pase se cierra hoy</strong> y no intentamos cobrarte de nuevo."
    else:
        dato = (f"Sigues con <strong>todos los cursos hasta el {corte}</strong>. Desde ese día no te cobramos "
                "más.")
    opciones = "".join(f'<label class="opcion"><input type="radio" name="motivo" value="{html.escape(m, quote=True)}">'
                       f'{html.escape(m)}</label>' for m in MOTIVOS)
    return f"""
<h1>¿Cancelar tu Pase Empresario?</h1>
<div class="dato">{ICONO_CALENDARIO}<span>{dato}</span></div>
<section class="dos-col"><div><b>Conservas</b><span>Tu avance y tus certificados</span>
<span>Las unidades 1 a 3 gratis</span></div><div><b>Pierdes</b><span>Las unidades 4 a 7</span>
<span>Certificados nuevos</span></div></section>
<form method="post" action="/mi-pase/cancelar" style="display:flex;flex-direction:column;gap:16px">
<input type="hidden" name="p" value="{firma}">
<fieldset><legend>¿Por qué cancelas? <span class="opc">(opcional)</span></legend>{opciones}</fieldset>
<button class="peligro">Sí, cancelar mi Pase</button>
<a class="boton sec" href="/mi-pase?p={firma}">Mejor no, seguir con el Pase</a></form>"""


def pantalla_cancelacion_lista(c, persona, sus, firma):
    aula = html.escape(c.moodle_url or "", quote=True)
    cursos = f'<a class="boton" href="{aula}">Ir a mis cursos {ICONO_FLECHA}</a>' if aula else ""
    correo = html.escape(persona["correo"])
    if sus["estado"] == "cancelada":
        texto, seguir = ("Tu Pase quedó cerrado y no te volvemos a cobrar. Conservas tu avance y las tres "
                         "primeras unidades gratis de cada curso.", "")
    else:
        corte = _fecha(sus["proximo_corte"])
        texto = f"Tienes todos los cursos <strong>hasta el {corte}</strong>. No te volvemos a cobrar."
        seguir = f"""<div class="aparte"><p><b>¿Cambiaste de opinión?</b></p>
<p class="nota" style="font-size:13px">Hasta el {corte} puedes seguir con el Pase sin volver a pagar ni poner la
tarjeta.</p><form method="post" action="/mi-pase/seguir"><input type="hidden" name="p" value="{firma}">
<button class="sec">Seguir con mi Pase</button></form></div>"""
    return f"""
<section class="estado"><span class="icono"><span class="lleno"><svg width="28" height="28" viewBox="0 0 24 24"
fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<path d="M5 12l5 5L20 7"/></svg></span></span>
<h1>Listo, cancelaste tu Pase</h1><p class="chico">{texto}</p>
<p class="chico" style="font-size:12px">Te enviamos la confirmación a {correo}.</p></section>
{cursos}{seguir}"""


def tablero_soporte(buscar, resultados, mensaje=""):
    """Buscador del tablero para cancelar o deshacer a pedido de la persona (WhatsApp, teléfono)."""
    e = lambda v: html.escape(str(v if v is not None else ""), quote=True)
    partes = ['<h2>Buscar persona</h2>']
    if mensaje:
        partes.append(f'<p class="aviso">{e(mensaje)}</p>')
    partes.append(f'<form method="get" action="/tablero" class="buscar"><input name="buscar" value="{e(buscar)}" '
                  'aria-label="Nombre, correo o documento" placeholder="Nombre, correo o documento">'
                  '<button class="sec">Buscar</button></form>')
    if buscar is None:
        return "".join(partes)

    def accion(pid, nombre, valor, texto, pregunta, clase="sec"):
        return (f'<form method="post" action="/tablero/accion" onsubmit="return confirm({e(json.dumps(pregunta))})">'
                f'<input type="hidden" name="persona" value="{pid}"><input type="hidden" name="buscar" '
                f'value="{e(buscar)}"><button name="accion" value="{valor}" class="{clase}">{texto}</button></form>')
    filas = []
    for r in resultados:
        n = r["nombre"]
        if r["estado"] == "activa" and r["cancelar_al_corte"]:
            estado = f"Cancela el {r['proximo_corte']}"
            botones = accion(r["id"], n, "deshacer", "Deshacer cancelación", f"¿{n} sigue con el Pase?")
        elif r["estado"] in ("activa", "en_mora"):
            estado = {"activa": "Activa", "en_mora": "En mora"}[r["estado"]]
            botones = (accion(r["id"], n, "cancelar_corte", "Cancelar al corte",
                              f"¿Cancelar el Pase de {n} en su fecha de corte?") +
                       accion(r["id"], n, "cancelar_ya", "Cancelar ya",
                              f"¿Cerrar YA el Pase de {n}? Pierde las unidades 4 a 7 hoy y no se devuelve dinero.",
                              "sec rojo"))
        else:
            estado, botones = {"cancelada": "Cancelada", "pendiente": "Sin pagar"}.get(r["estado"], r["estado"]), ""
        filas.append([f'{e(n)}<br><span class="nota">{e(r["correo"])} · {e(r["documento"])}</span>', e(estado),
                      e(r["proximo_corte"]), e(r["medio_enmascarado"] or r["medio"]),
                      f'<td><div class="acciones">{botones}</div></td>'])
    partes.append(tabla(["Persona", "Estado", "Corte", "Medio", "Acciones"], filas))
    partes.append('<p class="nota">Cada acción queda en el historial. «Cancelar ya» quita las unidades 4 a 7 de '
                  'inmediato y no devuelve dinero: úsalo solo para fraudes o pedidos expresos.</p>')
    return "".join(partes)


class App:
    def __init__(self, config: Config, pase: Pase = None):
        self.c = config
        self.pase = pase or Pase(config, moodle_mod.crear(config))
        self.cola = queue.Queue()
        self._fallos_admin, self._candado_admin = {}, threading.Lock()
        threading.Thread(target=self._trabajador, daemon=True).start()

    # ---- tablero: un usuario y contraseña en /etc/pase/pase.env, sesión firmada de 12 h
    INTENTOS_ADMIN, BLOQUEO_ADMIN = 5, 15 * 60

    def admin_configurado(self):
        return bool(os.environ.get("PASE_ADMIN_USUARIO")) and len(os.environ.get("PASE_ADMIN_CLAVE", "")) >= 10

    def _huella_admin(self):
        # Cambiar el usuario o la contraseña cierra todas las sesiones abiertas.
        texto = os.environ.get("PASE_ADMIN_USUARIO", "") + "\0" + os.environ.get("PASE_ADMIN_CLAVE", "")
        return hashlib.sha256(texto.encode()).hexdigest()[:16]

    def entrar_admin(self, usuario, clave, ip):
        ahora_ = time.time()
        with self._candado_admin:
            fallos = [t for t in self._fallos_admin.get(ip, []) if ahora_ - t < self.BLOQUEO_ADMIN]
            self._fallos_admin[ip] = fallos
            if len(fallos) >= self.INTENTOS_ADMIN or not self.admin_configurado():
                return None
            ok = (hmac.compare_digest(usuario.encode(), os.environ["PASE_ADMIN_USUARIO"].encode()) &
                  hmac.compare_digest(clave.encode(), os.environ["PASE_ADMIN_CLAVE"].encode()))
            if not ok:
                fallos.append(ahora_)
                return None
            self._fallos_admin.pop(ip, None)
        vence = int(ahora_) + 12 * 3600
        return f"{vence}.{self.pase.firma(f'admin:{vence}:{self._huella_admin()}')}"

    def sesion_admin_valida(self, valor):
        vence, _, f = (valor or "").partition(".")
        return (self.admin_configurado() and vence.isdigit() and int(vence) > time.time() and
                self.pase.firma_valida(f"admin:{vence}:{self._huella_admin()}", f))

    # La persona viaja firmada en la URL: nadie puede pagar ni consultar a nombre de otro.
    def firmar(self, pid):
        return f"{pid}.{self.pase.firma(pid)}"

    def verificar(self, firma):
        pid, _, f = (firma or "").partition(".")
        return int(pid) if pid.isdigit() and self.pase.firma_valida(pid, f) else None

    def _trabajador(self):
        while True:
            eid = self.cola.get()
            try:
                if eid is None:
                    self.pase.procesar_pendientes()
                else:
                    self.pase.procesar_evento(eid)
            finally:
                self.cola.task_done()

    def manejador(self):
        app = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                if os.environ.get("PASE_LOG", "1") == "1":
                    super().log_message(fmt, *args)

            def log_request(self, code="-", size="-"):
                # Solo método y ruta: los parámetros traen datos personales (Ley 1581) y enlaces firmados.
                ruta = urllib.parse.urlparse(getattr(self, "path", "")).path
                self.log_message('"%s %s" %s', getattr(self, "command", "-"), ruta, getattr(code, "value", code))

            def responder(self, codigo, cuerpo=b"", tipo="text/html; charset=utf-8", extra=None):
                self.send_response(codigo)
                self.send_header("Content-Type", tipo)
                self.send_header("Content-Length", str(len(cuerpo)))
                for k, v in (extra or {}).items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(cuerpo)

            def json(self, codigo, datos):
                self.responder(codigo, json.dumps(datos).encode(), "application/json")

            def admin_valido(self):
                galleta = http.cookies.SimpleCookie(self.headers.get("Cookie", ""))
                return app.sesion_admin_valida(galleta["pase_admin"].value if "pase_admin" in galleta else "")

            def galleta_admin(self, valor, segundos):
                segura = "; Secure" if app.c.url_publica.startswith("https://") else ""
                return {"Set-Cookie": f"pase_admin={valor}; Max-Age={segundos}; Path=/tablero; "
                                      f"HttpOnly; SameSite=Strict{segura}"}

            def redirigir(self, destino, extra=None):
                self.responder(303, extra={"Location": destino, **(extra or {})})

            def ip(self):
                reenviada = self.headers.get("X-Forwarded-For", "")
                if reenviada and self.client_address[0] == "127.0.0.1":
                    return reenviada.split(",")[0].strip()
                return self.client_address[0]

            def leer(self):
                return self.rfile.read(int(self.headers.get("Content-Length") or 0))

            def formulario(self):
                return dict(urllib.parse.parse_qsl(self.leer().decode(errors="replace")))

            # Mi Pase: el enlace firmado va en la URL; que no se guarde ni viaje a otros sitios.
            PRIVADO = {"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"}

            def mi_pase(self, titulo, cuerpo, codigo=200):
                return self.responder(codigo, pagina(titulo, cuerpo, app.c.entorno == "sandbox"), extra=self.PRIVADO)

            def cuenta(self, firma):
                """(pid, suscripción) del enlace de Mi Pase, o None si venció o no tiene Pase."""
                pid = app.pase.verificar_mi_pase(firma)
                sus = app.pase.suscripcion(pid) if pid else None
                return (pid, sus) if sus else None

            def confirmacion(self, datos):
                codigo, eid = app.pase.recibir_evento(datos, self.ip())
                if eid:
                    app.cola.put(eid)
                return self.json(codigo, {"ok": codigo == 200})

            def do_GET(self):
                u = urllib.parse.urlparse(self.path)
                q = dict(urllib.parse.parse_qsl(u.query))
                sb = app.c.entorno == "sandbox"
                if u.path == "/":
                    return self.responder(200, pagina("Inscripción", formulario(q.get("c", "sin-canal"), app.c), sb))
                if u.path == "/pagar":
                    pid = app.verificar(q.get("p"))
                    if not pid:
                        return self.responder(404, pagina("No encontrado", "<h1>Enlace no válido</h1>", sb))
                    return self.responder(200, pagina("Pase Empresario", pantalla_pago(
                        app.c, app.pase.persona(pid), q["p"]), sb))
                if u.path == "/pagar/checkout":
                    pid = app.verificar(q.get("p"))
                    if not pid:
                        return self.responder(404, b"")
                    _, url = app.pase.url_pago_manual(pid)
                    return self.responder(302, b"", extra={"Location": url})
                if u.path == "/checkout":
                    ref = q.get("r", "")
                    try:
                        datos = app.pase.firma_valida(f"pago:{ref}", q.get("f")) and app.pase.datos_checkout(ref)
                    except Exception as e:
                        print(f"Checkout {ref}: {e!r}"[:500], flush=True)
                        return self.responder(502, pagina("Intenta de nuevo", "<h1>No pudimos abrir el pago</h1>"
                                                          "<p>Intenta de nuevo en unos minutos.</p>", sb))
                    if not datos:
                        return self.responder(404, pagina("Enlace vencido", "<h1>Este enlace de pago ya no "
                                                          "está disponible</h1>", sb))
                    return self.responder(200, pagina("Pagar Pase", pantalla_checkout(app.c, datos), sb))
                if u.path == "/retorno":
                    # ePayco añade ?ref_payco=; nosotros pusimos ?ref=. Solo informa: no activa nada.
                    app.pase.anotar_ref_pasarela(q.get("ref"), q.get("ref_payco"))
                    fila = app.pase.uno("SELECT persona_id FROM pagos WHERE referencia=?", q.get("ref", ""))
                    firma = app.firmar(fila["persona_id"]) if fila else None
                    return self.responder(200, pagina("Confirmando pago", retorno(app.c, firma), sb))
                if u.path == "/webhooks/epayco":  # por si la confirmación se configura como GET
                    return self.confirmacion(q)
                if u.path == "/estado-pago":
                    fila = None
                    if q.get("ref"):
                        fila = app.pase.uno("SELECT estado FROM pagos WHERE referencia=?", q["ref"])
                    elif q.get("ref_payco"):
                        fila = app.pase.uno("SELECT estado FROM pagos WHERE ref_pasarela=?", q["ref_payco"])
                    return self.json(200, {"estado": fila["estado"] if fila else "PENDIENTE"})
                if u.path.startswith("/estaticos/") and u.path[11:] in ESTATICOS:
                    with open(ESTATICOS[u.path[11:]], "rb") as f:
                        return self.responder(200, f.read(), "image/svg+xml",
                                              {"Cache-Control": "public, max-age=86400"})
                if u.path in ("/mi-pase", "/mi-pase/cancelar", "/mi-pase/listo"):
                    cuenta = self.cuenta(q.get("p"))
                    if not cuenta:
                        return self.mi_pase("Mi Pase", pantalla_codigo(vencido=bool(q.get("p"))))
                    pid, sus = cuenta
                    if u.path == "/mi-pase/listo":
                        return self.mi_pase("Pase cancelado", pantalla_cancelacion_lista(
                            app.c, app.pase.persona(pid), sus, q["p"]))
                    if u.path == "/mi-pase/cancelar" and sus["estado"] in ("activa", "en_mora") \
                            and not sus["cancelar_al_corte"]:
                        return self.mi_pase("Cancelar mi Pase", pantalla_confirmar_cancelacion(app.c, sus, q["p"]))
                    return self.mi_pase("Mi Pase", pantalla_mi_pase(app.c, app.pase.persona(pid), sus, q["p"],
                                                                    app.firmar(pid)))
                if u.path == "/salud":
                    return self.json(200, {"ok": True, "entorno": app.c.entorno})
                if u.path in ("/tablero", "/tablero/pagos.csv"):
                    sin_cache = {"Cache-Control": "no-store"}
                    if not self.admin_valido():
                        if u.path != "/tablero":
                            return self.redirigir("/tablero")
                        return self.responder(200, pagina("Tablero", login_html(app.admin_configurado()), sb),
                                              extra=sin_cache)
                    if u.path == "/tablero":
                        buscar = q.get("buscar")
                        soporte = tablero_soporte(buscar, app.pase.buscar_personas(buscar) if buscar else [],
                                                  q.get("hecho", ""))
                        return self.responder(200, tablero_html(app.pase.tablero(), app.c.precio_centavos // 100,
                                                                sb, soporte), extra=sin_cache)
                    return self.responder(200, ("\ufeff" + app.pase.pagos_csv()).encode(), "text/csv; charset=utf-8",
                                          extra={**sin_cache, "Content-Disposition":
                                                 'attachment; filename="pagos-pase.csv"'})
                if u.path == "/admin/resumen":
                    token = os.environ.get("PASE_ADMIN_TOKEN")
                    if not token or self.headers.get("Authorization") != f"Bearer {token}":
                        return self.json(401, {"error": "no autorizado"})
                    return self.json(200, app.pase.resumen())
                self.responder(404, pagina("No encontrado", "<h1>Página no encontrada</h1>", sb))

            def do_POST(self):
                u = urllib.parse.urlparse(self.path)
                sb = app.c.entorno == "sandbox"
                if u.path == "/tablero/entrar":
                    datos = dict(urllib.parse.parse_qsl(self.leer().decode(errors="replace")))
                    sesion = app.entrar_admin(datos.get("usuario", ""), datos.get("clave", ""), self.ip())
                    if not sesion:
                        return self.responder(401, pagina("Tablero", login_html(
                            app.admin_configurado(), "Usuario o contraseña incorrectos."), sb))
                    return self.redirigir("/tablero", self.galleta_admin(sesion, 12 * 3600))
                if u.path == "/tablero/accion":
                    if not self.admin_valido():
                        return self.redirigir("/tablero")
                    datos = self.formulario()
                    pid = int(datos["persona"]) if datos.get("persona", "").isdigit() else 0
                    p = app.pase.persona(pid)
                    accion = datos.get("accion")
                    hecho = "No se pudo: la persona no está en un estado que lo permita."
                    if p and accion == "cancelar_corte" and app.pase.pedir_cancelacion(pid, "", "soporte"):
                        hecho = f"{p['nombre']}: cancelación programada al corte."
                    elif p and accion == "cancelar_ya" and app.pase.suscripcion(pid) and \
                            app.pase.suscripcion(pid)["estado"] in ("activa", "en_mora"):
                        app.pase.cancelar(pid, "cancelación por soporte", "soporte")
                        hecho = f"{p['nombre']}: Pase cerrado."
                    elif p and accion == "deshacer" and app.pase.deshacer_cancelacion(pid, "soporte"):
                        hecho = f"{p['nombre']}: sigue con el Pase."
                    q = urllib.parse.urlencode({"buscar": datos.get("buscar", ""), "hecho": hecho})
                    return self.redirigir(f"/tablero?{q}")
                if u.path == "/mi-pase/codigo":
                    correo = self.formulario().get("correo", "")[:200]
                    if app.pase.pedir_codigo(correo) and app.c.smtp_host:
                        # el código no espera al timer de correos (cada 5 minutos)
                        threading.Thread(target=app.pase.enviar_avisos, daemon=True).start()
                    return self.mi_pase("Mi Pase", pantalla_codigo(correo, enviado=True))
                if u.path == "/mi-pase/entrar":
                    datos = self.formulario()
                    pid = app.pase.validar_codigo(datos.get("correo"), datos.get("codigo"))
                    if not pid:
                        return self.mi_pase("Mi Pase", pantalla_codigo(
                            datos.get("correo", ""), enviado=True,
                            error="El código no es correcto o ya venció. Revísalo o pide otro."), 401)
                    firma = app.pase.firma_mi_pase(pid, ENLACE_CODIGO_HORAS * 3600)
                    return self.redirigir(f"/mi-pase?p={firma}", self.PRIVADO)
                if u.path in ("/mi-pase/cancelar", "/mi-pase/seguir"):
                    datos = self.formulario()
                    cuenta = self.cuenta(datos.get("p"))
                    if not cuenta:
                        return self.mi_pase("Mi Pase", pantalla_codigo(vencido=True), 401)
                    pid, firma = cuenta[0], urllib.parse.quote(datos["p"])
                    if u.path == "/mi-pase/seguir":
                        app.pase.deshacer_cancelacion(pid)
                        return self.redirigir(f"/mi-pase?p={firma}", self.PRIVADO)
                    motivo = datos.get("motivo", "")
                    if not app.pase.pedir_cancelacion(pid, motivo if motivo in MOTIVOS else ""):
                        return self.redirigir(f"/mi-pase?p={firma}", self.PRIVADO)
                    return self.redirigir(f"/mi-pase/listo?p={firma}", self.PRIVADO)
                if u.path == "/tablero/salir":
                    return self.redirigir("/tablero", self.galleta_admin("", 0))
                if u.path == "/webhooks/epayco":
                    crudo = self.leer().decode(errors="replace")
                    if "json" in self.headers.get("Content-Type", ""):
                        try:
                            datos = {k: str(v) for k, v in json.loads(crudo or "{}").items()}
                        except (ValueError, AttributeError):
                            return self.json(400, {"ok": False})
                    else:
                        datos = dict(urllib.parse.parse_qsl(crudo))
                    return self.confirmacion(datos)
                if u.path == "/inscripcion":
                    datos = dict(urllib.parse.parse_qsl(self.leer().decode()))
                    try:
                        pid = app.pase.inscribir(datos, datos.get("canal") or "sin-canal",
                                                 self.ip(), self.headers.get("User-Agent", ""))
                    except (ValueError, KeyError) as e:
                        return self.responder(400, pagina("Revisa tus datos", f"<h1>Revisa tus datos</h1>"
                                                          f"<p>{html.escape(str(e))}</p>", sb))
                    if datos.get("opcion") == "pase":
                        return self.responder(303, b"", extra={"Location": f"/pagar?p={app.firmar(pid)}"})
                    app.pase.registro_gratis(pid)
                    return self.responder(200, pagina("Registro listo", "<h1>¡Tu registro está listo!</h1>"
                                                      "<p>Te enviamos un correo con tu acceso al aula.</p>", sb))
                if u.path == "/pagar/token":
                    try:
                        d = json.loads(self.leer())
                        pid = app.verificar(d.get("p"))
                        if not pid or not d.get("token"):
                            return self.json(400, {"error": "solicitud no válida"})
                        ref, _ = app.pase.pagar_con_token(pid, str(d["token"]), d.get("enmascarado", ""),
                                                          self.ip())
                        return self.json(200, {"referencia": ref})
                    except Exception as e:
                        return self.json(502, {"error": str(e)[:300]})
                self.responder(404, b"")

        return H

    def servir(self):
        self.cola.put(None)  # al arrancar, procesa lo que haya quedado pendiente
        # Detrás de nginx escucha solo en 127.0.0.1 (PASE_HOST); nginx pone el HTTPS.
        srv = ThreadingHTTPServer((os.environ.get("PASE_HOST", "127.0.0.1"), self.c.puerto),
                                  self.manejador())
        print(f"Conector Pase ({self.c.entorno}) en {self.c.url_publica} · puerto {self.c.puerto}")
        srv.serve_forever()


if __name__ == "__main__":
    App(Config.desde_entorno()).servir()
