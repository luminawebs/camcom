"""Imagen del curso para Moodle (la que se ve en las tarjetas de «Mis cursos» y en la categoría).

Uso: python3 plantillas/imagen_curso.py cursos/<id>

Arma cursos/<id>/imagen-curso.jpg (1200 × 600) con el título del curso sobre un panel negro de la marca
y la ilustración de la Entrada de la Unidad 1 a la derecha. No llama a ninguna API.
- Ilustración: curso.json "imagen_curso": {"ilustracion": "ruta relativa al curso"} si existe;
  si no, ilustraciones/originales/u1-entrada.png y, en último caso, medios-moodle/u1-entrada.jpg.
- Texto inferior: "imagen_curso": {"nota": "..."}; por omisión «Unidades 1 a 3 gratis · <duración>».
Lo sube moodle/subir_moodle.py (o moodle/imagen_moodle.mjs para un curso ya publicado).
"""
import html, json, subprocess, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

RENDER = r"""
import { createRequire } from 'module';
import { execSync } from 'child_process';
const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const [entrada, salida] = process.argv.slice(2);
const nav = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
const p = await nav.newPage({ viewport: { width: 1200, height: 600 } });
await p.goto('file://' + entrada, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: salida, type: 'jpeg', quality: 86 });
await nav.close();
"""


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    curso = (RAIZ / sys.argv[1]).resolve() if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    datos = json.loads((curso / "curso.json").read_text(encoding="utf-8"))
    conf = datos.get("imagen_curso", {})
    candidatas = [conf.get("ilustracion"), "ilustraciones/originales/u1-entrada.png", "medios-moodle/u1-entrada.jpg"]
    ilustracion = next((curso / c for c in candidatas if c and (curso / c).exists()), None)
    if not ilustracion:
        sys.exit("No hay ilustración para la imagen del curso (falta la Entrada de la Unidad 1)")
    nota = conf.get("nota") or f"Unidades 1 a 3 gratis · {datos.get('duracion', '').strip()}".rstrip(" ·")

    pagina = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=block" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:600px;display:flex;font-family:Poppins,Inter,sans-serif;background:#141414;overflow:hidden}}
.panel{{width:540px;flex:none;padding:0 56px 0 64px;display:flex;flex-direction:column;justify-content:center;gap:26px;
  background:linear-gradient(160deg,#2e2e2e,#141414 70%);position:relative}}
.panel:before{{content:"";position:absolute;left:0;top:0;bottom:0;width:12px;background:#c8102e}}
.eti{{color:#ff8a9b;font-size:19px;font-weight:600;letter-spacing:.12em;text-transform:uppercase}}
h1{{color:#fff;font-size:{58 if len(datos['titulo']) <= 34 else 50}px;line-height:1.08;font-weight:700;text-wrap:balance}}
.nota{{align-self:flex-start;background:#c8102e;color:#fff;font-size:21px;font-weight:600;padding:9px 20px;border-radius:999px}}
.foto{{flex:1;background:url("{ilustracion.as_uri()}") center/cover no-repeat;position:relative}}
.foto:before{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#141414 0,rgba(20,20,20,0) 18%)}}
</style></head><body>
<div class="panel"><div class="eti">Aula Virtual Empresarial Soacha</div>
<h1>{html.escape(datos['titulo'])}</h1><div class="nota">{html.escape(nota)}</div></div>
<div class="foto"></div></body></html>"""

    salida = curso / "imagen-curso.jpg"
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "imagen.html").write_text(pagina, encoding="utf-8")
        (Path(tmp) / "render.mjs").write_text(RENDER, encoding="utf-8")
        subprocess.run(["node", str(Path(tmp) / "render.mjs"), str(Path(tmp) / "imagen.html"), str(salida)], check=True)
    print(f"✓ {salida.relative_to(RAIZ)} (ilustración: {ilustracion.relative_to(curso)})")


if __name__ == "__main__":
    main()
