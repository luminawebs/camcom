// Restaura un respaldo .mbz en Moodle recorriendo el asistente de restauración con Playwright.
// Lo llama moodle/subir_moodle.py; no se usa solo.
//
// Uso: node moodle/restaurar.mjs <archivo.mbz> <nombre corto> <categoría> <nombre completo> <usuario para REST>
// Variables de entorno: MOODLE_URL, MOODLE_USER, MOODLE_PASS (cuenta con rol Gestor en la categoría).
//
// - Si ya hay un curso con ese nombre corto, lo reemplaza: «Borrar el contenido del curso actual y después restaurar»,
//   conservando roles y matrículas (así el usuario del servicio web no pierde el acceso).
// - Si no hay, lo crea en la categoría.
// - Matricula como Profesor al usuario del servicio web (ClaudeBot) si no lo está, para que los ajustes por REST funcionen.
// Imprime en la última línea un JSON: {"curso": id, "accion": "nuevo" | "reemplazo"}.
// Si algo falla deja una captura y el HTML en /tmp/restaurar-error.{png,html}.
import { createRequire } from 'module';
import { execSync } from 'child_process';

const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const [mbz, corto, categoria, completo, botRest] = process.argv.slice(2);
if (!botRest) { console.error('Uso: node moodle/restaurar.mjs <mbz> <corto> <categoría> <nombre completo> <usuario REST>'); process.exit(2); }
const URL = process.env.MOODLE_URL.replace(/\/$/, '');
const paso = (t) => console.log('· ' + t);

const b = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
const p = await b.newPage();
p.setDefaultTimeout(60000);
// Moodle carga analítica y librerías de CDN que el entorno puede bloquear; no hacen falta para el asistente
await p.route(/clarity\.ms|googletagmanager|google-analytics/, (r) => r.abort());

async function boton(texto) {
  // Botón de envío del formulario visible con ese texto (los pasos del asistente usan input o button)
  const b = p.locator(`input[type=submit][value="${texto}"]:visible, button[type=submit]:visible:has-text("${texto}")`).first();
  await Promise.all([p.waitForLoadState('load'), p.waitForNavigation({ timeout: 600000 }), b.click()]);
}

async function marcar(nombre, valor) {
  // Ajuste sí/no del asistente por su nombre interno (no depende del idioma); si no está en este paso, no hace nada
  const campo = p.locator(`[name="${nombre}"]:not([type=hidden])`).first();
  if (!(await campo.count()) || (await campo.isDisabled())) return false;
  if ((await campo.evaluate((e) => e.tagName)) === 'SELECT') await campo.selectOption(valor ? '1' : '0');
  else await campo.setChecked(valor);
  return true;
}

async function siguiente() {
  // Botón principal de los pasos Ajustes, Esquema y Revisar («Siguiente», «Ejecutar restauración»)
  await Promise.all([p.waitForNavigation({ timeout: 600000 }), p.locator('#id_submitbutton').click()]);
}

async function enDestino() {
  // En el paso «Destino» la tabla de «Restaurar en un curso existente» lista los cursos por nombre corto;
  // devuelve el id del curso con ese nombre corto o null. Si la lista no lo muestra, lo busca.
  const buscar = async () => {
    for (const fila of await p.locator('tr.rcs-course').all()) {
      const celdas = (await fila.locator('td').allInnerTexts()).map((t) => t.trim());
      if (celdas.includes(corto)) return Number(await fila.locator('input[name=targetid]').getAttribute('value'));
    }
    return null;
  };
  let id = await buscar();
  if (id === null && (await p.locator('input[name=search]').count())) {
    await p.fill('input[name=search]', corto);
    await Promise.all([p.waitForNavigation(), p.locator('form:has(input[name=search]) button[name=searchcourses]').click()]);
    id = await buscar();
  }
  return id;
}

try {
  paso('Entrando a Moodle');
  await p.goto(URL + '/login/index.php');
  await p.fill('#username', process.env.MOODLE_USER);
  await p.fill('#password', process.env.MOODLE_PASS);
  await Promise.all([p.waitForNavigation(), p.click('#loginbtn')]);
  if (p.url().includes('/login/')) throw new Error('No se pudo iniciar sesión con MOODLE_USER / MOODLE_PASS');

  // siempre desde la categoría: el asistente ofrece ahí tanto curso nuevo como reemplazo de uno existente
  await p.goto(`${URL}/course/index.php`);
  const enlace = p.locator('a[href*="categoryid="]', { hasText: categoria }).first();
  if (!(await enlace.count())) throw new Error(`No encuentro la categoría «${categoria}»`);
  await Promise.all([p.waitForNavigation(), enlace.click()]);
  const contexto = await p.evaluate(() => M.cfg.contextid);

  paso('Subiendo el respaldo');
  await p.goto(`${URL}/backup/restorefile.php?contextid=${contexto}`);
  if (await p.getByText('no tiene los permisos', { exact: false }).count()) throw new Error('La cuenta no tiene permiso para restaurar aquí (falta el rol Gestor en la categoría)');
  await p.locator('.fp-btn-choose:visible, input[name=backupfilechoose]:visible').first().click();
  const dialogo = p.locator('.moodle-dialogue-base:visible .file-picker, .file-picker:visible').first();
  await dialogo.waitFor();
  const subir = dialogo.locator('.fp-repo', { hasText: /Subir|Upload/ }).first();
  if (await subir.count()) await subir.click();
  // el formulario de subida se vuelve a dibujar al elegir el repositorio: esperar el campo visible antes de usarlo
  const archivo = p.locator('.file-picker:visible .fp-upload-form input[type=file]:visible, .file-picker:visible input[name=repo_upload_file]:visible').first();
  await archivo.waitFor();
  await p.waitForTimeout(500);
  await archivo.setInputFiles(mbz);
  if (!(await archivo.evaluate((e) => e.files.length))) throw new Error('No se pudo adjuntar el .mbz en el selector de archivos');
  await p.locator('.file-picker:visible .fp-upload-btn:visible').first().click();
  await p.locator('.filepicker-filename a, .filepicker-filename').filter({ hasText: '.mbz' }).first().waitFor({ timeout: 300000 });
  await boton('Restaurar');

  paso('Confirmando el respaldo');
  await boton('Continuar');

  paso('Eligiendo el destino');
  const existente = await enDestino();
  const continuar = (f) => Promise.all([p.waitForNavigation(), f.locator('input[type=submit][value="Continuar"]').click()]);
  if (existente) {
    paso(`Ya existe el curso ${corto} (id ${existente}): se borra su contenido y se restaura encima`);
    const form = p.locator('form', { has: p.locator('input[name=target][value="3"]') });
    await form.locator('input[name=target][value="3"]').check();
    await form.locator(`input[name=targetid][value="${existente}"]`).check();
    await continuar(form);
  } else {
    paso(`No existe ${corto}: se crea en «${categoria}»`);
    const form = p.locator('form', { has: p.locator('input[name=target][value="2"]') });
    await form.locator('input[name=target][value="2"]').check();
    const cat = form.getByLabel(categoria, { exact: true });
    if (await cat.count()) await cat.first().check();
    await continuar(form);
  }

  paso('Ajustes de la restauración');
  await siguiente();

  paso('Esquema del curso');
  await marcar('setting_course_overwrite_conf', true);
  if (existente) {
    // conservar matrículas y roles: así ClaudeBot y los estudiantes no pierden el acceso al reemplazar
    await marcar('setting_course_keep_roles_and_enrolments', true);
    await marcar('setting_course_keep_groups_and_groupings', true);
  }
  for (const [n, v] of [['setting_course_course_fullname', completo], ['setting_course_course_shortname', corto]]) {
    const c = p.locator(`[name="${n}"]`);
    if ((await c.count()) && (await c.isEditable())) await c.fill(v);
  }
  await siguiente();

  paso('Restaurando (puede tardar)');
  await siguiente();
  const texto = await p.locator('#region-main').innerText();
  if (!/con éxito|successfully/i.test(texto)) throw new Error('Moodle no confirmó la restauración: ' + texto.slice(0, 500));

  // la página final trae un formulario «Continuar» hacia course/view.php con el id del curso en un campo oculto
  const idFinal = await p.locator('form[action*="/course/view.php"] input[name=id]').first().getAttribute('value').catch(() => null);
  const curso = existente || Number(idFinal) || null;
  if (!curso) throw new Error('La restauración terminó pero no encuentro el curso ' + corto);

  paso(`Revisando que ${botRest} esté matriculado`);
  await p.goto(`${URL}/user/index.php?id=${curso}&perpage=5000`);
  if (!(await p.locator('#participants').getByText(botRest, { exact: false }).count())) try {
    paso(`Matriculando a ${botRest} como Profesor`);
    await p.locator('input[type=submit][value="Matricular usuarios"], button:has-text("Matricular usuarios")').first().click();
    const modal = p.locator('.modal-dialog:visible').first();
    await modal.locator('input[type=search], input[placeholder*="Buscar"]').first().fill(botRest);
    await p.locator('.form-autocomplete-suggestions li', { hasText: botRest }).first().click();
    const rol = modal.locator('select[name=roletoassign]');
    await rol.selectOption({ label: 'Profesor' });
    await modal.locator('button[data-action=save], button:has-text("Matricular usuarios")').last().click();
    await p.locator('#participants').getByText(botRest, { exact: false }).first().waitFor();
  } catch (e) {
    // si ClaudeBot es Gestor en la categoría ya tiene acceso por REST aunque no esté matriculado
    console.log(`  (no pude matricular a ${botRest}: ${e.message.split('\n')[0]})`);
  }

  console.log(JSON.stringify({ curso, accion: existente ? 'reemplazo' : 'nuevo' }));
} catch (e) {
  await p.screenshot({ path: '/tmp/restaurar-error.png', fullPage: true }).catch(() => {});
  await import('fs').then((fs) => p.content().then((h) => fs.writeFileSync('/tmp/restaurar-error.html', h))).catch(() => {});
  console.error('✗ ' + e.message + `\n  (página: ${p.url()}; captura en /tmp/restaurar-error.png)`);
  process.exitCode = 1;
} finally {
  await b.close();
}
