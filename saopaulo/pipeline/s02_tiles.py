"""Tiles, attributes, the city config, water and land for the São Paulo viewer (saopaulo/web/data/).

Same formats as the Amsterdam viewer (pipeline/s03_tiles.py, s04_water.py), in a local frame centred on the
Praça da Sé. Each building is one part, as tall as GeoSampa's outline says; there is no terrain.
Per-building text the card shows (address, use, SQL) goes into small shards loaded on demand:
info/<gid // 4096>.json, a list indexed by gid % 4096.
"""
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely

import pipeline.s03_tiles as amsterdam
from pipeline.s04_water import pack as pack_polygons, polygons

from .area import CRS, DISTRICTS, ORIGIN
from .periods import PERIODS

OUT = Path("saopaulo/web/data")
RAW = Path("data-sp/raw")
TILE = 600.0
SIMPLIFY = 0.25
SHARD = 4096
MARGIN = 400  # metres around the districts, which end at the river banks; the Tietê and Pinheiros come into view

# The Amsterdam packer measures from its own origin; point it at the Sé.
amsterdam.DAM = ORIGIN
to_local = amsterdam.to_local


def area():
    d = gpd.read_file(RAW / "distritos.geojson").to_crs(CRS)
    names = (d.nm_distrito_municipal.str.normalize("NFKD").str.encode("ascii", "ignore").str.decode("ascii")
             .str.replace(" ", "_"))
    return d[names.isin(DISTRICTS)].union_all()


def water_and_land(extent):
    a = gpd.read_file(RAW / "agua.geojson").to_crs(CRS)
    water = shapely.make_valid(a[a.intersects(extent)].union_all()).intersection(extent)
    water = water.buffer(0.5).buffer(-0.5).simplify(1.0)
    water = [p for p in polygons(water) if p.area > 30]
    land = extent.difference(shapely.MultiPolygon(water)).simplify(1.0)
    land = [p for p in polygons(land) if p.area > 30]
    (OUT / "water.bin").write_bytes(pack_polygons(water))
    (OUT / "land.bin").write_bytes(pack_polygons(land))
    print(f"water {len(water)} polys {sum(p.area for p in water) / 1e6:.1f} km²; land {len(land)} polys")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    extent = area().buffer(MARGIN)
    water_and_land(extent)

    b = gpd.read_parquet("data-sp/buildings.parquet").reset_index(drop=True)
    b = b[b.representative_point().within(extent)].reset_index(drop=True)
    b["gid"] = b.index
    b["geometry"] = shapely.simplify(b.geometry.values, SIMPLIFY, preserve_topology=True)

    c = to_local(np.c_[b.geometry.centroid.x, b.geometry.centroid.y])
    b["x"], b["z"] = c[:, 0], c[:, 1]
    b["tx"] = np.floor(b.x / TILE).astype(int)
    b["tz"] = np.floor(b.z / TILE).astype(int)

    (OUT / "tiles").mkdir(exist_ok=True)
    index = []
    for (tx, tz), grp in b.groupby(["tx", "tz"]):
        origin = np.array([tx * TILE, tz * TILE])
        rows = [dict(gid=r.gid, year=int(r.year), flag=int(r.date_flag), period=int(r.period), floors=int(r.floors),
                     lay0=0, lay1=0, energy=0, parts=[(float(r.height), r.geometry)]) for r in grp.itertuples()]
        data = amsterdam.pack_tile(origin, rows)
        name = f"{tx}_{tz}.bin"
        (OUT / "tiles" / name).write_bytes(data)
        cx, cz = origin + TILE / 2
        index.append(dict(file=name, tx=int(tx), tz=int(tz), n=len(rows), bytes=len(data),
                          dist=round(float(np.hypot(cx, cz)))))
    index.sort(key=lambda t: t["dist"])

    # Packs, nearest the Sé first, so the city loads centre-out in few requests.
    packs, n_packs = [], 12
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

    # The Amsterdam attribute layout, so the viewer reads both alike; the id slot holds GeoSampa's outline id.
    attrs = np.zeros(len(b), dtype=[("bag", "<f8"), ("h", "<u2"), ("fsrc", "u1"), ("flag", "u1"), ("year", "<i2"), ("orig", "<i2"), ("mon", "<u4"), ("lay0", "<u4"), ("lay1", "<u4"), ("wk", "<i4"),
                                    ("energy", "u1"), ("pad", "u1", 3), ("x", "<f4"), ("z", "<f4")])
    attrs["bag"] = b.identificatie.astype("int64")
    attrs["h"] = np.round(b.height * 10).clip(0, 65535)
    attrs["fsrc"] = b.floors_src; attrs["flag"] = b.date_flag
    attrs["year"] = b.year; attrs["orig"] = b.orig
    attrs["wk"] = -1
    attrs["x"], attrs["z"] = b.x, b.z
    (OUT / "attrs.bin").write_bytes(attrs.tobytes())

    (OUT / "info").mkdir(exist_ok=True)
    sql = b.key.map(lambda k: f"{k[:3]}.{k[3:6]}.{k[6:10]}" + (f" (cond. {k[10:]})" if k[10:] not in ("", "00") else ""))
    info = list(zip(b.address, b.use, sql.where(b.key != "", ""), b.floors))
    for s in range(0, len(info), SHARD):
        (OUT / "info" / f"{s // SHARD}.json").write_text(
            json.dumps([list(r) for r in info[s:s + SHARD]], ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    hist = {}
    for p, y in zip(b.period, b.year):
        hist.setdefault(int(y), [0] * len(PERIODS))[p] += 1
    config = dict(
        city="sao-paulo", label="São Paulo", tileSize=TILE, origin=ORIGIN, infoShard=SHARD,
        home=dict(x=-700, z=2600, azimuth=200, elevation=42, span=17000),
        periods=[dict(key=k, label=en, label_pt=pt, **{"from": a}, to=z, color=col) for k, en, pt, a, z, col in PERIODS],
        yearMin=int(b.year.min()), yearMax=int(b.year.max()),
        histogram={str(k): v for k, v in sorted(hist.items())},
        attrStride=attrs.dtype.itemsize,
        tiles=index, packs=packs,
        stats=dict(buildings=len(b), exact=int((b.date_flag == 0).sum()), faint=int((b.date_flag == 1).sum()),
                   estimated=int((b.date_flag == 2).sum()), floorsIptu=int((b.floors_src == 0).sum()),
                   floorsHeight=int((b.floors_src == 1).sum())),
    )
    (OUT / "city.json").write_text(json.dumps(config, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    total = sum(t["bytes"] for t in index)
    print(f"{len(b)} buildings, {len(index)} tiles, {total / 1e6:.1f} MB, attrs {attrs.nbytes / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
