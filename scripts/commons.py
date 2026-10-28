import json, sys, urllib.request, urllib.parse, re, time, os
UA = "MallorcaPlanner/1.0 (personal trip planner; lukas) python-urllib"
def get(url):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=30).read()
        except Exception as e:
            if "429" in str(e): time.sleep(3 * (i + 1)); continue
            raise
    raise RuntimeError("rate limited")
def search(q, n=6):
    p = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": "6", "gsrsearch": q + " filetype:bitmap", "gsrlimit": str(n),
         "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": "800"}
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
    out = []
    for pg in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 99)):
        ii = pg["imageinfo"][0]; m = ii.get("extmetadata", {})
        strip = lambda s: re.sub(r"<[^>]+>", "", s or "").strip()
        out.append({"title": pg["title"], "thumb": ii.get("thumburl"), "w": ii.get("width"), "h": ii.get("height"), "mime": ii.get("mime"),
                    "page": ii.get("descriptionurl"), "artist": strip(m.get("Artist", {}).get("value"))[:80], "license": strip(m.get("LicenseShortName", {}).get("value"))})
    return out
if __name__ == "__main__":
    qs = json.load(open(sys.argv[1]))
    res = {}
    for key, q in qs.items():
        try: res[key] = search(q)
        except Exception as e: res[key] = str(e)
        time.sleep(1)
    json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
