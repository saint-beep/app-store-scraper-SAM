import csv
import json
import requests
import time
import os

API_SEARCH = "https://itunes.apple.com/search"
API_LOOKUP = "https://itunes.apple.com/lookup"


def search(term, country="US", limit=50):
    params = {
        "term": term,
        "country": country,
        "media": "software",
        "entity": "software",
        "limit": min(limit, 200)
    }
    
    response = requests.get(API_SEARCH, params=params, timeout=15)
    return response.json().get("results", [])


def parse_app(raw, search_term="", rank=0, country="US"):
    return {
        "country": country.upper(),
        "search_term": search_term,
        "rank": rank,
        "app_id": raw.get("trackId"),
        "name": raw.get("trackName"),
        "developer": raw.get("sellerName") or raw.get("artistName"),
        "genre": raw.get("primaryGenreName"),
        "rating": raw.get("averageUserRating"),
        "rating_count": raw.get("userRatingCount", 0),
        "price": raw.get("price", 0),
        "currency": raw.get("currency"),
        "version": raw.get("version"),
        "size_mb": round(int(raw.get("fileSizeBytes", 0)) / 1024 / 1024, 2),
        "min_os": raw.get("minimumOsVersion"),
        "release_date": raw.get("releaseDate", "")[:10],
        "last_update": raw.get("currentVersionReleaseDate", "")[:10],
        "store_url": raw.get("trackViewUrl")
    }


def export_csv(data, filename):
    if not data:
        print("Nu exista date de exportat.")
        return
    
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Salvat: {filename}")


def export_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Salvat: {filename}")


def main():
    os.system('cls')
    # Input
    term_input = input("\nTermen de cautare (scrie 'term_more' pentru mai multi): ")
    if term_input.lower() == "term_more":
        terms_raw = input("Introdu termenii separati prin virgula: ")
        terms = [t.strip() for t in terms_raw.split(",")]
    else:
        terms = [term_input]
    
    country_input = input("Tara [US] (scrie 'cr_more' pentru mai multe): ").strip() or "US"
    if country_input.lower() == "cr_more":
        countries_raw = input("Introdu tarile separate prin virgula (ex: US, RO, GB): ")
        countries = [c.strip().upper() for c in countries_raw.split(",")]
    else:
        countries = [country_input.upper()]
    
    limit = input("Numar rezultate [50]: ").strip()
    limit = int(limit) if limit else 50
    
    format_output = input("Format export (csv/json/both) [csv]: ").strip() or "csv"
    filename = input("Nume fisier [results]: ").strip() or "results"
    
    data = []
    for country in countries:
        for term in terms:
            print(f"\nCautare '{term}' in {country}...")
            results = search(term, country, limit)
            print(f"Gasite: {len(results)} aplicatii")
            
            for i, raw in enumerate(results, start=1):
                parsed = parse_app(raw, term, i, country)
                data.append(parsed)
            
            time.sleep(0.5)  # pauza intre cereri
    
    # Afisare primele 5
    print("\nPrimele 5 rezultate:")
    print("-" * 50)
    for app in data[:5]:
        print(f"{app['rank']}. {app['name']} - {app['developer']} - Rating: {app['rating']}")
    
    print(f"\nTotal: {len(data)} aplicatii")
    
    # Export
    if format_output in ["csv", "both"]:
        export_csv(data, f"{filename}.csv")
    
    if format_output in ["json", "both"]:
        export_json(data, f"{filename}.json")

if __name__ == "__main__":
    main()
