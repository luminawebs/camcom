#!/usr/bin/env python3
"""Arma el video corto de la Entrada de cada unidad: la ilustración del caso con la narración de Resemble AI.

Uso: python3 plantillas/video_entrada.py cursos/<id> [u1 u2 ...]

No llama a ninguna API: junta lo que ya existe en el curso.
- Imagen: ilustraciones/originales/uN-entrada.png (plantillas/ilustrar.py) o, si no está, medios-moodle/uN-entrada.jpg.
- Voz: medios-moodle/uN-entrada-narracion.mp3 (plantillas/narrar.py); su texto sale de narraciones.json.
El video es horizontal (960 × 700, como la ilustración), con un acercamiento lento sobre la imagen, el título de la
unidad al comienzo, subtítulos quemados frase por frase (repartidos según su largo) y la pregunta de la unidad en una
franja roja al final. Salida en <curso>/medios-moodle/: uN-entrada.mp4 y uN-entrada.vtt.
Después: python3 plantillas/armar_curso.py cursos/<id> (la Entrada muestra el video en lugar de la imagen y el audio).
"""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from video_resumen import duracion, ts  # noqa: E402

ANCHO, ALTO, FPS = 960, 700, 25
FINAL = 2.0  # segundos de imagen quieta con la pregunta después de la voz


def ass_t(s):
    return ts(s)[1:-1]  # h:mm:ss.cc


def video(curso: Path, u: str, c: dict, textos: dict):
    voz = curso / "medios-moodle" / f"{u}-entrada-narracion.mp3"
    img = curso / "ilustraciones" / "originales" / f"{u}-entrada.png"
    img = img if img.exists() else curso / "medios-moodle" / f"{u}-entrada.jpg"
    if not voz.exists() or not img.exists():
        print(f"  · {u}: falta la imagen o la narración, no se arma")
        return
    i = int(u[1:]) - 1
    e = c["unidades"][i]["entrada"]
    texto = textos[f"medios-moodle/{u}-entrada-narracion.mp3"]["texto"]
    dur_voz = duracion(voz)
    total = dur_voz + FINAL

    # subtítulos por frase (sin el título, que ya se ve en pantalla) y la pregunta en la franja roja
    frases = [f for f in re.split(r"(?<=[.:?!])\s+", texto.strip()) if f]
    largo = sum(len(f) for f in frases)
    vtt, eventos, t0, t_preg = ["WEBVTT", ""], [], 0.0, None
    for f in frases:
        t1 = t0 + dur_voz * len(f) / largo
        vtt += [f"{ts(t0)} --> {ts(t1)}", f, ""]
        if f.startswith("La pregunta de esta unidad"):
            t_preg = t0
        elif t_preg is None and f.rstrip(".") != e["titulo"]:
            eventos.append(f"Dialogue: 0,{ass_t(t0)},{ass_t(t1)},Sub,,0,0,0,,{f}")
        t0 = t1
    t_preg = t_preg if t_preg is not None else dur_voz
    eventos.append(f"Dialogue: 0,{ass_t(0)},{ass_t(4.5)},Tit,,0,0,0,,{{\\fad(300,400)}}Unidad {i + 1} · Entrada\\N{{\\fs40\\b1}}{e['titulo']}")
    eventos.append(f"Dialogue: 1,{ass_t(t_preg)},{ass_t(total)},Preg,,0,0,0,,{{\\fad(300,0)}}{e['pregunta']}")
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {ANCHO}", f"PlayResY: {ALTO}", "WrapStyle: 0", "",
           "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
           "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Sub,Inter,30,&H00FFFFFF,&H00FFFFFF,&H8C000000,&H8C000000,-1,0,0,0,100,100,0,0,3,10,0,2,70,70,36,1",
           "Style: Tit,Inter,24,&H00FFFFFF,&H00FFFFFF,&H00141414,&H00141414,0,0,0,0,100,100,0,0,3,14,0,7,40,40,36,1",
           "Style: Preg,Inter,36,&H00FFFFFF,&H00FFFFFF,&H002E10C8,&H002E10C8,-1,0,0,0,100,100,0,0,3,22,0,5,90,90,0,1", "",
           "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text", *eventos]
    tmp = Path(tempfile.mkdtemp(prefix="entrada-"))
    (tmp / "sub.ass").write_text("\n".join(ass), encoding="utf-8")
    n = int(total * FPS)
    vf = (f"scale={ANCHO * 4}:{ALTO * 4},zoompan=z='1+0.10*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={ANCHO}x{ALTO}:fps={FPS},"
          f"fade=in:0:10,ass={tmp / 'sub.ass'},format=yuv420p")
    salida = curso / "medios-moodle"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(img), "-i", str(voz),
                    "-af", f"apad=pad_dur={FINAL}", "-t", f"{total:.3f}", "-vf", vf,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-ar", "44100",
                    "-movflags", "+faststart", str(salida / f"{u}-entrada.mp4")], check=True)
    (salida / f"{u}-entrada.vtt").write_text("\n".join(vtt), encoding="utf-8")
    shutil.rmtree(tmp)
    f = salida / f"{u}-entrada.mp4"
    print(f"✓ {f.relative_to(curso)}  {duracion(f):.1f} s · {f.stat().st_size // 1024} KB")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    curso = Path(sys.argv[1]).resolve()
    c = json.loads((curso / "curso.json").read_text(encoding="utf-8"))
    textos = json.loads((curso / "narraciones.json").read_text(encoding="utf-8"))
    for u in sys.argv[2:] or [f"u{k}" for k in range(1, len(c["unidades"]) + 1)]:
        video(curso, u, c, textos)


if __name__ == "__main__":
    main()
