import requests
import time
import statistics
import random

API = "https://itunes.apple.com/search"

SEARCH_TERMS = ["fitness"]
COUNTRIES = ["RO"]

def test_api_rate_limit(num_requests: int = 10000):
    # testare rate limiting
    print(f"Testare Rate Limiting - {num_requests} request-uri")
    print(f"Termeni: {', '.join(SEARCH_TERMS)}")
    print(f"Tari: {', '.join(COUNTRIES)}")
    print("=" * 60)
    
    response_times = []
    errors = []
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })
    
    start_total = time.time()
    
    progress_interval = max(100, num_requests // 50)
    
    for i in range(num_requests):
        term = random.choice(SEARCH_TERMS)
        country = random.choice(COUNTRIES)
        
        start = time.time()
        try:
            r = session.get(API, params={
                "term": term,
                "country": country,
                "media": "software",
                "limit": 10
            }, timeout=15)
            
            elapsed = time.time() - start
            response_times.append(elapsed)
            
            if r.status_code != 200:
                errors.append({
                    "request": i + 1,
                    "status": r.status_code,
                    "time": elapsed
                })
                print(f"  [{i+1}] EROARE - Status: {r.status_code}")
            elif (i + 1) % progress_interval == 0:
                pct = (i + 1) / num_requests * 100
                avg_time = statistics.mean(response_times[-progress_interval:]) * 1000
                print(f"  [{i+1}/{num_requests}] ({pct:.0f}%) OK - avg: {avg_time:.0f}ms - erori: {len(errors)}")
                
        except requests.RequestException as e:
            elapsed = time.time() - start
            errors.append({
                "request": i + 1,
                "error": str(e),
                "time": elapsed
            })
            print(f"  [{i+1}] EXCEPTIE: {e}")
    
    total_time = time.time() - start_total
    
    # raport
    print("\n" + "=" * 60)
    print("REZULTATE TESTARE RATE LIMITING")
    print("=" * 60)
    print(f"Total request-uri:    {num_requests}")
    print(f"Request-uri reușite:  {num_requests - len(errors)}")
    print(f"Erori:                {len(errors)}")
    print(f"Rata succes:          {(num_requests - len(errors)) / num_requests * 100:.2f}%")
    print(f"Timp total:           {total_time:.2f}s ({total_time/60:.1f} minute)")
    print(f"Request-uri/secunda:  {num_requests/total_time:.2f}")
    print("-" * 60)
    print(f"Timp raspuns mediu:   {statistics.mean(response_times)*1000:.0f}ms")
    print(f"Timp raspuns min:     {min(response_times)*1000:.0f}ms")
    print(f"Timp raspuns max:     {max(response_times)*1000:.0f}ms")
    print(f"Deviatie standard:    {statistics.stdev(response_times)*1000:.0f}ms")
    
    sorted_times = sorted(response_times)
    p50 = sorted_times[int(len(sorted_times) * 0.50)] * 1000
    p95 = sorted_times[int(len(sorted_times) * 0.95)] * 1000
    p99 = sorted_times[int(len(sorted_times) * 0.99)] * 1000
    print(f"Percentila 50 (P50):  {p50:.0f}ms")
    print(f"Percentila 95 (P95):  {p95:.0f}ms")
    print(f"Percentila 99 (P99):  {p99:.0f}ms")
    print("=" * 60)
    
    if len(errors) == 0:
        print("\nCONCLUZIE: Nu s-a detectat rate limiting!")
    elif len(errors) / num_requests < 0.01:
        print(f"\nCONCLUZIE: Rate limiting minim ({len(errors)} erori)")
    else:
        print(f"\nATENTIE: {len(errors)} erori detectate!")
        for err in errors[:10]:
            print(f"  - Request #{err['request']}: {err.get('status', err.get('error'))}")


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    test_api_rate_limit(count)
