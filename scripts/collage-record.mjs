/*
  Films each map in scripts/collage-sites.mjs for 15 s at 720×540 into out-video/collage/<id>.mp4.

    cd ../stop-token && node ../amsterdam-by-building/scripts/collage-record.mjs [id ...]

  Each map gets 25 s to load; then the film starts, the map's own Play button is pressed when it has one (the
  city growing is the point of all of them); a map without one zooms in slowly instead.
*/
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { resolve, join } from "node:path";
import { SITES } from "./collage-sites.mjs";

const require = createRequire(resolve("package.json"));
const { chromium } = require("playwright");
const ffmpeg = require("ffmpeg-static");
const W = 720, H = 540, SECONDS = 15;
const out = resolve("out-video/collage");
const only = process.argv.slice(2);

const browser = await chromium.launch({ args: ["--use-angle=metal", "--enable-gpu", "--ignore-gpu-blocklist"] });
for (const [id, url] of SITES.filter(s => !only.length || only.includes(s[0]))) {
  if (id === "geneva") continue;
  const tmp = join(out, `.${id}`);
  rmSync(tmp, { recursive: true, force: true });
  mkdirSync(tmp, { recursive: true });
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, locale: "en-US" });
  const page = await ctx.newPage();
  try { await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 }); } catch (e) { console.log(id, e.message.slice(0, 80)); }
  await page.waitForTimeout(25000);
  if (id === "italia") { await page.getByText("Pavia", { exact: true }).first().click().catch(() => {}); await page.waitForTimeout(20000); }
  await page.mouse.move(W - 1, 1);  // out of the way: a pointer over the map opens its hover card

  const cdp = await ctx.newCDPSession(page);
  const frames = [];
  let k = 0;
  cdp.on("Page.screencastFrame", ({ data, metadata, sessionId }) => {
    const file = join(tmp, `${String(k++).padStart(5, "0")}.jpg`);
    writeFileSync(file, Buffer.from(data, "base64"));
    frames.push({ file, t: metadata.timestamp * 1000 });
    cdp.send("Page.screencastFrameAck", { sessionId }).catch(() => {});
  });
  await cdp.send("Page.startScreencast", { format: "jpeg", quality: 85, maxWidth: W, maxHeight: H, everyNthFrame: 1 });
  const t0 = Date.now();
  // the map's own Play: a button whose name or text says play, in any of the languages here
  const played = await page.evaluate(() => {
    const re = /play|reproduc|riproduc|reproduz|toista|lire|jouer|воспр|старт|afspelen|speel|▶|►/i;
    const marked = document.querySelector("button.play, #play, [role=button].play");
    const b = marked?.getBoundingClientRect().width ? marked : [...document.querySelectorAll("button,[role=button]")].find(el => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0 && re.test(`${el.getAttribute("aria-label") || ""} ${el.title || ""} ${el.textContent || ""}`);
    });
    if (b) { b.click(); return (b.getAttribute("aria-label") || b.textContent || "").trim().slice(0, 30); }
    return null;
  }).catch(() => null);
  // A map without Play moves another way: a slow zoom towards the centre.
  if (!played) await page.mouse.move(W / 2, H / 2 + 40);
  while (Date.now() - t0 < SECONDS * 1000) {
    if (!played) await page.mouse.wheel(0, -6);
    await page.waitForTimeout(120);
  }
  await cdp.send("Page.stopScreencast");
  await page.waitForTimeout(300);
  await ctx.close();

  // variable frame rate: each frame stays up as long as it really did, then a steady 30 fps
  const list = frames.map((f, i) => `file '${f.file}'\nduration ${(((frames[i + 1]?.t ?? f.t + 33) - f.t) / 1000).toFixed(3)}`).join("\n");
  writeFileSync(join(tmp, "list.txt"), list + `\nfile '${frames.at(-1).file}'\n`);
  execFileSync(ffmpeg, ["-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", join(tmp, "list.txt"),
    "-vf", `scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H},fps=30`, "-t", String(SECONDS),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", join(out, `${id}.mp4`)]);
  rmSync(tmp, { recursive: true, force: true });
  console.log(id, frames.length, "frames, play:", played);
}
await browser.close();
