#!/usr/bin/env python3
"""Fetch 48 h of gridded weather for Mallorca (Open-Meteo), sea state (Open-Meteo Marine) and recent radar
frames (RainViewer), and write a compact JSON for the trip planner page.  Usage: fetch_live.py OUT.json"""
import json, sys, math, io, base64, time, urllib.request, urllib.parse, datetime
from PIL import Image

UA = {"User-Agent": "MallorcaTripPlanner/1.0"}
LON0, LON1, LAT0, LAT1 = 2.30, 3.50, 39.25, 40.00
NX, NY = 7, 5

def get(url, binary=False):
    for i in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
            return data if binary else json.loads(data)
        except Exception as e:
            if i == 3: raise
            time.sleep(2 * (i + 1))

def grid():
    lons = [round(LON0 + (LON1 - LON0) * i / (NX - 1), 3) for i in range(NX)]
    lats = [round(LAT1 - (LAT1 - LAT0) * j / (NY - 1), 3) for j in range(NY)]
    return lons, lats

def forecast(lons, lats):
    pts = [(la, lo) for la in lats for lo in lons]
    q = {"latitude": ",".join(str(p[0]) for p in pts), "longitude": ",".join(str(p[1]) for p in pts),
         "hourly": "temperature_2m,precipitation,cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m,weather_code",
         "forecast_hours": 48, "timezone": "Europe/Madrid", "wind_speed_unit": "kmh"}
    res = get("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(q))
    res = res if isinstance(res, list) else [res]
    times = res[0]["hourly"]["time"]
    out = {"t": times, "temp": [], "rain": [], "cloud": [], "ws": [], "wd": [], "gust": [], "code": []}
    for r in res:
        h = r["hourly"]
        out["temp"].append([round(v) if v is not None else None for v in h["temperature_2m"]])
        out["rain"].append([round(v, 1) if v is not None else None for v in h["precipitation"]])
        out["cloud"].append([round(v) if v is not None else None for v in h["cloud_cover"]])
        out["ws"].append([round(v) if v is not None else None for v in h["wind_speed_10m"]])
        out["wd"].append([round(v) if v is not None else None for v in h["wind_direction_10m"]])
        out["gust"].append([round(v) if v is not None else None for v in h["wind_gusts_10m"]])
        out["code"].append(h["weather_code"])
    return out

SEA = {"Bucht von Alcúdia": (39.83, 3.18), "Bucht von Palma": (39.50, 2.68), "Nordküste (Sóller)": (39.83, 2.62), "Südostküste": (39.40, 3.30)}
def marine():
    q = {"latitude": ",".join(str(v[0]) for v in SEA.values()), "longitude": ",".join(str(v[1]) for v in SEA.values()),
         "hourly": "wave_height,wave_direction,sea_surface_temperature", "forecast_hours": 48, "timezone": "Europe/Madrid"}
    res = get("https://marine-api.open-meteo.com/v1/marine?" + urllib.parse.urlencode(q))
    res = res if isinstance(res, list) else [res]
    out = []
    for (name, (la, lo)), r in zip(SEA.items(), res):
        h = r["hourly"]
        out.append({"n": name, "lat": la, "lon": lo,
                    "wave": [round(v, 1) if v is not None else None for v in h["wave_height"]],
                    "sst": [round(v, 1) if v is not None else None for v in h["sea_surface_temperature"]]})
    return out

def merc(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

def radar():
    meta = get("https://api.rainviewer.com/public/weather-maps.json")
    host, frames = meta["host"], meta["radar"]["past"][-8:]
    Z = 7; n = 2 ** Z
    tx = lambda lon: (lon + 180) / 360 * n
    ty = lambda lat: (1 - merc(lat) / math.pi) / 2 * n
    x0, x1, y0, y1 = tx(LON0), tx(LON1), ty(LAT1), ty(LAT0)
    out = []
    for f in frames:
        canvas = Image.new("RGBA", ((int(x1) - int(x0) + 1) * 256, (int(y1) - int(y0) + 1) * 256))
        for X in range(int(x0), int(x1) + 1):
            for Y in range(int(y0), int(y1) + 1):
                url = f"{host}{f['path']}/256/{Z}/{X}/{Y}/2/1_0.png"
                try:
                    tile = Image.open(io.BytesIO(get(url, binary=True))).convert("RGBA")
                    canvas.paste(tile, ((X - int(x0)) * 256, (Y - int(y0)) * 256))
                except Exception:
                    pass
        box = (round((x0 - int(x0)) * 256), round((y0 - int(y0)) * 256), round((x1 - int(x0)) * 256), round((y1 - int(y0)) * 256))
        crop = canvas.crop(box)
        buf = io.BytesIO(); crop.save(buf, "PNG", optimize=True)
        ts = datetime.datetime.fromtimestamp(f["time"], datetime.timezone.utc).isoformat()
        out.append({"t": ts, "png": base64.b64encode(buf.getvalue()).decode(), "any": crop.getbbox() is not None})
    return out

if __name__ == "__main__":
    lons, lats = grid()
    data = {"made": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes"),
            "bbox": [LON0, LAT0, LON1, LAT1], "lons": lons, "lats": lats}
    data["fc"] = forecast(lons, lats)
    try: data["sea"] = marine()
    except Exception as e: data["sea"] = []; print("marine failed:", e, file=sys.stderr)
    try: data["radar"] = radar()
    except Exception as e: data["radar"] = []; print("radar failed:", e, file=sys.stderr)
    s = json.dumps(data, separators=(",", ":"))
    json.loads(s)
    open(sys.argv[1], "w").write(s.replace(chr(60), chr(92) + "u003c"))
    print("ok", len(s), "bytes,", len(data["fc"]["t"]), "hours,", len(data["radar"]), "radar frames,", sum(f["any"] for f in data["radar"]), "with echoes")
