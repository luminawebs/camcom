// Pone la imagen del curso en Moodle (Ajustes del curso › «Imagen del curso») con Playwright.
// La llama moodle/subir_moodle.py después de restaurar; también sirve sola para un curso ya publicado.
//
// Uso: node moodle/imagen_moodle.mjs <id del curso en Moodle> <imagen.jpg>
// Variables de entorno: MOODLE_URL, MOODLE_USER, MOODLE_PASS (la misma cuenta Gestor de restaurar.mjs).
// Borra la imagen anterior si la hay, sube la nueva y guarda. Si algo falla deja /tmp/imagen-error.{png,html}.
import { createRequire } from 'module';
import { execSync } from 'child_process';

const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const [curso, imagen] = process.argv.slice(2);
if (!imagen) { console.error('Uso: node moodle/imagen_moodle.mjs <id del curso> <imagen.jpg>'); process.exit(2); }
const URL = process.env.MOODLE_URL.replace(/\/$/, '');

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

  await p.goto(`${URL}/course/edit.php?id=${curso}`);
  const gestor = p.locator('#fitem_id_overviewfiles_filemanager .filemanager');
  await gestor.waitFor();
  // el gestor carga su lista por AJAX: esperar a que termine antes de mirar si hay imagen
  await gestor.locator('.filemanager-loading').waitFor({ state: 'hidden' }).catch(() => {});
  await p.waitForTimeout(800);

  // quitar la imagen anterior (el campo admite un solo archivo)
  for (let i = 0; i < 5 && (await gestor.locator('.fp-file:visible').count()); i++) {
    await gestor.locator('.fp-file:visible').first().click();
    await p.locator('.fp-file-delete:visible').first().click();
    await p.locator('.fp-dlg-butconfirm:visible, .modal-dialog:visible button[data-action=save], .modal-dialog:visible button:text-is("Sí"), .modal-dialog:visible button:text-is("Yes")').first().click();
    await p.waitForTimeout(800);
  }

  await gestor.locator('.fp-btn-add').click();
  const subir = p.locator('.file-picker:visible .fp-repo', { hasText: /Subir|Upload/ }).first();
  await subir.waitFor();
  await subir.click();
  const archivo = p.locator('.file-picker:visible .fp-upload-form input[type=file]:visible').first();
  await archivo.waitFor();
  await p.waitForTimeout(500);
  await archivo.setInputFiles(imagen);
  if (!(await archivo.evaluate((e) => e.files.length))) throw new Error('No se pudo adjuntar la imagen en el selector de archivos');
  await p.locator('.file-picker:visible .fp-upload-btn:visible').first().click();
  await gestor.locator('.fp-file:visible').first().waitFor({ timeout: 120000 });

  await Promise.all([p.waitForNavigation(), p.locator('#id_saveanddisplay').click()]);
  if (p.url().includes('/course/edit.php')) throw new Error('Moodle no guardó los ajustes del curso');
  console.log(`✓ imagen del curso puesta en ${URL}/course/view.php?id=${curso}`);
} catch (e) {
  await p.screenshot({ path: '/tmp/imagen-error.png', fullPage: true }).catch(() => {});
  await import('fs').then((fs) => p.content().then((h) => fs.writeFileSync('/tmp/imagen-error.html', h))).catch(() => {});
  console.error('✗ ' + e.message + `\n  (página: ${p.url()}; captura en /tmp/imagen-error.png)`);
  process.exitCode = 1;
} finally {
  await b.close();
}
