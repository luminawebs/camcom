// Certificado de 7 unidades con el Pase (mod_customcert) en un curso de Moodle.
// Uso: node moodle/certificado.mjs <spec.json> [--vista out.pdf]
//   spec = {"curso": 10, "seccion": 8, "cm": 1178 (si ya existe; si no, se crea),
//           "nombre": "Certificado del curso: …", "intro": "<p>…</p>",
//           "grupo": 1, "demuestra": [1141, …],                 // restricción: grupo del Pase + Demuestra de cada unidad completados
//           "curso_nombre": "La plata del negocio", "horas": 4}
// Variables de entorno: MOODLE_URL, MOODLE_USER, MOODLE_PASS.
// La plantilla se arma desde cero (borra los elementos que tenga la página) en A4 horizontal.
// Sin logo de la Cámara: texto «Aula Virtual Empresarial · EduNest».
import { createRequire } from 'module';
import { execSync } from 'child_process';
import fs from 'fs';

const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const iv = process.argv.indexOf('--vista');
const vista = iv > 0 ? process.argv[iv + 1] : null;
const URL = process.env.MOODLE_URL.replace(/\/$/, '');
const VERDE = '#1f5f4f', GRIS = '#555555';

const centro = (y, o) => ({ posx: 148, posy: y, width: 250, refpoint: 1, alignment: 'C', colour: '#222222', ...o });
const ELEMENTOS = [
  { element: 'border', name: 'Borde', width: 3, colour: VERDE },
  { element: 'text', name: 'Marca', text: 'AULA VIRTUAL EMPRESARIAL · EDUNEST', ...centro(20, { font: 'freesansb', fontsize: 12, colour: VERDE }) },
  { element: 'text', name: 'Título', text: 'CERTIFICADO', ...centro(34, { font: 'freesansb', fontsize: 30 }) },
  { element: 'text', name: 'Se certifica', text: 'Se certifica que', ...centro(60, { font: 'freesans', fontsize: 14, colour: GRIS }) },
  { element: 'studentname', name: 'Nombre', ...centro(72, { font: 'freesansb', fontsize: 26 }) },
  { element: 'text', name: 'Completó', text: 'completó las 7 unidades del curso', ...centro(94, { font: 'freesans', fontsize: 14, colour: GRIS }) },
  { element: 'text', name: 'Curso', text: spec.curso_nombre, ...centro(105, { font: 'freesansb', fontsize: 20, colour: VERDE }) },
  { element: 'text', name: 'Detalle', text: `con una dedicación aproximada de ${spec.horas} horas y aprobó la evaluación «Demuestra» de cada unidad.`, ...centro(122, { font: 'freesans', fontsize: 12, colour: GRIS }) },
  { element: 'text', name: 'Rótulo fecha', text: 'Fecha de emisión', posx: 90, posy: 150, width: 100, refpoint: 1, alignment: 'C', font: 'freesans', fontsize: 10, colour: GRIS },
  { element: 'date', name: 'Fecha', dateitem: '-1', dateformat: 'strftimedate', posx: 90, posy: 157, width: 100, refpoint: 1, alignment: 'C', font: 'freesansb', fontsize: 13, colour: '#222222' },
  { element: 'text', name: 'Rótulo código', text: 'Código de verificación', posx: 207, posy: 150, width: 100, refpoint: 1, alignment: 'C', font: 'freesans', fontsize: 10, colour: GRIS },
  { element: 'code', name: 'Código', posx: 207, posy: 157, width: 100, refpoint: 1, alignment: 'C', font: 'freesansb', fontsize: 13, colour: '#222222' },
  { element: 'text', name: 'Verificación', text: 'Verifica este certificado en portal.edunest.co con el código de verificación.', ...centro(186, { font: 'freesans', fontsize: 9, colour: GRIS }) },
];

const b = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
const ctx = await b.newContext({ acceptDownloads: true });
const p = await ctx.newPage();
p.setDefaultTimeout(90000);
await p.route(/clarity\.ms|googletagmanager|google-analytics/, (r) => r.abort());
try {
  await p.goto(URL + '/login/index.php');
  await p.fill('#username', process.env.MOODLE_USER);
  await p.fill('#password', process.env.MOODLE_PASS);
  await Promise.all([p.waitForNavigation(), p.click('#loginbtn')]);
  if (p.url().includes('/login/')) throw new Error('No se pudo iniciar sesión');

  const c = [{ type: 'group', id: spec.grupo }, ...spec.demuestra.map((cm) => ({ type: 'completion', cm, e: 1 }))];
  const restriccion = JSON.stringify({ op: '&', c, showc: c.map(() => true) });
  await p.goto(spec.cm ? `${URL}/course/modedit.php?update=${spec.cm}` : `${URL}/course/modedit.php?add=customcert&course=${spec.curso}&section=${spec.seccion}&return=0&sr=0`);
  await p.locator('#id_name').fill(spec.nombre);
  await p.evaluate(({ intro, restriccion }) => {
    const q = (s) => document.querySelector(s);
    q('[name="introeditor[text]"]').value = intro;
    window.tinymce?.get('id_introeditor')?.setContent(intro);
    q('[name=emailstudents]').value = '1';
    q('[name=verifyany]').value = '1';
    q('[name=availabilityconditionsjson]').value = restriccion;
    q('input[name=completion][value="2"]').checked = true;
    const v = q('input[name=completionview][type=checkbox]'); v.disabled = false; v.checked = true;
  }, { intro: spec.intro, restriccion });
  await Promise.all([p.waitForNavigation(), p.locator('#id_submitbutton').click()]);
  if (p.url().includes('modedit.php')) throw new Error('No se guardó la actividad: ' + (await p.locator('.error, .alert-danger').allInnerTexts()).join(' '));
  const cm = new URLSearchParams(new globalThis.URL(p.url()).search).get('id');
  const editar = await p.locator('a[href*="/mod/customcert/edit.php?tid="]').first().getAttribute('href');
  const tid = new URLSearchParams(new globalThis.URL(editar).search).get('tid');
  console.log(`· actividad cm ${cm}, plantilla ${tid}: restricción grupo ${spec.grupo} + ${spec.demuestra.length} Demuestra`);

  // página A4 horizontal y elementos desde cero
  await p.goto(`${URL}/mod/customcert/edit.php?tid=${tid}`);
  const pagina = await p.locator('[name^=pagewidth_]').first().getAttribute('name');
  const pageid = pagina.split('_')[1];
  const viejos = await p.locator('a[href*="action=deleteelement"]').evaluateAll((as) => as.map((a) => a.href));
  for (const h of viejos) {
    await p.goto(h);
    const si = p.locator('form button[type=submit], form input[type=submit]').filter({ hasText: /Sí|Yes|Continuar/ }).or(p.locator('input[value="Sí"], input[value="Yes"]'));
    if (await si.count()) await Promise.all([p.waitForNavigation(), si.first().click()]);
  }
  if (viejos.length) console.log(`· ${viejos.length} elemento(s) anteriores borrados`);
  await p.goto(`${URL}/mod/customcert/edit.php?tid=${tid}`);
  await p.fill(`[name=pagewidth_${pageid}]`, '297');
  await p.fill(`[name=pageheight_${pageid}]`, '210');
  await Promise.all([p.waitForNavigation(), p.click('[name=submitbtn]')]);

  for (const el of ELEMENTOS) {
    await p.goto(`${URL}/mod/customcert/edit_element.php?tid=${tid}&action=add&element=${el.element}&pageid=${pageid}`);
    await p.evaluate((el) => {
      for (const [k, v] of Object.entries(el)) {
        if (k === 'element') continue;
        const e = document.querySelector(`#region-main form [name="${k}"]:not([type=hidden])`);
        if (!e) continue;
        e.value = String(v);
        if (k === 'text') window.tinymce?.get(e.id)?.setContent(String(v));
      }
    }, el);
    await Promise.all([p.waitForNavigation(), p.click('[name=savechanges]')]);
    if (p.url().includes('edit_element.php')) throw new Error(`No se guardó el elemento ${el.name}: ` + (await p.locator('.error, .alert-danger, .invalid-feedback').allInnerTexts()).join(' '));
  }
  console.log(`· ${ELEMENTOS.length} elementos en la plantilla`);

  if (vista) {
    await p.goto(`${URL}/mod/customcert/edit.php?tid=${tid}`);
    const [d] = await Promise.all([p.waitForEvent('download'), p.click('[name=previewbtn]')]);
    await d.saveAs(vista);
    console.log(`· vista previa: ${vista}`);
  }
} catch (e) {
  await p.screenshot({ path: '/tmp/certificado-error.png', fullPage: true }).catch(() => {});
  console.error('✗ ' + e.message + ` (página: ${p.url()})`);
  process.exitCode = 1;
} finally {
  await b.close();
}
