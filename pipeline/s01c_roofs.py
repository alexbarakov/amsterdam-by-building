"""Roof surfaces of every building from the 3D BAG LoD 2.2 model (data/roofs.parquet).

LoD 2.2 gives each building its real roof: gables, hips, dormers, towers and spires, as planar faces labelled
ground (0), roof (1) and wall (2). Only the roof faces are kept; the viewer raises the walls from the roof's
open edges down to the ground, which gives the same walls (gable ends included) for a third of the data.
Heights are metres above the building's own ground level (b3_h_maaiveld)."""
import glob

import geopandas as gpd
import pandas as pd
import pyogrio
import shapely


def labels(s):
    return [int(v) for v in s.split(":", 1)[1].rstrip(")").split(",")]


def main():
    b = pd.read_parquet("data/buildings.parquet", columns=["identificatie", "b3_h_maaiveld"])
    ground = dict(zip(b.identificatie, b.b3_h_maaiveld))
    rows = []
    for f in sorted(glob.glob("data/raw/3dbag/*.gpkg")):
        x = pyogrio.read_dataframe(f, layer="lod22_3d")
        x = x[x.identificatie.isin(ground)]
        for i, g, s in zip(x.identificatie, x.geometry.values, x["labels"]):
            roofs = [p for p, l in zip(g.geoms, labels(s)) if l == 1]
            if not roofs:
                continue
            z0 = ground[i]
            roofs = [shapely.transform(p, lambda c: c - [0, 0, z0], include_z=True) for p in roofs]
            rows.append((i, shapely.MultiPolygon(roofs)))
    r = gpd.GeoDataFrame(pd.DataFrame(rows, columns=["identificatie", "geometry"]), geometry="geometry", crs=28992)
    # a building split over two tiles of the model comes twice: keep the richer copy
    r["n"] = shapely.get_num_geometries(r.geometry.values)
    r = r.sort_values("n", ascending=False).drop_duplicates("identificatie").drop(columns="n")
    r.to_parquet("data/roofs.parquet")
    print(len(r), "buildings with LoD 2.2 roofs of", len(b))


if __name__ == "__main__":
    main()
