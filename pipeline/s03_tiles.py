"""Pack buildings into 600 m binary tiles + a city config JSON.

Local frame: metres from the Dam, x east, z south (three.js, y up).
Tile layout (little-endian, every section 4-byte aligned):
  header  u32 magic, nB, nP, nR, nV; f32 originX, originZ
  B       u32 gid[nB]; i16 year[nB]; u8 flag[nB]; u8 period[nB]; u8 floors[nB]; u8 energy[nB] (0 none, 1 G … 12 A+++++);
          u32 lay0[nB]; u32 lay1[nB] (layer bits, see s05_layers); u32 partStart[nB+1]
  P       f32 height[nP]; u32 ringStart[nP+1]
  R       u32 vertStart[nR+1]; u8 hole[nR]
  V       i16 xz[2*nV], decimetres from the tile origin
"""
import json
import struct
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely

from .s02_attributes import clean_parts
from .periods import PERIODS

DAM = (121390.0, 487380.0)  # RD New
TILE = 600.0
SIMPLIFY = 0.25
OUT = Path("web/data")
MAGIC = 0x33424241  # 'ABB3'
ENERGY = ["G", "F", "E", "D", "C", "B", "A", "A+", "A++", "A+++", "A++++", "A+++++"]


def pad4(b: bytes) -> bytes:
    return b + b"\0" * (-len(b) % 4)


def to_local(coords: np.ndarray) -> np.ndarray:
    return np.c_[coords[:, 0] - DAM[0], -(coords[:, 1] - DAM[1])]


def rings_of(geom):
    polys = getattr(geom, "geoms", [geom])
    for poly in polys:
        if poly.is_empty:
            continue
        yield shapely.get_coordinates(poly.exterior)[:-1], 0
        for hole in poly.interiors:
            yield shapely.get_coordinates(hole)[:-1], 1


def pack_tile(origin, rows):
    gid, year, flag, period, floors, energy, lay0, lay1, part_start = [], [], [], [], [], [], [], [], [0]
    heights, ring_start, vert_start, holes, verts = [], [0], [0], [], []
    for b in rows:
        gid.append(b["gid"]); year.append(b["year"]); flag.append(b["flag"])
        period.append(b["period"]); floors.append(b["floors"])
        lay0.append(b["lay0"]); lay1.append(b["lay1"]); energy.append(b["energy"])
        for h, geom in b["parts"]:
            heights.append(h)
            for ring, hole in rings_of(geom):
                if len(ring) < 3:
                    continue
                loc = (to_local(ring) - origin) * 10
                verts.append(np.round(loc).astype(np.int16))
                holes.append(hole)
                vert_start.append(vert_start[-1] + len(ring))
            ring_start.append(len(holes))
        part_start.append(len(heights))
    nB, nP, nR = len(gid), len(heights), len(holes)
    V = np.concatenate(verts) if verts else np.zeros((0, 2), np.int16)
    out = struct.pack("<5I2f", MAGIC, nB, nP, nR, len(V), *origin)
    out += pad4(np.array(gid, "<u4").tobytes())
    out += pad4(np.array(year, "<i2").tobytes())
    out += pad4(np.array(flag, "u1").tobytes())
    out += pad4(np.array(period, "u1").tobytes())
    out += pad4(np.array(floors, "u1").tobytes())
    out += pad4(np.array(energy, "u1").tobytes())
    out += np.array(lay0, "<u4").tobytes() + np.array(lay1, "<u4").tobytes()
    out += pad4(np.array(part_start, "<u4").tobytes())
    out += pad4(np.array(heights, "<f4").tobytes())
    out += pad4(np.array(ring_start, "<u4").tobytes())
    out += pad4(np.array(vert_start, "<u4").tobytes())
    out += pad4(np.array(holes, "u1").tobytes())
    out += pad4(V.astype("<i2").tobytes())
    return out


def main():
    b = gpd.read_parquet("data/buildings.parquet")
    b = b.merge(pd.read_parquet("data/layers.parquet"), on="identificatie", how="left")
    labels = json.load(open("data/raw/energy.json"))
    b["energy"] = b.identificatie.str.slice(-16).map(lambda k: ENERGY.index(labels[k]) + 1 if labels.get(k) in ENERGY else 0)
    q = clean_parts(gpd.read_parquet("data/parts.parquet"))
    gid = {k: i for i, k in enumerate(b.identificatie)}
    ground = dict(zip(b.identificatie, b.b3_h_maaiveld))

    q = q[q.identificatie.isin(gid)].copy()
    q["h"] = (q.b3_h_70p - q.identificatie.map(ground)).clip(lower=2.5).fillna(2.5)
    q["geometry"] = shapely.simplify(q.geometry.values, SIMPLIFY, preserve_topology=True)
    parts = q.groupby("identificatie")[["h", "geometry"]].apply(lambda d: list(zip(d.h, d.geometry))).to_dict()

    c = to_local(np.c_[b.geometry.centroid.x, b.geometry.centroid.y])
    b["tx"] = np.floor(c[:, 0] / TILE).astype(int)
    b["tz"] = np.floor(c[:, 1] / TILE).astype(int)

    (OUT / "tiles").mkdir(parents=True, exist_ok=True)
    index = []
    for (tx, tz), grp in b.groupby(["tx", "tz"]):
        origin = np.array([tx * TILE, tz * TILE])
        rows = [dict(gid=gid[r.identificatie], year=int(r.year), flag=int(r.date_flag),
                     period=int(r.period), floors=int(r.floors),
                     lay0=int(r.lay0), lay1=int(r.lay1), energy=int(r.energy), parts=parts[r.identificatie])
                for r in grp.itertuples()]
        data = pack_tile(origin, rows)
        name = f"{tx}_{tz}.bin"
        (OUT / "tiles" / name).write_bytes(data)
        cx, cz = origin + TILE / 2
        index.append(dict(file=name, tx=int(tx), tz=int(tz), n=len(rows), bytes=len(data),
                          dist=round(float(np.hypot(cx, cz)))))
    index.sort(key=lambda t: t["dist"])

    # Bundle tiles into a few packs, nearest the Dam first, so the city loads centre-out in few requests.
    packs, n_packs = [], 8
    per = -(-len(index) // n_packs)
    for k in range(n_packs):
        chunk = index[k * per:(k + 1) * per]
        if not chunk:
            break
        name, offset, blob = f"pack{k}.bin", 0, bytearray()
        for t in chunk:
            data = (OUT / "tiles" / t["file"]).read_bytes()
            t.update(pack=name, offset=offset, length=len(data))
            blob += data; offset += len(data)
        (OUT / name).write_bytes(blob)
        packs.append(name)

    # Per-building lookup for hover: BAG id, height (dm), floors source, date flag.
    bag = b.identificatie.str.slice(-16).astype("int64").to_numpy()
    attrs = np.zeros(len(b), dtype=[("bag", "<f8"), ("h", "<u2"), ("fsrc", "u1"), ("flag", "u1"), ("year", "<i2"), ("orig", "<i2"), ("mon", "<u4"), ("lay0", "<u4"), ("lay1", "<u4"), ("wk", "<i4"),
                                    ("energy", "u1"), ("pad", "u1", 3), ("x", "<f4"), ("z", "<f4")])
    attrs["bag"] = bag
    attrs["h"] = np.round(b.height.fillna(0) * 10).clip(0, 65535)
    attrs["fsrc"] = b.floors_src; attrs["flag"] = b.date_flag
    attrs["year"] = b.year; attrs["orig"] = b.oorspronkelijkbouwjaar.astype(int)
    attrs["mon"] = pd.to_numeric(b.monument, errors="coerce").fillna(0).astype(int)
    attrs["lay0"] = b.lay0; attrs["lay1"] = b.lay1
    wk = pd.read_parquet("data/wiki_index.parquet").set_index("bag").wk
    attrs["wk"] = b.identificatie.str.slice(-16).map(wk).fillna(-1).astype(int)
    attrs["energy"] = b.energy
    cen = to_local(np.c_[b.geometry.centroid.x, b.geometry.centroid.y])
    attrs["x"], attrs["z"] = cen[:, 0], cen[:, 1]
    (OUT / "attrs.bin").write_bytes(attrs.tobytes())

    years = b.year.to_numpy()
    hist = {}
    for p, y in zip(b.period, years):
        hist.setdefault(int(y), [0] * len(PERIODS))[p] += 1
    config = dict(
        city="amsterdam", label="Amsterdam", tileSize=TILE, origin=DAM,
        # where a walk can start, besides the walker's own location
        starts=[dict(en=en, nl=nl, x=round(x - DAM[0], 1), z=round(-(y - DAM[1]), 1)) for en, nl, x, y in
                (("Dam", "Dam", *DAM), ("Centraal Station", "Centraal Station", 121880.0, 488060.0))],
        home=dict(x=0, z=200, azimuth=200, elevation=38, span=7000),
        periods=[dict(key=k, label=l, from_=a, to=bb, color=col) for k, l, a, bb, col in PERIODS],
        yearMin=int(years.min()), yearMax=int(years.max()),
        histogram={str(k): v for k, v in sorted(hist.items())},
        attrStride=attrs.dtype.itemsize,
        energy=dict(labels=ENERGY, counts=[int((b.energy == i).sum()) for i in range(len(ENERGY) + 1)]),
        tiles=index,
        packs=packs,
        stats=dict(buildings=len(b), exact=int((b.date_flag == 0).sum()),
                   faint=int((b.date_flag == 1).sum()), estimated=int((b.date_flag == 2).sum()),
                   monument=int((b.date_flag == 3).sum()), monumentApprox=int((b.date_flag == 4).sum()),
                   floorsBag3d=int((b.floors_src == 0).sum()), floorsHeight=int((b.floors_src == 1).sum())),
    )
    (OUT / "amsterdam.json").write_text(json.dumps(config, ensure_ascii=False, separators=(",", ":")).replace('"from_"', '"from"'))
    total = sum(t["bytes"] for t in index)
    print(f"{len(index)} tiles, {total/1e6:.1f} MB, attrs {attrs.nbytes/1e6:.1f} MB")


if __name__ == "__main__":
    main()
