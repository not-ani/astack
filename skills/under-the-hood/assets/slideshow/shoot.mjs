// Screenshots every slide at every step, so each build can be looked at, and reports console errors.
// Run: node src/shoot.mjs [index.html] [out-dir]   (defaults: <project>/index.html, <project>/shots)
// Playwright resolves from the current directory, then from the global npm root. If its pinned
// browser is missing, the newest Chromium already in the Playwright cache is used instead.
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync } from "node:fs";
import { createRequire } from "node:module";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const dir = new URL(".", import.meta.url).pathname;
const file = resolve(process.argv[2] ?? join(dir, "..", "index.html"));
const out = resolve(process.argv[3] ?? join(dir, "..", "shots"));

function loadPlaywright() {
  const roots = [join(process.cwd(), "x.js")];
  try { roots.push(join(execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim(), "x.js")); } catch {}
  for (const from of roots) {
    try { return createRequire(from)("playwright"); } catch {}
  }
  throw new Error("Playwright not found: run this from a project that has it, or npm i -g playwright");
}

function cachedChromium() {
  const cache = process.platform === "darwin" ? join(homedir(), "Library/Caches/ms-playwright") : join(homedir(), ".cache/ms-playwright");
  if (!existsSync(cache)) return undefined;
  const builds = readdirSync(cache).filter((d) => /^chromium-\d+$/.test(d)).sort((a, b) => +b.split("-")[1] - +a.split("-")[1]);
  const bins = ["chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing", "chrome-mac/Chromium.app/Contents/MacOS/Chromium", "chrome-linux/chrome", "chrome-linux64/chrome"];
  for (const b of builds) for (const bin of bins) if (existsSync(join(cache, b, bin))) return join(cache, b, bin);
  return undefined;
}

const { chromium } = loadPlaywright();
let browser;
try { browser = await chromium.launch(); } catch { browser = await chromium.launch({ executablePath: cachedChromium() }); }

const page = await browser.newPage({ viewport: { width: 1920, height: 1136 } });
const errors = [];
page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
page.on("pageerror", (e) => errors.push(String(e)));
await page.emulateMedia({ reducedMotion: "reduce" });
await page.goto(pathToFileURL(file).href);
await page.evaluate(() => document.fonts.ready);
mkdirSync(out, { recursive: true });

const slides = await page.evaluate(() => window.deck.slides);
const wide = [];
let shots = 0;
for (const [i, s] of slides.entries()) {
  for (let k = 0; k < s.steps; k++) {
    await page.evaluate(([i, k]) => window.deck.go(i, k), [i, k]);
    await page.waitForTimeout(60);
    const name = `${String(i).padStart(2, "0")}-${s.id}-${k + 1}.png`;
    await page.locator("#stage").screenshot({ path: join(out, name) });
    shots += 1;
  }
  // Code lines wider than their panel run past its border. Only the current slide has layout.
  wide.push(...await page.evaluate(() => [...document.querySelectorAll(".sl.cur .ln")]
    .filter((ln) => ln.scrollWidth > ln.clientWidth + 1).map((ln) => `${ln.closest(".sl").id}: ${ln.textContent.trim()}`)));
}
await browser.close();
console.log(`${shots} screenshots of ${slides.length} slides in ${out}`);
if (wide.length) { console.log(`code lines wider than their panel:\n${wide.join("\n")}`); process.exitCode = 1; }
if (errors.length) { console.log(`console errors:\n${errors.join("\n")}`); process.exitCode = 1; }
