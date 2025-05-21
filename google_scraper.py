from playwright.sync_api import sync_playwright, TimeoutError
from dataclasses import dataclass
from typing import List, Optional
import re


@dataclass
class Business:
    name: str
    category: str
    address: Optional[str]
    website: Optional[str]
    phone: Optional[str]
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    reviews: Optional[List[str]] = None
    emails: Optional[List[str]] = None
    lead_score: Optional[int] = None
    reputacion: Optional[str] = None
    segmento: Optional[str] = None


def scrape_google_maps(
    query: str, location: str, max_results: int = 10
) -> List[Business]:
    search_url = f"https://www.google.com/maps/search/{query}+{location}/"
    businesses = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport=None)
        page = context.new_page()
        page.goto(search_url)
        page.wait_for_timeout(5000)

        listings = page.locator(".hfpxzc")
        count = listings.count()

        if count == 0:
            print("No se encontraron resultados visibles.")
            browser.close()
            return businesses

        print(f"Se encontraron {count} resultados")

        for i in range(min(count, max_results)):
            try:
                item = listings.nth(i)
                item.scroll_into_view_if_needed()
                item.click()
                page.wait_for_timeout(2000)
                page.wait_for_selector("h1.DUwDvf", timeout=5000)

                panel = page.locator(".m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd").nth(0)
                panel.evaluate("e => e.scrollBy(0, 2000)")
                page.wait_for_timeout(1000)

                name = page.locator("h1.DUwDvf").text_content() or ""
                category = page.locator(".DkEaL").first.text_content() or ""
                address = page.locator(".rogA2c .Io6YTe").nth(0).text_content()

                phone, website = None, None
                rating = None
                reviews_count = None
                reviews = []

                try:
                    rating_node = page.locator(".fontDisplayLarge").first
                    if rating_node:
                        rating_text = rating_node.text_content()
                        if rating_text:
                            rating = float(rating_text.replace(",", "."))

                    reviews_node = page.locator("button.GQjSyb span").nth(0)
                    if reviews_node:
                        reviews_text = reviews_node.text_content()
                        match = re.search(
                            r"(\d+[.,]?\d*)",
                            reviews_text.replace(".", "").replace(",", ""),
                        )
                        if match:
                            reviews_count = int(match.group(1))

                    review_elements = page.locator(".MyEned")
                    for r in range(min(3, review_elements.count())):
                        review_text = (
                            review_elements.nth(r).locator(".wiI7pd").text_content()
                        )
                        if review_text:
                            reviews.append(review_text.strip())
                except Exception:
                    pass

                info_sections = page.locator(".UsdlK")
                for j in range(info_sections.count()):
                    section = info_sections.nth(j).text_content()
                    if section and (
                        "+57" in section or section.strip().startswith("+")
                    ):
                        phone = section
                    if info_sections.nth(j).locator("a").count() > 0:
                        href = (
                            info_sections.nth(j)
                            .locator("a")
                            .first.get_attribute("href")
                        )
                        if href and href.startswith("http"):
                            website = href

                if not phone:
                    elements = page.locator(".Io6YTe")
                    for k in range(elements.count()):
                        text = elements.nth(k).text_content().strip()
                        if re.match(
                            r"^(\+57\s?)?[3]\d{9}$", text.replace(" ", "")
                        ) or re.match(r"^3\d{8,9}$", text):
                            phone = text
                            break

                if not website:
                    buttons = page.locator("button")
                    for b in range(buttons.count()):
                        if buttons.nth(b).locator("a").count() > 0:
                            href = (
                                buttons.nth(b).locator("a").first.get_attribute("href")
                            )
                            if href and href.startswith("http"):
                                website = href
                                break

                if not website:
                    link = page.locator("a.CsEnBe[href^='http']")
                    if link.count() > 0:
                        website = link.first.get_attribute("href")

                businesses.append(
                    Business(
                        name,
                        category,
                        address,
                        website,
                        phone,
                        rating,
                        reviews_count,
                        reviews,
                    )
                )
                print(f"Negocio procesado: {name}")
            except Exception as e:
                print(f"Error procesando entrada {i}: {e}")

        browser.close()
    return businesses


if __name__ == "__main__":
    resultados = scrape_google_maps("agencia de marketing", "Bogotá", max_results=5)
    for negocio in resultados:
        print("🟢 Negocio encontrado:")
        print(f"  Nombre         : {negocio.name}")
        print(f"  Categoría      : {negocio.category}")
        print(f"  Dirección      : {negocio.address}")
        print(f"  Teléfono       : {negocio.phone}")
        print(f"  Web            : {negocio.website}")
        print(f"  Calificación   : {negocio.rating}")
        print(f"  Nº de Reseñas  : {negocio.reviews_count}")
        if negocio.reviews:
            print("  Reseñas        :")
            for r in negocio.reviews:
                print(f"    - {r}")
        print("-" * 40)
