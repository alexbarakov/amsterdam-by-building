"""Towers and spires above the LoD 2.2 model, from the AHN surface model (data/spires.parquet).

3D BAG reconstructs roofs from the national height scan (AHN) but leaves out what is too slender to be a roof
plane: the Nieuwe Kerk's model stops at 45 m, its spire reaches 108. For tall listed buildings the
AHN digital surface model (DSM, 0.5 m cells, PDOK WCS, CC0) is read inside the footprint; every cell more than
SPIRE_MIN above the model's own top becomes a 0.5 m square at its height. The viewer raises walls under these
squares like under any roof face, so a spire reads as a stack of fine columns, the way a point cloud does."""
import io
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
import shapely
from shapely.geometry import box

UA = {"User-Agent": "amsterdam-by-building/0.1 (https://stop-token.com/lab/amsterdam/)"}

WCS = "https://service.pdok.nl/rws/ahn/wcs/v1_0"
CACHE = Path("data/raw/ahn_dsm")
SPIRE_MIN = 3.0       # metres above the model's top
CELL = 0.5


def dsm(x0, y0, x1, y1):
    import rasterio
    f = CACHE / f"{int(x0)}_{int(y0)}_{int(x1)}_{int(y1)}.tif"
    if not f.exists():
        r = requests.get(WCS, headers=UA, timeout=120, params=[
            ("SERVICE", "WCS"), ("VERSION", "2.0.1"), ("REQUEST", "GetCoverage"), ("COVERAGEID", "dsm_05m"),
            ("FORMAT", "image/tiff"), ("SUBSET", f"x({x0},{x1})"), ("SUBSET", f"y({y0},{y1})")])
        r.raise_for_status()
        f.write_bytes(r.content)
    with rasterio.open(f) as src:
        a = src.read(1).astype(float)
        a[a > 1e30] = np.nan
        return a, src.transform


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    b = gpd.read_parquet("data/buildings.parquet", columns=["identificatie", "b3_h_maaiveld", "height", "geometry"])
    roofs = gpd.read_parquet("data/roofs.parquet").set_index("identificatie").geometry
    mon = {p for m in json.load(open("data/raw/layers/monuments.json")) for p in m["panden"]}
    # listed buildings only: elsewhere the scan's tall cells are as likely cranes and masts as towers
    cand = b[(b.height > 14) & b.identificatie.str.slice(-16).isin(mon)]
    print(len(cand), "candidates")
    rows = []
    for r in cand.itertuples():
        top = shapely.get_coordinates(roofs[r.identificatie], include_z=True)[:, 2].max() if r.identificatie in roofs.index else r.height
        x0, y0, x1, y1 = (np.floor(np.array(r.geometry.bounds) / CELL) * CELL) + [0, 0, CELL, CELL]
        a, tf = dsm(x0, y0, x1, y1)
        rel = a - r.b3_h_maaiveld
        ys, xs = np.where(rel > top + SPIRE_MIN)
        if not len(xs):
            continue
        squares = []
        for i, j in zip(ys, xs):
            px, py = tf * (j, i)          # top-left corner of the cell
            sq = box(px, py - CELL, px + CELL, py)
            if not r.geometry.contains(sq.centroid):
                continue
            h = round(float(rel[i, j]), 1)
            squares.append(shapely.force_3d(sq, h))
        if squares:
            rows.append((r.identificatie, shapely.MultiPolygon(squares), top, float(np.nanmax(rel))))
    s = gpd.GeoDataFrame(pd.DataFrame(rows, columns=["identificatie", "geometry", "model_top", "dsm_top"]),
                         geometry="geometry", crs=28992)
    s.to_parquet("data/spires.parquet")
    for r in s.sort_values("dsm_top", ascending=False).head(12).itertuples():
        print(f"{r.identificatie[-16:]}  model {r.model_top:5.1f} m  ->  {r.dsm_top:5.1f} m  ({len(r.geometry.geoms)} cells)")
    print(len(s), "buildings get towers or spires")


if __name__ == "__main__":
    main()
