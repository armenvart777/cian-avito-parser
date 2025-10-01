"""Проверяем поля дат в объявлениях Авито."""
from curl_cffi.requests import Session
import re, json, html as html_mod
from datetime import datetime

proxy_list = [
    "http://py38todw8o-mobile-country-RU-state-1496745-city-1496747-hold-query:IdaT1ciAUdk50dYX@185.132.133.7:443",
    "http://py38todw8o-mobile-country-RU-state-498671-city-532664-hold-query:IdaT1ciAUdk50dYX@190.2.142.241:443",
    "http://py38todw8o-mobile-country-RU-state-1496152-city-1496153-hold-query:IdaT1ciAUdk50dYX@62.112.8.229:443",
]
r = None
for p in proxy_list:
    try:
        s = Session(impersonate="chrome123")
        r = s.get("https://www.avito.ru/voronezh/kvartiry/prodam-ASgBAgICAUSSA8YQ?user=1&s=104", proxies={"http": p, "https": p}, timeout=60)
        if r.status_code == 200:
            break
    except:
        continue

html_text = r.text
mfe_pattern = re.compile(r'<script\s+type="mime/invalid"\s+data-mfe-state="true"[^>]*>(.*?)</script>', re.DOTALL)
for m in mfe_pattern.finditer(html_text):
    raw = m.group(1)
    if len(raw) < 1000:
        continue
    decoded = html_mod.unescape(raw)
    data = json.loads(decoded)
    items = data.get("state", {}).get("data", {}).get("catalog", {}).get("items", [])
    print(f"Items: {len(items)}")
    for i, item in enumerate(items[:5]):
        print(f"\n--- Item #{i}: {item.get('title', '')[:60]} ---")
        # Все поля с timestamp/date/time
        for key in ["sortTimeStamp", "allowTimeStamp", "jobSeekerUpdateTimeStamp", "turnOffDate", "isNew"]:
            val = item.get(key)
            if val:
                # Попробуем конвертировать timestamp
                if isinstance(val, (int, float)) and val > 1000000000:
                    ts = val / 1000 if val > 9999999999 else val
                    dt = datetime.fromtimestamp(ts)
                    print(f"  {key}: {val} -> {dt}")
                else:
                    print(f"  {key}: {val}")
        # iva может содержать дату
        iva = item.get("iva", {})
        if isinstance(iva, dict):
            for k, v in iva.items():
                if "date" in k.lower() or "time" in k.lower():
                    print(f"  iva.{k}: {v}")
    break
