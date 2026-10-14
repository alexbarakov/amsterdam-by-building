"""Fetch São Paulo's raw inputs from GeoSampa (Prefeitura de São Paulo) into data-sp/raw/.

  IPTU register     every taxed property: SQL key, construction year, floors, use, address (one CSV per year)
  Edificação        building outlines with heights, one shapefile per district (SIRGAS 2000 / UTM 23S)
  Lotes             fiscal lots with their SQL key, one GeoPackage per district
  WFS layers        district boundaries, water bodies, street segments

The download portal has no public links; its own page asks a PageMethod for each folder and opens
downloadArquivo.aspx with the file's path, which is what this script does.
"""
import json
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote

import requests

from .area import DISTRICTS

RAW = Path("data-sp/raw")
# The portal answers unfamiliar user agents with a bot-check page.
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/141.0"}
LIST = "https://geosampa.prefeitura.sp.gov.br/PaginasPublicas/_SBC.aspx/pesquisaArquivos"
GET = "https://download.geosampa.prefeitura.sp.gov.br/PaginasPublicas/downloadArquivo.aspx"
WFS = "https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/geoportal/wfs"
IPTU_YEAR = 2026
BUILDINGS = r"06_Habitação e Edificação\Edificação\Shapefile"
LOTS = r"12_Cadastro\Lotes\GPKG_ZIP"


def files(folder):
    r = requests.post(LIST, data=json.dumps({"pNomePasta": folder}), timeout=60,
                      headers={**UA, "Content-Type": "application/json; charset=utf-8"})
    return [f for f in r.json()["d"].split("|") if f]


def download(folder, name, out):
    if out.exists():
        return
    kind = folder.rsplit("\\", 1)[1]
    # The server reads the path as Latin-1 ('Habitação'); UTF-8 gets an error page.
    path = folder + "\\" + name.removesuffix(".zip")
    url = f"{GET}?orig=DownloadCamadas&arq={quote(path, encoding='latin-1')}&arqTipo={quote(kind, encoding='latin-1')}"
    with requests.get(url, headers=UA, timeout=600, stream=True) as r:
        r.raise_for_status()
        tmp = out.with_suffix(".part")
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    if not zipfile.is_zipfile(tmp):
        tmp.unlink()
        raise RuntimeError(f"not a zip: {name}")
    tmp.rename(out)
    print(name, out.stat().st_size // 1024, "KB")


def wfs(layer, out):
    if out.exists():
        return
    r = requests.get(WFS, headers=UA, timeout=600, params={
        "service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": f"geoportal:{layer}",
        "outputFormat": "application/json"})
    r.raise_for_status()
    out.write_bytes(r.content)
    print(layer, len(r.json()["features"]), "features")


def main():
    for d in ("edificacao", "lotes"):
        (RAW / d).mkdir(parents=True, exist_ok=True)
    download(r"12_Cadastro\IPTU_INTER\XLS_CSV", f"IPTU_{IPTU_YEAR}.zip", RAW / f"IPTU_{IPTU_YEAR}.zip")

    wanted = {d.upper() for d in DISTRICTS}
    jobs = [(BUILDINGS, f, RAW / "edificacao" / f) for f in files(BUILDINGS)
            if f.removeprefix("SHP_edificacao_").removesuffix(".zip") in wanted]
    # Lot files carry a district number: SIRGAS_GPKG_LOTES_78_SE.zip
    jobs += [(LOTS, f, RAW / "lotes" / f) for f in files(LOTS)
             if f.removesuffix(".zip").split("_", 4)[4] in wanted]
    missing = wanted - {Path(j[1]).stem.removeprefix("SHP_edificacao_") for j in jobs if j[0] == BUILDINGS}
    if missing:
        raise SystemExit(f"no building file for {sorted(missing)}")
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda j: download(*j), jobs))

    wfs("distrito_municipal", RAW / "distritos.geojson")
    wfs("massa_d_agua", RAW / "agua.geojson")
    wfs("hidrografia_restituida", RAW / "rios.geojson")


if __name__ == "__main__":
    main()
