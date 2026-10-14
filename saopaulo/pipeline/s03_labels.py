"""Street names, laid along the streets (saopaulo/web/data/labels.json, the format of pipeline/s07_labels.py).

Source: GeoSampa street segments (segmento_logradouro), centre lines with the street's type, title and name.
Each street's segments are merged and cut into 300 m cells; each piece gets one label at its middle, turned
along it. Avenues longer than 2 km show from afar (tier 1), the rest only up close.
"""
import json
import math
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import geopandas as gpd
import numpy as np
import requests
import shapely

from .area import CRS
from .s02_tiles import MARGIN, area, to_local

RAW = Path("data-sp/raw")
OUT = Path("saopaulo/web/data")
WFS = "https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/geoportal/wfs"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/141.0"}
CELL = 300
FETCH_CELL = 2000
# Street types that get a name on the map; accesses, alleys and the like are left out.
TYPE = {"AV": "Avenida", "R": "Rua", "AL": "Alameda", "PC": "Praça", "VD": "Viaduto", "TV": "Travessa",
        "LG": "Largo", "PTE": "Ponte", "ES": "Estrada", "LD": "Ladeira", "VIA": "Via", "TN": "Túnel"}
# The register abbreviates titles; the map spells them out.
TITLE = {"brig": "Brigadeiro", "cel": "Coronel", "dr": "Doutor", "dra": "Doutora", "mal": "Marechal",
         "prof": "Professor", "profa": "Professora", "eng": "Engenheiro", "gen": "General", "pe": "Padre",
         "sto": "Santo", "sta": "Santa", "pres": "Presidente", "des": "Desembargador", "min": "Ministro",
         "cap": "Capitão", "ten": "Tenente", "alm": "Almirante", "jorn": "Jornalista", "sen": "Senador",
         "dep": "Deputado", "ver": "Vereador", "cons": "Conselheiro", "cmte": "Comandante", "maj": "Major",
         "sgt": "Sargento", "arq": "Arquiteto", "bel": "Bacharel", "com": "Comendador", "dom": "Dom",
         "frei": "Frei", "gov": "Governador", "insp": "Inspetor", "mons": "Monsenhor", "vig": "Vigário",
         "nsra": "Nossa Senhora", "pref": "Prefeito", "visc": "Visconde", "bar": "Barão", "cde": "Conde"}
SMALL = {"da", "de", "do", "das", "dos", "e"}
WIDTH = {"Avenida": 30, "Viaduto": 22, "Ponte": 22}


def fetch_cell(x, y):
    # WFS 1.1 takes the box as x,y; the server answers at most 10,200 features, hence the 2 km cells.
    r = requests.get(WFS, headers=UA, timeout=300, params={
        "service": "WFS", "version": "1.1.0", "request": "GetFeature", "typeName": "geoportal:segmento_logradouro",
        "outputFormat": "application/json", "srsName": f"EPSG:{CRS}",
        "bbox": f"{x},{y},{x + FETCH_CELL},{y + FETCH_CELL},EPSG:{CRS}"})
    r.raise_for_status()
    feats = r.json()["features"]
    if len(feats) >= 10200:
        raise RuntimeError(f"cell {x},{y} hit the server's feature limit")
    return feats


def fetch(bounds):
    out = RAW / "logradouros.geojson"
    if not out.exists():
        x0, y0, x1, y1 = (int(v // FETCH_CELL * FETCH_CELL) for v in bounds)
        cells = [(x, y) for x in range(x0, x1 + 1, FETCH_CELL) for y in range(y0, y1 + 1, FETCH_CELL)]
        with ThreadPoolExecutor(4) as ex:
            parts = list(ex.map(lambda c: fetch_cell(*c), cells))
        seen, feats = set(), []
        for f in (f for p in parts for f in p):
            if f["id"] not in seen:
                seen.add(f["id"]); feats.append(f)
        out.write_text(json.dumps({"type": "FeatureCollection", "features": feats}), encoding="utf-8")
        print(len(feats), "street segments")
    return gpd.read_file(out).set_crs(CRS, allow_override=True)


def title(s):
    words = (s if isinstance(s, str) else "").lower().split()
    return " ".join(TITLE.get(w) or (w if (i and w in SMALL) else w.capitalize()) for i, w in enumerate(words))


def full_name(r):
    kind = r.cd_tipo_logradouro if isinstance(r.cd_tipo_logradouro, str) else ""
    prep = r.tx_preposicao_logradouro if isinstance(r.tx_preposicao_logradouro, str) else ""
    if kind not in TYPE:
        return ""
    parts = [TYPE[kind], title(r.cd_titulo_logradouro), prep.lower(), title(r.nm_logradouro)]
    return " ".join(p for p in parts if p)


def placement(piece, width):
    a, b = np.array(piece.coords[0]), np.array(piece.coords[-1])
    d = b - a
    if np.hypot(*d) < 1:
        return None
    mid = piece.interpolate(0.5, normalized=True)
    ang = math.degrees(math.atan2(-d[1], d[0]))  # local z points south
    ang = (ang + 90) % 180 - 90  # keep text upright
    x, z = to_local(np.array([[mid.x, mid.y]]))[0]
    return [round(float(x), 1), round(float(z), 1), round(ang, 1), round(float(piece.length)), width]


def main():
    extent = area().buffer(MARGIN)
    s = fetch(extent.bounds)
    s = s[s.intersects(extent)]
    s["name"] = [full_name(r) for r in s.itertuples()]
    labels = []
    for name, g in s.groupby("name"):
        if len(name) < 4:
            continue
        line = shapely.line_merge(shapely.union_all(g.geometry.values))
        line = line.intersection(extent)
        total = line.length
        kind = name.split()[0]
        width = WIDTH.get(kind, 14)
        x0, y0, x1, y1 = line.bounds
        pts = []
        for cx in np.arange(math.floor(x0 / CELL) * CELL, x1, CELL):
            for cy in np.arange(math.floor(y0 / CELL) * CELL, y1, CELL):
                cut = line.intersection(shapely.box(cx, cy, cx + CELL, cy + CELL))
                for piece in getattr(cut, "geoms", [cut]):
                    if piece.geom_type == "LineString" and piece.length > 60 and (p := placement(piece, width)):
                        pts.append(p)
        if pts:
            labels.append(dict(name=name, water=False, tier=1 if kind == "Avenida" and total > 2000 else 2, pts=pts))
    (OUT / "labels.json").write_text(json.dumps(labels, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(labels)} names, {sum(len(l['pts']) for l in labels)} placements,"
          f" {sum(l['tier'] == 1 for l in labels)} tier 1; {(OUT / 'labels.json').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
