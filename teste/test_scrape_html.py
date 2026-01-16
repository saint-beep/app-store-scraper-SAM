import requests
import json
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
}

def extrage_json_ld(soup):
    script = soup.find('script', {'type': 'application/ld+json'})
    if script:
        try:
            return json.loads(script.string)
        except:
            return None
    return None

def extrage_meta_tags(soup):
    data = {}
    for prop in ['og:title', 'og:description', 'og:image']:
        tag = soup.find('meta', {'property': prop})
        if tag and tag.get('content'):
            data[prop] = tag['content']
    return data

def test_app(url):
    print(f"\nURL: {url}")
    print("-" * 50)
    
    response = requests.get(url, headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"HTML size: {len(response.text)} caractere")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # JSON-LD
    print("\n[JSON-LD]")
    json_ld = extrage_json_ld(soup)
    if json_ld:
        print(f"  name: {json_ld.get('name')}")
        print(f"  applicationCategory: {json_ld.get('applicationCategory')}")
        print(f"  operatingSystem: {json_ld.get('operatingSystem')}")
        if 'offers' in json_ld:
            print(f"  price: {json_ld['offers'].get('price')} {json_ld['offers'].get('priceCurrency')}")
        if 'aggregateRating' in json_ld:
            print(f"  ratingValue: {json_ld['aggregateRating'].get('ratingValue')}")
            print(f"  reviewCount: {json_ld['aggregateRating'].get('reviewCount')}")
    else:
        print("  Nu exista")
    
    # meta tags
    print("\n[Meta Tags]")
    meta = extrage_meta_tags(soup)
    for k, v in meta.items():
        print(f"  {k}: {v[:60]}..." if len(v) > 60 else f"  {k}: {v}")
    
    # HTML direct
    print("\n[HTML Direct]")
    h1 = soup.find('h1')
    print(f"  h1: {h1.text.strip() if h1 else 'Nu exista'}")
    
    scripts = len(soup.find_all('script'))
    print(f"  nr. scripturi: {scripts}")

# Teste
print("=" * 50)
print("TEST EXTRAGERE DATE DIN HTML")
print("=" * 50)

test_app("https://apps.apple.com/us/app/instagram/id389801252")