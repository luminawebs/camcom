// Pasa cada guias-pdf/*.html a PDF (A5 vertical). Uso: node renderizar_pdf.mjs
import { createRequire } from 'module';
import { execSync } from 'child_process';
import { readdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
const aqui = process.argv[2] ? join(dirname(fileURLToPath(import.meta.url)), '..', process.argv[2]) : dirname(fileURLToPath(import.meta.url));
const nav = await chromium.launch();
const p = await nav.newPage();
for (const f of readdirSync(aqui).filter(f => f.endsWith('.html'))) {
  await p.goto('file://' + join(aqui, f));
  await p.pdf({ path: join(aqui, f.replace('.html', '.pdf')), preferCSSPageSize: true, printBackground: true });
  console.log('pdf', f);
}
await nav.close();
