// Renders scene.html to frames/00000.jpg ... with a few parallel browser workers.
// Usage: node render.mjs [fps] [workers]
// Delete frames/ (or a range of files in it) to re-render; existing frames are skipped.
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const FPS = Number(process.argv[2] || 30);
const WORKERS = Number(process.argv[3] || 3);
const url = pathToFileURL(path.resolve('scene.html')).href;
mkdirSync('frames', { recursive: true });

const browser = await chromium.launch();
const probe = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await probe.goto(url);
await probe.waitForFunction(() => window.__ready);
const duration = await probe.evaluate(() => window.DURATION);
writeFileSync('cues.json', JSON.stringify(await probe.evaluate(() => window.__cues), null, 1));
await probe.close();

const total = Math.round(duration * FPS);
const t0 = Date.now();
async function worker(w) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(url);
  await page.waitForFunction(() => window.__ready);  // fonts loaded, first frame drawn
  for (let i = w; i < total; i += WORKERS) {        // interleave frames across workers
    const name = `frames/${String(i).padStart(5, '0')}.jpg`;
    if (existsSync(name)) continue;                   // resumable: skip frames already written
    // Read the canvas pixels directly: faster than a page screenshot and exactly the canvas.
    const data = await page.evaluate(t => {
      window.renderAt(t);
      return document.getElementById('c').toDataURL('image/jpeg', 0.93);
    }, i / FPS);
    writeFileSync(name, Buffer.from(data.split(',')[1], 'base64'));
  }
  await page.close();
}
await Promise.all(Array.from({ length: WORKERS }, (_, w) => worker(w)));
await browser.close();
const s = (Date.now() - t0) / 1000;
console.log(`${total} frames in ${s.toFixed(1)} s (${(total / s / WORKERS).toFixed(1)} fps per worker)`);
