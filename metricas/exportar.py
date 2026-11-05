"""Exportador semanal de métricas del negocio (Moodle + Pase Empresario).

Escribe en la carpeta de datos (por defecto negocio/datos):
  - metricas-AAAA-Sss.md       resumen legible de la semana
  - metricas-semanales.csv     una fila por semana (se reemplaza si la semana ya estaba)
  - metricas-cursos.csv        una fila por curso y semana
  - estado/moodle-vistos.json  ids de Moodle ya vistos por curso, para contar matrículas nuevas

Solo cifras agregadas: ningún nombre, correo ni documento sale de aquí.

Uso:
  python -m metricas.exportar                    # última semana completa (lunes a domingo, hora Colombia)
  python -m metricas.exportar --semana 2026-W45
  python -m metricas.exportar --salida "D:/30 Cam de comercio de Soacha/negocio/datos"

Variables de entorno:
  MOODLE_URL, MOODLE_TOKEN    servicio web de Moodle (Claude Aula)
  PASE_URL                    https://pase.edunest.co (por defecto)
  PASE_METRICAS_TOKEN         llave de solo lectura de /metricas en el servidor del Pase
  METRICAS_EXCLUIR            ids de Moodle separados por coma que no cuentan (cuentas de prueba)
Si falta una fuente, el resto se exporta igual y el informe dice qué faltó.
"""
import argparse
import csv
import datetime as dt
import json
import os
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

COL = dt.timezone(dt.timedelta(hours=-5))
CURSOS = {10: "AVS-G01", 11: "AVS-G02", 12: "AVS-G03", 13: "AVS-G04", 14: "AVS-G05", 15: "AVS-G06"}
ROLES_EQUIPO = {"manager", "editingteacher", "teacher", "coursecreator"}
GRUPO_PASE = "pase-empresario"
COLUMNAS = [
    "semana", "desde", "hasta", "exportado", "entorno_pase",
    # 1. matrículas
    "estudiantes_total", "matriculas_nuevas", "primer_ingreso_semana", "inscritos_nuevos_pase",
    # 2. terminan U3
    "terminaron_u3", "pct_termina_u3",
    # 3. conversión U3 → Pase
    "terminaron_u3_con_pase", "conversion_u3_pase",
    # 4. pagos
    "pases_nuevos", "renovaciones", "pagos_aprobados", "pagos_rechazados", "recaudo_cop", "camara_25_cop",
    # 5. cancelaciones
    "cancelaciones_pedidas", "cancelaciones_efectivas", "pases_activos", "en_mora", "tasa_cancelacion",
    # 6. costo por suscriptor
    "gasto_marketing_cop", "costo_por_suscriptor_cop",
    "notas",
]
COLUMNAS_CURSO = ["semana", "moodle_id", "codigo", "curso", "estudiantes", "matriculas_nuevas",
                  "con_pase", "terminaron_u3", "pct_termina_u3", "terminaron_u3_con_pase"]


class ErrorMoodle(Exception):
    pass


# ---------------------------------------------------------------------------- fechas
def semana_iso(texto=None, hoy=None):
    """Devuelve (etiqueta, lunes, lunes siguiente). Sin texto: la última semana completa."""
    if texto:
        m = re.fullmatch(r"(\d{4})-?W(\d{1,2})", texto.strip(), re.I)
        if not m:
            raise SystemExit("La semana va como AAAA-Wss, por ejemplo 2026-W45")
        lunes = dt.date.fromisocalendar(int(m[1]), int(m[2]), 1)
    else:
        hoy = hoy or dt.datetime.now(COL).date()
        lunes = hoy - dt.timedelta(days=hoy.weekday() + 7)
    a, s, _ = lunes.isocalendar()
    return f"{a}-W{s:02d}", lunes, lunes + dt.timedelta(days=7)


def epoca(fecha):
    return int(dt.datetime.combine(fecha, dt.time(), COL).timestamp())


# ---------------------------------------------------------------------------- Moodle
class Moodle:
    def __init__(self, url, token):
        self.url, self.token = url.rstrip("/"), token

    def llamar(self, funcion, **params):
        datos = {"wstoken": self.token, "wsfunction": funcion, "moodlewsrestformat": "json"}
        for k, v in params.items():
            datos[k] = v
        req = urllib.request.Request(f"{self.url}/webservice/rest/server.php",
                                     urllib.parse.urlencode(datos).encode())
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read())
        if isinstance(res, dict) and res.get("exception"):
            raise ErrorMoodle(f"{funcion}: {res.get('errorcode')} {res.get('message', '')[:120]}")
        return res


def secciones_u3(contenidos):
    """Actividades con seguimiento de finalización de la Unidad 3."""
    sec = next((s for s in contenidos if re.match(r"unidad\s*3\b", s.get("name", ""), re.I)), None)
    sec = sec or next((s for s in contenidos if s.get("section") == 3), None)
    if not sec:
        return []
    return [m["id"] for m in sec.get("modules", []) if m.get("completion")]


def medir_moodle(m, cursos, lunes, siguiente, vistos, excluir):
    notas, filas = [], []
    estudiantes_sitio, con_pase_sitio, terminaron_sitio = set(), set(), set()
    primer_ingreso = set()
    finalizacion_ok = True
    for cid, codigo in cursos.items():
        info = m.llamar("core_course_get_courses", **{"options[ids][0]": cid})
        nombre = info[0]["fullname"] if info else f"curso {cid}"
        u3 = secciones_u3(m.llamar("core_course_get_contents", courseid=cid))
        usuarios = m.llamar("core_enrol_get_enrolled_users", courseid=cid)
        estudiantes, con_pase = set(), set()
        for u in usuarios:
            roles = {r["shortname"] for r in u.get("roles", [])}
            if u["id"] in excluir or roles & ROLES_EQUIPO or "student" not in roles:
                continue
            estudiantes.add(u["id"])
            if any(g["name"].lower().startswith(GRUPO_PASE) for g in u.get("groups", [])):
                con_pase.add(u["id"])
            if epoca(lunes) <= (u.get("firstaccess") or 0) < epoca(siguiente):
                primer_ingreso.add(u["id"])
        habia = str(cid) in vistos
        antes = set(vistos.get(str(cid), []))
        nuevos = estudiantes - antes
        vistos[str(cid)] = sorted(antes | estudiantes)
        terminaron = set()
        if u3 and finalizacion_ok:
            for uid in estudiantes:
                try:
                    est = m.llamar("core_completion_get_activities_completion_status", courseid=cid, userid=uid)
                except ErrorMoodle as e:
                    finalizacion_ok = False
                    notas.append("Sin datos de U3: el servicio de Moodle no deja leer la finalización "
                                 f"(agregar core_completion_get_activities_completion_status). {e}")
                    break
                hechas = {s["cmid"] for s in est.get("statuses", []) if s.get("state") in (1, 2)}
                if set(u3) <= hechas:
                    terminaron.add(uid)
        elif not u3:
            notas.append(f"Curso {cid}: no se encontró la Unidad 3 con actividades a completar.")
        pct = round(100 * len(terminaron) / len(estudiantes), 1) if estudiantes and finalizacion_ok else ""
        filas.append({"moodle_id": cid, "codigo": codigo, "curso": nombre, "estudiantes": len(estudiantes),
                      "matriculas_nuevas": len(nuevos) if habia else "",
                      "con_pase": len(con_pase), "terminaron_u3": len(terminaron) if finalizacion_ok else "",
                      "pct_termina_u3": pct,
                      "terminaron_u3_con_pase": len(terminaron & con_pase) if finalizacion_ok else ""})
        estudiantes_sitio |= estudiantes
        con_pase_sitio |= con_pase
        terminaron_sitio |= terminaron
    comparables = [f for f in filas if f["matriculas_nuevas"] != ""]
    if len(comparables) < len(filas):
        notas.append("Primera exportación de " + ", ".join(str(f["moodle_id"]) for f in filas if f not in comparables)
                     + ": esa semana es la línea base de matrículas (no hay con qué comparar).")
    total = {
        "estudiantes_total": len(estudiantes_sitio),
        "matriculas_nuevas": sum(f["matriculas_nuevas"] for f in comparables) if comparables else "",
        "primer_ingreso_semana": len(primer_ingreso),
    }
    if finalizacion_ok:
        total["terminaron_u3"] = len(terminaron_sitio)
        total["pct_termina_u3"] = round(100 * len(terminaron_sitio) / len(estudiantes_sitio), 1) \
            if estudiantes_sitio else ""
        total["terminaron_u3_con_pase"] = len(terminaron_sitio & con_pase_sitio)
        total["conversion_u3_pase"] = round(100 * len(terminaron_sitio & con_pase_sitio) / len(terminaron_sitio),
                                            1) if terminaron_sitio else ""
    return total, filas, notas


# ---------------------------------------------------------------------------- Pase
def medir_pase(url, token, lunes, siguiente):
    q = urllib.parse.urlencode({"desde": lunes.isoformat(), "hasta": siguiente.isoformat()})
    req = urllib.request.Request(f"{url.rstrip('/')}/metricas?{q}", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read())
    activos = d.get("pases_activos_hoy", 0)
    return {
        "entorno_pase": d.get("entorno", ""),
        "inscritos_nuevos_pase": d["inscritos_nuevos"], "pases_nuevos": d["pases_nuevos"],
        "renovaciones": d["renovaciones"], "pagos_aprobados": d["pagos_aprobados"],
        "pagos_rechazados": d["pagos_rechazados"], "recaudo_cop": d["recaudo_cop"],
        "camara_25_cop": d["camara_25_cop"], "cancelaciones_pedidas": d["cancelaciones_pedidas"],
        "cancelaciones_efectivas": d["cancelaciones_efectivas"], "pases_activos": activos,
        "en_mora": d.get("en_mora_hoy", 0),
        "tasa_cancelacion": round(100 * d["cancelaciones_efectivas"] / (activos + d["cancelaciones_efectivas"]), 1)
        if activos + d["cancelaciones_efectivas"] else "",
    }, d.get("por_canal", {})


def gasto_marketing(carpeta, semana):
    """Lee datos/gasto-marketing.csv (lo llena Marketing): semana,canal,gasto_cop,nota."""
    ruta = carpeta / "gasto-marketing.csv"
    if not ruta.exists():
        return None, {}
    total, por_canal = 0, {}
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        for fila in csv.DictReader(f):
            if (fila.get("semana") or "").strip().upper() != semana.upper():
                continue
            valor = int(re.sub(r"[^\d]", "", fila.get("gasto_cop") or "") or 0)
            total += valor
            canal = (fila.get("canal") or "sin-canal").strip()
            por_canal[canal] = por_canal.get(canal, 0) + valor
    return total, por_canal


# ---------------------------------------------------------------------------- salida
def reemplazar_filas(ruta, columnas, filas, semana):
    previas = []
    if ruta.exists():
        with open(ruta, encoding="utf-8-sig", newline="") as f:
            previas = [r for r in csv.DictReader(f) if r.get("semana") != semana]
    todas = sorted(previas + filas, key=lambda r: (r["semana"], str(r.get("moodle_id", ""))))
    with open(ruta, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, columnas, extrasaction="ignore")
        w.writeheader()
        w.writerows(todas)


def pesos(v):
    return f"${v:,.0f}".replace(",", ".") if isinstance(v, (int, float)) else "sin dato"


def dato(v, sufijo=""):
    return "sin dato" if v in ("", None) else f"{v}{sufijo}"


def informe_md(f, cursos, canales, gasto_canal):
    prueba = f.get("entorno_pase") == "sandbox"
    l = [f"# Métricas semana {f['semana']} ({f['desde']} a {f['hasta']})", "",
         f"Exportado {f['exportado']} (hora Colombia) por `metricas/exportar.py`. Solo cifras agregadas.", ""]
    if prueba:
        l += ["> **El Pase está en modo prueba:** pagos, recaudo y cancelaciones son de prueba, no ventas reales.", ""]
    l += ["| # | Métrica | Valor | Cómo se mide |", "|---|---|---|---|",
          f"| 1 | Matrículas nuevas en la semana | {dato(f.get('matriculas_nuevas'))} "
          f"(primer ingreso: {dato(f.get('primer_ingreso_semana'))}; inscritos en el Pase: "
          f"{dato(f.get('inscritos_nuevos_pase'))}) | Estudiantes que aparecen en algún curso y no estaban la semana "
          "anterior |",
          f"| 2 | % que termina la U3 | {dato(f.get('pct_termina_u3'), ' %')} ({dato(f.get('terminaron_u3'))} de "
          f"{dato(f.get('estudiantes_total'))}) | Acumulado: completó todas las actividades de la U3 de al menos un "
          "curso |",
          f"| 3 | Conversión U3 → Pase | {dato(f.get('conversion_u3_pase'), ' %')} "
          f"({dato(f.get('terminaron_u3_con_pase'))} con Pase) | Acumulado: de quienes terminaron una U3, cuántos "
          "tienen el Pase |",
          f"| 4 | Pagos | {dato(f.get('pagos_aprobados'))} aprobados ({dato(f.get('pases_nuevos'))} Pases nuevos, "
          f"{dato(f.get('renovaciones'))} renovaciones), {dato(f.get('pagos_rechazados'))} rechazados · recaudo "
          f"{pesos(f.get('recaudo_cop'))} · 25 % Cámara {pesos(f.get('camara_25_cop'))} | Pagos aprobados en la "
          "semana |",
          f"| 5 | Cancelaciones | {dato(f.get('cancelaciones_efectivas'))} efectivas, "
          f"{dato(f.get('cancelaciones_pedidas'))} pedidas · tasa {dato(f.get('tasa_cancelacion'), ' %')} · "
          f"activos hoy {dato(f.get('pases_activos'))}, en mora {dato(f.get('en_mora'))} | Efectivas ÷ (activos + "
          "efectivas) |",
          f"| 6 | Costo por suscriptor | {pesos(f.get('costo_por_suscriptor_cop'))} (gasto "
          f"{pesos(f.get('gasto_marketing_cop'))}) | Gasto de marketing de la semana ÷ Pases nuevos |", ""]
    l += ["## Por curso", "", "| Moodle | Código | Estudiantes | Nuevos | Con Pase | Terminaron U3 | % U3 |",
          "|---|---|---|---|---|---|---|"]
    for c in cursos:
        l.append(f"| {c['moodle_id']} | {c['codigo']} | {c['estudiantes']} | {dato(c['matriculas_nuevas'])} | "
                 f"{c['con_pase']} | {dato(c['terminaron_u3'])} | {dato(c['pct_termina_u3'], ' %')} |")
    if canales or gasto_canal:
        l += ["", "## Por canal (código ?c= del enlace de compra)", "",
              "| Canal | Inscritos nuevos | Pases nuevos | Recaudo | Gasto | Costo por Pase |", "|---|---|---|---|---|---|"]
        for canal in sorted(set(canales) | set(gasto_canal)):
            d = canales.get(canal, {})
            g = gasto_canal.get(canal)
            costo = pesos(g / d["pases_nuevos"]) if g and d.get("pases_nuevos") else "sin dato"
            l.append(f"| {canal} | {d.get('inscritos_nuevos', 0)} | {d.get('pases_nuevos', 0)} | "
                     f"{pesos(d.get('recaudo_cop', 0))} | {pesos(g) if g is not None else '—'} | {costo} |")
    if f.get("notas"):
        l += ["", "## Notas", ""] + [f"- {n}" for n in f["notas"].split(" | ")]
    return "\n".join(l) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--semana", help="AAAA-Wss; por defecto la última semana completa")
    ap.add_argument("--salida", default="negocio/datos", help="carpeta datos/ del negocio")
    ap.add_argument("--cursos", default=",".join(map(str, CURSOS)), help="ids de Moodle separados por coma")
    a = ap.parse_args(argv)
    semana, lunes, siguiente = semana_iso(a.semana)
    carpeta = pathlib.Path(a.salida)
    (carpeta / "estado").mkdir(parents=True, exist_ok=True)
    cursos = {int(c): CURSOS.get(int(c), f"curso-{c}") for c in a.cursos.split(",") if c.strip()}
    excluir = {int(x) for x in re.findall(r"\d+", os.environ.get("METRICAS_EXCLUIR", ""))}

    fila = {k: "" for k in COLUMNAS}
    fila.update(semana=semana, desde=lunes.isoformat(), hasta=(siguiente - dt.timedelta(days=1)).isoformat(),
                exportado=dt.datetime.now(COL).strftime("%Y-%m-%d %H:%M"))
    notas, filas_cursos, canales = [], [], {}

    ruta_vistos = carpeta / "estado" / "moodle-vistos.json"
    vistos = json.loads(ruta_vistos.read_text(encoding="utf-8")) if ruta_vistos.exists() else {}
    if os.environ.get("MOODLE_URL") and os.environ.get("MOODLE_TOKEN"):
        try:
            total, filas_cursos, n = medir_moodle(Moodle(os.environ["MOODLE_URL"], os.environ["MOODLE_TOKEN"]),
                                                  cursos, lunes, siguiente, vistos, excluir)
            fila.update(total)
            notas += n
            ruta_vistos.write_text(json.dumps(vistos, indent=1), encoding="utf-8")
        except (ErrorMoodle, urllib.error.URLError, OSError) as e:
            notas.append(f"Moodle no respondió: {e}")
    else:
        notas.append("Faltan MOODLE_URL / MOODLE_TOKEN: sin datos de Moodle.")

    token = os.environ.get("PASE_METRICAS_TOKEN")
    if token:
        try:
            datos, canales = medir_pase(os.environ.get("PASE_URL", "https://pase.edunest.co"), token, lunes, siguiente)
            fila.update(datos)
        except (urllib.error.URLError, OSError, KeyError, ValueError) as e:
            notas.append(f"El Pase no respondió en /metricas: {e}")
    else:
        notas.append("Falta PASE_METRICAS_TOKEN: sin datos del Pase (pagos, cancelaciones).")

    gasto, gasto_canal = gasto_marketing(carpeta, semana)
    if gasto is None:
        notas.append("No hay datos/gasto-marketing.csv: sin costo por suscriptor.")
    else:
        fila["gasto_marketing_cop"] = gasto
        if fila.get("pases_nuevos"):
            fila["costo_por_suscriptor_cop"] = round(gasto / fila["pases_nuevos"])
    fila["notas"] = " | ".join(notas)

    reemplazar_filas(carpeta / "metricas-semanales.csv", COLUMNAS, [fila], semana)
    reemplazar_filas(carpeta / "metricas-cursos.csv", COLUMNAS_CURSO,
                     [{"semana": semana, **c} for c in filas_cursos], semana)
    md = carpeta / f"metricas-{semana}.md"
    md.write_text(informe_md(fila, filas_cursos, canales, gasto_canal), encoding="utf-8")
    print(f"Listo: {md}")
    for n in notas:
        print(" -", n)
    return fila


if __name__ == "__main__":
    main()
