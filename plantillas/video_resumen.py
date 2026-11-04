#!/usr/bin/env python3
"""Arma un video vertical (1080 × 1920) de resumen con diapositivas de la marca y la voz de Resemble AI.

Uso: python3 plantillas/video_resumen.py cursos/<id> u1-resumen

Lee <curso>/video/<nombre>.json: una lista de diapositivas, cada una con lo que se ve (tipo, titulo, texto o items)
y lo que se dice ("voz"); "imagen" (opcional, ruta dentro del curso) pone una ilustración arriba. Por cada diapositiva genera la voz con la voz de curso.json "narracion" (plantillas/narrar.py),
la dibuja con Playwright y la deja en pantalla lo que dura su audio. Los subtítulos salen del mismo texto,
frase por frase, repartidos según su largo. Salida en <curso>/medios-moodle/: <nombre>.mp4 (subtítulos quemados)
y <nombre>.vtt (para el reproductor de Moodle). La clave va en RESEMBLE_API_KEY.
"""
import html, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import narrar  # noqa: E402

RAIZ = Path(__file__).resolve().parent
LOGO = (RAIZ.parent / "marca" / "edunest-blue.svg")
PAUSA = 0.5  # silencio al final de cada diapositiva

CSS = """*{box-sizing:border-box;margin:0}
body{width:1080px;height:1920px;font-family:Inter,'DejaVu Sans',sans-serif;background:#f6f6f7;color:#141414;overflow:hidden;position:relative}
.cab{position:absolute;top:0;left:0;right:0;padding:96px 88px 0;display:flex;justify-content:space-between;align-items:center;font-size:30px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6b6b72}
.cab svg{height:54px;width:auto}
.zona{position:absolute;left:88px;right:88px;top:300px;bottom:520px;display:flex;flex-direction:column;justify-content:center;gap:56px}
h1{font-size:96px;line-height:1.06;font-weight:800;letter-spacing:-.02em;text-wrap:balance}
.rojo{background:#c8102e;color:#fff}.rojo .cab{color:rgba(255,255,255,.8)}.rojo .cab svg *{fill:#fff!important}
.rojo p.sub{color:rgba(255,255,255,.88)}
p.sub{font-size:48px;line-height:1.3;color:#3a3a40;font-weight:500}
.items{display:flex;flex-direction:column;gap:32px}
.item{display:flex;gap:36px;align-items:flex-start;background:#fff;border-radius:36px;padding:40px 44px;box-shadow:0 4px 0 #e2e2e5}
.item .n{flex:none;width:92px;height:92px;border-radius:50%;background:#c8102e;color:#fff;font-size:52px;font-weight:800;display:flex;align-items:center;justify-content:center}
.item b{display:block;font-size:54px;line-height:1.1}
.item span{display:block;font-size:40px;color:#55555c;margin-top:10px}
.marca{width:140px;height:16px;background:#c8102e;border-radius:8px}
.rojo .marca{background:#fff}
.ruta{font-size:50px;font-weight:700;line-height:1.35;background:#fff;color:#141414;border-radius:36px;padding:44px}
.pie{position:absolute;left:88px;right:88px;bottom:400px;font-size:28px;color:#8d8d94}
.rojo .pie{color:rgba(255,255,255,.75)}
.ilus{display:block;width:100%;max-height:640px;object-fit:contain;border-radius:36px;background:#fff}
.con-img .zona{top:230px;gap:40px}.con-img h1{font-size:76px}.con-img p.sub{font-size:44px}"""


def dibujo(d, etiqueta, logo, imagen=None):
    t = lambda s: html.escape(s)
    rojo = d["tipo"] in ("portada", "cierre", "frase")
    if d["tipo"] == "lista":
        cuerpo = f"<h1>{t(d['titulo'])}</h1><div class='items'>" + "".join(
            f"<div class='item'><span class='n'>{k}</span><div><b>{t(a)}</b><span>{t(b)}</span></div></div>"
            for k, (a, b) in enumerate(d["items"], 1)) + "</div>"
    elif d["tipo"] == "cierre":
        cuerpo = f"<div class='marca'></div><h1>{t(d['titulo'])}</h1><div class='ruta'>{t(d['texto'])}</div>"
    else:
        cuerpo = f"<div class='marca'></div><h1>{t(d['titulo'])}</h1>" + (f"<p class='sub'>{t(d['texto'])}</p>" if d.get("texto") else "")
    if imagen:  # ilustración del curso arriba (plantillas/ilustrar.py), sin llamar a ninguna API
        cuerpo = f"<img class='ilus' src='{imagen.as_uri()}'>" + cuerpo.replace("<div class='marca'></div>", "")
    pie = "<div class='pie'>Voz generada con inteligencia artificial · Aula Virtual Empresarial Soacha</div>" if d["tipo"] == "cierre" else ""
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body class='{'rojo' if rojo else ''}{' con-img' if imagen else ''}'><div class='cab'>{logo}<span>{t(etiqueta)}</span></div>"
            f"<div class='zona'>{cuerpo}</div>{pie}</body></html>")


def duracion(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True, check=True).stdout)


def ts(s):
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    curso, nombre = Path(sys.argv[1]).resolve(), sys.argv[2]
    c = json.loads((curso / "curso.json").read_text(encoding="utf-8"))
    spec = json.loads((curso / "video" / f"{nombre}.json").read_text(encoding="utf-8"))
    clave = os.environ.get("RESEMBLE_API_KEY") or sys.exit("Falta RESEMBLE_API_KEY")
    voz = c["narracion"]["voz"]
    logo = LOGO.read_text(encoding="utf-8") if LOGO.exists() else ""
    tmp = Path(tempfile.mkdtemp(prefix="video-"))

    # 1. voz y dibujo de cada diapositiva
    htmls = []
    for k, d in enumerate(spec["diapositivas"]):
        narrar.sintetizar(narrar.limpiar(d["voz"]), voz, clave, tmp / f"{k}.mp3")
        (tmp / f"{k}.html").write_text(dibujo(d, spec["etiqueta"], logo, curso / d["imagen"] if d.get("imagen") else None), encoding="utf-8")
        htmls.append(tmp / f"{k}.html")
    js = ("import { createRequire } from 'module'; import { execSync } from 'child_process';"
          "const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');"
          "const b = await chromium.launch();"
          "const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });"
          "for (const f of process.argv.slice(2)) { await p.goto('file://' + f); await p.screenshot({ path: f.replace('.html', '.png') }); }"
          "await b.close();")
    (tmp / "r.mjs").write_text(js)
    subprocess.run(["node", str(tmp / "r.mjs"), *map(str, htmls)], check=True)

    # 2. un tramo de video por diapositiva y subtítulos por frase
    vtt, t0, tramos = ["WEBVTT", ""], 0.0, []
    for k, d in enumerate(spec["diapositivas"]):
        dur = duracion(tmp / f"{k}.mp3") + PAUSA
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(tmp / f"{k}.png"), "-i", str(tmp / f"{k}.mp3"),
                        "-af", f"apad=pad_dur={PAUSA}", "-t", f"{dur:.3f}", "-vf", "fade=in:0:8,format=yuv420p", "-r", "25",
                        "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-ar", "44100",
                        str(tmp / f"{k}.mp4")], check=True)
        tramos.append(tmp / f"{k}.mp4")
        frases = [f for f in re.split(r"(?<=[.:?!])\s+", d["voz"].strip()) if f]
        total = sum(len(f) for f in frases)
        ti = t0
        for f in frases:
            tf = ti + (dur - PAUSA) * len(f) / total
            vtt += [f"{ts(ti)} --> {ts(tf)}", f, ""]
            ti = tf
        t0 += dur
    (tmp / "lista.txt").write_text("".join(f"file '{p}'\n" for p in tramos))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "lista.txt"), "-c", "copy", str(tmp / "todo.mp4")], check=True)

    # 3. subtítulos quemados abajo (zona libre de las diapositivas) y archivo .vtt aparte
    salida = curso / "medios-moodle"
    salida.mkdir(exist_ok=True)
    (salida / f"{nombre}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "",
           "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
           "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Sub,Inter,50,&H00FFFFFF,&H00FFFFFF,&H8C000000,&H8C000000,-1,0,0,0,100,100,0,0,3,14,0,2,110,110,190,1", "",
           "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for i in range(2, len(vtt) - 1, 3):
        ini, fin = vtt[i].split(" --> ")
        ass.append(f"Dialogue: 0,{ini[1:-1]},{fin[1:-1]},Sub,,0,0,0,,{vtt[i + 1]}")
    (tmp / "sub.ass").write_text("\n".join(ass), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "todo.mp4"), "-vf", f"ass={tmp / 'sub.ass'}",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-tune", "stillimage", "-c:a", "copy", "-movflags", "+faststart",
                    str(salida / f"{nombre}.mp4")], check=True)
    shutil.rmtree(tmp)
    f = salida / f"{nombre}.mp4"
    print(f"✓ {f.relative_to(curso)}  {duracion(f):.1f} s · {f.stat().st_size // 1024} KB · subtítulos en {nombre}.vtt")


if __name__ == "__main__":
    main()
