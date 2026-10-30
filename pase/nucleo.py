"""Lógica del Pase: personas, pagos, confirmaciones de ePayco, cobro mensual y cohortes de Moodle.

Regla de oro (RF-14): la matrícula SOLO se activa por una confirmación de ePayco con firma
válida y verificada contra su API, nunca por la página de retorno del navegador.
"""
import calendar
import datetime as dt
import hashlib
import hmac
import json
import re
import secrets
import sqlite3
import sys
import threading
import urllib.parse

from . import epayco as ep

ESQUEMA = """
CREATE TABLE IF NOT EXISTS personas (
  id INTEGER PRIMARY KEY, tipo_doc TEXT, documento TEXT UNIQUE, nombre TEXT,
  correo TEXT UNIQUE, whatsapp TEXT, negocio TEXT, matricula_mercantil TEXT,
  municipio TEXT, estado TEXT NOT NULL DEFAULT 'interesado', canal_origen TEXT,
  moodle_user_id INTEGER, creado TEXT, actualizado TEXT);
CREATE TABLE IF NOT EXISTS canales_persona (persona_id INTEGER, codigo TEXT, fecha TEXT);
CREATE TABLE IF NOT EXISTS consentimientos (
  persona_id INTEGER, version_texto TEXT, acepta_datos INTEGER, acepta_whatsapp INTEGER,
  fecha TEXT, ip TEXT, user_agent TEXT);
CREATE TABLE IF NOT EXISTS suscripciones (
  id INTEGER PRIMARY KEY, persona_id INTEGER UNIQUE, estado TEXT, medio TEXT,
  payment_source_id TEXT, medio_enmascarado TEXT, renovacion_manual INTEGER DEFAULT 0,
  inicio TEXT, proximo_corte TEXT, intento INTEGER DEFAULT 0, proximo_intento TEXT,
  cancelar_al_corte INTEGER DEFAULT 0, cancelada_en TEXT, motivo TEXT);
CREATE TABLE IF NOT EXISTS pagos (
  id INTEGER PRIMARY KEY, suscripcion_id INTEGER, persona_id INTEGER, tipo TEXT,
  periodo TEXT, referencia TEXT UNIQUE, ref_pasarela TEXT, monto INTEGER,
  estado TEXT, metodo TEXT, intento INTEGER, creado TEXT, aprobado_en TEXT);
CREATE TABLE IF NOT EXISTS eventos_pasarela (
  id INTEGER PRIMARY KEY, ref_payco TEXT, status TEXT, payload_crudo TEXT,
  firma_valida INTEGER, recibido_en TEXT, procesado_en TEXT, error TEXT,
  UNIQUE (ref_payco, status));
CREATE TABLE IF NOT EXISTS eventos_rechazados (recibido_en TEXT, ip TEXT, payload_crudo TEXT);
CREATE TABLE IF NOT EXISTS historial (persona_id INTEGER, evento TEXT, detalle TEXT, origen TEXT, fecha TEXT);
CREATE TABLE IF NOT EXISTS avisos (
  id INTEGER PRIMARY KEY, para TEXT, asunto TEXT, cuerpo TEXT, creado TEXT, enviado_en TEXT,
  intentos INTEGER DEFAULT 0, error TEXT, html TEXT);
"""
MAX_INTENTOS_AVISO = 5

TEXTO_AUTORIZACION_V1 = (
    "Autorizo a Lúmina Interactiva S.A.S. (EduNest) y a la Cámara de Comercio de Soacha, "
    "como responsables, para tratar mis datos personales con el fin de gestionar mi registro, "
    "mis cursos, mis pagos del Pase Empresario y enviarme información de la plataforma, "
    "según la Ley 1581 de 2012 y sus políticas de tratamiento de datos. (v1, borrador)"
)


def ahora():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sumar_mes(fecha: dt.date) -> dt.date:
    a, m = (fecha.year + 1, 1) if fecha.month == 12 else (fecha.year, fecha.month + 1)
    return dt.date(a, m, min(fecha.day, calendar.monthrange(a, m)[1]))


class Pase:
    def __init__(self, config, moodle, cliente_pasarela=None, hoy=None):
        self.c, self.moodle = config, moodle
        self.pasarela = cliente_pasarela or ep.Epayco(config)
        self._hoy = hoy
        self.bd = sqlite3.connect(config.base_datos, check_same_thread=False, isolation_level=None)
        self.bd.row_factory = sqlite3.Row
        if self.bd.execute("SELECT 1 FROM sqlite_master WHERE name='eventos_wompi'").fetchone():
            self.bd.close()
            raise RuntimeError(f"{config.base_datos} es de la versión con Wompi: archívala y arranca "
                               "con una base nueva (solo tenía pagos de sandbox).")
        self.bd.executescript(ESQUEMA)
        columnas = {r[1] for r in self.bd.execute("PRAGMA table_info(avisos)")}
        for col, tipo in (("intentos", "INTEGER DEFAULT 0"), ("error", "TEXT"), ("html", "TEXT")):
            if col not in columnas:  # bases creadas antes del envío real
                self.bd.execute(f"ALTER TABLE avisos ADD COLUMN {col} {tipo}")
        self.candado = threading.RLock()
        clave = config.secreto_sesion or config.p_key or "solo-desarrollo"
        self._clave = hashlib.sha256(("sesion:" + clave).encode()).digest()

    # Enlaces firmados: nadie puede pagar ni consultar a nombre de otro.
    def firma(self, texto):
        return hmac.new(self._clave, str(texto).encode(), "sha256").hexdigest()[:24]

    def firma_valida(self, texto, firma):
        return bool(firma) and hmac.compare_digest(self.firma(texto), firma)

    def enlace_checkout(self, referencia):
        q = urllib.parse.urlencode({"r": referencia, "f": self.firma(f"pago:{referencia}")})
        return f"{self.c.url_publica}/checkout?{q}"

    def hoy(self) -> dt.date:
        return self._hoy() if callable(self._hoy) else (self._hoy or dt.date.today())

    def q(self, sql, *args):
        with self.candado:
            return self.bd.execute(sql, args)

    def uno(self, sql, *args):
        return self.q(sql, *args).fetchone()

    def historial(self, persona_id, evento, detalle="", origen="conector"):
        self.q("INSERT INTO historial VALUES (?,?,?,?,?)", persona_id, evento, detalle, origen, ahora())

    def avisar(self, para, asunto, cuerpo, html=None):
        for destino in ([para] if isinstance(para, str) else para):
            self.q("INSERT INTO avisos (para, asunto, cuerpo, html, creado) VALUES (?,?,?,?,?)",
                   destino, asunto, cuerpo, html, ahora())

    def avisar_con_diseno(self, para, tipo, **datos):
        """Aviso con la plantilla de marca (texto + HTML); ver plantillas_correo.py."""
        from .plantillas_correo import armar
        asunto, texto, cuerpo_html = armar(tipo, self.c, **datos)
        self.avisar(para, asunto, texto, cuerpo_html)

    def enviar_avisos(self, smtp=None):
        """Envía los avisos pendientes. Un fallo de un destinatario no frena a los demás; tras
        MAX_INTENTOS_AVISO fallos el aviso se deja (queda el error en la tabla)."""
        from .correo import Smtp
        # Un aviso «enviando:» de hace más de 15 min es de una corrida que se cayó a mitad.
        vencido = "enviando:" + (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=15)).isoformat(
            timespec="seconds")
        pendientes = self.q("SELECT * FROM avisos WHERE (enviado_en IS NULL OR "
                            "(enviado_en LIKE 'enviando:%' AND enviado_en < ?)) AND intentos < ? ORDER BY id",
                            vencido, MAX_INTENTOS_AVISO).fetchall()
        if not pendientes:
            return {"enviados": 0, "fallidos": 0}
        if smtp is None:
            if not self.c.smtp_host:
                return {"enviados": 0, "fallidos": 0, "sin_smtp": len(pendientes)}
            smtp = Smtp(self.c)
        enviados = fallidos = 0
        with smtp as s:
            for a in pendientes:
                # Reserva atómica: si otra corrida (el timer y probar-correo a la vez) ya lo tomó, se salta.
                if self.q("UPDATE avisos SET enviado_en=? WHERE id=? AND enviado_en IS ?",
                          "enviando:" + ahora(), a["id"], a["enviado_en"]).rowcount != 1:
                    continue
                try:
                    s.enviar(a["para"], a["asunto"], a["cuerpo"], a["html"])
                except Exception as exc:
                    fallidos += 1
                    self.q("UPDATE avisos SET enviado_en=NULL, intentos=intentos+1, error=? WHERE id=?",
                           str(exc)[:500], a["id"])
                else:
                    enviados += 1
                    self.q("UPDATE avisos SET enviado_en=?, intentos=intentos+1, error=NULL WHERE id=?",
                           ahora(), a["id"])
        return {"enviados": enviados, "fallidos": fallidos}

    def avisar_organizaciones(self, asunto, cuerpo):
        if self.c.avisos_correo:
            self.avisar_con_diseno(self.c.avisos_correo, "interno", asunto=asunto, texto=cuerpo)

    def estado(self, persona_id, nuevo, origen="conector"):
        p = self.persona(persona_id)
        if p["estado"] != nuevo:
            self.q("UPDATE personas SET estado=?, actualizado=? WHERE id=?", nuevo, ahora(), persona_id)
            self.historial(persona_id, "estado", f"{p['estado']} → {nuevo}", origen)

    def persona(self, persona_id):
        return self.uno("SELECT * FROM personas WHERE id=?", persona_id)

    def suscripcion(self, persona_id):
        return self.uno("SELECT * FROM suscripciones WHERE persona_id=?", persona_id)

    # ------------------------------------------------------------------ formulario
    def inscribir(self, datos, canal="sin-canal", ip="", user_agent=""):
        """RF-01 a RF-05: crea o actualiza la persona (deduplica por documento y correo)."""
        if datos.get("acepta_datos") not in (True, "1", "on", 1):
            raise ValueError("Falta la autorización de tratamiento de datos")
        correo = datos["correo"].strip().lower()
        doc = datos["documento"].strip()
        existente = self.uno("SELECT id FROM personas WHERE documento=? OR correo=?", doc, correo)
        campos = (datos.get("tipo_doc", "CC"), doc, datos["nombre"].strip(), correo,
                  datos.get("whatsapp", ""), datos.get("negocio", ""),
                  datos.get("matricula_mercantil", ""), datos.get("municipio", ""))
        if existente:
            pid = existente["id"]
            self.q("""UPDATE personas SET tipo_doc=?, documento=?, nombre=?, correo=?, whatsapp=?,
                      negocio=?, matricula_mercantil=?, municipio=?, actualizado=? WHERE id=?""",
                   *campos, ahora(), pid)
        else:
            pid = self.q("""INSERT INTO personas (tipo_doc, documento, nombre, correo, whatsapp,
                            negocio, matricula_mercantil, municipio, canal_origen, creado, actualizado)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                         *campos, canal, ahora(), ahora()).lastrowid
            self.historial(pid, "interesado", f"canal {canal}", "formulario")
        self.q("INSERT INTO canales_persona VALUES (?,?,?)", pid, canal, ahora())
        self.q("INSERT INTO consentimientos VALUES (?,?,?,?,?,?,?)", pid, TEXTO_AUTORIZACION_V1, 1,
               1 if datos.get("acepta_whatsapp") in (True, "1", "on", 1) else 0, ahora(), ip, user_agent)
        return pid

    def registro_gratis(self, persona_id):
        """RF-07 a RF-09: cuenta en Moodle + cohorte registro-gratis."""
        p = self.persona(persona_id)
        uid = self._usuario_moodle(p)
        self.moodle.agregar_a_cohorte(uid, self.c.cohorte_gratis)
        if p["estado"] == "interesado":
            self.estado(persona_id, "registro_gratis", "formulario")
        from .moodle import nombre_usuario
        self.avisar_con_diseno(p["correo"], "registro", nombre=p["nombre"], usuario=nombre_usuario(p["correo"]))
        return uid

    def _usuario_moodle(self, p):
        if p["moodle_user_id"]:
            return p["moodle_user_id"]
        uid = self.moodle.asegurar_usuario(dict(p))
        self.q("UPDATE personas SET moodle_user_id=? WHERE id=?", uid, p["id"])
        return uid

    # ------------------------------------------------------------------ pago inicial
    def _nueva_referencia(self, persona_id, periodo):
        n = self.uno("SELECT COUNT(*) n FROM pagos WHERE persona_id=? AND periodo=?",
                     persona_id, periodo)["n"]
        # El sufijo evita chocar con referencias ya usadas en ePayco si la base se reinicia
        return f"PASE-{persona_id}-{periodo}-{n + 1}-{secrets.token_hex(3)}"

    def _registrar_pago(self, persona_id, tipo, metodo, intento=1, periodo=None):
        periodo = periodo or self.hoy().strftime("%Y%m")
        ref = self._nueva_referencia(persona_id, periodo)
        sus = self.suscripcion(persona_id)
        self.q("""INSERT INTO pagos (suscripcion_id, persona_id, tipo, periodo, referencia, monto,
                  estado, metodo, intento, creado) VALUES (?,?,?,?,?,?,?,?,?,?)""",
               sus["id"] if sus else None, persona_id, tipo, periodo, ref, self.c.precio_centavos,
               "PENDIENTE", metodo, intento, ahora())
        return ref

    def _asegurar_suscripcion(self, persona_id, medio, fuente=None, enmascarado="", manual=False):
        if self.suscripcion(persona_id):
            self.q("""UPDATE suscripciones SET medio=?, payment_source_id=?, medio_enmascarado=?,
                      renovacion_manual=?, cancelar_al_corte=0 WHERE persona_id=?""",
                   medio, fuente, enmascarado, int(manual), persona_id)
        else:
            self.q("""INSERT INTO suscripciones (persona_id, estado, medio, payment_source_id,
                      medio_enmascarado, renovacion_manual) VALUES (?,?,?,?,?,?)""",
                   persona_id, "pendiente", medio, fuente, enmascarado, int(manual))
        self.q("UPDATE pagos SET suscripcion_id=(SELECT id FROM suscripciones WHERE persona_id=?) "
               "WHERE persona_id=? AND suscripcion_id IS NULL", persona_id, persona_id)

    def ip_persona(self, persona_id):
        fila = self.uno("SELECT ip FROM consentimientos WHERE persona_id=? AND ip<>'' "
                        "ORDER BY rowid DESC LIMIT 1", persona_id)
        return fila["ip"] if fila else ""

    def pagar_con_token(self, persona_id, token, enmascarado="", ip=""):
        """Tarjeta tokenizada en el navegador (directo a ePayco): crea el cliente en ePayco y
        hace el primer cobro con su token. EduNest solo guarda ids (RF-12)."""
        p = self.persona(persona_id)
        fuente = self.pasarela.crear_cliente(token, dict(p))
        self._asegurar_suscripcion(persona_id, "tarjeta", json.dumps(fuente), enmascarado)
        ref = self._registrar_pago(persona_id, "inicial", "tarjeta")
        tx = self.pasarela.cobrar_tarjeta(fuente, ref, dict(p), ip or self.ip_persona(persona_id))
        self.q("UPDATE pagos SET ref_pasarela=? WHERE referencia=?", tx["id"], ref)
        self.historial(persona_id, "pago_iniciado", f"tarjeta {ref}", "formulario")
        return ref, tx

    def url_pago_manual(self, persona_id):
        """PSE, Nequi, Daviplata o tarjeta sin guardar: Checkout de ePayco y renovación manual (RF-13)."""
        self._asegurar_suscripcion(persona_id, "checkout", manual=True)
        ref = self._registrar_pago(persona_id, "inicial", "checkout")
        self.historial(persona_id, "pago_iniciado", f"checkout {ref}", "formulario")
        return ref, self.enlace_checkout(ref)

    def datos_checkout(self, referencia):
        """Datos para abrir el Checkout de un pago aún pendiente (None si ya no se puede pagar)."""
        pago = self.uno("SELECT * FROM pagos WHERE referencia=?", referencia)
        if not pago or pago["estado"] != "PENDIENTE":
            return None
        return self.pasarela.datos_checkout(referencia, dict(self.persona(pago["persona_id"])))

    def anotar_ref_pasarela(self, referencia, ref_payco):
        """La página de retorno trae ?ref_payco=: se guarda para que la conciliación pueda
        consultarla. No activa nada; el estado siempre sale de la API de ePayco."""
        if referencia and ref_payco and re.fullmatch(r"[0-9A-Za-z]{1,40}", str(ref_payco)):
            self.q("UPDATE pagos SET ref_pasarela=? WHERE referencia=? AND ref_pasarela IS NULL "
                   "AND estado='PENDIENTE'", str(ref_payco), referencia)

    # ------------------------------------------------------------------ webhook
    def recibir_evento(self, datos: dict, ip=""):
        """RF-15 a RF-17: confirmación de ePayco (campos x_…). Devuelve (código_http, id | None).
        Rápido: no llama a nadie; la verificación contra la API va en la cola."""
        crudo = json.dumps(datos, ensure_ascii=False)
        if not ep.confirmacion_valida(datos, self.c.cliente_id, self.c.p_key):
            self.q("INSERT INTO eventos_rechazados VALUES (?,?,?)", ahora(), ip, crudo[:20000])
            return 401, None
        if str(datos.get("x_cust_id_cliente", self.c.cliente_id)) != str(self.c.cliente_id):
            self.q("INSERT INTO eventos_rechazados VALUES (?,?,?)", ahora(), ip, crudo[:20000])
            return 401, None
        codigo = str(datos.get("x_cod_transaction_state") or datos.get("x_cod_response") or "")
        try:
            eid = self.q("""INSERT INTO eventos_pasarela (ref_payco, status, payload_crudo,
                            firma_valida, recibido_en) VALUES (?,?,?,1,?)""",
                         str(datos["x_ref_payco"]), ep.ESTADOS.get(codigo, "PENDING"), crudo,
                         ahora()).lastrowid
        except sqlite3.IntegrityError:
            return 200, None  # repetido: ya está guardado, no se vuelve a procesar
        return 200, eid

    def procesar_pendientes(self):
        """Procesa eventos guardados sin procesar (cola). Se puede correr las veces que sea."""
        hechos = 0
        for fila in self.q("SELECT id FROM eventos_pasarela WHERE procesado_en IS NULL ORDER BY id").fetchall():
            hechos += self.procesar_evento(fila["id"])
        return hechos

    def procesar_evento(self, evento_id):
        with self.candado:
            ev = self.uno("SELECT * FROM eventos_pasarela WHERE id=?", evento_id)
            if not ev or ev["procesado_en"]:
                return 0
            try:
                tx = self.pasarela.transaccion(ev["ref_payco"])  # RF-18: doble verificación
                if tx["status"] == "PENDING":
                    raise ValueError(f"ref_payco {ev['ref_payco']} sigue pendiente en ePayco")
                self.aplicar_transaccion(tx, origen="confirmación ePayco")
                self.q("UPDATE eventos_pasarela SET procesado_en=?, error=NULL WHERE id=?", ahora(), evento_id)
                return 1
            except Exception as e:  # queda pendiente para el siguiente intento
                print(f"Evento {evento_id} pendiente: {e!r}"[:500], file=sys.stderr, flush=True)
                self.q("UPDATE eventos_pasarela SET error=? WHERE id=?", repr(e)[:500], evento_id)
                return 0

    def aplicar_transaccion(self, tx, origen="conector"):
        """RF-19. Aplica el estado REAL de una transacción consultada en la API de ePayco.

        Todo o nada: si Moodle falla, el pago no queda APPROVED sin matrícula y el
        siguiente intento lo vuelve a aplicar."""
        with self.candado:
            self.bd.execute("BEGIN")
            try:
                self._aplicar_transaccion(tx, origen)
            except BaseException:
                self.bd.execute("ROLLBACK")
                raise
            self.bd.execute("COMMIT")

    def _aplicar_transaccion(self, tx, origen):
        pago = self.uno("SELECT * FROM pagos WHERE referencia=?", tx["reference"])
        if not pago:
            raise ValueError(f"Referencia desconocida {tx['reference']}")
        if tx["amount_in_cents"] != pago["monto"] or tx.get("currency", "COP") != self.c.moneda:
            raise ValueError(f"Monto o moneda no coinciden en {tx['reference']}")
        if "prueba" in tx and tx["prueba"] != self.c.pruebas:
            # Con la llave pública cualquiera puede crear transacciones de prueba con nuestra
            # referencia: en producción una transacción de prueba nunca da acceso.
            raise ValueError(f"{tx['reference']}: transacción de {'prueba' if tx['prueba'] else 'producción'} "
                             f"en entorno {self.c.entorno}")
        estado = tx["status"]
        if pago["estado"] == estado:
            return  # nada nuevo
        if pago["estado"] in ("APPROVED", "VOIDED") and estado != "VOIDED":
            return  # un estado final no retrocede
        self.q("UPDATE pagos SET estado=?, ref_pasarela=?, metodo=COALESCE(?, metodo), "
               "aprobado_en=CASE WHEN ?='APPROVED' THEN ? ELSE aprobado_en END WHERE id=?",
               estado, tx["id"], (tx.get("payment_method_type") or "").lower() or None,
               estado, ahora(), pago["id"])
        pid = pago["persona_id"]
        self.historial(pid, f"pago_{estado.lower()}", pago["referencia"], origen)
        if estado == "APPROVED":
            self._pago_aprobado(pago, origen)
        elif estado in ("DECLINED", "ERROR"):
            self._pago_rechazado(pago, origen)
        elif estado == "VOIDED":
            self._pago_anulado(pago, origen)

    def _pago_aprobado(self, pago, origen):
        pid = pago["persona_id"]
        p, sus = self.persona(pid), self.suscripcion(pid)
        uid = self._usuario_moodle(p)
        self.moodle.agregar_a_cohorte(uid, self.c.cohorte_gratis)
        self.moodle.agregar_a_cohorte(uid, self.c.cohorte_pase)
        hoy = self.hoy()
        if sus["estado"] in ("activa", "en_mora") and sus["proximo_corte"]:
            corte = sumar_mes(dt.date.fromisoformat(sus["proximo_corte"]))
        else:
            corte = sumar_mes(hoy)
        self.q("""UPDATE suscripciones SET estado='activa', inicio=COALESCE(inicio, ?),
                  proximo_corte=?, intento=0, proximo_intento=NULL, cancelada_en=NULL, motivo=NULL
                  WHERE persona_id=?""", hoy.isoformat(), corte.isoformat(), pid)
        anterior = p["estado"]
        if anterior == "cancelado":
            self.estado(pid, "suscrito", origen)
            self.historial(pid, "reactivo", pago["referencia"], origen)
            self.avisar_organizaciones("Reactivación del Pase", f"{p['nombre']} volvió al Pase.")
        elif anterior in ("suscrito", "activo", "en_mora"):
            self.estado(pid, "activo", origen)
            self.historial(pid, "renovo", pago["referencia"], origen)
        else:
            self.estado(pid, "suscrito", origen)
            self.avisar_organizaciones("Nueva suscripción al Pase",
                                       f"{p['nombre']} ({p['negocio']}) · canal {p['canal_origen']}")
        if anterior not in ("suscrito", "activo", "en_mora"):
            sus = self.suscripcion(pid)
            self.avisar_con_diseno(p["correo"], "pase_activo", nombre=p["nombre"],
                                   medio=sus["medio_enmascarado"], proximo_corte=sus["proximo_corte"])

    def _pago_rechazado(self, pago, origen):
        pid = pago["persona_id"]
        p = self.persona(pid)
        if pago["tipo"] == "inicial":
            self.avisar_con_diseno(p["correo"], "pago_rechazado", nombre=p["nombre"])
            return
        sus = self.suscripcion(pid)
        intento = pago["intento"]
        corte = dt.date.fromisoformat(sus["proximo_corte"])
        if intento < len(self.c.reintentos_dias):
            siguiente = corte + dt.timedelta(days=self.c.reintentos_dias[intento])
            self.q("UPDATE suscripciones SET estado='en_mora', intento=?, proximo_intento=? WHERE persona_id=?",
                   intento, siguiente.isoformat(), pid)
            self.estado(pid, "en_mora", origen)
            if intento == 1:
                self.avisar_con_diseno(p["correo"], "cobro_fallido", nombre=p["nombre"], reintento=siguiente,
                                       medio=sus["medio_enmascarado"])
        else:
            self.cancelar(pid, "reintentos agotados", origen)

    def _pago_anulado(self, pago, origen):
        pid = pago["persona_id"]
        sus = self.suscripcion(pid)
        if sus and sus["estado"] == "activa":
            # el periodo vuelve a no estar pagado: se cobra de nuevo con el calendario de reintentos
            self.q("UPDATE suscripciones SET estado='en_mora', proximo_corte=?, intento=0, "
                   "proximo_intento=NULL WHERE persona_id=?", self.hoy().isoformat(), pid)
            self.estado(pid, "en_mora", origen)
            self.historial(pid, "anulado", pago["referencia"], origen)

    # ------------------------------------------------------------------ cobro mensual
    def cobro_mensual(self):
        """RF-21 a RF-25. Tarea diaria. Devuelve lista de (persona_id, acción)."""
        hoy, hechos = self.hoy(), []
        filas = self.q("SELECT * FROM suscripciones WHERE estado IN ('activa','en_mora')").fetchall()
        for s in filas:
            pid, corte = s["persona_id"], dt.date.fromisoformat(s["proximo_corte"])
            if s["cancelar_al_corte"] and hoy >= corte:
                self.cancelar(pid, "cancelación voluntaria", "tarea programada")
                hechos.append((pid, "cancelada"))
                continue
            if s["renovacion_manual"]:
                hechos += self._renovacion_manual(s, hoy, corte)
                continue
            fecha_cobro = dt.date.fromisoformat(s["proximo_intento"]) if s["proximo_intento"] else corte
            if hoy < fecha_cobro:
                continue
            intento = (s["intento"] or 0) + 1
            if intento > len(self.c.reintentos_dias):
                self.cancelar(pid, "reintentos agotados", "tarea programada")
                hechos.append((pid, "cancelada"))
                continue
            if self.uno("SELECT 1 FROM pagos WHERE persona_id=? AND tipo='mensual' AND intento=? "
                        "AND periodo=? AND estado='PENDIENTE'", pid, intento, corte.strftime("%Y%m")):
                continue  # ya hay un cobro en curso para este intento
            p = self.persona(pid)
            ref = self._registrar_pago(pid, "mensual", s["medio"], intento, corte.strftime("%Y%m"))
            self.q("UPDATE suscripciones SET intento=? WHERE persona_id=?", intento, pid)
            try:
                tx = self.pasarela.cobrar_tarjeta(json.loads(s["payment_source_id"]), ref, dict(p),
                                                  self.ip_persona(pid))
                self.q("UPDATE pagos SET ref_pasarela=? WHERE referencia=?", tx["id"], ref)
                hechos.append((pid, f"cobro {ref}"))
            except ep.ErrorEpayco as e:
                self.q("UPDATE pagos SET estado='ERROR' WHERE referencia=?", ref)
                self._pago_rechazado(self.uno("SELECT * FROM pagos WHERE referencia=?", ref), "tarea programada")
                hechos.append((pid, f"error {e.estado}"))
        return hechos

    def _renovacion_manual(self, s, hoy, corte):
        pid = s["persona_id"]
        periodo = corte.strftime("%Y%m")
        pend = self.uno("SELECT * FROM pagos WHERE persona_id=? AND periodo=? AND tipo='mensual'",
                        pid, periodo)
        if not pend and hoy >= corte - dt.timedelta(days=5):
            ref = self._registrar_pago(pid, "mensual", "checkout", 1, periodo)
            p = self.persona(pid)
            enlace = self.enlace_checkout(ref)
            self.avisar_con_diseno(p["correo"], "renovar", nombre=p["nombre"], corte=corte, enlace=enlace)
            return [(pid, f"enlace {ref}")]
        ultimo = corte + dt.timedelta(days=self.c.reintentos_dias[-1])
        if hoy > ultimo and not self.uno("SELECT 1 FROM pagos WHERE persona_id=? AND periodo=? "
                                         "AND estado='APPROVED'", pid, periodo):
            self.cancelar(pid, "renovación manual sin pago", "tarea programada")
            return [(pid, "cancelada")]
        if hoy > corte and s["estado"] == "activa":
            self.q("UPDATE suscripciones SET estado='en_mora' WHERE persona_id=?", pid)
            self.estado(pid, "en_mora", "tarea programada")
        return []

    def cancelar(self, persona_id, motivo, origen="conector"):
        """RF-23/24: sale de la cohorte del Pase (Moodle desactiva, no borra avance)."""
        p = self.persona(persona_id)
        self.q("""UPDATE suscripciones SET estado='cancelada', cancelada_en=?, motivo=?,
                  proximo_intento=NULL WHERE persona_id=?""", ahora(), motivo, persona_id)
        if p["moodle_user_id"]:
            self.moodle.quitar_de_cohorte(p["moodle_user_id"], self.c.cohorte_pase)
        sus = self.suscripcion(persona_id)
        if sus and sus["payment_source_id"]:
            try:  # no se vuelve a cobrar a esa tarjeta; para volver se tokeniza de nuevo
                self.pasarela.quitar_tarjeta(json.loads(sus["payment_source_id"]))
                self.historial(persona_id, "fuente_anulada", sus["medio_enmascarado"] or "", origen)
            except (ep.ErrorEpayco, ValueError) as e:
                self.historial(persona_id, "error_anular_fuente", str(e)[:300], origen)
        self.estado(persona_id, "cancelado", origen)
        self.historial(persona_id, "cancelo", motivo, origen)
        self.avisar_organizaciones("Cancelación del Pase", f"{p['nombre']}: {motivo}")
        self.avisar_con_diseno(p["correo"], "pase_termino", nombre=p["nombre"], motivo=motivo)

    def pedir_cancelacion(self, persona_id):
        """RF-26: el acceso sigue hasta el corte; no se vuelve a cobrar."""
        self.q("UPDATE suscripciones SET cancelar_al_corte=1 WHERE persona_id=?", persona_id)
        self.historial(persona_id, "pidio_cancelar", "", "persona")

    # ------------------------------------------------------------------ conciliación
    def conciliar(self):
        """RNF-05: recupera confirmaciones perdidas consultando en ePayco los pagos pendientes
        cuyo x_ref_payco se conoce (cobros con tarjeta y checkouts que volvieron al retorno)."""
        n = 0
        for pago in self.q("SELECT * FROM pagos WHERE estado='PENDIENTE' AND ref_pasarela IS NOT NULL").fetchall():
            try:
                tx = self.pasarela.transaccion(pago["ref_pasarela"])
                if tx["status"] != "PENDING":
                    self.aplicar_transaccion(tx, origen="conciliación")
                    n += 1
            except Exception as e:
                self.historial(pago["persona_id"], "error_conciliacion", repr(e)[:300])
        return n

    def tablero(self, dias_renovacion=7):
        """Datos del tablero interno: cifras del mes (hora Colombia), estados, canales, próximas
        renovaciones, últimos pagos y lo que está fallando."""
        col = dt.timezone(dt.timedelta(hours=-5))
        mes = dt.datetime.now(col).strftime("%Y-%m")
        aprobados = self.q("SELECT monto, aprobado_en FROM pagos WHERE estado='APPROVED'").fetchall()
        del_mes = [r["monto"] for r in aprobados if r["aprobado_en"] and
                   dt.datetime.fromisoformat(r["aprobado_en"]).astimezone(col).strftime("%Y-%m") == mes]
        filas = lambda sql, *a: [dict(r) for r in self.q(sql, *a).fetchall()]
        cuenta = lambda sql: {r[0] or "—": r[1] for r in self.q(sql).fetchall()}
        limite = (self.hoy() + dt.timedelta(days=dias_renovacion)).isoformat()
        return {
            "mes": mes,
            "personas": cuenta("SELECT estado, COUNT(*) FROM personas GROUP BY estado ORDER BY 2 DESC"),
            "suscripciones": cuenta("SELECT estado, COUNT(*) FROM suscripciones GROUP BY estado ORDER BY 2 DESC"),
            "canales": filas("""SELECT COALESCE(p.canal_origen,'sin-canal') canal, COUNT(*) inscritos,
                                  SUM(s.estado='activa') activos
                                FROM personas p LEFT JOIN suscripciones s ON s.persona_id=p.id
                                GROUP BY 1 ORDER BY 2 DESC"""),
            "recaudo_mes_cop": sum(del_mes) // 100,
            "pagos_mes": len(del_mes),
            "recaudo_total_cop": sum(r["monto"] for r in aprobados) // 100,
            "renovaciones": filas("""SELECT p.nombre, p.correo, s.proximo_corte, s.medio, s.medio_enmascarado,
                                       s.renovacion_manual, s.cancelar_al_corte
                                     FROM suscripciones s JOIN personas p ON p.id=s.persona_id
                                     WHERE s.estado='activa' AND s.proximo_corte <= ?
                                     ORDER BY s.proximo_corte""", limite),
            "en_mora": filas("""SELECT p.nombre, p.correo, s.proximo_corte, s.intento, s.proximo_intento
                                FROM suscripciones s JOIN personas p ON p.id=s.persona_id
                                WHERE s.estado='en_mora' ORDER BY s.proximo_intento"""),
            "ultimos_pagos": filas("""SELECT pg.creado, pg.aprobado_en, p.nombre, pg.tipo, pg.periodo, pg.monto,
                                        pg.estado, pg.metodo, pg.referencia
                                      FROM pagos pg LEFT JOIN personas p ON p.id=pg.persona_id
                                      ORDER BY pg.id DESC LIMIT 25"""),
            "avisos_con_error": filas("SELECT para, asunto, intentos, error FROM avisos "
                                      "WHERE enviado_en IS NULL AND error IS NOT NULL ORDER BY id DESC LIMIT 10"),
            "avisos_en_cola": self.uno("SELECT COUNT(*) n FROM avisos WHERE enviado_en IS NULL")["n"],
            "eventos_pendientes": self.uno("SELECT COUNT(*) n FROM eventos_pasarela "
                                           "WHERE procesado_en IS NULL")["n"],
            "eventos_rechazados": self.uno("SELECT COUNT(*) n FROM eventos_rechazados")["n"],
        }

    def pagos_csv(self):
        import csv
        import io
        sal = io.StringIO()
        w = csv.writer(sal)
        w.writerow(["referencia", "ref_epayco", "creado", "aprobado_en", "documento", "nombre", "correo",
                    "canal", "tipo", "periodo", "monto_cop", "estado", "metodo"])
        for r in self.q("""SELECT pg.referencia, pg.ref_pasarela, pg.creado, pg.aprobado_en, p.documento,
                             p.nombre, p.correo, p.canal_origen, pg.tipo, pg.periodo, pg.monto, pg.estado,
                             pg.metodo
                           FROM pagos pg LEFT JOIN personas p ON p.id=pg.persona_id ORDER BY pg.id"""):
            fila = list(r)
            fila[10] = (fila[10] or 0) // 100
            w.writerow(fila)
        return sal.getvalue()

    def resumen(self):
        cuenta = lambda sql: {r[0]: r[1] for r in self.q(sql).fetchall()}
        return {
            "personas": cuenta("SELECT estado, COUNT(*) FROM personas GROUP BY estado"),
            "pagos": cuenta("SELECT estado, COUNT(*) FROM pagos GROUP BY estado"),
            "recaudo_aprobado_cop": (self.uno("SELECT COALESCE(SUM(monto),0) s FROM pagos "
                                              "WHERE estado='APPROVED'")["s"]) // 100,
            "eventos_pendientes": self.uno("SELECT COUNT(*) n FROM eventos_pasarela "
                                           "WHERE procesado_en IS NULL")["n"],
            "eventos_rechazados": self.uno("SELECT COUNT(*) n FROM eventos_rechazados")["n"],
        }
