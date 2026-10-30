"""Servidor HTTP del conector: formulario, pago, retorno y confirmación de ePayco.

Solo biblioteca estándar de Python 3.9+. Uso:
    python -m pase.servidor          (lee la configuración del entorno)
"""
import base64
import datetime as dt
import hmac
import html
import json
import os
import queue
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import moodle as moodle_mod
from .config import Config
from .nucleo import TEXTO_AUTORIZACION_V1, Pase

CSS = """
:root{--azul:#0b3d6e;--verde:#1e8e5a;--fondo:#f5f7fa;--texto:#1d2733;--borde:#d5dde6}
*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
background:var(--fondo);color:var(--texto)}main{max-width:560px;margin:0 auto;padding:24px 16px 48px}
h1{color:var(--azul);font-size:1.5rem;margin:.2em 0 .6em}.caja{background:#fff;border:1px solid var(--borde);
border-radius:12px;padding:20px;margin:16px 0}label{display:block;margin:12px 0 4px;font-weight:600}
input,select{width:100%;padding:10px;border:1px solid var(--borde);border-radius:8px;font:inherit}
.check{display:flex;gap:10px;align-items:flex-start;font-weight:400}.check input{width:auto;margin-top:4px}
button,.boton{display:inline-block;background:var(--azul);color:#fff;border:0;border-radius:8px;
padding:12px 18px;font:inherit;font-weight:600;cursor:pointer;text-decoration:none;margin-top:12px}
.verde{background:var(--verde)}.sec{background:#fff;color:var(--azul);border:1px solid var(--azul)}
.fila{display:flex;gap:10px}.fila>div{flex:1}.nota{font-size:.875rem;color:#56606b}
.aviso{background:#fff7e0;border:1px solid #e9c46a;border-radius:8px;padding:10px 12px;font-size:.9rem}
.tabs button{margin-right:6px}input.mal{border-color:#c0392b;background:#fff4f2}.oculto{display:none}#msg{margin-top:12px;font-weight:600}
"""


def pagina(titulo, cuerpo, sandbox=True):
    banda = ('<p class="aviso">Ambiente de PRUEBAS (modo prueba de ePayco): no se hacen cobros reales.</p>'
             if sandbox else "")
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(titulo)}</title><style>{CSS}</style></head>"
            f"<body><main>{banda}{cuerpo}</main></body></html>").encode()


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
.dos{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}.vacio{padding:12px;color:#56606b}
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


def tablero_html(d, precio_cop, sandbox):
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
    cuerpo = ['<h1>Tablero del Pase Empresario</h1>',
              f'<p class="nota">Recaudo total aprobado: {pesos(d["recaudo_total_cop"])}. '
              '<a href="/tablero/pagos.csv">Descargar pagos (CSV)</a></p>']
    if alertas:
        cuerpo.append(f'<p class="aviso">{e(" · ".join(alertas))}</p>')
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


def formulario(canal):
    c = html.escape(canal)
    return f"""
<h1>Aula Virtual Empresarial Soacha</h1>
<p>Regístrate gratis para ver los cursos gratuitos, o toma el Pase Empresario para tener todos los certificados.</p>
<form class="caja" method="post" action="/inscripcion">
<input type="hidden" name="canal" value="{c}">
<label>Nombre completo</label><input name="nombre" required autocomplete="name">
<div class="fila"><div><label>Tipo</label><select name="tipo_doc"><option>CC</option><option>CE</option>
<option>NIT</option><option>PPT</option></select></div>
<div><label>Número de documento</label><input name="documento" required inputmode="numeric" pattern="[0-9A-Za-z\\-]{{5,15}}"></div></div>
<label>Correo</label><input name="correo" type="email" required autocomplete="email">
<label>WhatsApp</label><input name="whatsapp" inputmode="tel" pattern="(\\+?57)?3[0-9]{{9}}" placeholder="3001234567">
<label>Nombre del negocio</label><input name="negocio">
<label>Matrícula mercantil (opcional)</label><input name="matricula_mercantil">
<label>Municipio</label><input name="municipio" value="Soacha">
<label class="check"><input type="checkbox" name="acepta_datos" required>
<span>{html.escape(TEXTO_AUTORIZACION_V1)}</span></label>
<label class="check"><input type="checkbox" name="acepta_whatsapp"><span>Quiero recibir mensajes por WhatsApp (opcional).</span></label>
<button name="opcion" value="pase" class="verde">Quiero el Pase Empresario</button>
<button name="opcion" value="gratis" class="sec">Solo el registro gratis</button>
</form>"""


def pantalla_pago(c, persona, firma):
    precio = f"${c.precio_centavos // 100:,}".replace(",", ".")
    cfg = json.dumps({"pub": c.llave_publica, "p": firma})
    nombre, correo = html.escape(persona["nombre"]), html.escape(persona["correo"])
    ayuda = ('<p class="nota">Modo prueba: usa la tarjeta 4575 6231 8229 0326 (aprueba) o 4151 6115 2758 3283 '
             '(rechaza), vence 12/2027, CVC 123. Una tarjeta inventada no la acepta ePayco.</p>'
             if c.pruebas else "")
    return f"""
<h1>Pase Empresario · {precio} al mes</h1>
<p>Hola, {html.escape(persona['nombre'].split()[0])}. Con tarjeta el cobro se repite cada mes y puedes cancelar cuando quieras.</p>
<div class="caja">
<form id="tarjeta" onsubmit="return tarjeta(event)">
<input type="hidden" data-epayco="card[name]" value="{nombre}">
<input type="hidden" data-epayco="card[email]" value="{correo}">
<label>Número de tarjeta</label><input id="num" data-epayco="card[number]" inputmode="numeric" autocomplete="cc-number" required>
<div class="fila"><div><label>Mes</label><input id="mes" data-epayco="card[exp_month]" placeholder="08" inputmode="numeric" required></div>
<div><label>Año</label><input id="anio" data-epayco="card[exp_year]" placeholder="2028" inputmode="numeric" required></div>
<div><label>CVC</label><input id="cvc" data-epayco="card[cvc]" inputmode="numeric" required></div></div>
<label class="check"><input type="checkbox" id="acepto" required><span>Autorizo a EduNest a cobrar {precio}
cada mes a esta tarjeta por medio de ePayco hasta que cancele el Pase.</span></label>
<button class="verde">Pagar {precio}</button></form>
<p id="msg"></p>{ayuda}
<p class="nota">Los datos de tu tarjeta van directo a ePayco; EduNest no los ve ni los guarda.</p>
<p><a class="boton sec" href="/pagar/checkout?p={firma}">Pagar con PSE, Nequi o Daviplata (renuevas cada mes)</a></p>
</div>
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="{html.escape(c.token_js)}"></script>
<script>
const C={cfg};
const $id=id=>document.getElementById(id), msg=t=>$id('msg').textContent=t;
ePayco.setPublicKey(C.pub);
// Mensajes en español y el campo marcado (ePayco responde en inglés, p. ej. «…field is empty: number»)
const CAMPO={{number:['num','El número de tarjeta no es válido. Revísalo.'],cvc:['cvc','El CVC son los 3 o 4 dígitos del respaldo de la tarjeta.'],
 exp_month:['mes','El mes debe ser de 01 a 12.'],exp_year:['anio','La tarjeta está vencida o el año no es válido.'],
 date_exp:['mes','La fecha de vencimiento no es válida (mes 01 a 12 y año de 4 dígitos, sin vencer).'],
 name:['num','Falta el nombre del titular.'],email:['num','Falta un correo válido.']}};
function marcar(clave){{document.querySelectorAll('input.mal').forEach(e=>e.classList.remove('mal'));
 const c=CAMPO[clave]; if(!c) return false; const e=$id(c[0]); e.classList.add('mal');
 if(clave==='date_exp') $id('anio').classList.add('mal'); e.focus(); msg(c[1]); return true}}
function luhn(n){{let s=0;for(let i=0;i<n.length;i++){{let d=+n[n.length-1-i];if(i%2){{d*=2;if(d>9)d-=9}}s+=d}}return n.length>=13&&n.length<=19&&s%10===0}}
function revisar(num){{const m=+$id('mes').value, hoy=new Date(), cvc=$id('cvc').value;
 if(!luhn(num)) return 'number';
 if(!(m>=1&&m<=12)) return 'exp_month';
 if($id('anio').value.length===2) $id('anio').value='20'+$id('anio').value;  // ePayco espera el año con 4 dígitos
 const a=+$id('anio').value;
 if($id('anio').value.length!==4||a<hoy.getFullYear()||(a===hoy.getFullYear()&&m<hoy.getMonth()+1)) return 'exp_year';
 if(!/^\\d{{3,4}}$/.test(cvc)) return 'cvc'; return ''}}
function tarjeta(ev){{ev.preventDefault();
 for(const id of ['num','mes','anio','cvc']) $id(id).value=$id(id).value.replace(/\\D/g,'');
 const num=$id('num').value;
 const malo=revisar(num); if(malo) return marcar(malo)&&false;
 marcar('');msg('Procesando…');
 ePayco.token.create(window.jQuery?jQuery('#tarjeta'):$id('tarjeta'),async function(error,token){{
  if(error){{const t=String(error.description||error.message||error);
   const clave=Object.keys(CAMPO).find(k=>t.endsWith(': '+k)); if(clave&&marcar(clave)) return;
   return msg('ePayco no aceptó la tarjeta: '+t)}}
  try{{const r=await fetch('/pagar/token',{{method:'POST',headers:{{'Content-Type':'application/json'}},
   body:JSON.stringify({{p:C.p,token:String(token&&token.id||token),enmascarado:'**** '+num.slice(-4)}})}});
   const j=await r.json(); if(!r.ok) throw new Error(j.error||r.status);
   location='/retorno?ref='+encodeURIComponent(j.referencia)}}catch(e){{msg('No se pudo: '+e.message)}}}});
 return false}}
</script>"""


def pantalla_checkout(c, datos):
    precio = f"${c.precio_centavos // 100:,}".replace(",", ".")
    return f"""
<h1>Pase Empresario · {precio}</h1>
<div class="caja"><p>Paga con PSE, Nequi, Daviplata o tarjeta en la ventana segura de ePayco.
Este pago cubre un mes; antes del corte te enviamos el enlace para renovar.</p>
<button class="verde" onclick="abrir()">Pagar {precio}</button></div>
<script src="{html.escape(c.checkout_js)}"></script>
<script>
function abrir(){{ePayco.checkout.configure({json.dumps(datos)}).open()}}
</script>"""


RETORNO = """
<h1 id="t">Estamos confirmando tu pago</h1>
<div class="caja"><p id="e">Esto suele tardar menos de un minuto. No cierres esta página.</p></div>
<script>
const ref=new URLSearchParams(location.search).get('ref')||'';
const tx=new URLSearchParams(location.search).get('ref_payco')||'';
async function mirar(){const r=await fetch('/estado-pago?ref='+encodeURIComponent(ref)+'&ref_payco='+encodeURIComponent(tx));
 const j=await r.json();
 if(j.estado==='APPROVED'){document.getElementById('t').textContent='Pago aprobado';document.getElementById('e').innerHTML='¡Listo! Tu Pase está activo. Te enviamos un correo con el acceso al aula.';return}
 if(j.estado==='DECLINED'||j.estado==='ERROR'||j.estado==='VOIDED'){document.getElementById('e').textContent='El pago no se aprobó. Puedes intentarlo de nuevo.';return}
 setTimeout(mirar,2500)}
mirar();
</script>"""


class App:
    def __init__(self, config: Config, pase: Pase = None):
        self.c = config
        self.pase = pase or Pase(config, moodle_mod.crear(config))
        self.cola = queue.Queue()
        threading.Thread(target=self._trabajador, daemon=True).start()

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
                """Usuario cualquiera y como clave PASE_ADMIN_TOKEN (autenticación básica del navegador)."""
                token = os.environ.get("PASE_ADMIN_TOKEN", "")
                auth = self.headers.get("Authorization", "")
                if len(token) < 16 or not auth.startswith("Basic "):
                    return False
                try:
                    clave = base64.b64decode(auth[6:]).decode().split(":", 1)[1]
                except (ValueError, IndexError):
                    return False
                return hmac.compare_digest(clave.encode(), token.encode())

            def ip(self):
                reenviada = self.headers.get("X-Forwarded-For", "")
                if reenviada and self.client_address[0] == "127.0.0.1":
                    return reenviada.split(",")[0].strip()
                return self.client_address[0]

            def leer(self):
                return self.rfile.read(int(self.headers.get("Content-Length") or 0))

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
                    return self.responder(200, pagina("Inscripción", formulario(q.get("c", "sin-canal")), sb))
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
                    return self.responder(200, pagina("Confirmando pago", RETORNO, sb))
                if u.path == "/webhooks/epayco":  # por si la confirmación se configura como GET
                    return self.confirmacion(q)
                if u.path == "/estado-pago":
                    fila = None
                    if q.get("ref"):
                        fila = app.pase.uno("SELECT estado FROM pagos WHERE referencia=?", q["ref"])
                    elif q.get("ref_payco"):
                        fila = app.pase.uno("SELECT estado FROM pagos WHERE ref_pasarela=?", q["ref_payco"])
                    return self.json(200, {"estado": fila["estado"] if fila else "PENDIENTE"})
                if u.path == "/salud":
                    return self.json(200, {"ok": True, "entorno": app.c.entorno})
                if u.path in ("/tablero", "/tablero/pagos.csv"):
                    if not self.admin_valido():
                        return self.responder(401, pagina("Tablero", "<h1>Acceso restringido</h1>", sb),
                                              extra={"WWW-Authenticate": 'Basic realm="Tablero del Pase"'})
                    sin_cache = {"Cache-Control": "no-store"}
                    if u.path == "/tablero":
                        return self.responder(200, tablero_html(app.pase.tablero(),
                                                                app.c.precio_centavos // 100, sb), extra=sin_cache)
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
