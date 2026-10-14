"""Buildings with a year and floors: GeoSampa outlines joined to the IPTU register through the fiscal lots.

  outline → lot     the outline's inner point falls in the lot polygon
  lot → IPTU        setor + quadra + lote for an ordinary lot; setor + quadra + condomínio for a condominium,
                    whose units each carry their own lote number but share the condominium's code
  year              the median 'ano da construção corrigido' of the lot's units (0 = an empty plot, ignored)
  floors            the most any unit on the lot gives; else the outline's height ÷ 3 m

Date flags (shown paler on the map):
  0 exact      the register's year
  1 faint      a year the register gives far more often than the years around it. Up to 1959 these come in
               five-year steps (1919, 1924 … 1959) with almost nothing between them: the register dates older
               buildings to the end of a five-year span, so the map spreads each over its five years. 1970 is the
               other spike (about eight times as many as 1969 or 1971); it stays, marked uncertain.
  2 estimated  no unit with a year on the lot (exempt or public buildings, buildings outside any lot):
               median year of the twelve nearest dated buildings within 1 km
"""
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from .area import CRS
from .periods import period_index

RAW = Path("data-sp/raw")
OUT = Path("data-sp")
FLAG_EXACT, FLAG_FAINT, FLAG_ESTIMATED = 0, 1, 2
FLOORS_IPTU, FLOORS_HEIGHT = 0, 1
STOREY_M = 3.0
SPIKE = 3.0  # a year with more than three times the mean of the three years either side is a spike
IPTU_COLS = {"NUMERO DO CONTRIBUINTE": "sql", "NUMERO DO CONDOMINIO": "cond", "ANO DA CONSTRUCAO CORRIGIDO": "year",
             "QUANTIDADE DE PAVIMENTOS": "floors", "TIPO DE USO DO IMOVEL": "use",
             "NOME DE LOGRADOURO DO IMOVEL": "street", "NUMERO DO IMOVEL": "number"}


def read_zipped(folder, suffix):
    frames = []
    for z in sorted((RAW / folder).glob("*.zip")):
        names = [n for n in zipfile.ZipFile(z).namelist() if n.endswith(suffix) and not n.startswith("SAD69")]
        frames.append(gpd.read_file(f"/vsizip/{z.as_posix()}/{names[0]}").to_crs(CRS))
    return gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=CRS)


def lot_key(setor, quadra, lote, cond):
    """One key per lot polygon: a condominium is its own lot (lote 0000) whatever its units' numbers."""
    return np.where(cond == "00", setor + quadra + lote + "00", setor + quadra + "0000" + cond)


def iptu(setores):
    d = pd.read_csv(RAW / "IPTU_2026.csv", sep=";", encoding="utf-8", usecols=list(IPTU_COLS), dtype=str)
    d = d.rename(columns=IPTU_COLS)
    d = d[d.sql.str[:3].isin(setores)]
    d["key"] = lot_key(d.sql.str[:3], d.sql.str[3:6], d.sql.str[6:10], d.cond.str[:2])
    d["year"] = pd.to_numeric(d.year, errors="coerce").fillna(0).astype(int)
    d["floors"] = pd.to_numeric(d.floors, errors="coerce").fillna(0).astype(int)
    d = d[d.year > 1500]
    d["address"] = (d.street.fillna("").str.title() + " " + d.number.fillna("").str.lstrip("0")).str.split().str.join(" ")
    g = d.groupby("key")
    lots = pd.DataFrame({
        "year": g.year.median().round().astype(int),
        "floors": g.floors.max(),
        "units": g.size(),
        "use": g.use.agg(lambda s: s.mode().iat[0] if s.notna().any() else ""),
        "address": g.address.agg(lambda s: s.mode().iat[0] if len(s) else ""),
    })
    print(f"IPTU: {len(d)} units with a year on {len(lots)} lots")
    return lots


def spike_years(years):
    n = years.value_counts()
    out = []
    for y, c in n.items():
        around = [n.get(y + d, 0) for d in (-3, -2, -1, 1, 2, 3)]
        if c > 50 and c > SPIKE * max(1.0, float(np.mean(around))):
            out.append(int(y))
    return sorted(out)


def estimate(b):
    pts = np.c_[b.geometry.centroid.x, b.geometry.centroid.y]
    known = b.date_flag.values != FLAG_ESTIMATED
    tree = cKDTree(pts[known])
    years = b.year.values[known]
    todo = np.where(~known)[0]
    dist, nn = tree.query(pts[todo], k=12, distance_upper_bound=1000)
    for row, d, n in zip(todo, dist, nn):
        ok = np.isfinite(d)
        b.iat[row, b.columns.get_loc("year")] = int(np.median(years[n[ok]])) if ok.any() else 1970
    return b


def main():
    b = read_zipped("edificacao", ".shp").drop_duplicates("ed_id")
    b = b[b.geometry.notna() & ~b.geometry.is_empty & (b.ed_area > 6)].reset_index(drop=True)
    b["identificatie"] = b.ed_id.astype("int64").astype(str)
    lots = read_zipped("lotes", ".gpkg")
    lots["key"] = lot_key(lots.lo_setor, lots.lo_quadra, lots.lo_lote, lots.lo_condomi)
    print(f"{len(b)} outlines, {len(lots)} lots")

    reg = iptu(set(lots.lo_setor))
    pts = gpd.GeoDataFrame({"i": b.index}, geometry=b.geometry.representative_point(), crs=CRS)
    j = gpd.sjoin(pts, lots[["key", "geometry"]], predicate="within").drop_duplicates("i").set_index("i").key
    b["key"] = j.reindex(b.index)
    b = b.join(reg, on="key", rsuffix="_iptu")

    b["height"] = b.ed_altura.astype(float).clip(lower=2.5).fillna(3.0)
    has_year = b.year.notna()
    b["year"] = b.year.fillna(0).astype(int)
    b["date_flag"] = np.where(has_year, FLAG_EXACT, FLAG_ESTIMATED).astype(np.uint8)
    spikes = spike_years(b.year[has_year])
    print("spike years:", spikes)
    b.loc[b.year.isin(spikes) & has_year, "date_flag"] = FLAG_FAINT
    b["orig"] = np.where(has_year, b.year, 0)
    # Five-year steps: spread evenly over the span the register's year closes, the same way on every run.
    step = (b.date_flag == FLAG_FAINT) & (b.year < 1960) & (b.year % 5 == 4)
    u = pd.util.hash_pandas_object(b.identificatie, index=False).to_numpy() % 5
    b.loc[step, "year"] = b.year[step] - u[step.to_numpy()]
    b = estimate(b)

    by_height = np.clip(np.round(b.height / STOREY_M), 1, 127).astype(int)
    has_floors = b.floors.fillna(0) > 0
    b["floors"] = np.where(has_floors, b.floors.fillna(0).clip(1, 127), by_height).astype(int)
    b["floors_src"] = np.where(has_floors, FLOORS_IPTU, FLOORS_HEIGHT).astype(np.uint8)
    b["period"] = b.year.map(period_index).astype(np.uint8)
    b["use"] = b.use.fillna(""); b["address"] = b.address.fillna(""); b["key"] = b.key.fillna("")

    out = b[["identificatie", "key", "year", "orig", "date_flag", "floors", "floors_src", "height", "period",
             "use", "address", "geometry"]]
    out.to_parquet(OUT / "buildings.parquet")
    flags = out.date_flag.value_counts().to_dict()
    print(f"{len(out)} buildings; {has_year.sum()} dated by IPTU, {flags.get(FLAG_FAINT, 0)} on spike years,"
          f" {flags.get(FLAG_ESTIMATED, 0)} estimated; floors from IPTU {has_floors.sum()}")
    print(out.period.value_counts().sort_index().to_dict())


if __name__ == "__main__":
    main()
