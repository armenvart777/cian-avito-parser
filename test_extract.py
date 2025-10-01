"""Тест извлечения данных из Авито HTML — финальная проверка."""
from curl_cffi.requests import Session
import re, json, html as html_mod

proxy_list = [
    "http://py38todw8o-mobile-country-RU-state-1496745-city-1496747-hold-query:IdaT1ciAUdk50dYX@185.132.133.7:443",
    "http://py38todw8o-mobile-country-RU-state-498671-city-532664-hold-query:IdaT1ciAUdk50dYX@190.2.142.241:443",
    "http://py38todw8o-mobile-country-RU-state-1508290-city-1508291-hold-query:IdaT1ciAUdk50dYX@190.2.155.93:443",
    "http://py38todw8o-mobile-country-RU-state-1496152-city-1496153-hold-query:IdaT1ciAUdk50dYX@62.112.8.229:443",
]
r = None
for p in proxy_list:
    try:
        s = Session(impersonate="chrome123")
        r = s.get("https://www.avito.ru/voronezh/kvartiry/prodam-ASgBAgICAUSSA8YQ?user=1&s=104", proxies={"http": p, "https": p}, timeout=60)
        if r.status_code == 200:
            print(f"Proxy OK: {p.split('@')[1]}")
            break
    except Exception as e:
        print(f"Proxy failed {p.split('@')[1]}: {e}")
        continue
if r is None or r.status_code != 200:
    print("All proxies failed")
    import sys; sys.exit(1)

html_text = r.text
print(f"status={r.status_code}, len={len(html_text)}")

# Extract from data-mfe-state
mfe_pattern = re.compile(r'<script\s+type="mime/invalid"\s+data-mfe-state="true"[^>]*>(.*?)</script>', re.DOTALL)
for m in mfe_pattern.finditer(html_text):
    raw = m.group(1)
    if len(raw) < 1000:
        continue
    decoded = html_mod.unescape(raw)
    data = json.loads(decoded)

    # Navigate to items
    items = data.get("state", {}).get("data", {}).get("catalog", {}).get("items", [])
    print(f"\nItems found: {len(items)}")

    # Show first 3 items
    for i, item in enumerate(items[:3]):
        print(f"\n--- Item #{i} ---")
        print(f"  id: {item.get('id')}")
        print(f"  title: {item.get('title', '')[:80]}")
        print(f"  urlPath: {item.get('urlPath', '')[:80]}")
        print(f"  categoryId: {item.get('categoryId')}")

        # Price
        pd = item.get("priceDetailed", {})
        print(f"  priceDetailed: {json.dumps(pd, ensure_ascii=False)[:200]}")

        # Address
        addr = item.get("addressDetailed", {})
        print(f"  addressDetailed: {json.dumps(addr, ensure_ascii=False)[:200]}")

        loc = item.get("location", {})
        print(f"  location: {json.dumps(loc, ensure_ascii=False)[:200]}")

        # Description
        desc = item.get("description", "")
        print(f"  description: {desc[:100]}")

        # All top-level keys
        print(f"  ALL KEYS: {list(item.keys())}")

    break
