#!/usr/bin/env python3
"""Pone (o actualiza) la invitación al Pase al final de la última unidad gratuita de un curso ya publicado.

Uso: python3 moodle/invitacion_pase.py cursos/<id> <id del curso en Moodle>

Antes: python3 plantillas/armar_curso.py cursos/<id> (arma paginas/u3-pase.html desde "pase" en curso.json).
No restaura el curso, así que no borra el avance de nadie: crea la Página con moodle/pagina_moodle.mjs
(Playwright, cuenta MOODLE_USER) o, si ya hay una con el mismo nombre en la sección, le cambia el contenido.
Luego, por REST, la deja de última en la sección. Si el curso se vuelve a restaurar, la Página ya viene en el .mbz.
"""
import json, os, re, subprocess, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "moodle"))
from armar_respaldo import fragmento, leer_estructura  # noqa: E402
from subir_moodle import rest  # noqa: E402


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    curso, mid = sys.argv[1].rstrip("/"), int(sys.argv[2])
    for snum, (sname, pasos) in enumerate(leer_estructura(curso)):
        for nombre, _, destino in pasos:
            if destino.endswith("-pase.html"):
                break
        else:
            continue
        break
    else:
        sys.exit(f"{curso} no tiene página del Pase: agrega \"pase\" a curso.json y corre plantillas/armar_curso.py")
    paso, titulo = nombre.split(" | ", 1)
    titulo = f"{paso.split(' · ')[-1]}: {titulo}"
    html = fragmento(os.path.join(curso, destino))

    sec = next(s for s in rest("core_course_get_contents", courseid=mid) if s["section"] == snum)
    if not sec["name"].lower().startswith(sname.split(" · ")[0].lower()):
        sys.exit(f"La sección {snum} del curso {mid} es «{sec['name']}», no {sname}: revisa el curso antes de seguir")
    previo = next((m for m in sec["modules"] if m["modname"] == "page" and m["name"] == titulo), None)

    tmp = Path(f"/tmp/invitacion-pase-{mid}.html")
    tmp.write_text(html, encoding="utf-8")
    orden = ["node", str(RAIZ / "moodle/pagina_moodle.mjs"), str(mid), str(snum), titulo, str(tmp)]
    subprocess.run(orden + ([str(previo["id"])] if previo else []), check=True)

    sec = next(s for s in rest("core_course_get_contents", courseid=mid) if s["section"] == snum)
    nueva = next(m for m in sec["modules"] if m["modname"] == "page" and m["name"] == titulo)
    if sec["modules"][-1]["id"] != nueva["id"]:
        rest("core_courseformat_update_course", action="cm_move", courseid=mid, ids=[nueva["id"]], targetsectionid=sec["id"])
    print(f"✓ {titulo} → {os.environ['MOODLE_URL'].rstrip('/')}/mod/page/view.php?id={nueva['id']}")


if __name__ == "__main__":
    main()
