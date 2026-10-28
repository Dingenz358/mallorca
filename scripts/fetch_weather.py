#!/usr/bin/env python3
"""Daily forecast for Palma (Open-Meteo) plus sea temperature in the bay of Alcúdia, in the format of
data/weather.json. Days before today keep their previous entry.  Usage: fetch_weather.py data/weather.json"""
import json, sys, time, urllib.request, urllib.parse, datetime, zoneinfo

UA = {"User-Agent": "MallorcaTripPlanner/1.0"}
TZ = zoneinfo.ZoneInfo("Europe/Madrid")
DIRS = ["N", "NNO", "NO", "ONO", "O", "OSO", "SO", "SSO", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
TXT = {0: "Sonnig", 1: "Überwiegend sonnig", 2: "Teils sonnig", 3: "Bedeckt", 45: "Nebel", 48: "Nebel mit Reif",
       51: "Leichter Nieselregen", 53: "Nieselregen", 55: "Starker Nieselregen", 56: "Gefrierender Niesel", 57: "Gefrierender Niesel",
       61: "Leichter Regen", 63: "Regen", 65: "Starker Regen", 66: "Gefrierender Regen", 67: "Gefrierender Regen",
       71: "Leichter Schneefall", 73: "Schneefall", 75: "Starker Schneefall", 77: "Schneegriesel",
       80: "Einzelne Schauer", 81: "Schauer", 82: "Heftige Schauer", 85: "Schneeschauer", 86: "Schneeschauer",
       95: "Gewitter", 96: "Gewitter mit Hagel", 99: "Gewitter mit Hagel"}

def get(url):
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read())
        except Exception:
            if i == 3: raise
            time.sleep(2 * (i + 1))

def describe(code, cloud, rain_mm):
    """Daily code is the most severe of the day (often morning fog), so the look of the day comes from
    the mean cloud cover 9-18 h and the rain amount; the code only names the kind of rain."""
    if rain_mm >= 1 or (code >= 95 and rain_mm > 0.2):
        return "rain", TXT.get(code, "Regen") if code >= 51 else "Regen"
    k, t = ("sun", "Sonnig") if cloud < 20 else ("sun", "Überwiegend sonnig") if cloud < 35 else \
           ("part", "Teils sonnig") if cloud < 65 else ("cloud", "Überwiegend bewölkt") if cloud < 85 else ("cloud", "Bedeckt")
    if rain_mm >= 0.2: t += ", vereinzelt Tropfen"
    return k, t

def strength(kmh):
    return "schwach" if kmh < 12 else "mäßig" if kmh < 29 else "frisch" if kmh < 39 else "stark" if kmh < 50 else "stürmisch"

def main(path):
    try: old = json.load(open(path))
    except Exception: old = {}
    q = {"latitude": 39.57, "longitude": 2.65, "timezone": "Europe/Madrid", "forecast_days": 7, "wind_speed_unit": "kmh",
         "hourly": "cloud_cover", "daily": "precipitation_sum,weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant"}
    res = get("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(q))
    d, hr = res["daily"], res["hourly"]
    cloud = {}
    for t, c in zip(hr["time"], hr["cloud_cover"]):
        if c is not None and 9 <= int(t[11:13]) <= 18: cloud.setdefault(t[:10], []).append(c)
    today = datetime.datetime.now(TZ).date().isoformat()
    days = {k: v for k, v in (old.get("days") or {}).items() if k < today}
    for i, iso in enumerate(d["time"]):
        if d["weather_code"][i] is None or d["temperature_2m_max"][i] is None: continue
        code, ws, gust, wd = d["weather_code"][i], d["wind_speed_10m_max"][i], d["wind_gusts_10m_max"][i], d["wind_direction_10m_dominant"][i]
        cl = cloud.get(iso) or [50]
        k, txt = describe(code, sum(cl) / len(cl), d["precipitation_sum"][i] or 0)
        day = {"k": k, "txt": txt, "max": round(d["temperature_2m_max"][i]), "min": round(d["temperature_2m_min"][i])}
        if d["precipitation_probability_max"][i] is not None: day["rain"] = round(d["precipitation_probability_max"][i])
        if ws is not None and wd is not None:
            day["wind"] = {"dir": DIRS[round(wd / 22.5) % 16], "kmh": round(ws),
                           "txt": strength(ws) + (f", Böen bis {round(gust)} km/h" if gust is not None else "")}
        days[iso] = day
    out = {"asOf": datetime.datetime.now(TZ).strftime("%Y-%m-%dT%H:%M"), "days": dict(sorted(days.items())), "src": "Open-Meteo"}
    try:
        m = get("https://marine-api.open-meteo.com/v1/marine?" + urllib.parse.urlencode(
            {"latitude": 39.83, "longitude": 3.18, "current": "sea_surface_temperature", "timezone": "Europe/Madrid"}))
        sst = m["current"]["sea_surface_temperature"]
        if sst is not None:
            out["sea"] = {"temp": round(sst), "txt": "Bucht von Alcúdia, Modellwert Open-Meteo"}
    except Exception as e:
        print("marine failed:", e, file=sys.stderr)
        if old.get("sea"): out["sea"] = old["sea"]
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
    print("ok", len(out["days"]), "days, asOf", out["asOf"])

if __name__ == "__main__":
    main(sys.argv[1])
