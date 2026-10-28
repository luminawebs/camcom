// Pasa las pantallas a JPG, mide la zona que se toca y escribe el contenido.js de cada simulador.
// Uso: node renderizar.mjs   (antes: python3 armar_pantallas.py)
import { createRequire } from 'module';
import { execSync } from 'child_process';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const aqui = dirname(fileURLToPath(import.meta.url));
const curso = join(aqui, '..');
const spec = JSON.parse(readFileSync(join(aqui, 'pantallas.json'), 'utf-8'));
const nav = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

const p = await nav.newPage({ viewport: { width: 360, height: 760 }, deviceScaleFactor: 2 });
for (const [u, s] of Object.entries(spec.simuladores)) {
  const medios = join(curso, 'piezas', `u${u}-practica`, 'medios');
  mkdirSync(medios, { recursive: true });
  const pasos = [];
  for (const x of s.pasos) {
    await p.goto('file://' + join(aqui, x.html));
    const r = await p.locator('#objetivo').boundingBox();
    const pct = (v, t) => Math.round((v / t) * 1000) / 10;
    const m = 1.5; // margen de tolerancia en px a cada lado
    const x0 = Math.max(0, r.x - m), y0 = Math.max(0, r.y - m), x1 = Math.min(360, r.x + r.width + m), y1 = Math.min(760, r.y + r.height + m);
    const zona = { x: pct(x0, 360), y: pct(y0, 760), w: pct(x1 - x0, 360), h: pct(y1 - y0, 760) };
    await p.screenshot({ path: join(medios, x.imagen), type: 'jpeg', quality: 78 });
    pasos.push({ instruccion: x.instruccion,
      pantalla: { tipo: 'imagen', src: 'medios/' + x.imagen, alt: 'Pantalla de práctica simplificada: ' + x.instruccion },
      zona, pista: x.pista });
    console.log('jpg', `u${u}-practica/medios/${x.imagen}`, JSON.stringify(zona));
  }
  const c = { titulo: s.titulo, paso: 'Practica', unidad: `Unidad ${u}`, notaMinima: 60, verZonas: false, pasos,
    final: { titulo: '¡Lo lograste!', texto: s.final } };
  writeFileSync(join(curso, 'piezas', `u${u}-practica`, 'contenido.js'),
    `/* Vende más por WhatsApp Business · Unidad ${u} · Practica\n   Molde: componentes/simulador-pantalla · lo escribe pantallas/renderizar.mjs (no editar a mano:\n   cambia pantallas/armar_pantallas.py y vuelve a correr los dos scripts).\n   Pantallas simplificadas, no capturas reales. */\nwindow.CONTENIDO = ${JSON.stringify(c, null, 2)};\n`);
}

const v = await nav.newPage({ viewport: { width: 800, height: 600 } });
for (const [id, x] of Object.entries(spec.vistas)) {
  await v.goto('file://' + join(aqui, x.html));
  await v.waitForTimeout(150);
  await v.screenshot({ path: join(curso, x.destino), type: 'jpeg', quality: 80 });
  console.log('jpg', x.destino);
}
await nav.close();
