import subprocess
import tempfile
import json
import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google_scraper import Business

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/scrape")
def scrape_endpoint(
    query: str = Query(...), location: str = Query(...), max_results: int = 5
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
        tmp_path = tmp_file.name

    try:
        result = subprocess.run(
            ["python", "run_scraper.py", query, location, str(max_results), tmp_path],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al ejecutar scraper:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}",
        )

    with open(tmp_path, "r", encoding="utf-8") as f:
        datos = json.load(f)

    os.remove(tmp_path)
    resultados = [Business(**item) for item in datos]
    return [r.__dict__ for r in resultados]
