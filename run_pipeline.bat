@echo off
echo Starting Signals Platform Data Pipeline...

call venv\Scripts\activate

echo [1/3] Ingesting E-Commerce Data...
python ingestion/fetch_olist.py

echo [2/3] Ingesting Financial Markets & GitHub Activity...
python ingestion/fetch_markets.py
python ingestion/fetch_github.py

echo [3/3] Ingesting Quantified Self (Spotify) Data...
python ingestion/fetch_spotify.py

echo Pipeline Execution Complete!
pause