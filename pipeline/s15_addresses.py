"""One address per building for its card (web/data/addr/<k>.json).

BAG gives every address (verblijfsobject) the building (pand) it is in. A building with several addresses shows the
lowest number on its main street, the street with most of its addresses, and how many more it has: 'Herengracht 476'
or 'Kaapstadweg 36A' with 'and 3 more'. Shards of 4,096 buildings in gid order, loaded when a card needs one:
  [[address, more], ...] with null for a building without an address (sheds, bridges, most outbuildings).
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

OUT = Path("web/data/addr")
SHARD = 4096


def main():
    bag = pd.read_parquet("data/buildings.parquet", columns=["identificatie"]).identificatie.str.slice(-16)
    gid = {k: i for i, k in enumerate(bag)}
    per = defaultdict(set)
    for a in json.load(open("data/raw/addresses.json")):
        g = gid.get(a["pandidentificatie"])
        if g is None or not a["openbare_ruimte"]:
            continue
        per[g].add((a["openbare_ruimte"], a["huisnummer"], a["huisletter"] or ""))

    rows = [None] * len(bag)
    for g, addrs in per.items():
        street = Counter(s for s, _, _ in addrs).most_common(1)[0][0]
        n, letter = min((n, l) for s, n, l in addrs if s == street)
        rows[g] = [f"{street} {n}{letter}", len(addrs) - 1]

    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.json"):
        f.unlink()
    for k in range(0, len(rows), SHARD):
        (OUT / f"{k // SHARD}.json").write_text(json.dumps(rows[k:k + SHARD], ensure_ascii=False, separators=(",", ":")))
    have = sum(r is not None for r in rows)
    print(f"{have:,} of {len(rows):,} buildings have an address;",
          sum(f.stat().st_size for f in OUT.glob("*.json")) // 1024, "KB in", len(list(OUT.glob("*.json"))), "shards")


if __name__ == "__main__":
    main()
