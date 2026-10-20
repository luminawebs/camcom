"""Servidor HTTP del conector: formulario, pago, retorno y webhook de Wompi.

Solo biblioteca estándar de Python 3.9+. Uso:
    python -m pase.servidor          (lee la configuración del entorno)
"""
import hashlib
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
.tabs button{margin-right:6px}.oculto{display:none}#msg{margin-top:12px;font-weight:600}
"""


def pagina(titulo, cuerpo, sandbox=True):
    banda = ('<p class="aviso">Ambiente de PRUEBAS (sandbox de Wompi): no se hacen cobros reales.</p>'
             if sandbox else "")
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(titulo)}</title><style>{CSS}</style></head>"
            f"<body><main>{banda}{cuerpo}</main></body></html>").encode()


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
<div><label>Número de documento</label><input name="documento" required inputmode="numeric" pattern="[0-9A-Za-z-]{{5,15}}"></div></div>
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


def pantalla_pago(c, persona, comercio, firma):
    acept = comercio["aceptacion"]
    datos = comercio.get("datos_personales") or {}
    precio = f"${c.precio_centavos // 100:,}".replace(",", ".")
    cfg = json.dumps({
        "api": c.api_wompi, "pub": c.llave_publica, "p": firma,
        "acept": acept["acceptance_token"], "datos": datos.get("acceptance_token", ""),
    })
    enlace_datos = (f' y la <a href="{html.escape(datos["permalink"])}" target="_blank">autorización de '
                    f'datos personales</a>' if datos.get("permalink") else "")
    return f"""
<h1>Pase Empresario · {precio} al mes</h1>
<p>Hola, {html.escape(persona['nombre'].split()[0])}. El cobro se repite cada mes y puedes cancelar cuando quieras.</p>
<div class="caja">
<label class="check"><input type="checkbox" id="acepto"><span>Acepto los
<a href="{html.escape(acept['permalink'])}" target="_blank">términos de Wompi</a>{enlace_datos}.</span></label>
<div class="tabs"><button type="button" onclick="ver('tarjeta')">Tarjeta</button>
<button type="button" onclick="ver('nequi')">Nequi</button>
<button type="button" class="sec" onclick="location='/pagar/pse?p={firma}'">PSE (renuevas cada mes)</button></div>
<div id="tarjeta"><label>Número de tarjeta</label><input id="num" inputmode="numeric" autocomplete="cc-number">
<div class="fila"><div><label>Mes</label><input id="mes" placeholder="08" inputmode="numeric"></div>
<div><label>Año</label><input id="anio" placeholder="28" inputmode="numeric"></div>
<div><label>CVC</label><input id="cvc" inputmode="numeric"></div></div>
<label>Nombre en la tarjeta</label><input id="titular" autocomplete="cc-name">
<button class="verde" onclick="tarjeta()">Pagar {precio}</button></div>
<div id="nequi" class="oculto"><label>Celular Nequi</label><input id="cel" inputmode="tel">
<button class="verde" onclick="nequi()">Enviar solicitud a Nequi</button></div>
<p id="msg"></p>
<p class="nota">Los datos de tu tarjeta van directo a Wompi; EduNest no los ve ni los guarda.</p>
</div>
<script>
const C={cfg};
const $=id=>document.getElementById(id), msg=t=>$('msg').textContent=t;
function ver(t){{$('tarjeta').classList.toggle('oculto',t!=='tarjeta');$('nequi').classList.toggle('oculto',t!=='nequi')}}
async function wompi(ruta,cuerpo){{const r=await fetch(C.api+ruta,{{method:cuerpo?'POST':'GET',
 headers:{{'Content-Type':'application/json','Authorization':'Bearer '+C.pub}},body:cuerpo&&JSON.stringify(cuerpo)}});
 const j=await r.json(); if(!r.ok) throw new Error((j.error&&JSON.stringify(j.error.messages||j.error.reason))||r.status); return j.data}}
async function enviar(tipo,token,masc){{const r=await fetch('/pagar/token',{{method:'POST',headers:{{'Content-Type':'application/json'}},
 body:JSON.stringify({{p:C.p,tipo,token,acept:C.acept,datos:C.datos,enmascarado:masc}})}});
 const j=await r.json(); if(!r.ok) throw new Error(j.error||r.status); location='/retorno?ref='+encodeURIComponent(j.referencia)}}
async function tarjeta(){{if(!$('acepto').checked) return msg('Debes aceptar los términos.');
 try{{msg('Procesando…');const num=$('num').value.replace(/\\D/g,'');
 const t=await wompi('/tokens/cards',{{number:num,cvc:$('cvc').value,exp_month:$('mes').value,exp_year:$('anio').value,card_holder:$('titular').value}});
 await enviar('CARD',t.id,'**** '+num.slice(-4))}}catch(e){{msg('No se pudo: '+e.message)}}}}
async function nequi(){{if(!$('acepto').checked) return msg('Debes aceptar los términos.');
 try{{const cel=$('cel').value.replace(/\\D/g,'');let t=await wompi('/tokens/nequi',{{phone_number:cel}});
 msg('Aprueba la solicitud en tu app Nequi…');
 for(let i=0;i<60&&t.status==='PENDING';i++){{await new Promise(r=>setTimeout(r,3000));t=await wompi('/tokens/nequi/'+t.id)}}
 if(t.status!=='APPROVED') return msg('Nequi no aprobó la solicitud.');
 await enviar('NEQUI',t.id,'Nequi ***'+cel.slice(-4))}}catch(e){{msg('No se pudo: '+e.message)}}}}
</script>"""


RETORNO = """
<h1 id="t">Estamos confirmando tu pago</h1>
<div class="caja"><p id="e">Esto suele tardar menos de un minuto. No cierres esta página.</p></div>
<script>
const ref=new URLSearchParams(location.search).get('ref')||'';
const tx=new URLSearchParams(location.search).get('id')||'';
async function mirar(){const r=await fetch('/estado-pago?ref='+encodeURIComponent(ref)+'&id='+encodeURIComponent(tx));
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
        clave = os.environ.get("PASE_SECRETO_SESION") or config.secreto_integridad or "solo-desarrollo"
        self._clave = hashlib.sha256(("sesion:" + clave).encode()).digest()
        self.cola = queue.Queue()
        threading.Thread(target=self._trabajador, daemon=True).start()

    # La persona viaja firmada en la URL: nadie puede pagar ni consultar a nombre de otro.
    def firmar(self, pid):
        return f"{pid}.{hmac.new(self._clave, str(pid).encode(), 'sha256').hexdigest()[:24]}"

    def verificar(self, firma):
        pid, _, _ = (firma or "").partition(".")
        return int(pid) if pid.isdigit() and hmac.compare_digest(self.firmar(int(pid)), firma) else None

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

            def leer(self):
                return self.rfile.read(int(self.headers.get("Content-Length") or 0))

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
                    comercio = app.pase.wompi.comercio()
                    return self.responder(200, pagina("Pase Empresario", pantalla_pago(
                        app.c, app.pase.persona(pid), comercio, q["p"]), sb))
                if u.path == "/pagar/pse":
                    pid = app.verificar(q.get("p"))
                    if not pid:
                        return self.responder(404, b"")
                    _, url = app.pase.url_pago_manual(pid)
                    return self.responder(302, b"", extra={"Location": url})
                if u.path == "/retorno":
                    # Wompi devuelve ?id=<transacción>; nosotros añadimos ?ref=. Solo informa.
                    return self.responder(200, pagina("Confirmando pago", RETORNO, sb))
                if u.path == "/estado-pago":
                    fila = None
                    if q.get("ref"):
                        fila = app.pase.uno("SELECT estado FROM pagos WHERE referencia=?", q["ref"])
                    elif q.get("id"):
                        fila = app.pase.uno("SELECT estado FROM pagos WHERE wompi_transaction_id=?", q["id"])
                    return self.json(200, {"estado": fila["estado"] if fila else "PENDIENTE"})
                if u.path == "/salud":
                    return self.json(200, {"ok": True, "entorno": app.c.entorno})
                if u.path == "/admin/resumen":
                    token = os.environ.get("PASE_ADMIN_TOKEN")
                    if not token or self.headers.get("Authorization") != f"Bearer {token}":
                        return self.json(401, {"error": "no autorizado"})
                    return self.json(200, app.pase.resumen())
                self.responder(404, pagina("No encontrado", "<h1>Página no encontrada</h1>", sb))

            def do_POST(self):
                u = urllib.parse.urlparse(self.path)
                sb = app.c.entorno == "sandbox"
                if u.path == "/webhooks/wompi":
                    codigo, eid = app.pase.recibir_evento(
                        self.leer(), self.headers.get("X-Event-Checksum", ""), self.client_address[0])
                    if eid:
                        app.cola.put(eid)
                    return self.json(codigo, {"ok": codigo == 200})
                if u.path == "/inscripcion":
                    datos = dict(urllib.parse.parse_qsl(self.leer().decode()))
                    try:
                        pid = app.pase.inscribir(datos, datos.get("canal") or "sin-canal",
                                                 self.client_address[0], self.headers.get("User-Agent", ""))
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
                        if not pid or d.get("tipo") not in ("CARD", "NEQUI"):
                            return self.json(400, {"error": "solicitud no válida"})
                        ref, _ = app.pase.pagar_con_token(pid, d["tipo"], d["token"], d["acept"],
                                                          d.get("datos") or None, d.get("enmascarado", ""))
                        return self.json(200, {"referencia": ref})
                    except Exception as e:
                        return self.json(502, {"error": str(e)[:300]})
                self.responder(404, b"")

        return H

    def servir(self):
        self.cola.put(None)  # al arrancar, procesa lo que haya quedado pendiente
        srv = ThreadingHTTPServer(("0.0.0.0", self.c.puerto), self.manejador())
        print(f"Conector Pase ({self.c.entorno}) en {self.c.url_publica} · puerto {self.c.puerto}")
        srv.serve_forever()


if __name__ == "__main__":
    App(Config.desde_entorno()).servir()
