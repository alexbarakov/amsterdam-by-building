# Amsterdam, building by building

Every building standing in Amsterdam today, 192,000 of them, by age and historical context.
**Live:** https://stop-token.com/lab/amsterdam/

A non-commercial project, made for curiosity and learning. Inspired by Sasha Bogachev's
[Paris, building by building](https://paris.bogachev.fr); the architecture, a data pipeline feeding a three.js city, follows his.

**Want to add a layer?** See [CONTRIBUTING.md](CONTRIBUTING.md). A layer can be a hand-picked list of buildings with a story
each, or a rule over an open dataset.

## How it works

```
open data ──► pipeline/ (Python) ──► web/data/ (binary tiles + JSON) ──► web/ (three.js, no build step)
```

| Step | What it does |
|---|---|
| `s00_fetch_*` | Downloads BGT water, the city's open datasets, energy labels, BAG addresses |
| `s01_load` | 3D BAG tiles → buildings and their LoD 1.3 parts |
| `s02_attributes` | Cleans construction years (placeholders, rounded years, monument register), floors, heights |
| `s03_tiles` | Packs 600 m tiles into 8 bundles, writes per-building attributes and the city config |
| `s04_water` | Water and land polygons |
| `s05_layers` | Resolves every context layer to a bit per building; adds Dutch texts |
| `s06_wiki` | Names, photos and extracts from Wikidata, Wikipedia and Commons |
| `s07_labels` | Street and canal names placed along their outlines |
| `s08_curated` | Checks hand-written stories against Wikipedia and geocodes them |
| `s09_residents` | Finds addresses of well-known residents in Dutch Wikipedia |
| `s10_commons` | Finds more building photos on Commons by address in the file name |
| `s11_facts` | Checks the 'Did you know' facts against Wikipedia |
| `s13_quests` | Resolves the quests (`quests.py`) to buildings and checks every claim |
| `s14_search` | Search index: street names and named buildings, plus every BAG address (`s00_fetch_addresses`) in one file per first letter |
| `s12_archive` | Up to six archive photos per building from the Stadsarchief beeldbank, via the Amsterdam Time Machine knowledge graph |

## Run it

```bash
uv sync
# raw inputs: see the docstrings of s00_* and s01_load (3D BAG tiles, PDOK boundary, RCE and Wikidata exports)
for s in s01_load s02_attributes s05_layers s03_tiles s04_water s06_wiki s07_labels s12_archive s13_quests s14_search; do uv run python -m pipeline.$s; done
python3 -m http.server 8642 --directory web
```

Raw downloads (`data/`) and generated output (`web/data/`) are not in the repository: they are large and rebuilt by the pipeline.

## Data decisions

- **Years.** BAG gives every building a construction year but not always a true one: 729 carry the placeholder 1005,
  and the old centre has ten times more buildings dated 1905 than the years around it. Both are estimated from dated
  neighbours. Round years before 1800 are spread across their rounding step. Where the national monument register (RCE)
  dates a building earlier than BAG, which often records a rebuilding, the register wins (Westerkerk: 1761 → 1627).
- **Stories.** Every hand-written story names its Wikipedia article; `s08_curated` checks that the article contains the
  story's key facts and the address, then geocodes the address to its BAG building. Entries that fail are dropped.
- **Not included.** The last addresses of Holocaust victims: the only dataset linking the Joods Monument to buildings has
  no open licence.

## Licence

Code: MIT (see [LICENSE](LICENSE)). Data keeps the licence of its source: 3D BAG CC BY 4.0; BAG, BGT, RCE, Wikidata and
most City of Amsterdam data CC0; some city datasets and the street panoramas CC BY 4.0; Wikipedia text CC BY-SA;
Wikimedia Commons photos each under their own licence, credited in the app. Stadsarchief Amsterdam photos are
shown from the archive's image server and link to their records; the app stores only their identifiers.
