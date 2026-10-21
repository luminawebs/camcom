#!/usr/bin/env python3
"""Genera las ilustraciones de un curso con un modelo de imagen de Gemini (Google AI Studio).

Uso: python3 plantillas/ilustrar.py cursos/<id> [--solo ID ...] [--forzar] [--modelo gemini-2.5-flash-image]

Lee <curso>/ilustraciones.json:
    {"estilo": "...", "personajes": {"edgar": "descripción fija", ...},
     "imagenes": [{"id": "u1-entrada", "proporcion": "4:3", "personajes": ["edgar"], "escena": "...",
                   "destinos": ["medios-moodle/u1-entrada.jpg", "piezas/u1-aprende/medios/ilustracion-1.jpg"]}]}
Primero dibuja una hoja de personaje por cada personaje (ilustraciones/personajes/<id>.png) y luego cada escena
mandando esas hojas como referencia, para que Édgar, Yuli y Wilson se vean igual en todo el curso.

- El original queda en ilustraciones/originales/<id>.png; cada destino es un JPG de máx. 800 px de ancho y ≤ 150 KB.
- No vuelve a pagar por una imagen que ya existe si su texto no cambió (--forzar las rehace; --solo rehace esas).
- ilustraciones/registro.json lleva cada llamada a la API: modelo, tokens y costo estimado en USD.
La clave va en la variable de entorno GEMINI_API_KEY (nunca en el repositorio).
Después: python3 plantillas/armar_curso.py cursos/<id> --scorm
"""
import argparse, base64, datetime, hashlib, io, json, os, sys, time, urllib.error, urllib.request
from pathlib import Path

from PIL import Image

API = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"
# Precio de lista en USD por millón de tokens (ai.google.dev/pricing). Una imagen de salida son 1290 tokens ≈ USD 0,039.
PRECIOS = {"gemini-2.5-flash-image": (0.30, 30.0)}
MAX_KB, ANCHO = 150, 800


def llamar(modelo, partes, proporcion):
    cuerpo = {"contents": [{"parts": partes}],
              "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": proporcion}}}
    req = urllib.request.Request(API.format(modelo), json.dumps(cuerpo).encode(),
                                 {"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and intento < 3:
                time.sleep(2 ** (intento + 2))
                continue
            sys.exit(f"Error {e.code} de Gemini: {e.read().decode()[:400]}")
    uso = d.get("usageMetadata", {})
    for p in d.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in p:
            return base64.b64decode(p["inlineData"]["data"]), uso
    sys.exit(f"Gemini no devolvió imagen: {json.dumps(d)[:400]}")


def costo(modelo, uso):
    ent, sal = PRECIOS.get(modelo, PRECIOS["gemini-2.5-flash-image"])
    return round(uso.get("promptTokenCount", 0) * ent / 1e6 + uso.get("candidatesTokenCount", 0) * sal / 1e6, 4)


def jpg(png: bytes, destino: Path):
    im = Image.open(io.BytesIO(png)).convert("RGB")
    if im.width > ANCHO:
        im = im.resize((ANCHO, round(im.height * ANCHO / im.width)), Image.LANCZOS)
    for q in range(85, 40, -5):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= MAX_KB * 1024:
            break
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(buf.getvalue())
    return buf.tell() // 1024


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("curso")
    ap.add_argument("--solo", nargs="*", default=[])
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--modelo", default="gemini-2.5-flash-image")
    a = ap.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("Falta la variable de entorno GEMINI_API_KEY")
    curso = Path(a.curso).resolve()
    spec = json.loads((curso / "ilustraciones.json").read_text(encoding="utf-8"))
    base = curso / "ilustraciones"
    (base / "personajes").mkdir(parents=True, exist_ok=True)
    (base / "originales").mkdir(exist_ok=True)
    reg_f = base / "registro.json"
    reg = json.loads(reg_f.read_text(encoding="utf-8")) if reg_f.exists() else {"hechas": {}, "llamadas": []}

    def generar(clave, archivo, partes, proporcion):
        texto = "\n".join(p.get("text", "") for p in partes) + a.modelo
        huella = hashlib.sha1(texto.encode()).hexdigest()[:12]
        if archivo.exists() and reg["hechas"].get(clave) == huella and not a.forzar and clave not in a.solo:
            return archivo.read_bytes(), False
        png, uso = llamar(a.modelo, partes, proporcion)
        archivo.write_bytes(png)
        usd = costo(a.modelo, uso)
        reg["hechas"][clave] = huella
        reg["llamadas"].append({"id": clave, "modelo": a.modelo, "fecha": datetime.datetime.now().isoformat(timespec="seconds"),
                                "tokens_entrada": uso.get("promptTokenCount", 0), "tokens_imagen": uso.get("candidatesTokenCount", 0), "usd": usd})
        reg_f.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  ✓ {clave}  (USD {usd})")
        return png, True

    hojas = {}
    for pid, desc in spec["personajes"].items():
        partes = [{"text": f"{spec['estilo']}\n\nCharacter reference sheet: the same person shown full body from the front and "
                           f"in three-quarter view, plus a close-up of the face, on a plain white background. No text, no labels.\n"
                           f"Character: {desc}"}]
        hojas[pid], _ = generar(f"personaje-{pid}", base / "personajes" / f"{pid}.png", partes, "1:1")

    for im in spec["imagenes"]:
        if a.solo and im["id"] not in a.solo:
            continue
        partes = [{"inlineData": {"mimeType": "image/png", "data": base64.b64encode(hojas[p]).decode()}} for p in im.get("personajes", [])]
        nombres = ", ".join(f"image {k + 1} is {p.capitalize()}" for k, p in enumerate(im.get("personajes", [])))
        refs = f"Use the attached character sheets for the characters ({nombres}); keep their faces, hair, clothes and proportions exactly. " if nombres else ""
        partes.append({"text": f"{spec['estilo']}\n\n{refs}Scene: {im['escena']}\nNo text, letters, numbers or logos anywhere in the image."})
        png, nueva = generar(im["id"], base / "originales" / f"{im['id']}.png", partes, im.get("proporcion", "4:3"))
        for d in im["destinos"]:
            kb = jpg(png, curso / d)
            if nueva:
                print(f"    → {d} ({kb} KB)")

    total = sum(x["usd"] for x in reg["llamadas"])
    print(f"Imágenes generadas en total: {len(reg['llamadas'])} · costo estimado USD {total:.2f}")


if __name__ == "__main__":
    main()
