# Ancient Ways Atlas — Export Package

**Generated:** 2026-10-13 · **Editor:** Laurie (laurie@playnicedigital.com)
**For:** the Wabash cartographer **and** the Hilltowns (Westerlo, NY) cartographer

This package carries **257 routes and nodes** — the continental Ancient-Ways
layer built this cycle: the full Indiana core, the Great Lakes / Old Northwest
portages and trails, the Northeast trunks, and the **complete 131-path Wallace
*Indian Paths of Pennsylvania* corpus**, all page-verified against the book.

---

## ⚠️ READ FIRST — THIS IS A MERGE, NOT A REPLACE

**Do not overwrite your existing ways layer with this file.**

These 257 features **do not contain** the ~560 global routes already in the
guide's `data/layers/ways_layer_v169-B169.json`. This is an *additive* layer.
If you drop it in as a replacement you will delete 560 existing routes.

**Correct ingest:**
1. **Append** these routes to the existing collection — do not swap the file.
2. **Check for ID collisions first.** All IDs here are namespaced
   (`TR-`, `TRC-`, `PA-`, `WW-`, `RS-`, `VL-`, `LM-`, `AN-`). Confirm none of
   these already exist in your layer. If any do, rename *these* (they are the
   newcomers), never the incumbents.
3. The incumbent 560-route layer remains the master for everything it already
   covers; this layer only *adds* reach (continental trails + the PA corpus).

If a corridor here duplicates a route you already hold with tighter geometry or
better-dated nodes, **keep yours** and treat this one as a cross-reference —
these are deliberately flagged by tier (see below) so you can tell page-verified
geometry from schematic corridors at a glance.

---

## Files

| File | What it is |
|---|---|
| `wabash_ways_atlas.geojson` | **Authoritative source.** 257 features, WGS84 lon/lat, region-tagged. Ingest from this. |
| `wabash_ways_atlas.csv` | Same records, flat — for spreadsheet QA and eyeballing. |
| `ways_layer_NA_draft.json` | **DRAFT convenience** in the guide's ways-layer spirit (class/tier/era/group/geom_type/coordinates/note). Field names are best-effort — **verify against `WAYS_data_dictionary.md` and the `emit_ways_layer()` parser before ingest.** |
| `ancient_ways_atlas.html` | Self-contained offline viewer (tile-less SVG map, pan/zoom, filters, click-for-detail). Open in any browser; no network needed. |

---

## Field mapping (geojson → guide ways-layer)

| Guide field | Comes from (geojson) | Notes |
|---|---|---|
| `name` | `properties.name` | verbatim |
| `class` | `properties.ttype` / `category` | see class list below |
| `tier` (A/B/C) | `properties.confidence` | mapping below |
| `era` | `properties.era` where present | aboriginal / military / settler-road / removal |
| `group` | `properties.region` | Indiana & Ohio Valley / Great Lakes / Old Northwest / Northeast |
| `note` | `properties.description` + `source` + `confidence` | concatenate for provenance |
| geometry | `geometry.coordinates` | LineString = polyline, Point = node |

The `ways_layer_NA_draft.json` already applies this mapping — but it is a
**draft**; the geojson is authoritative, so re-derive from it if the field names
don't match your parser.

---

## Confidence → tier

Two-tier confidence, collapsed to the guide's A/B/C:

- **Tier A — page-verified (129 routes).** Geometry traced from a named primary
  page: Wallace's per-path pages (PA corpus), Wilson 1919, Hulbert, Hinsdale.
  `confidence` reads `… (Wallace page-verified)`, `located`, or `high`.
- **Tier B — corridor (57 routes).** Route corridor is documented; the drawn
  line follows named anchor points but the exact channel is interpolated.
  `confidence` = `corridor`.
- **Tier C — approximate (71 routes).** City-to-city or schematic placement;
  shape is indicative, not surveyed. `confidence` = `approx*`, `located-approx`.

**Nothing here is a silent guess.** If a Wallace key-map sketch disagreed with
its detail page, the detail page won and the sketch was discarded — a dozen such
corrections were made this cycle (French Creek, Great Path, Great Island, Great
Minquas, Great Warriors, Cayahaga, Catawba, Delaware, Tulpehocken, Tioga,
Paxtang, Pechoquealin, Penns Creek, Tuscarora, Virginia).

---

## What's inside (counts)

**By region** — Indiana & Ohio Valley 88 · Great Lakes / Old Northwest 18 · Northeast 151
**By geometry** — 197 lines · 60 nodes
**By tier** — A 129 · B 57 · C 71

**By class** — indian-path 131 · indian-trace 37 · portage 19 · landmark 16 ·
waterway 12 · reserve 11 · pioneer-road/trace 7 · settlement/village 4 ·
military-road 3 · anchor 3 · bison-and-native-trace 2 · wagon-road 2 · plus
salt-route, removal-route, state-road, road (1 each).

**ID blocks** — `PA-` 145 (131 paths + portages + appendix roads) ·
`TR-` 64 + `TRC-` 2 (Indiana → continental traces) · `LM-` 16 landmarks ·
`WW-` 12 waterways · `RS-` 11 reserves · `VL-` 4 villages · `AN-` 3 anchors.

---

## Provenance (primary sources)

- **Paul A. W. Wallace, *Indian Paths of Pennsylvania* (1965)** — all 131 paths,
  page-verified against the full-book screenshot campaign (Oct 9–12). This is the
  most complete digital rendering of that corpus I'm aware of.
- **George R. Wilson, *Early Indiana Trails and Surveys* (1919)** — Indiana core.
- **Archer B. Hulbert, *Historic Highways of America*** (V1/V2/V7/V8) — Great
  Lakes & Old Northwest portages and thoroughfares.
- **W. B. Hinsdale, *Archaeological Atlas of Michigan*** — Michigan trails.
- **Baker, *St. Joseph–Kankakee Portage*** — the South Bend carrying-place.
- Dunn (placename glossary), La Salle 1679 portage accounts, IN.gov history blog.

---

## Per-guide notes

### Wabash cartographer
- **67 features fall within ~150 km of Prophetstown** — the Indiana core lights up
  directly. Footprint-connecting traces: the Strawtown/Lafayette Trace
  (Tecumseh's Anderson→Prophetstown route), the Ouiatanon hub spokes, the
  Wabash–Maumee portage at Kekionga, Buffalo Trace (its real `TR-001`).
- The battlefield/river georeference was **corrected this cycle**: monument =
  `(-86.8444, 40.5062)` (was ~1.2 km too far east); rivers re-anchored to the
  real confluence at Prophetstown `(-86.8333, 40.5000)`. See the Burnett's Creek
  cross-reference for the QA that caught it.

### Hilltowns cartographer (Westerlo, NY)
- **~37 features fall within ~250 km of Westerlo** — the Northeast corpus reaches
  you via the northern-tier PA paths and the trunk routes: the **Iroquois Trail
  (Great Central Trail)** `TR-062`, the **Old/New Connecticut Paths**
  `TR-063/064`, and the Susquehanna-to-Hudson paths (Minisink, Wyalusing,
  Towanda/Genesee Road, Sheshequin, Tioga).
- These are the *approach corridors* to the Catskill/Hudson country, not
  Westerlo-local paths yet — most are tier B/C at your latitude. A dedicated
  NY / Catskill / Hudson pull (Beauchamp, Morgan's *League of the Iroquois*) is
  the natural next batch if you want page-verified Hilltowns-local geometry.

---

## Known limits / honest caveats

- Continental trunk routes (TR-062..067) are **corridor-grade**, not page-traced.
- `ways_layer_NA_draft.json` is a **draft** — field names unverified against the
  live parser. Trust the geojson.
- Portage nodes approximate the carry; put a modern topo under them before you
  publish a precise channel.
- This layer is **additive**. Re-read the merge warning at the top before ingest.
