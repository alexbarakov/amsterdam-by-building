"""The ontology graph (web/data/graph.json): people, events and organisations linked to buildings by checked texts.

Texts: stories of the curated layers, 'Did you know' facts and residents' quotes. A link keeps the text as evidence,
with its source. Residents (s09) join as people of their own. A building node carries its name and position, so the
graph page can say where it is (buildings of one name are one place) and the map can fly there.
"""
import json
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd

from .s03_tiles import DAM as ORIGIN
from .ontology import ENTITIES, PERSON

RESIDENT_MIN_LINKS = 15


def main():
    layers = {L["id"]: L for L in json.load(open("web/data/layers.json"))}
    b = gpd.read_parquet("data/buildings.parquet", columns=["identificatie", "year", "geometry"])
    b["bag"] = b.identificatie.str.slice(-16)
    c = b.geometry.centroid
    where = {k: (round(x - ORIGIN[0], 1), round(-(y - ORIGIN[1]), 1), int(yr))
             for k, x, y, yr in zip(b.bag, c.x, c.y, b.year)}

    # Texts about buildings: (bag, building name, English, Dutch, source, where the text comes from)
    texts = []
    # Dutch stories live in the layer notes; a curated layer may be a group of a bigger one (the world layer).
    nl_of = {(b, n["story"]): n.get("story_nl") for L in layers.values() for b, n in L.get("notes", {}).items()
             if n.get("story")}
    for L in json.load(open("data/curated.json")):
        for e in L["entries"]:
            texts.append((e["bag"], e["name"], e["story"], nl_of.get((e["bag"], e["story"])), e["source"],
                          layers.get(L["id"], {}).get("title", L["title"])))
    # A building with several names in the stories (one pand holds the Waalse Kerk and part of the Prinsenhof) shows
    # them all; a name that only repeats another with a gloss ("Koornbeurs" / "Vleeshal (Koornbeurs)") is dropped.
    by_bag = {}
    for t in texts:
        by_bag.setdefault(t[0], []).append(t[1])
    names = {}
    for bag, ns in by_bag.items():
        ns = list(dict.fromkeys(ns))
        keep = [n for n in ns if not any(m != n and (n in m or m.split(" (")[0] == n.split(" (")[0] and len(m) < len(n))
                                         for m in ns)]
        names[bag] = " / ".join(keep)
    for bag, f in json.load(open("web/data/facts.json")).items():
        texts.append((bag, names.get(bag), f["en"], f["nl"], f["source"], "Did you know"))

    nodes, links = [], []
    for eid, kind, en, nl, years, pattern in ENTITIES:
        rx = re.compile(pattern)
        seen = set()
        for bag, name, story, story_nl, source, origin in texts:
            if bag in where and rx.search(story) and (bag, story) not in seen:
                seen.add((bag, story))
                links.append(dict(e=eid, bag=bag, text=story, text_nl=story_nl, source=source, via=origin))
        if seen:
            nodes.append(dict(id=eid, type=kind, label=en, label_nl=nl, years=years))
        else:
            print("no building for", eid)
    have = {n["id"] for n in nodes}

    # Residents: one node per person, linked by the quote that names the address.
    for r in json.load(open("data/residents.json")):
        # Only residents known well beyond the city (Wikipedia in RESIDENT_MIN_LINKS languages or more), or one
        # who is already an entity, so the graph stays readable.
        if r["bag"] not in where or (r["links"] < RESIDENT_MIN_LINKS and not any(
                e[1] == PERSON and re.search(e[5], r["person"]) for e in ENTITIES)):
            continue
        # A resident who is already an entity (Vermeer, Agneta Matthes) joins that node.
        known = next((e for e in ENTITIES if e[1] == PERSON and re.search(e[5], r["person"])), None)
        rid = known[0] if known else "res:" + r["wikidata"].rsplit("/", 1)[1]
        if not known and not any(n["id"] == rid for n in nodes):
            years = "–".join(x for x in (r["born"], r["died"]) if x)
            nodes.append(dict(id=rid, type=PERSON, label=r["person"], label_nl=r["person"], years=years,
                              desc=r.get("desc"), resident=True))
        if known and rid not in have:
            continue
        links.append(dict(e=rid, bag=r["bag"], text=r["quote"], text_nl=r["quote"], source=r["url"], via="Who lived here"))

    # Places: the buildings of one name (a hofje of eight houses, a church of two panden) become one node.
    wiki = json.load(open("web/data/wiki.json"))
    wk = pd.read_parquet("data/wiki_index.parquet").set_index("bag").wk
    addr = {}
    for r in json.load(open("data/residents.json")):
        addr.setdefault(r["bag"], r["address"] or r["person"])
    places, place_of = {}, {}
    for bag in sorted({l["bag"] for l in links}):
        w = wiki[wk[bag]] if bag in wk.index else {}
        name = names.get(bag) or (w.get("label") if w else None) or addr.get(bag) or bag
        pid = "p:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        p = places.setdefault(pid, dict(name=name, bags=[], year=9999, photo=None, _xz=[]))
        x, z, year = where[bag]
        p["bags"].append(bag)
        p["_xz"].append((x, z))
        p["year"] = min(p["year"], year)
        p["photo"] = p["photo"] or ((w.get("image") or {}).get("thumb") if w else None)
        place_of[bag] = pid
    for p in places.values():
        xz = p.pop("_xz")
        p["x"], p["z"] = round(sum(a for a, _ in xz) / len(xz), 1), round(sum(b for _, b in xz) / len(xz), 1)
    merged = {}
    for l in links:  # one link per entity and place; the texts of its buildings are joined
        k = (l["e"], place_of[l["bag"]])
        m = merged.setdefault(k, dict(e=l["e"], p=k[1], texts=[]))
        t = dict(text=l["text"], text_nl=l["text_nl"], source=l["source"], via=l["via"])
        if t not in m["texts"]:
            m["texts"].append(t)
    links = list(merged.values())
    out = dict(nodes=nodes, places=places, links=links)
    Path("web/data/graph.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    deg = {}
    for l in links:
        deg.setdefault(l["e"], set()).add(l["p"])
    print(len(nodes), "entities,", len(places), "places,", sum(len(p["bags"]) for p in places.values()), "buildings,",
          len(links), "links")
    print(sorted(((len(v), k) for k, v in deg.items()), reverse=True)[:15])


if __name__ == "__main__":
    main()
