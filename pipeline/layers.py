"""Layers: historical contexts, each a set of buildings.

A layer has one or more groups; every group takes one bit of a 64-bit mask per building.
Each source function returns {bag pand id (16 digits): group key}. Layers are listed in
historical order; the viewer shows them in this order.

Sources are fetched by s00_fetch_layers.py. Every one is open (CC0, CC-BY or the open terms of
maps.amsterdam.nl). The last addresses of Holocaust victims are deliberately absent: the only
dataset that links them to buildings (Amsterdam Time Machine / Joods Monument) carries no
licence and asks not to be used without permission.
"""
import csv
import json
import re
from functools import cache

import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point
from pyproj import Transformer

LAYERS = []
RAW = "data/raw/layers"


def layer(**meta):
    def wrap(fn):
        LAYERS.append(dict(meta, source_fn=fn))
        return fn
    return wrap


# ---------- shared lookups ----------

@cache
def buildings() -> gpd.GeoDataFrame:
    b = gpd.read_parquet("data/buildings.parquet", columns=["identificatie", "year", "geometry"])
    b["bag"] = b.identificatie.str.slice(-16)
    return b


@cache
def monuments() -> list[dict]:
    return json.load(open(f"{RAW}/monuments.json"))


@cache
def wikidata_panden() -> dict[str, set[str]]:
    out = {}
    for r in csv.DictReader(open("data/raw/wd_monuments.csv")):
        if r["bag"]:
            out.setdefault(r["nr"], set()).add(r["bag"].zfill(16))
    return out


def panden_of(nr) -> set[str]:
    """Buildings of a monument: the city register's links, else Wikidata's."""
    nr = str(nr)
    own = {p for m in monuments() if str(m["nr"]) == nr for p in m["panden"]}
    return own or wikidata_panden().get(nr, set())


@cache
def monument_panden() -> dict[str, set[str]]:
    out = {}
    for m in monuments():
        out.setdefault(str(m["nr"]), set()).update(m["panden"])
    for nr, ps in wikidata_panden().items():
        if not out.get(nr):
            out[nr] = set(ps)
    return out


@cache
def rce_texts() -> dict[str, str]:
    return {r["nr"]: r["txt"] for r in csv.DictReader(open("data/raw/rce_descriptions.csv"))}


def by_monument(keyed: dict[str, str]) -> dict[str, str]:
    """{monument nr: group} → {pand: group}."""
    mp = monument_panden()
    return {p: g for nr, g in keyed.items() for p in mp.get(str(nr), ())}


def within(polygons: gpd.GeoDataFrame, key_col: str) -> dict[str, str]:
    """Buildings whose centroid falls inside a polygon, keyed by the polygon's group."""
    b = buildings()
    pts = gpd.GeoDataFrame({"bag": b.bag}, geometry=b.geometry.centroid, crs=28992)
    j = gpd.sjoin(pts, polygons[[key_col, "geometry"]], predicate="within")
    return dict(zip(j.bag, j[key_col]))


def near_points(points: gpd.GeoDataFrame, key_col: str, radius: float) -> dict[str, str]:
    """Buildings within `radius` metres of a point (the building at or around an address)."""
    b = buildings()
    j = gpd.sjoin(b[["bag", "geometry"]], points[[key_col, "geometry"]].set_geometry(points.buffer(radius)),
                  predicate="intersects")
    return dict(zip(j.bag, j[key_col]))


def rd(geom_json) -> shapely.Geometry:
    return shapely.geometry.shape(geom_json if isinstance(geom_json, dict) else json.loads(geom_json))


TO_RD = Transformer.from_crs(4326, 28992, always_xy=True)


# ---------- layers ----------

@layer(
    id="gables", section="Architecture", title="Gables", era="1600–1800",
    text=("A canal house shows its age in its top. Stepped gables belong to the early 1600s, neck gables "
          "to the middle of the century, bell gables to the decades around 1700, and the flat cornice "
          "to the 1700s, when the richest owners hid the roof altogether."),
    caveat="Listed houses only: the register of national monuments names the gable of each.",
    source=("Rijksmonumentenregister, RCE", "https://monumentenregister.cultureelerfgoed.nl"),
    groups=[("trap", "Stepped gable"), ("hals", "Neck gable"), ("klok", "Bell gable"), ("lijst", "Cornice")],
)
def gables():
    pats = [("trap", r"trapgevel"), ("hals", r"halsgevel"), ("klok", r"klokgevel"),
            ("lijst", r"rechte lijst|lijstgevel|verhoogde lijst")]
    keyed = {}
    for nr, t in rce_texts().items():
        t = t.lower()
        hits = [(m.start(), k) for k, p in pats for m in [re.search(p, t)] if m]
        if hits:
            keyed[nr] = min(hits)[1]  # the first gable named is the house's own
    return by_monument(keyed)


@layer(
    id="trade", section="Trade and empire", title="Warehouses and the companies", era="1600–1800",
    text=("Amsterdam stored the goods of the world in its houses. Warehouses with shutters, hoisting beams "
          "and stacked loading doors line the Brouwersgracht, the western islands and the Entrepotdok. "
          "The East and West India Companies ran their trade from a handful of buildings that still stand."),
    source=("Rijksmonumentenregister, RCE", "https://monumentenregister.cultureelerfgoed.nl"),
    groups=[("pakhuis", "Warehouse")],
)
def trade():
    keyed = {nr: "pakhuis" for nr, t in rce_texts().items() if re.search(r"\bpakhuis|pakhuizen", t.lower()[:200])}
    return by_monument(keyed)


@layer(
    id="unesco", section="Architecture", title="The canal ring", era="1613–1665",
    text=("The seventeenth-century ring of canals, dug in three phases and built up with merchants' houses, "
          "has been a UNESCO World Heritage site since 2010. The buffer zone around it protects the views."),
    source=("Gemeente Amsterdam, UNESCO zones", "https://api.data.amsterdam.nl/v1/monumenten/unesco/"),
    groups=[("Kernzone", "World Heritage site"), ("Bufferzone", "Buffer zone")],
)
def unesco():
    rows = json.load(open(f"{RAW}/unesco.json"))
    g = gpd.GeoDataFrame({"zone": [r["naam"] for r in rows]}, geometry=[rd(r["geometrie"]) for r in rows], crs=28992)
    core = within(g[g.zone == "Kernzone"], "zone")
    buffer = within(g[g.zone == "Bufferzone"], "zone")
    return {**buffer, **core}


@layer(
    id="faith", section="Faith and community", title="Faith and charity", era="1400–1900",
    text=("Under the Republic, Catholics worshipped in hidden churches behind house fronts, Jews from Portugal "
          "and Central Europe built the city's great synagogues, and wealthy citizens founded hofjes: "
          "courtyards of almshouses for the elderly poor."),
    source=("Gemeente Amsterdam, monuments register", "https://api.data.amsterdam.nl/v1/monumenten/monumenten/"),
    groups=[("worship", "Church"), ("synagogue", "Synagogue"), ("hofje", "Hofje")],
)
def faith():
    keyed = {}
    for m in monuments():
        name = (m["name"] or "").lower()
        if m["function"] == "religie":
            keyed[str(m["nr"])] = "worship"
        if "hofje" in name:
            keyed[str(m["nr"])] = "hofje"
        if "synago" in name:
            keyed[str(m["nr"])] = "synagogue"
    for r in csv.DictReader(open("data/raw/wd_monuments.csv")):
        l = r["label"].lower()
        if "synago" in l:
            keyed[r["nr"]] = "synagogue"
        elif "hofje" in l and r["nr"] not in keyed:
            keyed[r["nr"]] = "hofje"
    return by_monument(keyed)


STYLE_GROUPS = [
    ("neo", "Neo-Renaissance", ("Neo-Renaissance", "Neo-Hollandse Renaissance")),
    ("eclectic", "Eclecticism", ("Eclecticisme",)),
    ("nouveau", "Art Nouveau", ("Art Nouveau",)),
    ("berlage", "Berlage school", ("Berlagianisme", "Rationalisme")),
    ("as", "Amsterdam School", ("Amsterdamse school", "Late Amsterdamse school", "Expressionisme")),
    ("nb", "Nieuwe Bouwen", ("Nieuwe Bouwen", "Functionalisme")),
]


@layer(
    id="styles", section="Architecture", title="Architecture styles", era="1850–1940",
    text=("Between Cuypers' Rijksmuseum and the white blocks of the Nieuwe Bouwen, Amsterdam tried on a style "
          "a generation. Berlage stripped ornament back to brick; his pupils of the Amsterdam School turned brick "
          "into sculpture across the new housing districts."),
    caveat="Listed buildings only: the register tags the style of about one national monument in three.",
    source=("Rijksmonumentenregister, RCE", "https://linkeddata.cultureelerfgoed.nl"),
    groups=[(k, label) for k, label, _ in STYLE_GROUPS],
)
def styles():
    to_group = {s: k for k, _, names in STYLE_GROUPS for s in names}
    keyed = {}
    for r in json.load(open(f"{RAW}/rce_styles.json")):
        g = to_group.get(r["style"])
        if g:
            keyed.setdefault(r["nr"], g)
    return by_monument(keyed)


ARCHITECTS = [
    ("cuypers", "Cuypers", ("Cuypers, P.J.H.", "Cuypers, Ed.", "Cuypers, Ed")),
    ("berlage", "Berlage", ("Berlage, H.P.",)),
    ("vangendt", "Van Gendt", ("Gendt, A.L. van",)),
    ("as", "Amsterdam School architects", ("Klerk, M. de", "Kramer, P.L.", "Westerman, A.J.", "Rutgers, G.J.",
                                           "Boterenbrood, J.G.", "Kruyswijk, C.", "Roodenburgh, J.R.", "Staal, J.F.",
                                           "Gratama, J.", "Kropholler, A.J.", "Wijdeveld, H.Th.", "Epen, J.C. van",
                                           "Croix, J.F. la")),
    ("pw", "Public Works", ("Publieke Werken", "Dienst Publieke Werken", "Publieke Werken, Dienst der")),
    ("nb", "Nieuwe Bouwen", ("Duiker, J.", "Merkelbach, B.", "Eesteren, C. van", "Rietveld, G.Th.", "Stam, M.",
                             "Bijvoet, B.", "Elling, P.")),
]
ORDE_FILES = ["orde_centrum_gebouwen", "orde_gordel_gebouwen", "orde_ring_gebouwen", "orde_aup_gebouwen"]


@cache
def orde() -> gpd.GeoDataFrame:
    frames = []
    for f in ORDE_FILES:
        g = gpd.read_file(f"{RAW}/{f}.geojson").to_crs(28992)
        g.columns = [c.lower() for c in g.columns]
        frames.append(g[["architect", "bouwjaar", "orde", "geometry"]])
    return gpd.GeoDataFrame(pd.concat(frames), crs=28992)


@layer(
    id="architects", section="Architecture", title="Architects", era="1870–1940",
    text=("A few names built much of the city that visitors photograph: Cuypers the Rijksmuseum and Centraal "
          "Station, Van Gendt the Concertgebouw, Berlage the Exchange, the Amsterdam School architects the "
          "housing blocks of Zuid and West, the city's own Public Works its schools and bridges, and the "
          "Nieuwe Bouwen its first glass and concrete."),
    caveat=("From the monuments register and the city's survey of cultural-historical value, which names the "
            "architect for the centre and the districts built up to 1965."),
    source=("Gemeente Amsterdam, monuments register and orde survey", "https://maps.amsterdam.nl/open_geodata/"),
    groups=[(k, label) for k, label, _ in ARCHITECTS],
)
def architects():
    def group_of(name):
        name = name if isinstance(name, str) else ""
        for k, _, names in ARCHITECTS:
            if any(n in name for n in names):
                return k
    out = {}
    for m in monuments():
        k = group_of(m["architect"])
        if k:
            for p in m["panden"]:
                out[p] = (k, {"story": f"Designed by {m['architect']}.", "story_nl": f"Ontworpen door {m['architect']}."})
    o = orde()
    o["k"] = o.architect.map(group_of)
    o = o[o.k.notna()]
    b = buildings()
    pts = gpd.GeoDataFrame({"bag": b.bag}, geometry=b.geometry.centroid, crs=28992)
    j = gpd.sjoin(pts, o, predicate="within")
    for bag, k, a, y in zip(j.bag, j.k, j.architect, j.bouwjaar):
        year = f" ({y})" if str(y).isdigit() and int(y) > 1000 else ""
        out.setdefault(bag, (k, {"story": f"Designed by {a}{year}.", "story_nl": f"Ontworpen door {a}{year}."}))
    return out


@layer(
    id="housing", section="The modern city", title="Housing Act homes", era="1901–1940",
    text=("The Housing Act of 1901 let housing associations build with public money. Within forty years "
          "they had replaced the slums with whole districts of sound workers' homes, and they still own "
          "these blocks today."),
    caveat="Buildings built 1901–1940 in blocks a housing association owns today; some were bought later.",
    source=("AFWC, housing associations' stock 2025", "https://maps.amsterdam.nl/open_geodata/"),
    groups=[("woningwet", "Housing association, built 1901–1940")],
)
def housing():
    g = gpd.read_file(f"{RAW}/social_housing.geojson").to_crs(28992)
    g["k"] = "woningwet"
    hit = within(g, "k")
    years = dict(zip(buildings().bag, buildings().year))
    return {p: k for p, k in hit.items() if 1901 <= years[p] <= 1940}


PLANNED = [
    ("Plan Zuid", "Plan Zuid"), ("Admiralenbuurt", "Admiralenbuurt"), ("Betondorp", "Betondorp"),
    ("Van Eesteren Museum", "Western garden cities"), ("later", "Bijlmermeer, IJplein, Plan Van Gool"),
]
LATER_PLANS = {"IJplein", "Bijlmermuseum", "Plan Van Gool"}  # small: one colour, so the layers fit in 64 bits


@layer(
    id="planned", section="The modern city", title="The planned city", era="1915–1980",
    text=("Twentieth-century Amsterdam grew by plan: Berlage's Plan Zuid, the concrete village of Betondorp, "
          "Van Eesteren's garden cities in the west, the honeycomb high-rise of the Bijlmermeer and the "
          "1980s renewal of IJplein. The city now protects each of them as a cityscape."),
    source=("Gemeente Amsterdam, protected cityscapes", "https://api.data.amsterdam.nl/v1/beschermdestadsdorpsgezichten/"),
    groups=[(name, label) for name, label in PLANNED],
)
def planned():
    rows = json.load(open(f"{RAW}/stadsgezichten.json"))
    g = gpd.GeoDataFrame({"naam": [r["naam"] for r in rows]}, geometry=[rd(r["geometry"]) for r in rows], crs=28992)
    g["naam"] = g.naam.map(lambda n: "later" if n in LATER_PLANS else n)
    return within(g[g.naam.isin([n for n, _ in PLANNED])], "naam")


@layer(
    id="war", section="War and occupation", title="Under fire, 1940–1945", era="1940–1945",
    text=("Amsterdam was spared the destruction of Rotterdam, yet bombs, shells and crashing aircraft still "
          "hit hundreds of addresses. The city archive mapped each incident from the reports of the time."),
    caveat="Buildings within 15 m of a recorded incident; some stand on the site of the building that was hit.",
    source=("Stadsarchief Amsterdam, WWII incidents", "https://maps.amsterdam.nl/open_geodata/"),
    groups=[("bomb", "Bombs, shells and gunfire"), ("crash", "Aircraft crash"), ("damage", "Damage nearby")],
)
def war():
    g = gpd.read_file(f"{RAW}/ww2_damage.geojson").to_crs(28992)
    kind = g.Soort.fillna("").str.lower()
    g["k"] = kind.map(lambda s: "crash" if "vliegtuig" in s else "damage" if "omgeving" in s or "schade" in s else "bomb")
    return near_points(g, "k", 15)


@layer(
    id="noord1943", section="War and occupation", title="The raid on Noord, 17 July 1943", era="1943",
    text=("Allied bombers aimed at the Fokker aircraft works in Noord and missed: their bombs fell on the "
          "streets around it and killed 158 people. Buildings near the impacts that date from after the war "
          "mark what had to be rebuilt."),
    caveat="Buildings within 40 m of a recorded impact of that day.",
    source=("Gemeente Amsterdam, wartime impacts", "https://api.data.amsterdam.nl/v1/ontplofbare_oorlogsresten/"),
    groups=[("rebuilt", "Built after 1943"), ("stood", "Standing before 1943")],
)
def noord1943():
    rows = [r for r in json.load(open(f"{RAW}/ww2_impacts.json")) if "RAP_19430717" in (r.get("hyperlink") or r.get("pdf") or "")]
    g = gpd.GeoDataFrame({"k": ["hit"] * len(rows)}, geometry=[rd(r["geometrie"]) for r in rows], crs=28992)
    hit = near_points(g, "k", 40)
    years = dict(zip(buildings().bag, buildings().year))
    return {p: ("rebuilt" if years[p] > 1943 else "stood") for p in hit}


TECHNIQUE = {"Reliëf": "relief", "Schildering": "mural", "Mozaïek": "mosaic", "Sculptuur": "sculpture",
             "Glasappliqué": "glass appliqué", "Sgraffito": "sgraffito", "Baksteenmozaïek": "brick mosaic",
             "Glas, anders": "glass work", "Glas-in-lood": "stained glass", "Glas-in-beton": "glass in concrete"}


@layer(
    id="wallart", section="The modern city", title="Art on the walls", era="1945–1985",
    text=("After the war the city spent a share of every public building's budget on art. Reliefs, mosaics, "
          "murals and glass were built into schools, offices and housing blocks; the city has surveyed them and "
          "ranked the best."),
    source=("Gemeente Amsterdam, wall art survey", "https://maps.amsterdam.nl/wandkunst/"),
    groups=[("wallart", "Wall art")],
)
def wallart():
    g = gpd.read_file(f"{RAW}/wandkunst.geojson").to_crs(28992)
    g["k"] = g.Waardering.map(lambda w: "top" if w == "Top" else "valuable")
    out = {}
    b = buildings()
    for _, r in g.iterrows():
        near = b[b.distance(r.geometry) < 12]
        if near.empty:
            continue
        bag = near.iloc[(near.distance(r.geometry)).argmin()].bag if len(near) > 1 else near.bag.iloc[0]
        tech = TECHNIQUE.get(r.Techniek, (r.Techniek or "work").lower())
        year = f", {r.Jaartal}" if r.Jaartal else ""
        tech_nl = (r.Techniek or "kunstwerk").lower()
        top, top_nl = (" Ranked of top value.", " Gewaardeerd als topstuk.") if r.k == "top" else ("", "")
        out[bag] = ("wallart", {"story": f"“{r.Titel_kunstwerk}”, a {tech} by {r.Kunstenaar}{year}.{top}",
                                "story_nl": f"“{r.Titel_kunstwerk}”, {tech_nl} van {r.Kunstenaar}{year}.{top_nl}"})
    return out


@layer(
    id="arcam", section="The modern city", title="Prize-winning architecture", era="1987–today",
    text=("Every year ARCAM, Amsterdam's architecture centre, nominates the best new buildings in the city for "
          "the Amsterdam Architecture Prize, chosen by a jury and by the public."),
    source=("ARCAM, Amsterdam Architecture Prize", "https://maps.amsterdam.nl/open_geodata/"),
    groups=[("won", "Winner"), ("nominated", "Nominated")],
)
def arcam():
    g = gpd.read_file(f"{RAW}/architectuurprijs_arcam.geojson").to_crs(28992)
    out = {}
    b = buildings()
    for _, r in g.iterrows():
        near = b[b.distance(r.geometry) < 15]
        if near.empty:
            continue
        won = "prijs" in (r.Win_genomineerd or "").lower()
        verdict = {"Vakprijs": "won the jury prize", "Publieksprijs": "won the public prize",
                   "Publieksprijs - Vakprijs": "won both the jury and the public prize"}.get(r.Win_genomineerd, "was nominated")
        story = f"{r.Project} by {r.Architect} {verdict} in {r.Jaar}."
        verdict_nl = {"Vakprijs": "won de vakprijs", "Publieksprijs": "won de publieksprijs",
                      "Publieksprijs - Vakprijs": "won de vak- en de publieksprijs"}.get(r.Win_genomineerd, "werd genomineerd")
        story_nl = f"{r.Project} van {r.Architect} {verdict_nl} in {r.Jaar}."
        for bag in near.bag:
            out[bag] = ("won" if won else "nominated", {"story": story, "story_nl": story_nl})
    return out


@layer(
    id="streetart", section="The modern city", title="Street art", era="1990–today",
    text=("Amsterdam paints its blank walls: portraits of Johan Cruijff and Ramses Shaffy, Eduardo Kobra's Anne Frank, "
          "and dozens of murals commissioned for whole housing blocks in Nieuw-West and Noord. Each work links to "
          "its article or its map entry."),
    caveat="Murals and graffiti with a Wikidata item or an OpenStreetMap entry, placed on the nearest building.",
    source=("Wikidata, Wikipedia and OpenStreetMap", "https://nl.wikipedia.org/wiki/Muurschildering"),
    groups=[("mural", "Murals and street art")],
)
def streetart():
    b = buildings()
    sidx = b.sindex
    to_rd = Transformer.from_crs(4326, 28992, always_xy=True)
    works = {}
    for r in csv.DictReader(open("data/raw/wd_streetart.csv")):
        if r["i"] in works or not r["coord"]:
            continue
        lon, lat = map(float, r["coord"][6:-1].split())
        artist = r["artistLabel"] if r["artistLabel"] and not r["artistLabel"].startswith("http") else ""
        works[r["i"]] = dict(name=r["iLabel"], artist=artist, year=r["inception"][:4], url=r["nl"] or r["i"],
                             at=to_rd.transform(lon, lat), kind="mural")
    osm = json.load(open("data/raw/osm_streetart.json"))["elements"]
    for e in osm:
        t = e["tags"]
        qid = t.get("wikidata")
        if qid and f"http://www.wikidata.org/entity/{qid}" in works:
            continue
        c = e.get("center") or e
        kind = "mural" if t.get("artwork_type") == "mural" else "graffiti"
        name = t.get("name") or ("Mural" if kind == "mural" else "Graffiti")
        works[f"osm{e['id']}"] = dict(name=name, artist=t.get("artist_name", ""), year=t.get("start_date", "")[:4],
                                       url=f"https://www.openstreetmap.org/{e['type']}/{e['id']}",
                                       at=to_rd.transform(c["lon"], c["lat"]), kind=kind)
    out = {}
    for w in works.values():
        pt = Point(w["at"])
        near = b.iloc[sidx.query(pt.buffer(30), predicate="intersects")]
        if near.empty:
            continue
        bag = near.iloc[near.distance(pt).argmin()].bag
        by = f" by {w['artist']}" if w["artist"] else ""
        by_nl = f" van {w['artist']}" if w["artist"] else ""
        year = f", {w['year']}" if w["year"] else ""
        what, what_nl = ("a mural", "muurschildering") if w["kind"] == "mural" else ("street art", "straatkunst")
        out.setdefault(bag, ("mural", {"name": w["name"], "name_nl": w["name"], "source": w["url"],
                                          "story": f"“{w['name']}”, {what}{by}{year}.",
                                          "story_nl": f"“{w['name']}”, {what_nl}{by_nl}{year}."}))
    return out


@layer(
    id="heritage", section="Architecture", title="Protected heritage", era="All periods",
    text=("About one building in twelve is a listed monument: by the State for national significance, "
          "or by the city for local value."),
    source=("Gemeente Amsterdam, monuments register", "https://api.data.amsterdam.nl/v1/monumenten/monumenten/"),
    groups=[("Rijksmonument", "National monument"), ("Gemeentelijk monument", "Municipal monument")],
)
def heritage():
    out = {}
    for m in monuments():
        for p in m["panden"]:
            if m["status"] == "Rijksmonument" or p not in out:
                out[p] = m["status"]
    return out


def _curated_layer(L):
    groups = L.get("groups") or [(L["id"], L["title"])]

    def fn():
        out = {}
        for e in L["entries"]:
            out.setdefault(e["bag"], []).append((e["group"], {"story": e["story"], "source": e["source"], "name": e["name"],
                                                           "address": e["address"]}))
        if L["id"] == "jewish":
            # Synagogues in the monuments register that the curated list does not name.
            for nr, ps in monument_panden().items():
                m = next((m for m in monuments() if str(m["nr"]) == nr), None)
                if m and "synago" in (m["name"] or "").lower():
                    for p in ps:
                        out.setdefault(p, [("community", {"story": f"{m['name']}."})])
        return out

    section = L.get("section") or {"jewish": "Faith and community", "secrets": "Discover"}.get(L["id"], "Trade and empire")
    LAYERS.append(dict(id=L["id"], section=section, title=L["title"], era=L["era"], text=L["intro"],
                       caveat=L.get("caveat"), source=("Wikipedia, per building", "https://www.wikipedia.org"),
                       groups=[tuple(g) for g in groups], source_fn=fn))


# The country layers are too small alone; they become groups of one layer, each with its own colour.
WORLD = ["russia", "britain", "france", "germany", "sephardic", "asia", "atlantic"]
_curated = json.load(open("data/curated.json"))
_world = [L for L in _curated if L["id"] in WORLD]
_curated_layer(dict(
    id="world", title="The world in Amsterdam", era="1586–today",
    intro=("Refugees, merchants, occupiers and colonies tied Amsterdam to the world. Each colour is a country or "
           "a community; every building carries its own story and source."),
    groups=[(L["id"], L["title"]) for L in _world],
    entries=[dict(e, group=L["id"]) for L in _world for e in L["entries"]]))
for _L in _curated:
    if _L["id"] not in WORLD:
        _curated_layer(_L)


# Residents: its own mode in the viewer, not one of the context layers.
def _residents():
    out = {}
    for r in json.load(open("data/residents.json")):
        n = out.setdefault(r["bag"], ("res", {"name": r["person"], "people": []}))[1]
        n["people"].append({k: r[k] for k in ("person", "born", "died", "desc", "quote", "url", "links", "address")})
    return out


LAYERS.append(dict(
    id="residents", section="Discover", title="Who lived here", era="1600–today",
    text=("Painters, writers, scientists and sailors whose Wikipedia biography names the Amsterdam address where "
          "they lived or worked. Pick a name to fly to the house."),
    caveat=("Found automatically in Dutch Wikipedia and matched to today's address; house numbers have sometimes "
            "changed, and some houses were rebuilt since."),
    source=("Dutch Wikipedia, via Wikidata", "https://nl.wikipedia.org"),
    groups=[("res", "Home of a well-known resident")], source_fn=_residents))
