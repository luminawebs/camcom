// Ajustes del tramo del Pase en un curso de Moodle: resumen de secciones y restricción al grupo del Pase.
// Lo llama moodle/sumar_tramo.py; no se usa solo.
//
// Uso: node moodle/pase_ajustes.mjs <spec.json>
//   spec = {"curso": 10,
//           "secciones": [{"id": 326, "num": 4, "html": "...", "pase": true}, ...],   // pase: restringir al grupo
//           "actividades": [1201, 1202],                                              // cm a restringir al grupo
//           "portada": {"id": 313, "reemplazos": [["texto viejo", "texto nuevo"]]}}    // cambios puntuales en la sección 0
// Variables de entorno: MOODLE_URL, MOODLE_USER, MOODLE_PASS (cuenta Gestor de la categoría).
// La restricción es «Pertenece al grupo …», visible para quien no la cumple (así ve la unidad y el botón del Pase).
import { createRequire } from 'module';
import { execSync } from 'child_process';
import fs from 'fs';

const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const URL = process.env.MOODLE_URL.replace(/\/$/, '');
let restriccion;

const b = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
const p = await b.newPage();
p.setDefaultTimeout(90000);
await p.route(/clarity\.ms|googletagmanager|google-analytics/, (r) => r.abort());
try {
  await p.goto(URL + '/login/index.php');
  await p.fill('#username', process.env.MOODLE_USER);
  await p.fill('#password', process.env.MOODLE_PASS);
  await Promise.all([p.waitForNavigation(), p.click('#loginbtn')]);
  if (p.url().includes('/login/')) throw new Error('No se pudo iniciar sesión');
  // grupo que crea la Sincronización de cohortes de pase-empresario («pase-empresario cohort» o «cohorte»)
  await p.goto(`${URL}/group/index.php?id=${spec.curso}`);
  const grupos = await p.locator('#groups option').evaluateAll((o) => o.map((x) => [x.value, x.textContent.trim()]));
  const grupo = grupos.find(([, t]) => /pase-empresario cohort/i.test(t));
  if (!grupo) throw new Error('El curso no tiene el grupo del Pase (Sincronización de cohortes de pase-empresario)');
  restriccion = JSON.stringify({ op: '&', c: [{ type: 'group', id: Number(grupo[0]) }], showc: [true] });
  console.log(`· grupo del Pase: ${grupo[1]} (id ${grupo[0]})`);

  for (const s of spec.secciones) {
    await p.goto(`${URL}/course/editsection.php?id=${s.id}&sr=0`);
    await p.waitForFunction(() => window.tinymce?.get('id_summary_editor')?.initialized, null, { timeout: 60000 });
    // TinyMCE reescribe el área de texto al guardar: se cambia en los dos
    await p.evaluate((h) => { document.getElementById('id_summary_editor').value = h; tinymce.get('id_summary_editor').setContent(h); }, s.html);
    if (s.pase) await p.evaluate((j) => { document.querySelector('[name=availabilityconditionsjson]').value = j; }, restriccion);
    await Promise.all([p.waitForNavigation(), p.locator('#id_submitbutton').click()]);
    console.log(`· sección ${s.num}: resumen${s.pase ? ' y restricción del Pase' : ''}`);
  }

  if (spec.portada?.reemplazos?.length) {
    await p.goto(`${URL}/course/editsection.php?id=${spec.portada.id}&sr=0`);
    await p.waitForFunction(() => window.tinymce?.get('id_summary_editor')?.initialized, null, { timeout: 60000 });
    const n = await p.evaluate((rs) => {
      const e = tinymce.get('id_summary_editor');
      let h = e.getContent(), k = 0;
      for (const [a, b] of rs) if (h.includes(a)) { h = h.split(a).join(b); k++; }
      document.getElementById('id_summary_editor').value = h;
      e.setContent(h);
      return k;
    }, spec.portada.reemplazos);
    await Promise.all([p.waitForNavigation(), p.locator('#id_submitbutton').click()]);
    console.log(`· portada: ${n} cambio(s)`);
  }

  for (const cm of spec.actividades) {
    await p.goto(`${URL}/course/modedit.php?update=${cm}`);
    const campo = p.locator('[name=availabilityconditionsjson]');
    await campo.waitFor({ state: 'attached' });
    await p.evaluate((j) => { document.querySelector('[name=availabilityconditionsjson]').value = j; }, restriccion);
    await Promise.all([p.waitForNavigation(), p.locator('#id_submitbutton2').click()]);
    if (p.url().includes('modedit.php')) throw new Error(`No se guardó la actividad ${cm}: ` + (await p.locator('.error, .alert-danger').allInnerTexts()).join(' '));
    console.log(`· actividad ${cm}: restricción del Pase`);
  }
} catch (e) {
  await p.screenshot({ path: '/tmp/pase-ajustes-error.png', fullPage: true }).catch(() => {});
  console.error('✗ ' + e.message + ` (página: ${p.url()})`);
  process.exitCode = 1;
} finally {
  await b.close();
}
