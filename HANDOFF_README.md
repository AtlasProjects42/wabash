# Ye Olde Navigators Guide — build log and handoff

*A community field guide for the Wabash country around Prophetstown State Park (Battle Ground / Lafayette / West Lafayette, Tippecanoe County, Indiana). Built from the community-field-guide starter kit v1 (the NY Hilltowners atlas, v1013, with its data removed). Editor: Laurie. Atlas assistant: Claude.*

The Hilltowns log this tree descends from is kept beside this file as `HILLTOWNS_HANDOFF_README.md` — its delivery ritual, data rules, pin logic and schema sections still apply; its version history does not.

---

## Where things stand — v6 (2026-10-06)

**Changes since v5:** the **Ancient Ways layer** — the global ancient-routes dataset from Laurie's Ways project (`data/layers/ways_layer_v169-B169.json`, 560 routes, schema v2 — polylines, a different model from the POI point pins) brought in as a toggle grouped with Folklore.
- **New build step** `emit_ways_layer()` in `build/build.py`: reads the newest `data/layers/ways_layer*.json`, pre-builds two GeoJSON FeatureCollections + a per-route notes map → `site/data_ways.js` (`window.WAYS`, ~2 MB). 560 routes → **682 line features** (122 extra are antimeridian splits — segments crossing 180° are broken so no line smears across the globe; verified 0 features span >180°), **5,553 named nodes** (shaping/unnamed nodes dropped). Decisions from Laurie: colour **by class** (7 classes), render **all named nodes** (zoom-thinned: major types — terminus/port/pass/caravanserai/wall-gate/oasis/shrine — at every zoom, the rest from z8, labels from z9), notes from the layer only.
- **New atlas module** (self-contained, end of `index.template.html`): injects an "Ancient Ways" checkbox into `#catsStory` beside Folklore; on first tick fetches `data_ways.js`, adds line layers (land solid, water dashed, colour by class, opacity by confidence tier A/B/C), a node circle layer and a node-label symbol layer, all **beneath the POI pins** so pins stay clickable. Click a line or node → a scrollable popup with the route's class, tier, era, group and full scholarly note. Sensitive routes (14) keep their generalized coordinates and say so in the popup; nothing is re-precised. The base and day/night switches only toggle visibility (never setStyle), so the layer persists across them.
- Build: `BUILD OK — 739 records / 726 mappable`, plus the Ways layer. Headless test ticks the checkbox: `window.WAYS` loads, both layers add and go visible, untick hides them, **0 page errors**. **Not sandbox-verifiable:** the actual line/label rendering (needs map tiles) — confirm on the live site. On the Prophetstown home view only ~6 routes are nearby; it's a global layer, zoom/pan out to see it (said in the checkbox tooltip and the module comment).
- **Not included:** `ways_lore.json` (122 lore entries) was omitted from the export per its data dictionary; the layer's own route notes are what render. Request that file from the Ways chat if the extra lore is wanted later.
- Staged alongside the data for provenance: `data/layers/WAYS_brief_v169.md`, `WAYS_data_dictionary.md`, `ways_routes_index.csv`.

## Where things stand — v5 (2026-10-06)

**Changes since v4:** the **Amtrak/VIA network** from the Hilltowns project (`train_stations_transportation.xlsx`, 751 rows) merged into the Transportation sheet by column name (the source header row carried two stray columns and a VLOOKUP). 679 rows imported with coordinates; **72 rows skipped for having no coordinates** — all VIA Rail flag stops in the Québec/Ontario bush (Anjou, Bima, Club Beaudin…), listed in the build log of this session; they had no coordinates in the source either. The kit's example row (`Hudson Amtrak Station`, Display = No) shadowed the real Hudson row on the existence-guard; example deleted, real row added. 10 Indiana stations present (South Bend, Elkhart, Waterloo, Connersville, Indianapolis, Crawfordsville, Lafayette, Rensselaer, Dyer, Hammond-Whiting). Transportation stays `default_on: false` in the manifest (toggle layer).
- Build: `BUILD OK — 739 records (726 mappable)`; `data.js` 384 KB. 683 warnings = 679 Amtrak preview-image fetches the sandbox can't make — CI will fetch them once and cache (BRIEF §5.1.4 is the real fix: commit `preview-cache.json`). Smoke: 7 pages, 0 errors.
- Tag style in the imported rows is the Hilltowns' ("Train Station; Amtrak; …", two rows lead with "Transportation") — left as imported, per Laurie's "keep the whole network".

## Where things stand — v4 (2026-10-06)

**Changes since v3:** batch 2 — **32 preserves and trails** (`scripts/poi_batch2_2026-10-06.py`). Nineteen pinned: 12 NICHES preserves with trails (Clegg, Granville Sand Barrens/Whistler, Black Rock, Black Rock Barrens, Weiler-Leopold, Mulvey Pond, Howell Woods, Potawatomi Trail, Berkshire-Tarnowski, Frogs' Glory, Fall Creek Gorge, Crow's Grove) and 7 others (Ross Hills Park, Peters Mill Access, Wabash & Erie Canal Park, Martell Forest, Happy Hollow, Trailhead Park). Thirteen NICHES tracts **without trails are directory-only** (`Anchor Type: none`, no coordinates) so no pin sends anyone into a hunt-season bottomland; two of those (Hickory Grove Farm, Whistler Woods) do have trails but no Google listing — they need coordinates from NICHES' own map before they get a pin. Moyer-Gould Woods hidden (storm-closed since June 2026 per NICHES). NICHES properties carry `Dawn-Dusk` and, where the county page says so, a `12-01 → 10-31` season (closed November for the deer-control hunt).
- Build: `BUILD OK — 60 records (47 mappable)`. Smoke: 7 pages, 0 errors; directory 60.
- **Kit gap found:** `Season Start/End` is read by the build and honoured by the calendar's Explore-nearby (`inSeason()`, wraps the year) but the **atlas does not hide out-of-season pins** — BRIEF §3.1 says it should. Add the gate in `index.template.html` next code pass.
- **Unverified from the sandbox:** pin rendering (markers attach after the map style loads, which needs tiles). Data verified: 47 records with lat/lng in `data.js`.
- Amtrak: Laurie has the whole US/Canada network in the Hilltowns project; the kit's Transportation sheet is empty. Awaiting that sheet (and any `data/layers/` JSON) to merge.

## Where things stand — v3 (2026-10-06)

**Changes since v2:**
- **First 30 POIs** in `data/points_of_interest.xlsx` — Farm Stands 7 (one hidden), Adventures 21, Arts & Entertainment 2. Every coordinate, address and phone is from a Google Places lookup made today, with the `place_id` in Notes (the brief's accepted source). Hours: the three markets from their official pages (Greater Lafayette Commerce release, westlafayette.in.gov, purdue.edu) with seasons set; everything else "as listed on Google today" and said so in Notes. Descriptions are assistant drafts from official pages and place type, never from reviews. Hidden pending Laurie: Prairie View Farms (unclear whether a retail stand). Flagged in Notes: Lafayette market's season end (10-31 placeholder), Fort Ouiatenon "24 hours" (county park, dawn–dusk likelier), Flint Creek's split hours, Annie's Orchard no hours.
- `place.json → keys`: Laurie's eBird and USGS keys carried over from the Hilltowns (per person, not per site).
- `index.template.html` fix: `openNow()` read today's hours cell by the *viewer's* weekday (`new Date().getDay()`); now `nyDowKey()` — the region's day, like `isDimmed()` already did. A Hilltowns latent bug that BRIEF §10 warns about.
- Build: `BUILD OK — 29 records (29 mappable)`, 15 warnings (13 are preview-image fetches the sandbox can't make; they retry in CI). Smoke: 7 pages, 0 errors; directory lists 29 with 24 core-town highlights.
- Directory shows a "Source" line per card — the kit's behaviour; fine.

**Next POI batches (same method):** Restaurants (downtown Lafayette + Battle Ground + Delphi), Lodging (Prophetstown campground, Battle Ground / West Lafayette), NICHES preserves individually (Black Rock, Weiler-Leopold, Clegg Memorial Garden…), Wolf Park / Prophetstown programs as events, Antiques & Vintage, Arts & Entertainment (Long Center, Wells Community Cultural Center, Haan Museum, Art Museum of Greater Lafayette), Independent Media (WBAA, Journal & Courier, Lafayette Independent).

## Where things stand — v2 (2026-10-06)

**Changes since v1 (Laurie's answers + research):**
- Elevation 540 ft confirmed by Laurie (`center.elev_ft`); note softened accordingly.
- **Moon names: Myaamia (Miami) lunar months** — *myaamia kiilhswaakani* — from the Myaamia Center (Miami University / Miami Tribe of Oklahoma). Why Miami and not Shawnee: the Wabash–Tippecanoe confluence is Miami (Wea / Piankeshaw) homeland — the Wea town and French post of Ouiatenon sat just below Lafayette — while Prophetstown (1808–12) was Tenskwatawa and Tecumseh's pan-tribal town, Shawnee-led, with Potawatomi, Kickapoo, Winnebago, Ottawa, Ojibwe, Wyandot and Delaware residents. The Myaamia Center publishes a living lunar calendar with a stated rule; no comparable published Shawnee month list with a reckoning rule turned up. Twelve names + *waawiita kiilhswa* 'Lost Moon', in `place.json → moons`, with source URLs.
- **Reckoning (new `skyline.js` mode `june_solstice`):** the June solstice must fall inside *paaphsaahka niipinwiki* (mid-summer moon); moons are counted from it; when 13 lunations separate two mid-summer moons the lost moon is inserted after *mahkwa kiilhswa* (Black Bear Moon), "in the dead of winter". Tested in the real `skyline.js` code against the Center's published dates: their 2024 new year (day 7 of *mahkoonsa* = 2024-02-17) → ours gives *mahkoonsa* day 8 (we count from astronomical new moon, they from first light — one day); their "28 waawiita kiilhswa (2026)" post in mid-Feb 2026 → ours gives *waawiita* day 27 on Feb 14. Their list of past lost-moon years (2013, 2015, 2018, 2026) matches ours for 2015/2018/2026 and differs at 2012/2013 (solstice 1½ days after a new moon — a boundary call) and omits 2021/2023 (astronomically unavoidable under the stated rule; the list reads as incomplete). The tooltip says "a reckoning, not the Tribe's own calendar". Compare each winter to the Center's calendar.
- **USGS gauges registered** (`place.json → water`), each verified on its waterdata.usgs.gov site page today; all show period of record through 2026-10-06 so are presumed live — *confirm on first live load*: Wabash at Logansport 03329000, Tippecanoe near Ora 03331500, Tippecanoe near Delphi 03333050, Deer Creek near Delphi 03329700, South Fork Wildcat near Lafayette 03334500, Wildcat Creek near Lafayette 03335000, Wabash at Lafayette 03335500, Wabash at Covington 03336000. Four chains (Wabash / Tippecanoe / Wildcat / Deer), eyebrows, named waters (+ Burnett Creek). No wells yet. Logansport and Ora are outside the 50 km sweep but are explicit transect sites, so they appear.
- Build: `BUILD OK`, 0 records, 2 warnings. Smoke harness: 7 pages, 0 errors. Header shows *šaašaakayolia kiilhswa* · Grass Burning Moon for 2026-10-06.

**Research roadmap — what to pursue, in payoff order**

| Layer | Source | What to do | Who |
|---|---|---|---|
| Signals · stations | xmACIS2 — xmacis.rcc-acis.org → Station Data → Daily data listing | Pick every co-op / CoCoRaHS / first-order station within ~30 mi of Prophetstown (search by county: Tippecanoe, Carroll, White, Clinton, Montgomery, Warren, Benton); export full period of record as CSV → `data/stations/<slug>.csv`; register in `place.json → weather.stations`. One long first-order record (Purdue / West Lafayette) + the nearest active CoCoRaHS + any closed station with real temps. | Laurie exports; assistant registers and builds |
| Signals · keys | api.waterdata.usgs.gov (free key); ebird.org/api/keygen (free key) | Request both; paste into `place.json → keys`. eBird refuses browser calls without a key. | Laurie |
| Society | nothing to collect | Radii already set; check the live page. | — |
| Atlas · POIs | Visit Lafayette–West Lafayette 2026 Experience Guide (PDF); Purdue Farmers Market page; Lafayette Farmers Market / West Lafayette Farmers Market / Battle Ground sites; Tippecanoe County Parks; Indiana DNR properties; Wabash River Enhancement Corp; Tippecanoe County Historical Association; Lafayette & West Lafayette parks depts; Carroll / White County tourism | Assistant compiles per-category candidate sheets (name, address, website, hours as stated, source URL, Display=No, coords blank). Laurie verifies coordinates in Google Maps/Places (the brief's rule: never geocode a bare address) — or we connect a Places tool and the assistant verifies. 20–50 per session. | assistant → Laurie |
| Calendar · events | Library ICS feeds (Tippecanoe County Public Library, West Lafayette PL), city/county calendars, Purdue Convocations, Tippecanoe Arts Federation, Prophetstown SP programs | Stand up the ingestor chat when the first three pages are live. | separate chat |
| Phenology · microseasons | Laurie's own year + Purdue Extension, Indiana Phenology, Nature Conservancy Indiana, iNat seasonality for the box | Slow layer; the kit's structure is ready. | microseasons chat |
| On record · climate events | NWS Indianapolis / Northern Indiana event summaries, Indiana State Climate Office (Purdue), Journal & Courier archives, Tippecanoe County Historical Assn, USGS flood reports for the Wabash | Separate register chat, same `climate_events.xlsx` schema. | register chat |
| Folklore | Tippecanoe County Historical Association, Indiana Historical Society, Myaamia Center publications, Shawnee Tribe, Potawatomi (Pokagon, Citizen) archives, Battle of Tippecanoe sources | Separate chat; Nation sources before settler retellings. | folklore chat |
| Water (optional) | IDEM (Indiana Dept of Environmental Management) 303(d) list and TMDLs for the Wabash/Wildcat; EPA ECHO/TRI; Indiana Water Monitoring Inventory | Only if someone will research it properly. | later |

## Where things stand — v1 (2026-10-06)

**What this version is.** The empty, localised skeleton. `config/place.json` is the single source of every place-specific value, and every file that `LOCALIZE.md` listed now reads from it. Nothing has been added to any data master. `BUILD OK — 0 records, 2 warnings` (the two are the kit's placeholder folklore sheet and single example microseason).

**Decisions taken this version (Laurie, 2026-10-06):**
- Centre = Prophetstown State Park, 40.5000 N / −86.8333 W (Wikipedia, rounded to the minute; DNR mapping address 5545 Swisher Rd, West Lafayette IN 47906). Elevation entered as ~540 ft (confirmed by Laurie in v2).
- Brand: "Ye Olde Navigators Guide" (header stack: *Ye Olde* / *Navigators Guide*).
- Timezone `America/Indiana/Indianapolis` (Tippecanoe County is Eastern; the NW and SW corners of the state are Central — if the radius ever reaches them, nothing changes, the site keeps the region's one zone by design).
- **Landing page is the Atlas** (`place.json` → `"landing": "atlas"`), per the priority on Signs + Signals, Society Pages and the Atlas. The calendar still builds at `calendar.html`. Flip to `"calendar"` any time.
- All Hilltowns categories kept as-is in `manifest.json` (Laurie: fill as we go). The nine "WIP" environmental layers still exist, empty, behind the unlinked `wipmap.html`.
- Core towns (gold highlight on calendar/directory) are a **placeholder list** in `place.json` → `towns.core`: Battle Ground, West Lafayette, Lafayette, Dayton, Brookston, Delphi, Americus, Buck Creek. Edit freely.
- Moon names: the Hilltowns header showed the Onondaga Nation's thirteen moons. That table was place-specific and is now `place.json` → `moons.names` (empty for Prophetstown, so the header shows phase only). **Research item, not a guess** — Shawnee / Miami / Potawatomi / Kickapoo sources, with the source URL recorded in `moons.source`.

**What changed in the code (all of it is "read place.json instead"):**
- `build/build.py`: loads `config/place.json`, validates centre/timezone, derives `instagram_url`, `href_atlas`/`href_calendar`, `share_card_url`; stamps `{{place.a.b}}` tokens, `<!-- @@if:key -->…<!-- @@endif -->` blocks and the `<!-- @@ticker -->` marker into every page; injects `<script src="place.js">` before `</head>` and GoatCounter before `</body>` only when `analytics.goatcounter` is set; emits `site/place.js` (`window.PLACE`, `window.CENTER`, `window.TZ`). Stations register (`weather.stations`), hearts namespace, preview-cache URL, User-Agent, no-preview hosts all from place.json. "Today" for event expiry is computed in the region's zone (`now_local()`), not UTC. Landing page per `place.json`.
- `index.template.html`: `HOME`, map zoom, `CENTER` (was `BERNE`), `homeDateISO` (was `berneDateISO`), like/share storage keys, titles/og, brand/about copy, epigraph, ticker, instagram block — all tokens or `window.PLACE`.
- `skyline.js`: `CENTER`, `WX_POINT` (was `HUYCK`), timezone in every `Intl` call and Open-Meteo query, radio presets from `place.json` → `radio` (no presets = no tuner), moon names from `place.json` → `moons`.
- `signals.js`: centre, timezone, `INAT_DIST_KM`, `INAT_DAYS`, `EBIRD_*`, `USGS_KEY`, `WATER_BBOX_KM`, `STREAM_SITES`, `WELL_SITES`, `WELL_NOTE`, `WATER_CHAIN`, `CHAINS`, `WATER_CAP`, `NAMED_WATERS`, the 7-day chart order (`water.chart_order`, else every chain in order, then wells/lakes/tidal). The reanalysis source key is `'home'` (was `'berne'`).
- `calendar.html`: standing features and all six Explore-nearby curation lists from `place.json` → `calendar.*`; `NEARBY_EXCLUDE_CATS` is now derived (any `wip` layer, plus `"nearby": false` in the manifest — set on Natural History); `CORE_TOWNS` from `towns.core`.
- `directory.html`: core-town highlight from `towns.core`, state suffix from `state_abbr`/`state_name`.
- `partials/header.html`, `footer.html`: brand lines, nav order Atlas → Calendar with hrefs that follow the landing setting, Instagram links only when a handle is set.
- `about.html`: rewritten to a tokenised minimum with two `[Editor: …]` placeholders. The Hilltowns FAQ was that site's voice, not the kit's.
- `signals.html`, `society.html`, `bulletin.html`, `instagram.html`, `tradingpost.html`, `waterwip.html`: titles/meta/copy tokens.
- `.github/workflows/build.yml`: `config/**` added to the rebuild paths.
- `manifest.json`: `site_title` removed (lives in place.json); `"nearby": false` on Natural History.
- `data/stations/README.md`: rewritten for the place.json register.
- `scripts/v1_localize_patch.py`: the exact patch that produced this tree (already applied; for the record). `scripts/smoke_harness.js`: the headless check used below.

**Verified in the sandbox (headless Chromium, every external feed aborted or mocked, viewer timezone deliberately set to Los Angeles):** all seven pages load with zero page errors; the header reads *Ye Olde / Navigators Guide*; sunrise · sunset shows 7:49 am · 7:23 pm for Oct 6 — correct for 40.5 N / −86.83 in Indiana time, so the clock is pinned to the region, not the viewer; `window.PLACE.timezone` = `America/Indiana/Indianapolis`; the MapLibre map initialises at 40.500 / −86.833, zoom 10.5; the Signals picker reads "ERA5 reanalysis for the Prophetstown grid cell"; no `{{place.…}}` token survives into `site/`; no `instagram` string survives (handle is blank); `place.js` is injected into all 12 built pages. Clean-room rebuild from a fresh copy: `BUILD OK`.

**Not verified from the sandbox — check after first deploy:**
- Map tiles (OpenFreeMap / Esri) and the live Open-Meteo, USGS, iNaturalist and eBird feeds — the sandbox can't reach any of them. Expect Society Pages and the water section to say "unreachable" until the first live load, and the USGS section to be empty until gauges are registered.
- The share card and favicon in `images/` are still the Hilltowns raccoon. `og:image` resolves to `{domain}/images/share-card.png` and `domain` is still `https://example.org/` — set `domain` once the Pages URL exists.
- Stratospheric-wind and winds-aloft panels: mocked, not exercised against real Open-Meteo hourly fields.

**Still Hilltowns, on purpose, for now:**
- `bulletin.html` stock sample cards (unlinked page) and `waterwip.html` + `water.js` + `build/water.py` (unlinked; the whole water package is a separate research project — BRIEF §3.7). Historical comments in `signals.js` that explain the water logic by Hilltowns example.
- `data/*.xlsx` example rows (Display = No) and the single example microseason.

**Next (Phase 1 → 4, in the order Laurie asked):**
1. Laurie: GitHub repo, Pages source = GitHub Actions, push this tree; set `domain` in `place.json`; first live look at Atlas, Signals, Society.
2. Signals Phase 4: stations within ~30 mi on xmACIS2 (candidates to check there, not confirmed: a West Lafayette / Purdue co-op record, Lafayette, Delphi, Frankfort) → `data/stations/`, registered in `place.json`. USGS gauges: Wabash at Lafayette, Tippecanoe near Delphi / at Ora, Wildcat Creek near Lafayette — look up on `api.waterdata.usgs.gov`, never from memory. eBird + USGS keys into `place.json → keys`.
3. Society: nothing to configure — the radii are set (40 km iNat box, 25 km eBird); confirm the circle on the live page.
4. Atlas: first 20 POIs with Places-verified coordinates, one category at a time.

---

## Owner of each file (decide once — BRIEF §5.3)

| File | Owner | Notes |
|---|---|---|
| `config/place.json` | editor | every place value; the assistant edits only on instruction |
| `manifest.json` | editor + assistant | categories |
| `data/points_of_interest.xlsx`, `folklore_legends.xlsx`, `microseasons.*`, `climate_events.xlsx`, `trading_post.xlsx` | editor (research chats feed them) | hide, never delete |
| `data/events.xlsx` | events ingestor (not stood up yet) | replaced wholesale; durable rules in `agenda_quiet.txt`, `events_carryover.py` |
| `data/stations/*.csv` | editor (xmACIS exports) | registered in place.json |
| `data/water/` | water research chat | optional |
| everything else | assistant | versioned, built, verified, packaged |

## Delivery ritual

As in BRIEF §4: edit → read back → clean `site/` rebuild, `BUILD OK` → headless check (`scripts/smoke_harness.js`, or the feed-mocking harnesses in `scripts/*_harness/` once their fixtures are re-pointed at Indiana sites) → README header + log line + version bump → clean-room rebuild → full zip + CHANGED-ONLY zip → one short message.

Run the smoke harness: `NODE_PATH=<global node_modules> node scripts/smoke_harness.js site out/` (needs Playwright; MapLibre is served from `scripts/signals_harness/node_modules` if installed).

---

## Log

- **v6 — 2026-10-06.** Ancient Ways layer: global routes dataset as a Folklore-grouped toggle; new emit_ways_layer() + atlas line/node module. 560 routes / 682 line features / 5,553 nodes. BUILD OK; headless toggle clean, 0 errors; visual pending live.
- **v5 — 2026-10-06.** Amtrak/VIA network merged (679 rows; 72 VIA flag stops had no coords). BUILD OK, 739 records / 726 mappable.
- **v4 — 2026-10-06.** 32 preserves/trails (19 pinned, 13 directory-only). BUILD OK, 60 records / 47 mappable. Atlas season-gate gap logged.
- **v3 — 2026-10-06.** First 30 POIs (Places-verified), keys carried over, openNow weekday fix. BUILD OK, 29 records. Smoke: 7 pages, 0 errors.
- **v2 — 2026-10-06.** Elevation confirmed; Myaamia moon names + solstice reckoning (`skyline.js` mode `june_solstice`), tested against the Center's 2024/2026 dates; 8 USGS gauges registered and verified on their site pages; research roadmap. BUILD OK, 0 records, 2 warnings. Smoke: 7 pages, 0 errors.
- **v1 — 2026-10-06.** Localised skeleton from starter kit v1. place.json created; 20 files rewired; Onondaga moon table moved out of code; landing = atlas; all categories kept; no data. BUILD OK, 0 records, 2 warnings. Headless: 7 pages, 0 errors.
