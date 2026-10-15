"""Search index: buildings by name, address or street (web/data/search/).

index.json, loaded on the first use of the search box:
  streets: [name, buildings] for every street (BAG openbare ruimte) with at least one address on a building.
  names: [label, label_nl or null, gid, kind] for named buildings (Wikidata, curated stories) and well-known residents.
{key}.json, one shard per first character of the normalised street name, loaded when a street is chosen or a house
  number typed: {street: [[number, gid], ...]}, numbers in order, each pointing at its building.
gid is the building's row in data/buildings.parquet, the order of the tiles and attrs.bin.
"""
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import pandas as pd

OUT = Path("web/data/search")


def normal(s):
    """As normal() in app.js: lower case, no accents, runs of anything else become one space."""
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def shard(name):
    k = normal(name)[:1]
    return k if k.isalpha() else "0"


def main():
    bag = pd.read_parquet("data/buildings.parquet", columns=["identificatie"]).identificatie.str.slice(-16)
    gid = {k: i for i, k in enumerate(bag)}

    by_street = defaultdict(dict)
    for a in json.load(open("data/raw/addresses.json")):
        g = gid.get(a["pandidentificatie"])
        if g is None or not a["openbare_ruimte"]:
            continue
        num = f'{a["huisnummer"]}{a["huisletter"] or ""}'
        # one entry per number; a plain number keeps its own building over its lettered neighbours
        by_street[a["openbare_ruimte"]].setdefault(num, (g, a["huisnummer"]))

    streets, shards = [], defaultdict(dict)
    for name, nums in sorted(by_street.items()):
        entries = [[num, g] for num, (g, n) in sorted(nums.items(), key=lambda kv: (kv[1][1], kv[0]))]
        shards[shard(name)][name] = entries
        streets.append([name, len({g for _, g in entries})])

    names, seen = [], set()

    def add(label, label_nl, g, kind):
        if not label or g is None:
            return
        # Wikidata labels many listed houses by their address ('Herengracht 476'): the address search finds those
        if kind == "building" and re.search(r"\d", label):
            return
        if label_nl and re.search(r"\d", label_nl):
            label_nl = None
        k = (label.lower(), g)
        if k not in seen:
            seen.add(k)
            names.append([label, label_nl if label_nl and label_nl != label else None, g, kind])

    wiki = json.load(open("web/data/wiki.json"))
    first = pd.read_parquet("data/wiki_index.parquet").groupby("wk").bag.first()
    for k, bg in first.items():
        w = wiki[k] or {}
        add(w.get("label"), w.get("label_nl"), gid.get(bg), "building")
    for L in json.load(open("data/curated.json")):
        for e in L["entries"]:
            add(e["name"], e.get("name_nl"), gid.get(e["bag"]), "building")
    for r in json.load(open("data/residents.json")):
        add(r["person"], None, gid.get(r["bag"]), "person")

    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.json"):
        f.unlink()
    dump = lambda p, o: p.write_text(json.dumps(o, ensure_ascii=False, separators=(",", ":")))
    dump(OUT / "index.json", dict(streets=streets, names=names))
    for k, v in shards.items():
        dump(OUT / f"{k}.json", v)
    sizes = {f.stem: f.stat().st_size // 1024 for f in OUT.glob("*.json")}
    n_addr = sum(len(v) for s in shards.values() for v in s.values())
    print(f"{len(streets)} streets, {n_addr} numbers, {len(names)} names; index {sizes.pop('index')} KB, "
          f"{len(sizes)} shards, largest {max(sizes.values())} KB, total {sum(sizes.values())} KB")


if __name__ == "__main__":
    main()
