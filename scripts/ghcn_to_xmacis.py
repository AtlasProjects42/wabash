#!/usr/bin/env python3
"""Convert an NCEI GHCN-Daily "Climate Data Online" CSV (STATION,NAME,...,DATE,PRCP,SNOW,SNWD,TAVG,TMAX,TMIN,...)
into the station CSV layout build.py expects (Date,MaxT,MinT,AvgT,Precip,Snow,SnowDepth). Handles a file that
holds several stations (splits by STATION id). Assumes CDO "standard units" (temps °F, precip/snow inches) —
warns if the temperatures look metric. Prints a place.json → weather.stations snippet for each station.

Usage:  python3 -I scripts/ghcn_to_xmacis.py <ncei.csv> [more.csv ...] --out data/stations
"""
import csv, sys, re, os, statistics

OUT = "data/stations"
args = [a for a in sys.argv[1:]]
if "--out" in args:
    i = args.index("--out"); OUT = args[i+1]; del args[i:i+2]
inputs = args
if not inputs:
    sys.exit("give one or more NCEI GHCN-Daily CSV paths")
os.makedirs(OUT, exist_ok=True)

def slugify(name):
    s = re.sub(r",?\s+[A-Z]{2}\s+US$", "", name.strip())        # drop ", IN US"
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s

def feet(elev_m):
    try: return round(float(elev_m) * 3.28084)
    except (TypeError, ValueError): return None

stations = {}   # id -> {meta, rows}
for path in inputs:
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid = row.get("STATION", "").strip()
            if not sid: continue
            st = stations.setdefault(sid, {"name": row.get("NAME", sid).strip(),
                                           "lat": row.get("LATITUDE", ""), "lon": row.get("LONGITUDE", ""),
                                           "elev_m": row.get("ELEVATION", ""), "rows": []})
            st["rows"].append(row)

snippets = []
for sid, st in stations.items():
    rows = sorted(st["rows"], key=lambda r: r.get("DATE", ""))
    # unit sanity: standard-units °F maxima sit well under ~130; tenths-°C would be in the hundreds
    tmaxv = [float(r["TMAX"]) for r in rows if r.get("TMAX", "").strip() not in ("", )][:4000]
    metric = bool(tmaxv) and statistics.median([abs(v) for v in tmaxv]) > 200
    slug = slugify(st["name"])
    outp = os.path.join(OUT, slug + ".csv")
    hi = lo = None; real_temp_days = 0
    with open(outp, "w", newline="", encoding="utf-8") as g:
        w = csv.writer(g)
        w.writerow(["Date", "MaxT", "MinT", "AvgT", "Precip", "Snow", "SnowDepth"])
        for r in rows:
            def v(k): x = r.get(k, ""); return x.strip() if x else ""
            mx, mn = v("TMAX"), v("TMIN")
            if mx and mn: real_temp_days += 1
            w.writerow([v("DATE"), mx, mn, v("TAVG"), v("PRCP"), v("SNOW"), v("SNWD")])
    first = rows[0].get("DATE", "")[:10]; last = rows[-1].get("DATE", "")[:10]
    el = feet(st["elev_m"])
    has_daily_temp = real_temp_days > 365        # enough real Max/Min to draw the year-by-year lines
    snippets.append({
        "slug": slug, "id": sid, "name_hint": st["name"], "lat": st["lat"], "lon": st["lon"],
        "elev_ft": el, "span": first + "→" + last, "temp_days": real_temp_days,
        "daily": has_daily_temp, "metric_warning": metric, "out": outp
    })

print("# converted stations:")
for s in snippets:
    print(f"  {s['slug']}  ({s['id']})  {s['span']}  elev {s['elev_ft']}ft  temp-days {s['temp_days']}  -> {s['out']}"
          + ("  [!! TEMPS LOOK METRIC — re-export in standard units]" if s["metric_warning"] else ""))
print("\n# place.json weather.stations entries (edit name/active before use):")
import json as _j
for s in snippets:
    print("  " + _j.dumps({
        "slug": s["slug"],
        "name": re.sub(r",?\s+[A-Z]{2}\s+US$", "", s["name_hint"]).title() + " (co-op) · confirm county",
        "elev_ft": s["elev_ft"], "active": False, "daily": s["daily"],
        "lat": round(float(s["lat"]), 4) if s["lat"] else None,
        "lng": round(float(s["lon"]), 4) if s["lon"] else None
    }, ensure_ascii=False))
