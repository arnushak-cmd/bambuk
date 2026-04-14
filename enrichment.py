import csv
import json
import sys
import time
from urllib.request import urlopen, Request

from regex import parse

# nominatim — бесплатный geocoding от osm, но просит не чаще 1 req/sec
# open-meteo — погода, тоже бесплатно и без ключа


def reverse_geocode(lat, lon):
    url = (
        f"https://nominatim.openstreetmap.org/reverse"
        f"?lat={lat}&lon={lon}&format=json&accept-language=en"
    )
    req = Request(url, headers={"User-Agent": "bambuk-homework/1.0"})
    try:
        resp = json.loads(urlopen(req, timeout=5).read())
        addr = resp.get("address", {})
        return {
            "country": addr.get("country", ""),
            "city": addr.get("city") or addr.get("town") or addr.get("village", ""),
        }
    except Exception as e:
        return {"country": f"err: {e}", "city": ""}


def get_weather(lat, lon, date_str):
    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={date_str}&end_date={date_str}"
        f"&daily=temperature_2m_mean,precipitation_sum"
        f"&timezone=auto"
    )
    try:
        resp = json.loads(urlopen(url, timeout=5).read())
        daily = resp.get("daily", {})
        return {
            "temp_c": daily.get("temperature_2m_mean", [None])[0],
            "precip_mm": daily.get("precipitation_sum", [None])[0],
        }
    except Exception:
        return {"temp_c": None, "precip_mm": None}


def to_float(s):
    return float(s.replace(",", "."))


def enrich_row(row, dry_run=False):
    """добавляет country, city, temp_c, precip_mm"""
    lat = to_float(row["lat"])
    lon = to_float(row["lon"])

    if dry_run:
        row.update({"country": "?", "city": "?", "temp_c": "?", "precip_mm": "?"})
        return row

    geo = reverse_geocode(lat, lon)
    row["country"] = geo["country"]
    row["city"] = geo["city"]
    time.sleep(1.1)

    weather = get_weather(lat, lon, row["checkin"])
    row["temp_c"] = weather["temp_c"]
    row["precip_mm"] = weather["precip_mm"]

    return row


# --dry-run чтоб не ждать апи, просто показывает план

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv

    src = "sample_bookings.csv"
    try:
        with open(src) as f:
            lines = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"нет {src}, сначала python generator.py")
        sys.exit(1)

    rows = [parse(l) for l in lines if parse(l)]
    print(f"читаю {len(rows)} строк")
    if dry_run:
        print("(dry-run)\n")

    enriched = []
    for i, row in enumerate(rows, 1):
        r = enrich_row(row, dry_run=dry_run)
        enriched.append(r)
        print(f"  {i:>2}. {row['id']}  {row['checkin']}  -> {r.get('city','?')}, {r.get('temp_c','?')}°C")

    # сохраняем с теми же ; что в оригинале
    out = "enriched_sample.csv"
    out_fields = [
        "id", "ipv6", "paid_at", "lon", "lat", "checkin", "checkout",
        "country", "city", "temp_c", "precip_mm",
    ]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, delimiter=";")
        w.writeheader()
        w.writerows(enriched)

    print(f"\n-> {out}")
