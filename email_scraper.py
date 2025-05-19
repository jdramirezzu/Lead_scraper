import re
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from google_scraper import Business, scrape_google_maps


def extract_emails_from_website(url: str, timeout: int = 10) -> List[str]:
    emails = []
    try:
        response = requests.get(
            url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        found_emails = set(
            re.findall(r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,6}", soup.get_text())
        )

        for email in found_emails:
            if not any(x in email for x in ["example", "test", "noreply", "no-reply"]):
                emails.append(email)

    except Exception as e:
        print(f"Error al visitar {url}: {e}")

    return emails


def calcular_lead_score(business: Business) -> int:
    score = 0
    if business.emails:
        score += 30
    if business.website:
        score += 20
    if business.rating:
        if business.rating >= 4.5:
            score += 30
        elif business.rating >= 3.5:
            score += 20
        else:
            score += 10
    if business.reviews_count:
        if business.reviews_count >= 100:
            score += 20
        elif business.reviews_count >= 20:
            score += 10
    return score


def clasificar_reputacion(business: Business) -> str:
    if business.rating is None:
        return "Desconocida"
    if business.rating >= 4.5:
        return "Excelente"
    elif business.rating >= 3.5:
        return "Buena"
    elif business.rating >= 2.5:
        return "Regular"
    else:
        return "Pobre"


def segmentar_negocio(business: Business) -> str:
    if (
        business.emails
        and business.rating
        and business.rating >= 4
        and (business.reviews_count or 0) > 50
    ):
        return "Listo para contactar"
    elif business.rating and business.rating < 3.5:
        return "Reputación débil"
    elif not business.website or not business.emails:
        return "Oportunidad digital"
    return "General"


if __name__ == "__main__":
    resultados = scrape_google_maps("marketing", "Ontario", max_results=5)

    for negocio in resultados:
        negocio.emails = (
            extract_emails_from_website(negocio.website) if negocio.website else []
        )
        negocio.lead_score = calcular_lead_score(negocio)
        reputacion = clasificar_reputacion(negocio)
        segmento = segmentar_negocio(negocio)

        print("🟢 Negocio encontrado:")
        print(f"  Nombre         : {negocio.name}")
        print(f"  Categoría      : {negocio.category}")
        print(f"  Dirección      : {negocio.address}")
        print(f"  Teléfono       : {negocio.phone}")
        print(f"  Web            : {negocio.website}")
        print(
            f"  Correos        : {', '.join(negocio.emails) if negocio.emails else 'Ninguno encontrado'}"
        )
        print(f"  Calificación   : {negocio.rating}")
        print(f"  Nº de Reseñas  : {negocio.reviews_count}")
        print(f"  Lead Score     : {negocio.lead_score}")
        print(f"  Reputación     : {reputacion}")
        print(f"  Segmento       : {segmento}")
        if negocio.reviews:
            print("  Reseñas        :")
            for r in negocio.reviews:
                print(f"    - {r}")
        print("-" * 40)
