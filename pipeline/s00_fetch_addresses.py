"""Every address in the municipality with its building, for the search (BAG via PDOK, CC0).

Two downloads in 1 km cells over the city's bounds:
1. verblijfsobjecten (WFS): each object with its pand, written to data/raw/verblijfsobjecten.json.
2. addresses (OGC API 'adres'): every nummeraanduiding with the object it addresses. Unlike the verblijfsobject's own
   address fields this includes the side addresses: the Anne Frank House, Prinsengracht 263-267, is a side address of
   Westermarkt 10.
data/raw/addresses.json: street (openbare ruimte), number, letter, addition, postcode, verblijfsobject and pand.
Ligplaatsen and standplaatsen (houseboats, caravans) have no pand and are left out.
"""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

from .s00_fetch_water import BOUNDS

UA = {"User-Agent": "amsterdam-by-building/0.1 (https://stop-token.com/lab/amsterdam/)"}
WFS = "https://service.pdok.nl/lv/bag/wfs/v2_0"
ADRES = "https://api.pdok.nl/kadaster/bag/ogc/v2/collections/adres/items"
RD = "http://www.opengis.net/def/crs/EPSG/0/28992"
GEMEENTE_CODE = "0363"
CELL = 1000
PAGE = 1000
VBO = Path("data/raw/verblijfsobjecten.json")


def get(url, params=None):
    for attempt in range(5):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=120)
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError):
            if attempt == 4:
                raise


def vbo_cell(x, y):
    out, start = [], 0
    while True:
        fs = get(WFS, {"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeName": "bag:verblijfsobject",
                       "outputFormat": "application/json", "count": PAGE, "startIndex": start,
                       "bbox": f"{x},{y},{x + CELL},{y + CELL}"})["features"]
        out += [[f["properties"]["identificatie"], f["properties"]["pandidentificatie"]] for f in fs
                if f["properties"]["identificatie"].startswith(GEMEENTE_CODE)]
        if len(fs) < PAGE:
            return out
        start += PAGE


def adres_cell(x, y):
    out = []
    d = get(ADRES, {"f": "json", "limit": PAGE, "bbox": f"{x},{y},{x + CELL},{y + CELL}", "bbox-crs": RD,
                    "bronhouder_identificatie": GEMEENTE_CODE})
    while True:
        out += [f["properties"] for f in d["features"]
                if f["properties"]["adresseerbaar_object_type"] == "Verblijfsobject"]
        nxt = next((l["href"] for l in d["links"] if l["rel"] == "next"), None)
        if not nxt:
            return out
        d = get(nxt)


def main():
    cells = [(x, y) for x in range(BOUNDS[0], BOUNDS[2], CELL) for y in range(BOUNDS[1], BOUNDS[3], CELL)]
    if not VBO.exists():
        with ThreadPoolExecutor(6) as ex:
            pand = dict(p for part in ex.map(lambda c: vbo_cell(*c), cells) for p in part)
        VBO.write_text(json.dumps(pand))
    pand = json.loads(VBO.read_text())
    with ThreadPoolExecutor(6) as ex:
        parts = list(ex.map(lambda c: adres_cell(*c), cells))
    seen, rows = set(), []
    for a in (a for p in parts for a in p):
        k = (a["identificatie"], a["adresseerbaar_object_identificatie"])
        if k in seen:
            continue
        seen.add(k)
        rows.append(dict(openbare_ruimte=a["openbare_ruimte_naam"], huisnummer=int(a["huisnummer"]),
                         huisletter=a["huisletter"] or "", toevoeging=a["toevoeging"] or "", postcode=a["postcode"],
                         verblijfsobject=a["adresseerbaar_object_identificatie"],
                         pandidentificatie=pand.get(a["adresseerbaar_object_identificatie"])))
    Path("data/raw/addresses.json").write_text(json.dumps(rows, ensure_ascii=False))
    print(len(pand), "verblijfsobjecten;", len(rows), "addresses,", sum(not r["pandidentificatie"] for r in rows),
          "without a pand")


if __name__ == "__main__":
    main()
