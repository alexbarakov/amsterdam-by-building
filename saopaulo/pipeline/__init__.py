"""LAYRS: São Paulo, the data pipeline. Run from the repository root, in order:

    uv run python -m saopaulo.pipeline.s00_fetch       # GeoSampa: IPTU register, outlines, lots, districts, water
    uv run python -m saopaulo.pipeline.s01_buildings   # outlines + lots + IPTU → data-sp/buildings.parquet
    uv run python -m saopaulo.pipeline.s02_tiles       # tiles, attributes, city.json, water, land, card shards
    uv run python -m saopaulo.pipeline.s03_labels      # street names

The viewer is saopaulo/web/ (saopaulo/run.bat serves it). The districts on the map are listed in area.py.
"""
