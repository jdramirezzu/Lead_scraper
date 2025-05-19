from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from email_scraper import (
    extract_emails_from_website,
    calcular_lead_score,
    clasificar_reputacion,
    segmentar_negocio,
)
from google_scraper import Business
from typing import List
import subprocess
import json
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/scrape", response_model=List[Business])
def scrape_endpoint(
    query: str = Query(...), location: str = Query(...), max_results: int = 5
):
    # Ruta al script que ejecuta el scraping y guarda el resultado como JSON
    temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    temp_json.close()

    subprocess.run(
        ["python", "run_scraper.py", query, location, str(max_results), temp_json.name],
        check=True,
    )

    with open(temp_json.name, "r", encoding="utf-8") as f:
        datos = json.load(f)

    os.remove(temp_json.name)

    resultados = [Business(**item) for item in datos]

    for negocio in resultados:
        negocio.emails = (
            extract_emails_from_website(negocio.website) if negocio.website else []
        )
        negocio.lead_score = calcular_lead_score(negocio)
        negocio.reputacion = clasificar_reputacion(negocio)
        negocio.segmento = segmentar_negocio(negocio)

    return resultados
