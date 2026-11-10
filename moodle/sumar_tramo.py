#!/usr/bin/env python3
"""Agrega a un curso que ya está en Moodle lo nuevo de su respaldo (tramo del Pase: U4-U7, Demuestra de U1-U3,
proyecto final y certificado) SIN borrar nada: las actividades que ya existen y el avance de los estudiantes quedan igual.

Uso: python3 moodle/sumar_tramo.py cursos/<id> --id <id del curso en Moodle> [--probar]

Antes: python3 moodle/publicar_curso.py cursos/<id> --corto AVS-Gnn (arma el respaldo completo del curso de 7 unidades).

1. Compara el respaldo completo con lo que hay en Moodle (REST, MOODLE_TOKEN): una actividad ya existe si en la misma
   sección hay otra del mismo tipo y con el mismo nombre.
2. Arma un respaldo reducido solo con las actividades nuevas y lo restaura con «Fusionar» (moodle/restaurar.mjs --sumar).
3. Ordena cada sección como en el respaldo completo (el mismo paso de subir_moodle.py).
4. Avisa de las páginas «[Configurar] …» ocultas que el respaldo ya no trae (p. ej. el antiguo «Reto final»): se quitan a mano.
5. Con moodle/pase_ajustes.mjs: pone el resumen de las secciones U4-U7 y CIERRE (la cabecera de la unidad y la tarjeta
   del Pase para quien no lo tiene) y restringe al grupo del Pase las secciones U4-U7 y las actividades marcadas
   «🔒 Pase» en estructura.md (Demuestra de U1-U3, proyecto final y certificado).
--probar hace el paso 1 y muestra lo que sumaría, sin tocar Moodle.
"""
import argparse, json, os, re, subprocess, sys, tempfile, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from subir_moodle import RAIZ, URL, esperado, rest, revisar  # noqa: E402

COMPRA = "https://pase.edunest.co/?c={}"


def reducir(mbz, salida, quitar):
    """Copia el .mbz sin las actividades de `quitar` (ids de módulo del respaldo). Edita el XML como texto para no
    cambiar su formato: Moodle rechaza un moodle_backup.xml reescrito por otro serializador."""
    z = zipfile.ZipFile(mbz)
    mb = z.read("moodle_backup.xml").decode("utf-8")
    dirs, fileids = set(), set()
    for bloque in re.findall(r"\s*<activity>\s*<moduleid>.*?</activity>", mb, re.S):
        mid = re.search(r"<moduleid>(\d+)</moduleid>", bloque).group(1)
        if mid in quitar:
            d = re.search(r"<directory>([^<]+)</directory>", bloque).group(1).rstrip("/") + "/"
            dirs.add(d)
            if d + "inforef.xml" in z.namelist():
                fileids |= set(re.findall(r"<id>(\d+)</id>", z.read(d + "inforef.xml").decode("utf-8")))
            mb = mb.replace(bloque, "", 1)
    mb = re.sub(r"\s*<setting>\s*<level>activity</level>\s*<activity>[a-z]+_(\d+)</activity>.*?</setting>",
                lambda m: "" if m.group(1) in quitar else m.group(0), mb, flags=re.S)
    files = re.sub(r"\s*<file id=\"(\d+)\">.*?</file>", lambda m: "" if m.group(1) in fileids else m.group(0),
                   z.read("files.xml").decode("utf-8"), flags=re.S)
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as out:
        for n in z.namelist():
            if any(n.startswith(d) for d in dirs):
                continue
            data = z.read(n)
            if n == "moodle_backup.xml":
                data = mb.encode("utf-8")
            elif n == "files.xml":
                data = files.encode("utf-8")
            elif n.startswith("sections/") and n.endswith("section.xml"):
                sec = data.decode("utf-8")
                m = re.search(r"<sequence>([^<]*)</sequence>", sec)
                if m:
                    seq = ",".join(x for x in m.group(1).split(",") if x and x not in quitar)
                    sec = sec.replace(m.group(0), f"<sequence>{seq}</sequence>")
                data = sec.encode("utf-8")
            out.writestr(n, data)


def resumenes(mbz):
    """{número de sección: resumen HTML} del respaldo completo (ya procesado por publicar_curso.py)."""
    z = zipfile.ZipFile(mbz)
    out = {}
    for n in z.namelist():
        if n.startswith("sections/") and n.endswith("section.xml"):
            sec = ET.fromstring(z.read(n))
            out[int(sec.findtext("number"))] = (sec.findtext("name"), sec.findtext("summary") or "")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("curso")
    ap.add_argument("--categoria", default="Categoría General")
    ap.add_argument("--bot", default="ClaudeBot")
    ap.add_argument("--id", type=int, required=True, help="id del curso en Moodle (p. ej. 10 para AVS-G01)")
    ap.add_argument("--probar", action="store_true")
    a = ap.parse_args()
    curso_dir = Path(a.curso).resolve()
    info = json.loads((curso_dir / "curso.json").read_text(encoding="utf-8"))
    gratis = (info.get("pase") or {}).get("gratis", 0)
    if not gratis:
        sys.exit("curso.json no tiene tramo del Pase (pase.gratis)")
    mbz = sorted((RAIZ / "moodle" / curso_dir.name).glob("respaldo-*.mbz"))[-1]
    completo, corto, secciones = esperado(mbz)
    cid = a.id
    contenido = rest("core_course_get_contents", courseid=cid)
    hay = {s["section"]: [(m["modname"], m["name"]) for m in s["modules"]] for s in contenido}

    # actividades del respaldo que ya están (misma sección, tipo y nombre)
    z = zipfile.ZipFile(mbz)
    raiz = ET.fromstring(z.read("moodle_backup.xml"))
    numero = {}
    for s in raiz.find("information/contents/sections"):
        sec = ET.fromstring(z.read(f"{s.findtext('directory')}/section.xml"))
        numero[s.findtext("sectionid")] = int(sec.findtext("number"))
    quitar, nuevas = set(), []
    libres = {k: list(v) for k, v in hay.items()}
    for act in raiz.find("information/contents/activities"):
        num, clave = numero[act.findtext("sectionid")], (act.findtext("modulename"), act.findtext("title"))
        if clave in libres.get(num, []):
            libres[num].remove(clave)
            quitar.add(act.findtext("moduleid"))
        else:
            nuevas.append((num, *clave))
    sobran = [(n, *k) for n, v in libres.items() for k in v]
    print(f"Curso {corto} (id {cid}): {len(quitar)} actividades ya están, {len(nuevas)} nuevas")
    for n, mod, t in nuevas:
        print(f"  + sección {n} · {mod} · {t}")
    for n, mod, t in sobran:
        print(f"  ? en Moodle y no en el respaldo: sección {n} · {mod} · {t}" + ("  → quitar a mano" if t.startswith("[Configurar]") else ""))
    if a.probar:
        return

    if nuevas:
        if True:
            reducido = mbz.with_name(f"suma-{mbz.name}")   # se deja junto al respaldo para revisar
            reducir(mbz, reducido, quitar)
            print(f"Restaurando {len(nuevas)} actividades nuevas con «Fusionar»…")
            r = subprocess.run(["node", str(RAIZ / "moodle" / "restaurar.mjs"), str(reducido), corto, a.categoria, completo, a.bot, "--sumar"],
                               stdout=subprocess.PIPE, text=True)
            lineas = r.stdout.strip().splitlines()
            print("\n".join(lineas[:-1]))
            if r.returncode or not lineas or json.loads(lineas[-1]).get("curso") != cid:
                sys.exit("✗ La restauración no terminó; mira el mensaje de arriba.")

    # páginas «[Configurar]» que el respaldo ya no trae
    contenido = rest("core_course_get_contents", courseid=cid)
    viejas = [m["id"] for s in contenido for m in s["modules"]
              if m["name"].startswith("[Configurar]") and (s["section"], m["modname"], m["name"]) in sobran]
    if viejas:  # no se borran solas: quedan ocultas para que alguien del equipo las quite a mano
        print(f"  (quedan {len(viejas)} páginas [Configurar] viejas y ocultas para quitar a mano: cm {viejas})")

    total, faltan, movidas = revisar(cid, corto, f"{corto}-{curso_dir.name}", secciones)

    # resúmenes de sección y restricciones del Pase
    contenido = rest("core_course_get_contents", courseid=cid)
    # el grupo del Pase lo busca pase_ajustes.mjs en la página de grupos (ClaudeBot no puede leer grupos por REST)
    res = resumenes(mbz)
    canal = info["pase"].get("canal", f"curso-{info['id']}")
    tarjeta = (f'<div class="as-tarjeta as-pila"><span class="as-eti">Con el Pase Empresario</span>'
               f'<p>Esta unidad se abre con el Pase Empresario: sigues en este mismo curso, con tu avance, y al final recibes el certificado.</p>'
               f'<p><a class="btn btn-primary" href="{COMPRA.format(canal)}" target="_blank" rel="noopener">Sigue con el Pase Empresario</a></p>'
               f'<p class="as-sec">Si ya tienes el Pase, sigue con los pasos de abajo.</p></div>')
    secs = []
    for s in contenido:
        n = s["section"]
        if n == 0 or n not in res:
            continue
        nombre, html = res[n]
        if gratis < n <= len(info["unidades"]):
            k = html.rfind("</div>")   # la tarjeta va dentro del contenedor .as de la cabecera
            html = html[:k] + tarjeta + "\n" + html[k:] if k >= 0 else html + tarjeta
            secs.append({"id": s["id"], "num": n, "html": html, "pase": True})
        elif n <= gratis or nombre.upper() == "CIERRE":   # cabeceras de U1-U3 («de 7», Demuestra con candado) y cierre
            secs.append({"id": s["id"], "num": n, "html": html, "pase": False})
    # actividades del Pase: las marcadas «🔒 Pase» en el respaldo (Demuestra U1-U3) y las del CIERRE con Pase
    pase_nombres = set()
    for linea in (curso_dir / "estructura.md").read_text(encoding="utf-8").splitlines():
        m = re.search(r"U(\d+) · Demuestra \| (.+?) \[", linea)
        if m and int(m.group(1)) <= gratis:
            pase_nombres.add(f"Demuestra: {m.group(2)}")
    pase_nombres |= {"[Configurar] Proyecto final entre pares (Taller)", "[Configurar] Certificado del curso (Certificado personalizado)"}
    acts = [m["id"] for s in contenido for m in s["modules"] if m["name"] in pase_nombres]
    # portada (sección 0): solo se cambia el nombre de la tarjeta de Cierre; el resto lo dejó tramo_pase.mjs
    viejo, nuevo = info["cierre"].get("titulo"), (info.get("cierre_pase") or {}).get("titulo")
    s0 = next(s for s in contenido if s["section"] == 0)
    portada = [[f'<span class="as-portada__nombre">{viejo}</span>', f'<span class="as-portada__nombre">{nuevo}</span>']] \
        if viejo and nuevo and viejo != nuevo else []
    spec = {"curso": cid, "secciones": secs, "actividades": acts, "portada": {"id": s0["id"], "reemplazos": portada}}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False)
    print(f"Ajustes: {len(secs)} secciones, {len(acts)} actividades restringidas al grupo del Pase")
    r = subprocess.run(["node", str(RAIZ / "moodle" / "pase_ajustes.mjs"), f.name])
    os.unlink(f.name)
    if r.returncode:
        sys.exit("✗ Los ajustes del Pase no terminaron")

    reg = curso_dir / "registro-produccion.md"
    if reg.exists():
        from datetime import datetime, timezone
        cuando = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        reg.write_text(reg.read_text(encoding="utf-8").rstrip() + "\n" +
                       f"- {cuando} · suma del tramo del Pase en Moodle: {URL}/course/view.php?id={cid} · {len(nuevas)} actividades nuevas · "
                       f"{total - len(faltan)}/{total} en su sección" + (f" · faltan: {'; '.join(faltan)}" if faltan else "") + "\n", encoding="utf-8")
    sys.exit(1 if faltan else 0)


if __name__ == "__main__":
    main()
