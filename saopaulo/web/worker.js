// Turns one binary tile into an extruded mesh. Positions stay in decimetres from the tile origin.
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
