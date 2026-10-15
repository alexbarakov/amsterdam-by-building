// Turns one binary tile into a mesh. Positions stay in decimetres from the tile origin.
// A part is either a LoD 1.3 prism (walls and a flat roof at its height) or, with height -1, a LoD 2.2 roof face
// whose vertices carry their own height; a building of roof faces gets its walls from the faces' open edges,
// dropped to the ground, which rebuilds gable ends and steps between roofs.
import { ShapeUtils, Vector2 } from './vendor/three.core.js';

function parse(buf) {
  const h = new DataView(buf);
  const nB = h.getUint32(4, true), nP = h.getUint32(8, true), nR = h.getUint32(12, true), nV = h.getUint32(16, true);
  const origin = [h.getFloat32(20, true), h.getFloat32(24, true)];
  let o = 28;
  const take = (Type, n) => { const a = new Type(buf, o, n); o += Math.ceil(n * Type.BYTES_PER_ELEMENT / 4) * 4; return a; };
  return {
    nB, origin,
    gid: take(Uint32Array, nB), year: take(Int16Array, nB), flag: take(Uint8Array, nB),
    period: take(Uint8Array, nB), floors: take(Uint8Array, nB), energy: take(Uint8Array, nB),
    lay0: take(Uint32Array, nB), lay1: take(Uint32Array, nB), partStart: take(Uint32Array, nB + 1),
    height: take(Float32Array, nP), ringStart: take(Uint32Array, nP + 1),
    vertStart: take(Uint32Array, nR + 1), hole: take(Uint8Array, nR), xz: take(Int16Array, 2 * nV),
    y: take(Int16Array, nV),
  };
}

function build(t) {
  let nVert = 0, nIdx = 0;
  for (let r = 0; r < t.hole.length; r++) {
    const n = t.vertStart[r + 1] - t.vertStart[r];
    nVert += n * 5; nIdx += n * 6 + n * 3;
  }
  const pos = new Int16Array(nVert * 3), bld = new Uint16Array(nVert), idx = new Uint32Array(nIdx);
  let v = 0, k = 0;
  for (let b = 0; b < t.nB; b++) {
    if (t.partStart[b + 1] > t.partStart[b] && t.height[t.partStart[b]] < 0) {
      // LoD 2.2: roof faces, then walls under every edge that only one face has
      const edges = new Map();
      for (let p = t.partStart[b]; p < t.partStart[b + 1]; p++) {
        const r0 = t.ringStart[p], r1 = t.ringStart[p + 1];
        let contour = null; const holes = [], ids = [];
        for (let r = r0; r < r1; r++) {
          const s0 = t.vertStart[r], n = t.vertStart[r + 1] - s0;
          const ring = [];
          for (let i = 0; i < n; i++) {
            const a = s0 + i, c = s0 + ((i + 1) % n);
            const ka = `${t.xz[2 * a]},${t.xz[2 * a + 1]},${t.y[a]}`, kc = `${t.xz[2 * c]},${t.xz[2 * c + 1]},${t.y[c]}`;
            const key = ka < kc ? ka + '|' + kc : kc + '|' + ka;
            const e = edges.get(key);
            if (e) e.n++; else edges.set(key, { n: 1, a, c });
            ring.push(new Vector2(t.xz[2 * a], t.xz[2 * a + 1]));
            ids.push(a);
          }
          if (!t.hole[r] && !contour) contour = ring; else holes.push(ring);
        }
        if (!contour || contour.length < 3) continue;
        const start = v;
        for (const a of ids) { pos.set([t.xz[2 * a], t.y[a], t.xz[2 * a + 1]], v * 3); bld[v] = b; v++; }
        for (const tri of ShapeUtils.triangulateShape(contour, holes)) {
          idx.set([start + tri[0], start + tri[1], start + tri[2]], k); k += 3;
        }
      }
      for (const { n, a, c } of edges.values()) {
        if (n !== 1) continue;
        const ax = t.xz[2 * a], az = t.xz[2 * a + 1], cx = t.xz[2 * c], cz = t.xz[2 * c + 1];
        pos.set([ax, 0, az, cx, 0, cz, cx, t.y[c], cz, ax, t.y[a], az], v * 3);
        bld.fill(b, v, v + 4);
        idx.set([v, v + 1, v + 2, v, v + 2, v + 3], k);
        v += 4; k += 6;
      }
      continue;
    }
    for (let p = t.partStart[b]; p < t.partStart[b + 1]; p++) {
      const top = Math.round(t.height[p] * 10);
      const r0 = t.ringStart[p], r1 = t.ringStart[p + 1];
      const contour = [], holes = [];
      // Walls
      for (let r = r0; r < r1; r++) {
        const s = t.vertStart[r], e = t.vertStart[r + 1], n = e - s;
        const ring = [];
        for (let i = 0; i < n; i++) {
          const a = s + i, c = s + ((i + 1) % n);
          const ax = t.xz[2 * a], az = t.xz[2 * a + 1], cx = t.xz[2 * c], cz = t.xz[2 * c + 1];
          pos.set([ax, 0, az, cx, 0, cz, cx, top, cz, ax, top, az], v * 3);
          bld.fill(b, v, v + 4);
          idx.set([v, v + 1, v + 2, v, v + 2, v + 3], k);
          v += 4; k += 6;
          ring.push(new Vector2(ax, az));
        }
        if (!t.hole[r] && !contour.length) contour.push(...ring);
        else holes.push(ring);
      }
      // Roof
      const roofStart = v;
      const all = contour.concat(...holes);
      for (const pt of all) { pos.set([pt.x, top, pt.y], v * 3); bld[v] = b; v++; }
      for (const tri of ShapeUtils.triangulateShape(contour, holes)) {
        idx.set([roofStart + tri[0], roofStart + tri[1], roofStart + tri[2]], k); k += 3;
      }
    }
  }
  // Per-building lookup, two texels: [year, period + 16*flag, floors, global id], [layer bits in four 16-bit words].
  const attr = new Float32Array(t.nB * 8);
  for (let b = 0; b < t.nB; b++) {
    attr.set([t.year[b], t.period[b] + 16 * t.flag[b], t.floors[b] + 128 * t.energy[b], t.gid[b],
      t.lay0[b] & 0xffff, t.lay0[b] >>> 16, t.lay1[b] & 0xffff, t.lay1[b] >>> 16], b * 8);
  }
  return { pos: pos.subarray(0, v * 3), bld: bld.subarray(0, v), idx: idx.subarray(0, k), attr, origin: t.origin, nB: t.nB };
}

self.onmessage = ({ data: { buf, id } }) => {
  const m = build(parse(buf));
  self.postMessage({ id, ...m }, [m.pos.buffer, m.bld.buffer, m.idx.buffer, m.attr.buffer]);
};
