# Weather stations (xmACIS2 daily listings, NOAA GHCN-Daily via NRCC)

One CSV per station, the xmACIS2 "Daily Data Listing" export (Date, MaxT, MinT, AvgT, precip, snow,
depth, xmACIS's own HDD/CDD/GDD and normals/departures). `build.py` turns each into per-year
cumulative degree days for the Signs + Signals page (`site/station_dd.js`).

**Register stations in `config/place.json` → `weather.stations`** (v1, 2026-10-06 — no longer in build.py):

```json
{"slug": "lafayette_8s", "name": "Lafayette 8 S (co-op) · Tippecanoe Co.", "elev_ft": 650,
 "active": true, "daily": true, "lat": 40.37, "lng": -86.91}
```

- `slug` = the CSV's file name without `.csv`.
- `daily: true` ships raw daily highs/lows for the year charts — continuous records only (it costs ~1/3 of the file per station).
- `lat`/`lng` only matter for a CLOSED station with daily temps: the Signals chart draws a modeled current-year line (ERA5 at that point, dashed) beside its history. Omit otherwise.
- Elevation to the nearest ~50 ft from the xmACIS station metadata; say "elev. approx." in the name if it is a guess.

How to find stations for a new region: xmACIS2 (`xmacis.rcc-acis.org`) → Station Data → "Daily data listing" → pick stations within ~30 mi of the centre (co-op, CoCoRaHS, first-order), full period of record, CSV. Phase 4 of the brief.

Empty for the Navigators Guide as of v1.
