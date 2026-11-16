// Builds one offline file from deck.html by inlining the Geist fonts, so the deck needs no network.
// Copy this folder to <project>/src, then run: node src/build.mjs [out.html]   (default: <project>/index.html)
import { readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const dir = new URL(".", import.meta.url).pathname;
const out = resolve(process.argv[2] ?? join(dir, "..", "index.html"));

const faces = [
  ["Geist", 400, "Geist-Regular", "Geist Regular"],
  ["Geist", 500, "Geist-Medium", "Geist Medium"],
  ["Geist", 600, "Geist-SemiBold", "Geist SemiBold"],
  ["Geist Mono", 400, "GeistMono-Regular", "Geist Mono Regular"],
  ["Geist Mono", 500, "GeistMono-Medium", "Geist Mono Medium"],
  ["Geist Mono", 600, "GeistMono-SemiBold", "Geist Mono SemiBold"],
];

const css = faces
  .map(([family, weight, file, local]) => {
    const data = readFileSync(join(dir, "fonts", `${file}.woff2`)).toString("base64");

    return `@font-face{font-family:"${family}";font-style:normal;font-weight:${weight};font-display:block;src:local("${local}"),local("${file}"),url(data:font/woff2;base64,${data}) format("woff2")}`;
  })
  .join("\n");

const license = readFileSync(join(dir, "fonts", "OFL.txt"), "utf8");
const html = readFileSync(join(dir, "deck.html"), "utf8")
  .replace("/*@FONTS@*/", css)
  .replace("<head>", `<head>\n<!-- Bundled font license\n${license}\n-->`);

writeFileSync(out, html);
console.log(`${out}: ${(html.length / 1024).toFixed(0)} KB`);
