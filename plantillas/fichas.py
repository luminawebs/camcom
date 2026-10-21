#!/usr/bin/env python3
"""Fichas verticales del paso Llévatelo (1080 × 1920, para guardar en el celular). Reemplazan el diseño manual en Canva.

Uso: python3 plantillas/fichas.py cursos/<id> [--solo 2]

Arma cursos/<id>/fichas/uN-ficha.jpg (JPG de máximo 250 KB) con el contenido de "llevatelo" de cada unidad en curso.json:
título, las tres frases del resumen y la fórmula o regla. Arriba va la ilustración de la Entrada de la unidad
(ilustraciones/originales/uN-entrada.png o, si no hay, medios-moodle/uN-entrada.jpg). No llama a ninguna API.
- "llevatelo": {"ficha": {"ilustracion": "ruta relativa al curso"}} cambia la imagen de esa unidad.
- "[VERIFICAR …]" no sale en la ficha; otro texto entre corchetes sale entre paréntesis. **negrita** funciona.
armar_curso.py muestra la ficha en la página de Llévatelo con su botón de descarga, y publicar_curso.py la mete en el .mbz.
"""
import html, io, json, re, subprocess, sys, tempfile
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
MAX_KB = 250

RENDER = r"""
import { createRequire } from 'module';
import { execSync } from 'child_process';
const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const pares = process.argv.slice(2);
const nav = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
const p = await nav.newPage({ viewport: { width: 1080, height: 1920 } });
for (let i = 0; i < pares.length; i += 2) {
  await p.goto('file://' + pares[i], { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => window.ajustar && window.ajustar());
  await p.screenshot({ path: pares[i + 1], type: 'png' });
}
await nav.close();
"""

# Si el contenido no cabe, achica la letra de a poco hasta que el cuerpo quepa en la ficha.
AJUSTAR = """<script>
window.ajustar = () => {
  const c = document.querySelector('.cuerpo'); let k = 1;
  while (c.scrollHeight > c.clientHeight + 1 && k > 0.6) { k -= 0.03; document.documentElement.style.setProperty('--k', k); }
};
</script>"""


def limpiar(s):
    s = re.sub(r"\s*\[VERIFICAR[^\]]*\]", "", s)
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]", r"(\1)", s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def formula(s):
    """Las rutas con flechas se ven como pasos; las fórmulas con «·» en renglones."""
    partes = [p.strip() for p in re.split(r"\s*→\s*", s)]
    partes = [p[:1].upper() + p[1:] for p in partes]
    if len(partes) > 2:
        return '<ol class="ruta">' + "".join(f"<li>{limpiar(p)}</li>" for p in partes) + "</ol>"
    renglones = [p.strip() for p in s.split(" · ")]
    renglones = [r[:1].upper() + r[1:] for r in renglones]
    return "".join(f"<p>{limpiar(r)}</p>" for r in renglones)


def ilustracion(curso, i, L):
    candidatas = [L.get("ficha", {}).get("ilustracion"), f"ilustraciones/originales/u{i}-entrada.png", f"medios-moodle/u{i}-entrada.jpg"]
    return next((curso / c for c in candidatas if c and (curso / c).exists()), None)


def pagina(datos, i, u, foto):
    L = u["llevatelo"]
    puntos = "".join(f'<li><span class="n">{k}</span><span>{limpiar(x)}</span></li>' for k, x in enumerate(L["resumen"], 1))
    arriba = (f'<div class="foto" style="background-image:url(\'{foto.as_uri()}\')"></div>' if foto else '<div class="foto foto--sin"></div>')
    corto = datos.get("titulo_corto", datos["titulo"])
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&display=block" rel="stylesheet">
<style>
:root{{--k:1;--rojo:#c8102e;--negro:#141414}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:Poppins,Inter,'DejaVu Sans',sans-serif;background:#fff;color:var(--negro);
  display:flex;flex-direction:column}}
.foto{{height:700px;flex:none;background:center/cover no-repeat var(--negro);position:relative}}
.foto--sin{{height:300px}}
.foto:after{{content:"";position:absolute;inset:auto 0 0 0;height:260px;background:linear-gradient(0deg,rgba(20,20,20,.92),rgba(20,20,20,0))}}
.cab{{position:absolute;left:72px;right:72px;top:620px;transform:translateY(-100%);z-index:1;display:flex;flex-direction:column;gap:14px}}
.foto--sin + .cab{{top:240px}}
.chip{{align-self:flex-start;background:var(--rojo);color:#fff;font-weight:700;font-size:28px;letter-spacing:.08em;text-transform:uppercase;
  padding:10px 26px;border-radius:999px}}
.curso{{color:#fff;font-size:30px;font-weight:500;opacity:.92}}
.cuerpo{{flex:1;min-height:0;overflow:hidden;padding:calc(56px*var(--k)) 72px 0;display:flex;flex-direction:column;gap:calc(44px*var(--k))}}
h1{{font-size:calc(66px*var(--k));line-height:1.1;font-weight:800;text-wrap:balance;position:relative;padding-bottom:calc(28px*var(--k))}}
h1:after{{content:"";position:absolute;left:0;bottom:0;width:120px;height:10px;border-radius:5px;background:var(--rojo)}}
.puntos{{list-style:none;display:flex;flex-direction:column;gap:calc(30px*var(--k))}}
.puntos li{{display:flex;gap:28px;align-items:flex-start;font-size:calc(38px*var(--k));line-height:1.32;font-weight:500;color:#2a2a2e}}
.puntos .n{{flex:none;width:calc(64px*var(--k));height:calc(64px*var(--k));border-radius:50%;background:var(--rojo);color:#fff;
  font-weight:800;font-size:calc(34px*var(--k));display:flex;align-items:center;justify-content:center;margin-top:-2px}}
.formula{{background:var(--negro);color:#fff;border-radius:28px;padding:calc(38px*var(--k)) 48px;border-left:16px solid var(--rojo)}}
.formula small{{display:block;color:#ff8a9b;font-size:calc(28px*var(--k));font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  margin-bottom:calc(14px*var(--k))}}
.formula p{{font-size:calc(40px*var(--k));line-height:1.3;font-weight:700}}
.formula p + p{{margin-top:calc(10px*var(--k))}}
.ruta{{list-style:none;counter-reset:r;display:flex;flex-direction:column;gap:calc(10px*var(--k))}}
.ruta li{{counter-increment:r;font-size:calc(36px*var(--k));line-height:1.25;font-weight:700;display:flex;gap:18px}}
.ruta li:before{{content:counter(r);flex:none;color:#ff8a9b;width:34px}}
.pie{{flex:none;margin:0 72px;padding:34px 0 56px;border-top:3px solid #e6e6e8;display:flex;justify-content:space-between;
  align-items:center;gap:24px;font-size:24px;color:#6b6b72}}
.pie b{{color:var(--negro);font-weight:700}}
.pie .guarda{{text-align:right;color:var(--rojo);font-weight:700}}
</style>{AJUSTAR}</head><body>
{arriba}
<div class="cab"><span class="chip">Unidad {i} · Llévatelo</span><span class="curso">{html.escape(corto)}</span></div>
<main class="cuerpo">
  <h1>{limpiar(L['titulo'])}</h1>
  <ol class="puntos">{puntos}</ol>
  <div class="formula"><small>{limpiar(L.get('etiqueta_formula', 'La fórmula'))}</small>{formula(L['formula'])}</div>
</main>
<footer class="pie"><span><b>Aula Virtual Empresarial</b><br>Cámara de Comercio de Soacha</span>
<span class="guarda">Guarda esta ficha<br>en tu celular</span></footer>
</body></html>"""


def a_jpg(png, salida):
    img = Image.open(png).convert("RGB")
    for q in range(88, 40, -4):
        b = io.BytesIO()
        img.save(b, "JPEG", quality=q, optimize=True, progressive=True)
        if b.tell() <= MAX_KB * 1024:
            break
    salida.write_bytes(b.getvalue())
    return q, b.tell() // 1024


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    curso = Path(args[0]).resolve()
    solo = int(args[args.index("--solo") + 1]) if "--solo" in args else None
    datos = json.loads((curso / "curso.json").read_text(encoding="utf-8"))
    (curso / "fichas").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pares, hechas = [], []
        for i, u in enumerate(datos["unidades"], 1):
            if "llevatelo" not in u or (solo and i != solo):
                continue
            foto = ilustracion(curso, i, u["llevatelo"])
            (tmp / f"u{i}.html").write_text(pagina(datos, i, u, foto), encoding="utf-8")
            pares += [str(tmp / f"u{i}.html"), str(tmp / f"u{i}.png")]
            hechas.append((i, foto))
        (tmp / "render.mjs").write_text(RENDER, encoding="utf-8")
        subprocess.run(["node", str(tmp / "render.mjs"), *pares], check=True)
        for i, foto in hechas:
            salida = curso / "fichas" / f"u{i}-ficha.jpg"
            q, kb = a_jpg(tmp / f"u{i}.png", salida)
            print(f"✓ {salida.relative_to(curso.parent.parent)} · {kb} KB (calidad {q})" + (f" · ilustración {foto.relative_to(curso)}" if foto else " · sin ilustración"))


if __name__ == "__main__":
    main()
