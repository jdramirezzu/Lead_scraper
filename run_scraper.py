import sys
import json
from google_scraper import scrape_google_maps

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Uso: python run_scraper.py <query> <location> <max_results> <output_path>"
        )
        sys.exit(1)

    query = sys.argv[1]
    location = sys.argv[2]
    max_results = int(sys.argv[3])
    output_path = sys.argv[4]

    resultados = scrape_google_maps(query, location, max_results)
    data = [r.__dict__ for r in resultados]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
