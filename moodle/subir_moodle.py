#!/usr/bin/env python3
"""Sube un curso a Moodle: restaura su respaldo .mbz (curso nuevo o reemplazo) y lo deja revisado por REST.

Uso: python3 moodle/subir_moodle.py cursos/<id> [--categoria "Categoría General"] [--solo-revisar]

Antes: python3 moodle/publicar_curso.py cursos/<id> --corto AVS-Gnn (arma moodle/<id>/respaldo-*.mbz).

1. moodle/restaurar.mjs recorre el asistente de restauración con Playwright, con la cuenta MOODLE_USER / MOODLE_PASS
   (rol Gestor en la categoría). Si ya hay un curso con el mismo nombre corto, borra su contenido y restaura encima
   conservando roles y matrículas; si no, crea el curso en la categoría. Matricula a ClaudeBot como Profesor si falta.
2. Por REST, con MOODLE_TOKEN (ClaudeBot): pone el número de ID (<corto>-<id del curso>) y revisa que cada actividad
   esté en la sección y el orden que trae el respaldo; las que no, las mueve (core_courseformat_update_course, cm_move).
3. Agrega el resultado al final de cursos/<id>/registro-produccion.md.
--solo-revisar se salta la restauración y hace solo el paso 2 sobre el curso que ya está en Moodle.
"""
import argparse, json, os, re, subprocess, sys, urllib.parse, urllib.request, zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

RAIZ = Path(__file__).resolve().parents[1]
URL = os.environ.get("MOODLE_URL", "").rstrip("/")


def rest(funcion, **params):
    datos = [("wstoken", os.environ["MOODLE_TOKEN"]), ("wsfunction", funcion), ("moodlewsrestformat", "json")]
    for k, v in params.items():
        if isinstance(v, list):
            datos += [(f"{k}[{i}]", x) for i, x in enumerate(v)]
        elif isinstance(v, dict):
            datos += [(f"{k}[{kk}]", vv) for kk, vv in v.items()]
        elif v is not None:
            datos.append((k, v))
    r = urllib.request.urlopen(f"{URL}/webservice/rest/server.php", urllib.parse.urlencode(datos).encode(), timeout=120)
    res = json.loads(r.read() or "null")
    if isinstance(res, dict) and res.get("exception"):
        raise RuntimeError(f"{funcion}: {res.get('message')}")
    return res


def esperado(mbz):
    """Del respaldo: nombre completo, nombre corto y, por número de sección, la lista ordenada de actividades."""
    z = zipfile.ZipFile(mbz)
    raiz = ET.fromstring(z.read("moodle_backup.xml"))
    info = raiz.find("information")
    numero = {}
    for s in info.find("contents/sections"):
        sec = ET.fromstring(z.read(f"{s.findtext('directory')}/section.xml"))
        numero[s.findtext("sectionid")] = int(sec.findtext("number"))
    secciones = {}
    for a in info.find("contents/activities"):
        secciones.setdefault(numero[a.findtext("sectionid")], []).append((a.findtext("modulename"), a.findtext("title")))
    return info.findtext("original_course_fullname"), info.findtext("original_course_shortname"), secciones


def revisar(curso, corto, idnumber, secciones):
    rest("core_course_update_courses", **{"courses[0][id]": curso, "courses[0][idnumber]": idnumber})
    print(f"✓ número de ID: {idnumber}")
    contenido = rest("core_course_get_contents", courseid=curso)
    sec_id = {s["section"]: s["id"] for s in contenido}
    # cada actividad del respaldo se busca por tipo y nombre; las repetidas («Resumen en video» de cada unidad) se
    # distinguen por id: Moodle las crea en el orden del respaldo aunque las deje en otra sección
    libres = {}
    for s in contenido:
        for m in s["modules"]:
            libres.setdefault((m["modname"], m["name"]), []).append(m["id"])
    for v in libres.values():
        v.sort()
    actual = {s["section"]: [m["id"] for m in s["modules"]] for s in contenido}
    movidas, faltan = 0, []
    for num in sorted(secciones):
        ids = []
        for clave in secciones[num]:
            if libres.get(clave):
                ids.append(libres[clave].pop(0))
            else:
                faltan.append(f"{clave[1]} ({clave[0]})")
        if num not in sec_id:
            faltan.append(f"sección {num}")
            continue
        if [i for i in actual.get(num, []) if i in ids] != ids:
            # mover todas las de la sección, en orden, al final de ella deja el orden del respaldo
            rest("core_courseformat_update_course", action="cm_move", courseid=curso, ids=ids, targetsectionid=sec_id[num])
            movidas += 1
            print(f"  · sección {num}: actividades reubicadas ({len(ids)})")
    total = sum(len(v) for v in secciones.values())
    if faltan:
        print("✗ no encontré en Moodle: " + "; ".join(faltan))
    print(f"✓ {total - len(faltan)} de {total} actividades en su sección" + (f" ({movidas} secciones reordenadas)" if movidas else ""))
    return total, faltan, movidas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("curso")
    ap.add_argument("--categoria", default="Categoría General")
    ap.add_argument("--corto", help="nombre corto en Moodle si no es el del respaldo (p. ej. para una prueba aparte)")
    ap.add_argument("--bot", default="ClaudeBot", help="usuario del servicio web que se matricula como Profesor")
    ap.add_argument("--solo-revisar", type=int, metavar="ID_CURSO", help="no restaura; solo revisa ese curso por REST")
    a = ap.parse_args()
    for v in ("MOODLE_URL", "MOODLE_TOKEN") + (() if a.solo_revisar else ("MOODLE_USER", "MOODLE_PASS")):
        if not os.environ.get(v):
            sys.exit(f"Falta la variable de entorno {v}")
    curso_dir = Path(a.curso).resolve()
    mbzs = sorted((RAIZ / "moodle" / curso_dir.name).glob("respaldo-*.mbz"))
    if not mbzs:
        sys.exit(f"No hay respaldo en moodle/{curso_dir.name}/: corre antes moodle/publicar_curso.py")
    mbz = mbzs[-1]
    completo, corto, secciones = esperado(mbz)
    corto = a.corto or corto
    idnumber = f"{corto}-{curso_dir.name}"

    if a.solo_revisar:
        curso, accion = a.solo_revisar, "revisión"
    else:
        print(f"Subiendo {mbz.name} ({mbz.stat().st_size // 1024 // 1024} MB) como {corto}…")
        r = subprocess.run(["node", str(RAIZ / "moodle" / "restaurar.mjs"), str(mbz), corto, a.categoria, completo, a.bot],
                           stdout=subprocess.PIPE, text=True)
        lineas = r.stdout.strip().splitlines()
        print("\n".join(lineas[:-1]))
        if r.returncode or not lineas:
            sys.exit("✗ La restauración no terminó; mira el mensaje de arriba.")
        res = json.loads(lineas[-1])
        curso, accion = res["curso"], res["accion"]
        print(f"✓ curso {'creado' if accion == 'nuevo' else 'reemplazado'}: {URL}/course/view.php?id={curso}")

    total, faltan, movidas = revisar(curso, corto, idnumber, secciones)

    reg = curso_dir / "registro-produccion.md"
    if reg.exists():
        cuando = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        linea = (f"- {cuando} · {accion} en Moodle: {URL}/course/view.php?id={curso} · {mbz.name} · "
                 f"{total - len(faltan)}/{total} actividades en su sección" + (f", {movidas} secciones reordenadas" if movidas else "")
                 + (f" · faltan: {'; '.join(faltan)}" if faltan else ""))
        texto = reg.read_text(encoding="utf-8")
        if "## Subidas a Moodle" not in texto:
            texto = texto.rstrip() + "\n\n## Subidas a Moodle\n\nLas agrega `moodle/subir_moodle.py`.\n"
        reg.write_text(texto.rstrip() + "\n" + linea + "\n", encoding="utf-8")
    sys.exit(1 if faltan else 0)


if __name__ == "__main__":
    main()
