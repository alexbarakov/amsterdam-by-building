@echo off
rem Serve the São Paulo viewer on http://localhost:8643 and open it in the browser.
rem saopaulo\web\data is not in the repository: build it with the pipeline first (see saopaulo\pipeline\__init__.py).
cd /d "%~dp0"
if not exist web\data\city.json (
  echo web\data is missing: run the pipeline first, see saopaulo\pipeline\__init__.py
  exit /b 1
)
start "" http://localhost:8643/
python -m http.server 8643 --directory web
