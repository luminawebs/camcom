#!/usr/bin/env python3
"""Arma un respaldo de Moodle (.mbz, formato moodle2, Moodle 4.3) a partir de un curso producido con armar_curso.py.

Uso: python3 moodle/armar_respaldo.py cursos/<id> --corto AVS-G01 [--salida moodle/<id>]

Lee estructura.md (orden y nombres), paginas/*.html (fragmentos) y scorm/*.zip.
Crea: secciones con su cabecera como resumen, Páginas, SCORM 1.2 (con contenido ya extraído)
y Foros de preguntas y respuestas. Lo que necesita configurarse a mano en Moodle (Retroalimentación,
Cuestionario, Taller, Certificado) entra como Página oculta "[Configurar] ..." con su ficha.
El curso queda visible y con finalización activada (pedido de David, 2026-10-09).
"""
import argparse, hashlib, io, json, os, re, sys, time, zipfile
from xml.sax.saxutils import escape

NULL = "$@NULL@$"
NOW = int(time.time())
V43 = "2023100900"


def x(v):
    return NULL if v is None else escape(str(v))


def el(tag, v):
    return f"<{tag}>{x(v)}</{tag}>"


def fields(d):
    return "\n".join("    " + el(k, v) for k, v in d.items())


def fragmento(ruta):
    s = open(ruta, encoding="utf-8").read()
    m = re.search(r"<!-- =+ COPIAR DESDE AQU[IÍ] =+ -->(.*?)<!-- =+ HASTA AQU[IÍ] =+ -->", s, re.S)
    if not m:
        sys.exit(f"Sin marcas COPIAR en {ruta}")
    return m.group(1).strip()


def portada(info, estructura, curso=None):
    """Sección 0: video de bienvenida + tarjeta por unidad (y CIERRE). portada.js enlaza cada tarjeta
    a la primera actividad visible de su sección; portada.css oculta las demás secciones."""
    tarjetas = []
    for snum, (sname, _) in enumerate(estructura):
        if snum == 0:
            continue
        if sname == "CIERRE":
            eti, nombre = "Cierre", info.get("cierre", {}).get("titulo") or "Cierre del curso"
        else:
            eti, nombre = sname.split(" · ", 1)[0].title(), sname.split(" · ", 1)[-1]
        tarjetas.append(f'<a class="as-portada__unidad as-sec-{snum}" href="#section-{snum}">'
                        f'<span class="as-eti">{escape(eti)}</span><span class="as-portada__nombre">{escape(nombre)}</span>'
                        '<span class="as-portada__ir">Explorar →</span></a>')
    video = ('<div class="as-hueco as-hueco--video"><b>Video de bienvenida</b><span>Reemplaza este recuadro por el enlace '
             'al video (YouTube o MP4): Moodle lo convierte en reproductor.</span></div>')
    if curso and os.path.exists(os.path.join(curso, "medios-moodle", "bienvenida.mp4")):
        video = ('<video controls preload="metadata" playsinline style="width:100%;display:block;border-radius:12px">'
                 '<source src="@@PLUGINFILE@@/bienvenida.mp4" type="video/mp4"></video>')
    return f"""<div class="as as-portada">
<div class="as-portada__cabeza">
<div class="as-portada__video">{video}</div>
<div class="as-portada__datos"><span class="as-eti">Curso gratuito · {escape(info.get("duracion", ""))}</span><span class="as-portada__titulo">{escape(info["titulo"])}</span><p>{escape(info.get("promesa", ""))}</p></div>
</div>
<div class="as-portada__grid">
{chr(10).join(tarjetas)}
</div>
</div>"""


def leer_estructura(curso):
    """Devuelve [(seccion, [(nombre, tipo, destino)])] desde estructura.md."""
    secciones, actual = [], None
    for linea in open(os.path.join(curso, "estructura.md"), encoding="utf-8"):
        m = re.match(r"^[├└]── (INICIO|UNIDAD \d+ · .+?|CIERRE)\s+\(", linea)
        if m:
            actual = (m.group(1), [])
            secciones.append(actual)
            continue
        m = re.match(r"^[│ ]\s+[├└]── (.+?) \[(.+?)\] → (\S+)", linea)
        if m and actual:
            actual[1].append((m.group(1).strip(), m.group(2), m.group(3)))
    return secciones


class Respaldo:
    def __init__(self):
        self.files = {}      # contenthash -> bytes
        self.filerecs = []   # registros de files.xml
        self.out = {}        # ruta -> texto
        self.fid = 0

    def add_file(self, ctx, comp, area, filepath, filename, data, mime, itemid=0):
        h = hashlib.sha1(data).hexdigest()
        self.files[h] = data
        self.fid += 1
        self.filerecs.append(dict(id=self.fid, contenthash=h, contextid=ctx, component=comp, filearea=area,
                                  itemid=itemid, filepath=filepath, filename=filename, userid=None, filesize=len(data),
                                  mimetype=mime, status=0, timecreated=NOW, timemodified=NOW,
                                  source=None if filename == "." else filename, author=None, license=None,
                                  sortorder=0, repositorytype=None, repositoryid=None, reference=None))
        return self.fid

    def add_dir(self, ctx, comp, area, filepath):
        return self.add_file(ctx, comp, area, filepath, ".", b"", "document/unknown")

    def files_xml(self):
        out = ['<?xml version="1.0" encoding="UTF-8"?>', "<files>"]
        for r in self.filerecs:
            rid = r.pop("id")
            out.append(f'  <file id="{rid}">')
            out += ["    " + el(k, v) for k, v in r.items()]
            out.append("  </file>")
            r["id"] = rid
        out.append("</files>")
        return "\n".join(out)


MIMES = {".html": "text/html", ".js": "application/javascript", ".css": "text/css", ".xml": "application/xml",
         ".zip": "application/zip", ".png": "image/png", ".jpg": "image/jpeg", ".pdf": "application/pdf",
         ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".mp3": "audio/mp3", ".mp4": "video/mp4"}


def mime(n):
    return MIMES.get(os.path.splitext(n)[1].lower(), "application/octet-stream")


def adjuntar(r, curso, html, ctx, comp, area, itemid=0):
    """Agrega al respaldo cada archivo citado como @@PLUGINFILE@@/<nombre> (tomado de <curso>/medios-moodle/)."""
    ids = []
    nombres = sorted(set(re.findall(r"@@PLUGINFILE@@/([^\"'?#<>\s]+)", html)))
    if nombres:
        ids.append(r.add_file(ctx, comp, area, "/", ".", b"", "document/unknown", itemid))
    for n in nombres:
        ruta = os.path.join(curso, "medios-moodle", n)
        if not os.path.exists(ruta):
            sys.exit(f"Falta {ruta} (citado en {comp}/{area})")
        ids.append(r.add_file(ctx, comp, area, "/", n, open(ruta, "rb").read(), mime(n), itemid))
    return ids


def comunes_actividad(r, d, fileids):
    r.out[f"{d}/roles.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<roles>\n  <role_overrides>\n  </role_overrides>\n  <role_assignments>\n  </role_assignments>\n</roles>'
    r.out[f"{d}/grades.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<activity_gradebook>\n  <grade_items>\n  </grade_items>\n  <grade_letters>\n  </grade_letters>\n</activity_gradebook>'
    r.out[f"{d}/grade_history.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<grade_history>\n  <grade_grades>\n  </grade_grades>\n</grade_history>'
    r.out[f"{d}/grading.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<areas>\n</areas>'
    r.out[f"{d}/competencies.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<course_module_competencies>\n  <competencies>\n  </competencies>\n</course_module_competencies>'
    r.out[f"{d}/filters.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<filters>\n  <filter_actives>\n  </filter_actives>\n  <filter_configs>\n  </filter_configs>\n</filters>'
    r.out[f"{d}/calendar.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<events>\n</events>'
    r.out[f"{d}/comments.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<comments>\n</comments>'
    refs = "".join(f"\n    <file>\n      <id>{i}</id>\n    </file>" for i in fileids)
    r.out[f"{d}/inforef.xml"] = ('<?xml version="1.0" encoding="UTF-8"?>\n<inforef>' +
                                 (f"\n  <fileref>{refs}\n  </fileref>" if fileids else "") + "\n</inforef>")


def module_xml(cmid, modname, secid, secnum, visible, completion, completionview=0, version=V43):
    d = dict(modulename=modname, sectionid=secid, sectionnumber=secnum, idnumber="", added=NOW, score=0, indent=0,
             visible=visible, visibleoncoursepage=1, visibleold=visible, groupmode=0, groupingid=0,
             completion=completion, completiongradeitemnumber=None, completionpassgrade=0,
             completionview=completionview, completionexpected=0, availability=None, showdescription=0,
             downloadcontent=1, lang="")
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<module id="{cmid}" version="{version}">\n{fields(d)}\n'
            "    <tags>\n    </tags>\n</module>")


def actividad(r, inst, cmid, ctx, modname, cuerpo):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<activity id="{inst}" moduleid="{cmid}" modulename="{modname}" contextid="{ctx}">\n'
            f'  <{modname} id="{inst}">\n{cuerpo}\n  </{modname}>\n</activity>')


def scoes_de(zipdata):
    z = zipfile.ZipFile(io.BytesIO(zipdata))
    man = z.read("imsmanifest.xml").decode("utf-8")
    mid = re.search(r'<manifest[^>]*identifier="([^"]+)"', man).group(1)
    org = re.search(r'<organization identifier="([^"]+)">\s*<title>(.*?)</title>', man, re.S)
    hrefs = dict(re.findall(r'<resource identifier="([^"]+)"[^>]*href="([^"]+)"', man))
    items = re.findall(r'<item identifier="([^"]+)" identifierref="([^"]+)"[^>]*>\s*<title>(.*?)</title>', man, re.S)
    scoes = [dict(manifest=mid, organization="", parent="/", identifier=org.group(1), launch="", scormtype="",
                  title=org.group(2))]
    for ident, ref, title in items:
        scoes.append(dict(manifest=mid, organization=org.group(1), parent=org.group(1), identifier=ident,
                          launch=hrefs[ref], scormtype="sco", title=title))
    return z, scoes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("curso")
    ap.add_argument("--corto", required=True, help="nombre corto del curso en Moodle, p. ej. AVS-G01")
    ap.add_argument("--salida")
    a = ap.parse_args()
    curso = a.curso.rstrip("/")
    info = json.load(open(os.path.join(curso, "curso.json"), encoding="utf-8"))
    cid = info["id"]
    idnumber = f"{a.corto}-{cid}"
    salida = a.salida or os.path.join(os.path.dirname(os.path.abspath(__file__)), cid)
    os.makedirs(salida, exist_ok=True)
    estructura = leer_estructura(curso)

    r = Respaldo()
    COURSEID, COURSECTX = 9000, 90000
    acts, secs, settings, resumen = [], [], [], []
    cm, inst = 100, 0
    for snum, (sname, pasos) in enumerate(estructura):
        secid = 200 + snum
        nombre_sec = sname.replace("UNIDAD", "Unidad", 1)
        prefijo = None
        m = re.match(r"Unidad (\d+)", nombre_sec)
        if m:
            prefijo = f"u{m.group(1)}"
        elif sname == "CIERRE":
            prefijo = "99"
        resumen_sec = portada(info, estructura, curso) if snum == 0 else ""
        if prefijo == "99":
            resumen_sec = fragmento(os.path.join(curso, "paginas/99-cierre.html"))
        elif prefijo:
            resumen_sec = fragmento(os.path.join(curso, f"paginas/{prefijo}-cabecera.html"))
        secuencia = []
        for nombre, tipo, destino in pasos:
            if destino == "paginas/99-cierre.html":
                continue  # ya es el resumen de la sección CIERRE
            cm += 1
            inst += 1
            ctx = 300 + cm
            titulo = nombre.split(" | ", 1)[-1] if " | " in nombre else nombre
            if " | " in nombre:
                paso = nombre.split(" | ")[0].split(" · ")[-1]
                titulo = f"{paso}: {titulo}"
            fileids = []
            if destino.startswith("piezas/"):
                pieza = destino.split("/")[1]
                zipname = f"{cid}-{pieza}.zip"
                data = open(os.path.join(curso, "scorm", zipname), "rb").read()
                modname = "scorm"
                fileids.append(r.add_dir(ctx, "mod_scorm", "package", "/"))
                fileids.append(r.add_file(ctx, "mod_scorm", "package", "/", zipname, data, "application/zip"))
                z, scoes = scoes_de(data)
                dirs = set()
                for n in z.namelist():
                    if n.endswith("/"):
                        continue
                    fp = "/" + os.path.dirname(n) + "/" if os.path.dirname(n) else "/"
                    parts = fp.strip("/").split("/") if fp != "/" else []
                    for k in range(len(parts) + 1):
                        dp = "/" + "/".join(parts[:k]) + ("/" if k else "")
                        if dp not in dirs:
                            dirs.add(dp)
                            fileids.append(r.add_dir(ctx, "mod_scorm", "content", dp))
                    fileids.append(r.add_file(ctx, "mod_scorm", "content", fp, os.path.basename(n), z.read(n), mime(n)))
                sco_xml = []
                for i, s in enumerate(scoes, 1):
                    sid = inst * 100 + i
                    sco_xml.append(f'      <sco id="{sid}">\n' + "\n".join("        " + el(k, v) for k, v in s.items()) +
                                   f"\n        {el('sortorder', i)}\n        <sco_datas>\n        </sco_datas>\n"
                                   "        <seq_ruleconds>\n        </seq_ruleconds>\n        <seq_rolluprules>\n        </seq_rolluprules>\n"
                                   "        <seq_objectives>\n        </seq_objectives>\n        <sco_tracks>\n        </sco_tracks>\n      </sco>")
                launch = inst * 100 + 2
                body = fields(dict(name=titulo, scormtype="local", reference=zipname, intro="", introformat=1,
                                   version="SCORM_1.2", maxgrade=100, grademethod=1, whatgrade=0, maxattempt=0,
                                   forcecompleted=0, forcenewattempt=0, lastattemptlock=0, masteryoverride=1,
                                   displayattemptstatus=1, displaycoursestructure=0, updatefreq=0,
                                   sha1hash=hashlib.sha1(data).hexdigest(), md5hash="", revision=1, launch=launch,
                                   skipview=2, hidebrowse=1, hidetoc=3, nav=1, navpositionleft=-100, navpositiontop=-100,
                                   auto=0, popup=0, options="", width=100, height=500, timeopen=0, timeclose=0,
                                   timemodified=NOW, completionstatusrequired=6, completionscorerequired=None,
                                   completionstatusallscos=0, autocommit=0))
                body += "\n    <scoes>\n" + "\n".join(sco_xml) + "\n    </scoes>"
                visible, completion, cview = 1, 2, 0
            elif "Foro" in tipo:
                modname = "forum"
                intro = fragmento(os.path.join(curso, destino))
                body = fields(dict(type="qanda", name=titulo, intro=intro, introformat=1, duedate=0, cutoffdate=0,
                                   assessed=0, assesstimestart=0, assesstimefinish=0, scale=0, maxbytes=0,
                                   maxattachments=1, forcesubscribe=0, trackingtype=1, rsstype=0, rssarticles=0,
                                   timemodified=NOW, warnafter=0, blockafter=0, blockperiod=0,
                                   completiondiscussions=0, completionreplies=2, completionposts=0,
                                   displaywordcount=0, lockdiscussionafter=0, grade_forum=0))
                body += ("\n    <discussions>\n    </discussions>\n    <subscriptions>\n    </subscriptions>\n"
                         "    <digests>\n    </digests>\n    <readposts>\n    </readposts>\n"
                         "    <trackedprefs>\n    </trackedprefs>\n    <poststags>\n    </poststags>\n    <grades>\n    </grades>")
                visible, completion, cview = 1, 2, 0
            else:
                modname = "page"
                contenido = fragmento(os.path.join(curso, destino))
                actividad_moodle = tipo.split(" · ")[0].split(" (")[0]
                configurar = actividad_moodle in ("Retroalimentación", "Cuestionario", "Taller", "Certificado personalizado")
                if configurar:
                    titulo = f"[Configurar] {titulo} ({actividad_moodle})"
                    contenido = (f'<p><strong>Para el equipo:</strong> reemplaza esta página por la actividad '
                                 f'<strong>{escape(tipo)}</strong> y usa este texto como su descripción.</p>\n' + contenido)
                body = fields(dict(name=titulo, intro="", introformat=1, content=contenido, contentformat=1,
                                   legacyfiles=0, legacyfileslast=None, display=5,
                                   displayoptions='a:3:{s:12:"printheading";s:1:"0";s:10:"printintro";s:1:"0";s:17:"printlastmodified";s:1:"0";}',
                                   revision=1, timemodified=NOW))
                fileids += adjuntar(r, curso, contenido, ctx, "mod_page", "content")
                visible, completion, cview = (0, 0, 0) if configurar else (1, 2, 1)
            d = f"activities/{modname}_{cm}"
            r.out[f"{d}/{modname}.xml"] = actividad(r, inst, cm, ctx, modname, body)
            r.out[f"{d}/module.xml"] = module_xml(cm, modname, secid, snum, visible, completion, cview)
            comunes_actividad(r, d, fileids)
            acts.append((cm, secid, modname, titulo, d))
            secuencia.append(str(cm))
            resumen.append(f"{nombre_sec} · {modname} · {titulo}{'' if visible else ' (oculta)'}")
        sd = f"sections/section_{secid}"
        r.out[f"{sd}/section.xml"] = (f'<?xml version="1.0" encoding="UTF-8"?>\n<section id="{secid}">\n' + fields(dict(
            number=snum, name=nombre_sec, summary=resumen_sec, summaryformat=1, sequence=",".join(secuencia),
            visible=1, availabilityjson=None, timemodified=NOW)) + "\n</section>")
        secfiles = adjuntar(r, curso, resumen_sec, COURSECTX, "course", "section", secid)
        refs = "".join(f"\n    <file>\n      <id>{i}</id>\n    </file>" for i in secfiles)
        r.out[f"{sd}/inforef.xml"] = ('<?xml version="1.0" encoding="UTF-8"?>\n<inforef>' +
                                     (f"\n  <fileref>{refs}\n  </fileref>" if secfiles else "") + "\n</inforef>")
        secs.append((secid, nombre_sec, sd))

    # Curso
    corto = a.corto
    nombre = info["titulo"]
    r.out["course/course.xml"] = (f'<?xml version="1.0" encoding="UTF-8"?>\n<course id="{COURSEID}" contextid="{COURSECTX}">\n' + fields(dict(
        shortname=corto, fullname=nombre, idnumber=idnumber,
        summary=fragmento(os.path.join(curso, "paginas/00-cabecera-curso.html")), summaryformat=1, format="topics",
        showgrades=0, newsitems=0, startdate=NOW, enddate=0, marker=0, maxbytes=0, legacyfiles=0, showreports=0,
        visible=1, groupmode=0, groupmodeforce=0, defaultgroupingid=0, lang="", theme="", timecreated=NOW,
        timemodified=NOW, requested=0, showactivitydates=0, showcompletionconditions=1, pdfexportfont=None,
        enablecompletion=1, completionnotify=0)) +
        '\n  <category id="1">\n    <name>Miscellaneous</name>\n    <description>$@NULL@$</description>\n  </category>\n'
        "  <tags>\n  </tags>\n  <customfields>\n  </customfields>\n  <courseformatoptions>\n"
        "    <courseformatoption>\n      <format>topics</format>\n      <sectionid>0</sectionid>\n      <name>hiddensections</name>\n      <value>1</value>\n    </courseformatoption>\n"
        "    <courseformatoption>\n      <format>topics</format>\n      <sectionid>0</sectionid>\n      <name>coursedisplay</name>\n      <value>0</value>\n    </courseformatoption>\n"
        "  </courseformatoptions>\n</course>")
    vacio = {
        "course/inforef.xml": "<inforef>\n</inforef>",
        "course/roles.xml": "<roles>\n  <role_overrides>\n  </role_overrides>\n  <role_assignments>\n  </role_assignments>\n</roles>",
        "course/enrolments.xml": "<enrolments>\n  <enrols>\n  </enrols>\n</enrolments>",
        "course/filters.xml": "<filters>\n  <filter_actives>\n  </filter_actives>\n  <filter_configs>\n  </filter_configs>\n</filters>",
        "course/calendar.xml": "<events>\n</events>",
        "course/comments.xml": "<comments>\n</comments>",
        "course/competencies.xml": "<course_competencies>\n  <competencies>\n  </competencies>\n  <user_competencies>\n  </user_competencies>\n</course_competencies>",
        "course/completiondefaults.xml": "<course_completion_defaults>\n</course_completion_defaults>",
        "roles.xml": "<roles_definition>\n</roles_definition>",
        "users.xml": "<users>\n</users>",
        "groups.xml": "<groups>\n  <groupings>\n  </groupings>\n</groups>",
        "outcomes.xml": "<outcomes_definition>\n</outcomes_definition>",
        "scales.xml": "<scales_definition>\n</scales_definition>",
        "questions.xml": "<question_categories>\n</question_categories>",
        "badges.xml": "<badges>\n</badges>",
    }
    for k, v in vacio.items():
        r.out[k] = '<?xml version="1.0" encoding="UTF-8"?>\n' + v
    r.out["files.xml"] = r.files_xml()

    filename = f"respaldo-{corto.lower()}-{cid}.mbz"
    root = dict(filename=filename, imscc11=0, users=0, anonymize=0, role_assignments=0, activities=1, blocks=0,
                files=1, filters=0, comments=0, badges=0, calendarevents=0, userscompletion=0, logs=0,
                grade_histories=0, questionbank=0, groups=0, competencies=0, customfield=0,
                contentbankcontent=0, xapistate=0, legacyfiles=0)
    st = [f"      <setting>\n        <level>root</level>\n        <name>{k}</name>\n        <value>{x(v)}</value>\n      </setting>" for k, v in root.items()]
    for secid, _, _ in secs:
        for n, v in (("included", 1), ("userinfo", 0)):
            st.append(f"      <setting>\n        <level>section</level>\n        <section>section_{secid}</section>\n"
                      f"        <name>section_{secid}_{n}</name>\n        <value>{v}</value>\n      </setting>")
    for cmid, _, modname, _, _ in acts:
        for n, v in (("included", 1), ("userinfo", 0)):
            st.append(f"      <setting>\n        <level>activity</level>\n        <activity>{modname}_{cmid}</activity>\n"
                      f"        <name>{modname}_{cmid}_{n}</name>\n        <value>{v}</value>\n      </setting>")
    acts_xml = "\n".join(
        f"        <activity>\n          <moduleid>{c}</moduleid>\n          <sectionid>{s}</sectionid>\n          <modulename>{m}</modulename>\n"
        f"          <title>{x(t)}</title>\n          <directory>{d}</directory>\n        </activity>" for c, s, m, t, d in acts)
    secs_xml = "\n".join(
        f"        <section>\n          <sectionid>{s}</sectionid>\n          <title>{x(t)}</title>\n          <directory>{d}</directory>\n        </section>"
        for s, t, d in secs)
    r.out["moodle_backup.xml"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<moodle_backup>
  <information>
    <name>{filename}</name>
    <moodle_version>2023100902</moodle_version>
    <moodle_release>4.3.2 (Build: 20231222)</moodle_release>
    <backup_version>{V43}</backup_version>
    <backup_release>4.3</backup_release>
    <backup_date>{NOW}</backup_date>
    <mnet_remoteusers>0</mnet_remoteusers>
    <include_files>1</include_files>
    <include_file_references_to_external_content>0</include_file_references_to_external_content>
    <original_wwwroot>https://aula-soacha.invalid</original_wwwroot>
    <original_site_identifier_hash>{hashlib.md5(b'aula-soacha-armar-respaldo').hexdigest()}</original_site_identifier_hash>
    <original_course_id>{COURSEID}</original_course_id>
    <original_course_format>topics</original_course_format>
    <original_course_fullname>{x(nombre)}</original_course_fullname>
    <original_course_shortname>{x(corto)}</original_course_shortname>
    <original_course_startdate>{NOW}</original_course_startdate>
    <original_course_enddate>0</original_course_enddate>
    <original_course_contextid>{COURSECTX}</original_course_contextid>
    <original_system_contextid>1</original_system_contextid>
    <details>
      <detail backup_id="{hashlib.md5(filename.encode() + str(NOW).encode()).hexdigest()}">
        <type>course</type>
        <format>moodle2</format>
        <interactive>1</interactive>
        <mode>10</mode>
        <execution>1</execution>
        <executiontime>0</executiontime>
      </detail>
    </details>
    <contents>
      <activities>
{acts_xml}
      </activities>
      <sections>
{secs_xml}
      </sections>
      <course>
        <courseid>{COURSEID}</courseid>
        <title>{x(corto)}</title>
        <directory>course</directory>
      </course>
    </contents>
    <settings>
{chr(10).join(st)}
    </settings>
  </information>
</moodle_backup>"""

    destino = os.path.join(salida, filename)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for ruta, texto in sorted(r.out.items()):
            z.writestr(ruta, texto.encode("utf-8"))
        for h, data in r.files.items():
            z.writestr(f"files/{h[:2]}/{h}", data)
    with open(os.path.join(salida, "contenido-del-respaldo.txt"), "w", encoding="utf-8") as f:
        f.write(f"{nombre}\nNombre corto: {corto} · Número de ID: {idnumber}\n\n" + "\n".join(resumen) + "\n")
    print(destino, os.path.getsize(destino), "bytes,", len(acts), "actividades,", len(secs), "secciones")


if __name__ == "__main__":
    main()
