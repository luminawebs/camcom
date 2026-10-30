// Agrega el tramo del Pase (Unidades 4 a 7) a un curso ya publicado en Moodle, sin reemplazarlo.
//
// Uso: node moodle/tramo_pase.mjs <id del curso en Moodle> <cursos/<id>/curso.json> [--probar]
// Variables de entorno: MOODLE_URL, MOODLE_USER, MOODLE_PASS (cuenta Gestor de la categoría).
//
// Qué hace (modelo de dos tramos de ruta-por-metas: U1-U3 gratis, U4-U7 con el Pase):
// - Inserta 4 secciones antes de CIERRE con el nombre «Unidad N · <título>» y un resumen con los
//   7 pasos «En preparación» y el botón «Sigue con el Pase Empresario».
// - Restringe U4-U7 al grupo que crea la Sincronización de cohortes de pase-empresario
//   («pase-empresario cohort»). El conector del Pase solo mueve la cohorte: pagar abre, cancelar cierra.
// - Quita la restricción que tuviera la Unidad 3 (tramo gratis).
// - En la portada (resumen de la sección 0) agrega las tarjetas U4-U7 con enlace a la compra y
//   corre la de Cierre a su nueva sección.
// Títulos: curso.json › pase.unidades (4 textos u objetos {titulo, meta}); canal de compra curso-<corto>.
// Si las unidades 4 a 7 ya existen no hace nada. --probar muestra lo que haría sin guardar.
// Antes, el curso necesita el método «Sincronizar cohorte (pase-empresario)» con «Crear nuevo grupo».
import { createRequire } from 'module';
import { execSync } from 'child_process';
import fs from 'fs';

const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const [curso, rutaJson] = process.argv.slice(2);
const probar = process.argv.includes('--probar');
if (!rutaJson) { console.error('Uso: node moodle/tramo_pase.mjs <id del curso> <curso.json> [--probar]'); process.exit(2); }
const URL = process.env.MOODLE_URL.replace(/\/$/, '');
const datos = JSON.parse(fs.readFileSync(rutaJson, 'utf8'));
const unidades = (datos.pase?.unidades || []).map((u) => (typeof u === 'string' ? { titulo: u } : u));
if (unidades.length !== 4) { console.error('curso.json necesita pase.unidades con 4 títulos'); process.exit(2); }
const corto = (datos.corto || process.env.CORTO || '').toLowerCase();
const compra = 'https://pase.edunest.co/?c=curso-' + (corto || `moodle-${curso}`);
const PASOS = ['Entrada', 'Aprende', 'Practica', 'Aplica', 'Demuestra', 'Llévatelo', 'Profundiza'];

function resumen(n, u) {
  const pasos = PASOS.map((x, i) => `<li class="as-paso"><span class="as-paso__n">${i + 1}</span><span class="as-paso__t"><strong>${x}</strong><small>En preparación</small></span><span class="as-chip as-chip--gris">Pronto</span></li>`).join('');
  return `<div class="as as-pila">
<div class="as-banda as-pila"><span class="as-eti">Unidad ${n} de 7 · Con el Pase Empresario</span>
<h2>${u.titulo}</h2>
${u.meta ? `<p>${u.meta}</p>` : ''}
</div>
<ol class="as-pasos">${pasos}</ol>
<div class="as-tarjeta as-pila"><span class="as-eti">Tramo del Pase</span>
<p>Esta unidad se abre con el Pase Empresario: sigues en este mismo curso, con tu avance, y al final recibes el certificado de las 7 unidades.</p>
<p><a class="btn btn-primary" href="${compra}" target="_blank" rel="noopener">Sigue con el Pase Empresario</a></p>
<p class="as-sec">Si ya tienes el Pase, la unidad se abre sola en unos minutos.</p>
</div>
</div>`;
}

const b = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
const p = await b.newPage();
p.setDefaultTimeout(60000);
await p.route(/clarity\.ms|googletagmanager|google-analytics/, (r) => r.abort());
await p.goto(URL + '/login/index.php');
await p.fill('#username', process.env.MOODLE_USER);
await p.fill('#password', process.env.MOODLE_PASS);
await Promise.all([p.waitForNavigation(), p.click('#loginbtn')]);

// Grupo del Pase
await p.goto(`${URL}/group/index.php?id=${curso}`);
const grupos = await p.locator('#groups option').evaluateAll((o) => o.map((x) => [x.value, x.textContent.trim()]));
const grupo = grupos.find(([, t]) => /pase-empresario cohort/i.test(t));
if (!grupo) { console.error('El curso no tiene el grupo «pase-empresario cohort»: falta la Sincronización de cohortes del Pase.'); process.exit(1); }
const restriccion = JSON.stringify({ op: '&', c: [{ type: 'group', id: Number(grupo[0]) }], showc: [true] });

// Secciones actuales (id y nombre) desde la página del curso en modo edición
async function secciones() {
  await p.goto(`${URL}/course/view.php?id=${curso}`);
  return p.locator('li.section[data-sectionid]').evaluateAll((l) => l.map((s) => ({
    num: Number(s.getAttribute('data-number') ?? s.id.replace('section-', '')),
    id: Number(s.getAttribute('data-id')),
    nombre: (s.querySelector('.sectionname')?.textContent || '').trim(),
  })));
}
let secs = await secciones();
if (secs.some((s) => /^Unidad 4\b/.test(s.nombre))) { console.log('El curso ya tiene la Unidad 4; no se cambia nada.'); await b.close(); process.exit(0); }
const u3 = secs.find((s) => /^Unidad 3\b/.test(s.nombre));
if (!u3) { console.error('No encuentro la Unidad 3'); process.exit(1); }
const insertar = u3.num + 1;
console.log(`Grupo ${grupo[1]} (id ${grupo[0]}); U4-U7 entran en las secciones ${insertar}-${insertar + 3}; compra: ${compra}`);
if (probar) { await b.close(); process.exit(0); }

const sesskey = await p.evaluate(() => M.cfg.sesskey);
await p.goto(`${URL}/course/changenumsections.php?courseid=${curso}&insertsection=${insertar}&numsections=4&sesskey=${sesskey}`);
secs = await secciones();

async function editar(id, { nombre, html, disponibilidad }) {
  await p.goto(`${URL}/course/editsection.php?id=${id}&sr=0`);
  if (nombre !== undefined) {
    const c = p.locator('#id_name_customize');
    if ((await c.count()) && !(await c.isChecked())) await c.check();
    await p.fill('[name="name[value]"]', nombre);
  }
  if (html !== undefined) {
    // El editor TinyMCE reescribe el área de texto al guardar: se cambia en los dos
    await p.waitForFunction(() => window.tinymce?.get('id_summary_editor')?.initialized, null, { timeout: 30000 });
    await p.evaluate((h) => { document.getElementById('id_summary_editor').value = h; tinymce.get('id_summary_editor').setContent(h); }, html);
  }
  if (disponibilidad !== undefined) await p.evaluate((j) => { document.querySelector('[name=availabilityconditionsjson]').value = j; }, disponibilidad);
  await Promise.all([p.waitForNavigation(), p.locator('#id_submitbutton').click()]);
}

for (let i = 0; i < 4; i++) {
  const s = secs.find((x) => x.num === insertar + i);
  await editar(s.id, { nombre: `Unidad ${4 + i} · ${unidades[i].titulo}`, html: resumen(4 + i, unidades[i]), disponibilidad: restriccion });
  console.log(`· Unidad ${4 + i} (sección ${s.num}, id ${s.id})`);
}
await editar(u3.id, { disponibilidad: '' });
console.log('· Unidad 3 sin restricción');

// Portada: tarjetas U4-U7 antes de la de Cierre, que pasa a su nueva sección
const s0 = secs.find((x) => x.num === 0);
await p.goto(`${URL}/course/editsection.php?id=${s0.id}&sr=0`);
await p.waitForFunction(() => window.tinymce?.get('id_summary_editor')?.initialized, null, { timeout: 30000 });
const portada = await p.evaluate(({ unidades, compra, viejo, nuevo }) => {
  const e = tinymce.get('id_summary_editor');
  let h = e.getContent();
  if (!h.includes('as-portada__grid')) return 'sin portada';
  const tarjetas = unidades.map((u, i) => `<a class="as-portada__unidad as-portada__unidad--pase" data-sec="${4 + i}" href="${compra}" target="_blank" rel="noopener"><span class="as-eti">Unidad ${4 + i} · Con el Pase</span><span class="as-portada__nombre">${u.titulo}</span><span class="as-portada__ir">🔒 Con el Pase Empresario →</span></a>`).join('\n');
  const cierre = new RegExp(`<a class="as-portada__unidad as-sec-${viejo}" href="#section-${viejo}">`);
  h = cierre.test(h) ? h.replace(cierre, `${tarjetas}\n<a class="as-portada__unidad as-sec-${nuevo}" href="#section-${nuevo}">`)
    : h.replace(/(<\/div>\s*<\/div>\s*)$/, `${tarjetas}$1`);
  h = h.replace(/Curso gratuito · ([^<]*)/, 'Unidades 1 a 3 gratis · 4 a 7 con el Pase');
  document.getElementById('id_summary_editor').value = h;
  e.setContent(h);
  return 'ok';
}, { unidades, compra, viejo: insertar, nuevo: insertar + 4 });
if (portada === 'ok') await Promise.all([p.waitForNavigation(), p.locator('#id_submitbutton').click()]);
console.log('· Portada:', portada);
await b.close();
