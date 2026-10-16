/*
  Renders scripts/collage-globe.html (copied next to its assets in out-video/collage/globe/) frame by frame (30 fps, as long as the page's DURATION) into
  out-video/building-by-building-globe.mp4. Needs the films from collage-record.mjs, cut into frames in
  out-video/collage/globe/f/<id>/, and d3, topojson-client, world-atlas land-50m (as land.js) and Natural Earth
  populated places (as places.js, [lon, lat, pop_max]) beside them.

    cd ../stop-token && node ../amsterdam-by-building/scripts/collage-globe.mjs [frame ...]

  With frame numbers it only writes those frames as JPEGs, for checking.
*/
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { copyFileSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { resolve, join } from "node:path";

const require = createRequire(resolve("package.json"));
const { chromium } = require("playwright");
const ffmpeg = require("ffmpeg-static");
const dir = resolve("out-video/collage/globe");
copyFileSync(fileURLToPath(new URL("./collage-globe.html", import.meta.url)), join(dir, "globe.html"));
const frames = Object.fromEntries(readdirSync(join(dir, "f")).map(id => [id, readdirSync(join(dir, "f", id)).length]));
const only = process.argv.slice(2).map(Number);
const out = join(dir, "out");
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1080 } });
await page.addInitScript(f => { window.FRAMES = f; }, frames);
await page.goto("file://" + join(dir, "globe.html"));
const total = Math.round(await page.evaluate(() => window.DURATION) * 30);
const list = only.length ? only : Array.from({ length: total }, (_, i) => i);
for (const i of list) {
  await page.evaluate(i => window.renderFrame(i), i);
  await page.locator("canvas").screenshot({ path: join(out, `${String(i).padStart(4, "0")}.jpg`), type: "jpeg", quality: 92 });
}
await browser.close();
if (!only.length) {
  execFileSync(ffmpeg, ["-loglevel", "error", "-y", "-framerate", "30", "-i", join(out, "%04d.jpg"), "-c:v", "libx264",
    "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", resolve("out-video/building-by-building-globe.mp4")]);
  console.log("out-video/building-by-building-globe.mp4");
}
