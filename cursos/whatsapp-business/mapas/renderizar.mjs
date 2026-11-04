// Pasa cada mapas/*.html a PNG (1080 px de ancho). Uso: node renderizar.mjs
import { createRequire } from 'module';
import { execSync } from 'child_process';
const { chromium } = createRequire(import.meta.url)(execSync('npm root -g').toString().trim() + '/playwright');
import { readdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
const aqui = dirname(fileURLToPath(import.meta.url));
const nav = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await nav.newPage({ viewport: { width: 1080, height: 800 } });
for (const f of readdirSync(aqui).filter(f => f.endsWith('.html'))) {
  await p.goto('file://' + join(aqui, f));
  await p.screenshot({ path: join(aqui, f.replace('.html', '.png')), fullPage: true });
  console.log('png', f);
}
await nav.close();
