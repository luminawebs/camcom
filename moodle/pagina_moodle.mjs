// Agrega o cambia una Página en un curso ya publicado, sin restaurar (no borra el avance de nadie).
// La llama moodle/invitacion_pase.py; sirve para cualquier Página suelta.
//
// Uso: node moodle/pagina_moodle.mjs <id del curso> <número de sección> <nombre> <contenido.html> [cmid para cambiar]
// Variables de entorno: MOODLE_URL, MOODLE_USER, MOODLE_PASS (la misma cuenta Gestor de restaurar.mjs).
// Sin cmid crea la Página al final de la sección; con cmid reemplaza nombre y contenido. Sin finalización.
// Si algo falla deja /tmp/pagina-error.{png,html}.
import { createRequire } from 'module';
import { execSync } from 'child_process';
import fs from 'fs';

const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const [curso, seccion, nombre, archivo, cmid] = process.argv.slice(2);
if (!archivo) { console.error('Uso: node moodle/pagina_moodle.mjs <curso> <sección> <nombre> <contenido.html> [cmid]'); process.exit(2); }
const URL = process.env.MOODLE_URL.replace(/\/$/, '');
const contenido = fs.readFileSync(archivo, 'utf-8');

const b = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
const p = await b.newPage();
p.setDefaultTimeout(60000);
await p.route(/clarity\.ms|googletagmanager|google-analytics/, (r) => r.abort());

try {
  await p.goto(URL + '/login/index.php');
  await p.fill('#username', process.env.MOODLE_USER);
  await p.fill('#password', process.env.MOODLE_PASS);
  await Promise.all([p.waitForNavigation(), p.click('#loginbtn')]);
  if (p.url().includes('/login/')) throw new Error('No se pudo iniciar sesión con MOODLE_USER / MOODLE_PASS');

  await p.goto(cmid ? `${URL}/course/modedit.php?update=${cmid}&return=0`
                    : `${URL}/course/modedit.php?add=page&type=&course=${curso}&section=${seccion}&return=0`);
  await p.locator('#id_name').waitFor();
  await p.fill('#id_name', nombre);
  // el contenido va por el editor (TinyMCE o Atto) para que no lo pise al guardar; si no hay editor, al textarea
  await p.waitForTimeout(1500);
  const puesto = await p.evaluate((html) => {
    if (window.tinymce && window.tinymce.get('id_page')) { window.tinymce.get('id_page').setContent(html); return 'tinymce'; }
    const atto = document.querySelector('#id_pageeditable');
    if (atto) { atto.innerHTML = html; atto.dispatchEvent(new Event('input', { bubbles: true })); }
    document.querySelector('#id_page').value = html;
    return atto ? 'atto' : 'textarea';
  }, contenido);
  // sin finalización: la invitación no cuenta para terminar la unidad
  const fin = p.locator('select#id_completion');
  if (await fin.count()) await fin.selectOption('0');
  const sinFin = p.locator('input[name=completion][value="0"]');
  if (await sinFin.count()) await sinFin.check({ force: true });

  await Promise.all([p.waitForNavigation(), p.locator('#id_submitbutton2').click()]);
  if (p.url().includes('/course/modedit.php')) {
    const err = await p.locator('.error, .invalid-feedback:visible').allInnerTexts();
    throw new Error('Moodle no guardó la Página: ' + err.join(' · '));
  }
  console.log(`✓ Página «${nombre}» ${cmid ? 'cambiada' : 'creada'} en el curso ${curso}, sección ${seccion} (editor: ${puesto})`);
} catch (e) {
  await p.screenshot({ path: '/tmp/pagina-error.png', fullPage: true }).catch(() => {});
  await p.content().then((h) => fs.writeFileSync('/tmp/pagina-error.html', h)).catch(() => {});
  console.error('✗ ' + e.message + `\n  (página: ${p.url()}; captura en /tmp/pagina-error.png)`);
  process.exitCode = 1;
} finally {
  await b.close();
}
