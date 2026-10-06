# Community Field Guide — build brief and handoff

*How the NY Hilltowners Folk Atlas was built (v1013, Oct 2026), what we learned over ~1,000 versions, and how to build the next one for any US community. Written for a fresh Claude instance and its human editor. The starter kit beside this file is the Hilltowns code with the Hilltowns data removed.*

---

## 0. Read this first

You are building a **community field guide**: a static website that shows a region's places, events, folklore, natural cycles and public-record data on one map and a few companion pages, kept honest by an editor who owns the data. The reference build is live at nyhilltowners.com (Helderberg Hilltowns, Albany County NY).

Three things decide whether a second build goes well:

1. **The editor owns the data; you own the code.** Every fact on the site comes from a spreadsheet the editor can open. You never invent a place, a coordinate, an hour or a date. You verify, you add with a dated note, you hide rather than delete.
2. **Place is configuration, not code.** The Hilltowns build hard-coded its coordinates, station lists, river gauges and place names in ~15 files. Do not repeat that. Section 6 tells you where to put them.
3. **Ship every change as a versioned, rebuilt, clean-room-verified package.** The ritual in Section 8 is what let one editor and one assistant make a thousand changes without losing track.

If you only have an hour: read Sections 1, 2, 6 and 8, then run the kit's build.

---

## 1. What the thing is

One static site, built by one Python script from spreadsheets, hosted on GitHub Pages, no server, no database, no framework.

| Page | What it does | Source |
|---|---|---|
| **Atlas** (`index.html`) | MapLibre map with every category as a toggle: events (next 48 h glow), businesses (lit when open today, glowing when open now), folklore, natural history, transportation, and heavier "WIP" layers behind an unlinked `wipmap.html`. Pins carry hours, tags, hearts, share. | `index.template.html` |
| **Calendar** (`calendar.html`, also the landing page) | Agenda + month view of events, "Explore nearby" module keyed to a chosen date. | `calendar.html` |
| **Directory** (`directory.html`) | A–Z listing of every displayed POI with hours/phone/site. | `directory.html` |
| **Signs + Signals** (`signals.html`) | Nature dashboard: sun/moon, sky, air, winds aloft (850/700/500/10 hPa), rain & snow year-to-date, year-by-year weather history from 1940 (ERA5) and from every local co-op station we could find, phenology (24 microseasons beside an "On record" climate-event register), USGS water levels and 7-day charts. | `signals.html` + `signals.js` |
| **Society Pages** (`society.html`) | Who's been seen: iNaturalist research-grade observations (14-day leaderboard, 5-day photo grid, 18 taxonomic pulls) and eBird sightings. | `society.html` + `signals.js` |
| **Water** (`waterwip.html`, unlinked) | Water-quality instrument panel: two transects from the divide to the river, node cards, biology, reservoir TMDL, blooms/toxins, groundwater, outfalls vs permit limits, TRI air releases, map, provenance, plus 23 plain-English contaminant profiles with diagrams and world standards. | `waterwip.html` + `water.js` + `build/water.py` |
| About, Bulletin, Instagram, Trading Post | Static / light pages. | one html each |

Shared across pages: `partials/header.html` (brand, skyline widget with live sun/moon/strat wind, nav), `partials/footer.html`, `skyline.js`.

---

## 2. Architecture

```
data/*.xlsx  +  data/water/*.xlsx  +  data/stations/*.csv  +  data/*.md
        │
        ▼
build/build.py  (openpyxl; deterministic; exits 1 on any validation ERROR)
   ├─ parse_poi / parse_events / parse_folklore   → records (one dict per pin)
   ├─ preview-image cache (OG image per website; cached JSON, parallel fetch, retried next build)
   ├─ hearts (per-slug counter via abacus API; cached)
   ├─ emit_page(): stamps partials/header+footer into each *.html, marks active nav
   ├─ lazy layers: categories with "lazy": true → data_<key>.js, loaded only when toggled
   ├─ build/water.py  → data_water.js (pre-aggregated, with cell-colour provenance)
   ├─ station csv → station_dd.js (per-year cumulative degree days)
   └─ microseasons.md + climate_events.xlsx → phenology_expected.js / phenology_history.js
        │
        ▼
site/   (index.html, calendar.html, data.js ≈ 6 MB, data_*.js, *.js, images/)
        │
        ▼
GitHub Actions (.github/workflows/build.yml): push to main → build → deploy Pages
```

**Why static + spreadsheets.** The editor can fix a wrong hour in Excel. Nothing can go down at 2 a.m. The whole site is a folder you can zip. Live data (weather, water, wildlife) is fetched by the browser from public APIs at view time; the build never depends on them.

**Why one build script.** Every validation lives in one place. `BUILD OK — N records, 0 errors` is the only green light. A failed build leaves the last good site in place.

**Hard limits learned the hard way**
- GitHub Pages: keep `data.js` under ~8 MB; above that, split into lazy layers (we did: mines 6 MB, orphan wells 6.5 MB, water 6.7 MB, each loaded on toggle).
- Package size: chat file sends cap at 30 MB → split full zips into part1/part2.
- Browser APIs: iNaturalist caps at 200 per page and rate-limits bursts (fire 2 at a time, page sequentially, name the HTTP status when it fails); eBird refuses cross-site browser calls unless you have a key and stay under its distance; USGS retired its old service in 2026 (use api.waterdata.usgs.gov with a key). Open-Meteo is the one that never complained.

---

## 3. The data masters (schemas)

Every master is an .xlsx with a header row. Never rename a header; the build maps on exact names.

### 3.1 `points_of_interest.xlsx` — one sheet per category (we own it)
Columns: `ID, Name, Tags, Address, Latitude, Longitude, Description, Monday…Sunday, Website, Phone, Glyph, Image, Image Credit, Notes, Display, Anchor Type, Season Start, Season End, Recur Weeks, Recur Days, Recur Except, Recur Time, Source`.
- `Tags`: `; `-separated, Title Case, singular, hyphenated compounds. First tag = the category. Searchable; the long tail of once-used tags needs periodic pruning (`scripts/tag_audit.py`, `tag_merge.py`).
- `Display`: Yes/No. **Never delete a row** — set No and write why in Notes.
- `Anchor Type`: `premise` (pin at the address) · `approximate` · `proxy` · `none` (directory only, no pin).
- Hours: free text per day (`9am-5pm`, `Closed`, `By appointment`, `Dawn-Dusk`, blank). These drive lit/dim/glow.
- `Season Start/End` (MM-DD) hide a pin out of season; `Recur *` mark meeting-type POIs (glow only in the window; excluded from the calendar).
- `Notes`: the audit trail — `YYYY-MM-DD: added/changed … per <editor>`; where the coords and hours came from.
- A sheet is a category; `manifest.json` maps sheet → key, label, colour, glyph, default on/off, lazy, wip.

### 3.2 `events.xlsx` — ingestor-owned
Columns: `ID, Event Name, Venue, Address, Latitude, Longitude, Description, Start Date, End Date, Time, Website, Glyph, Image, Image Credit, Notes, Display, Tags, Source, Added, Agenda, Recur Weeks, Recur Days, Recur Except, Recur Time` + sheets `Auto-Inbox, Sources, Ingest Log, Manual Check`.
- A separate "ingestor" (another Claude chat with scrapers for ICS feeds and venue pages) produces `events_NN.xlsx`; the atlas replaces `data/events.xlsx` wholesale. **Hand edits are lost on the next drop**, so durable event rules live in files the atlas owns: `data/agenda_quiet.txt` (patterns kept off the agenda), `scripts/events_carryover.py` (edits re-applied after each drop).
- Model A contract: one fully-dated row per occurrence; recurrence columns are metadata, never expanded by the build.
- Past events are skipped at build (the record count drops daily — that's the calendar, not a bug).

### 3.3 `folklore_legends.xlsx` (we own it)
`Locked ID, Short Title, Tale / Being, Nation / People, General Location, Latitude, Longitude, Location Certainty, Story Summary, In-Story Timeframe, Recorded By, Year Recorded, Original Publication, Source Book, Page(s), Notes, Image, Image Credit, Display, Website, Tags, Feature Rank`. Location certainty drives the pin tier (exact / vicinity / region); a "wonder score" sorts the sidebar.

### 3.4 `microseasons.md` + `microseasons.xlsx`
Twenty-four ~15-day microseasons for the place, each with Sky & Light / Weather & Ground / Flora / Birds / Animals / Insects & Fungi / Garden & Orchard / Foodways / Nature Health Watch, plus "Ghost" entries (what is absent) and a deep-time preface. Written by Claude with the editor, from the editor's own observations plus regional phenology sources. The build parses `### N. Name — Mon D–D` headings into `phenology_expected.js`.

### 3.5 `climate_events.xlsx` — the "On record" register
`ID, Start date, End date, Year, Category, Event name, Area affected, Key measurement, Station / gauge, Impact summary, Primary source, Source URL, Confidence (A–D), Anchor date fields, Show on timeline`. 856 events 1600s–2026 for the Hilltowns, every one with a source. Built in its own research chat; hazard glyphs are classified from `Category`.

### 3.6 `data/stations/*.csv` — weather stations
One xmACIS2 "Daily Data Listing" CSV per NOAA co-op / CoCoRaHS / first-order station, registered in `build.py STATIONS` with display name, elevation and active flag. 38 stations for the Hilltowns, 1869–present. The README in that folder explains how to add one.

### 3.7 `data/water/` — water-quality package (fourth master, research-chat-owned)
A 64-sheet workbook with cell-colour provenance (blue = verbatim from source, black = derived, yellow = assumption), GeoJSON layers, source PDFs, `contaminant_profiles.md` (23 hand-written profiles), `standards_world.csv` (279 standards, every row with the URL that states it), `molecules.csv` (diagram specs → `scripts/draw_molecules.py` → SVGs). Replace wholesale from the research chat; never hand-patch.

---

## 4. The workflow that worked

**Roles.** One editor (owns the data, makes every judgment call, deploys). One atlas assistant (code, build, packaging, verification). Specialist chats feed it: an events ingestor, a water-research chat, a climate-register chat, a microseasons chat. Each hands over a file; the atlas never reaches into their work.

**The delivery ritual** (every change, no exceptions):
1. Edit source — xlsx via openpyxl (never by hand-typing coordinates), or the HTML/JS/Python.
2. Read back what you wrote.
3. Rebuild from a clean `site/`; expect `BUILD OK`, zero ERRORs.
4. Verify in a headless browser (Playwright harnesses in `scripts/*_harness/` mock every external feed; take screenshots; look at them).
5. Write the README: the "Where things stand" header block (what this version changed and why, what is unverified) and a one-line log entry; bump the version.
6. Clean-room: copy the source tree, delete `site/` and caches, rebuild, confirm BUILD OK.
7. Package: full zip (split in two if >30 MB) + a CHANGED-ONLY zip of every file touched since the last version the editor deployed. Send both plus the flat masters the editor pulls directly.
8. Tell the editor in one short message what changed, what you could not verify from the sandbox, and what to look for after deploy.

**Standing data rules**
- Never geocode from a bare address. Coordinates come from Google Places, a USGS/DEC record, or the editor. Say in Notes where they came from.
- Existence-guard before every add (normalised name + address).
- Hours exactly as the source states them; "no hours" is a valid state (neutral pin), "Closed" is a different state (dim).
- Every number on a dashboard traces to a document; if it can't, leave it off. Non-detects are "not detected (< limit)", never zero.
- Prose about health or environment keeps the agency's own hedging. A field guide, not a warning label.
- When a feed fails, the page says what failed and with what status; it never shows "no results" for an outage.

**How the editor and assistant talk.** Short asks, quick builds, screenshots when the sandbox can render it, honest "I couldn't verify X from here, check Y after deploy" when it can't. The README is the memory between sessions; a new chat reads its header block and continues from the next version number.

---

## 5. What we'd do differently (improvements for build #2)

Ranked by payoff.

### 5.1 Build
1. **One `place.json`.** Centre lat/lng, name, timezone, bounding boxes (map, iNat, eBird, water), the station list, USGS site lists, river chains, named waters, brand strings. Every file reads it. (Hilltowns has these in ~15 places — see Section 6.) Make this the first commit.
2. **Split `build.py`** (1,700 lines) into `build/poi.py`, `events.py`, `folklore.py`, `pages.py`, `previews.py`, `stations.py`, with `build.py` as the orchestrator. Same for `index.template.html` (3,000 lines): move the pin logic to `atlas.js`.
3. **Schema validation as a test.** A `scripts/validate.py` that checks every master's headers, coordinate ranges, Display values, hour syntax, tag style, and date formats, run by the Action before the build. Today validation is scattered in the parsers.
4. **Preview-image cache committed, not fetched.** 2,900 of the 3,000 build warnings are OG-image fetches that fail in CI. Fetch previews in a separate scheduled job, commit `preview-cache.json`, and make the main build read-only.
5. **Lazy layers from day one** for anything over ~5,000 pins; a 15 MB `data.js` was painful to undo.
6. **Hourly scheduled build** (Actions cron) so "past events drop off" and hearts refresh without a push.
7. **Harness in CI.** The Playwright harnesses exist; run them in the Action with mocked feeds and fail on page errors.

### 5.2 Design
1. **Design tokens in one CSS file** (`tokens.css`): the palette (validated for colour-blind separation on the navy ground — keep the validator), type scale, spacing. Pages currently repeat the same ~40 rules each.
2. **The instrument-panel register** (eyebrow / big number / detail line, thin SVG marks, reference lines labelled, one axis per chart, no dual axes) worked for Signals and Water. Write it down as a component sheet and reuse it.
3. **Every chart self-reports**: source line, refresh cadence, what a gap means ("no DEC report" vs "no bloom"). Readers trusted the pages because the gaps were drawn.
4. **Mobile first for the map.** The Hilltowns map was desktop-first and patched; start with the phone layout (bottom sheet for pin details, toggle drawer).
5. **One nav, fewer pages.** Signals grew until it had to be split (Society Pages). Plan pages by *who reads them when*: visitors (calendar, atlas), residents (directory, signals), researchers (water).
6. **Accessibility pass early**: focus order on the carousel and pickers, `aria-label` on SVG charts, reduced-motion for the canvas effects. All retrofitted here.

### 5.3 Workflow
1. **Git from the first version**, with the assistant committing to a branch and the editor merging. Zips-in-chat worked but a 30 MB split zip per change is friction, and "CHANGED-ONLY since last deploy" had to be tracked by hand.
2. **Ingestor and atlas share one repo** so event rules don't have to round-trip through briefs.
3. **A `data/CHANGELOG.md` per master** (the Notes column is the audit trail today, which is fine for rows but not for schema changes).
4. **Decide the "owner" of each file in a table in the README on day one** (we did this at ~v600 after confusion).
5. **Keys and secrets**: public rate-limit keys (eBird, USGS) in the page are acceptable for a community site; anything that costs money goes in a GitHub secret with a build-time fetch.
6. **Name the version in the zip and the README header, nothing else.** Simple, and it survived 1,000 iterations.

---

## 6. Localising: every place-specific thing in the kit

The kit ships with the Hilltowns values still in code so nothing is broken; replace them in this order. `LOCALIZE.md` in the kit lists each with file and line.

| Where | What | Replace with |
|---|---|---|
| `index.template.html` `HOME`, `BERNE`; `skyline.js` `BERNE`, `HUYCK`; `signals.js` `LAT/LNG` | map centre, sky-calc point, water-box centre | your centre point (one value, read from place.json) |
| `partials/header.html`, `footer.html`, every `<title>`/`og:` | brand, site name, Instagram handle | yours |
| `manifest.json` `site_title`; categories | title; the category list, colours, glyphs | keep the schema; rename categories to what your region has |
| `build/build.py` `STATIONS`, `DAILY_STATIONS`, `STATION_LL`, `PREVIEW_CACHE_URL`, `HEARTS_NS/URL`, `User-Agent` | weather stations; cache URLs; hearts namespace | your stations (xmACIS2 exports), your domain, your namespace |
| `signals.js` `STREAM_SITES`, `WELL_SITES`, `CHAINS`, `WATER_CHAIN`, `WELL_NOTE`, `NAMED_WATERS`, `INAT_DIST_KM`, `EBIRD_DIST/BACK`, `EBIRD_KEY`, `USGS_KEY`, picker option text | USGS gauges, river chains, wildlife radius, API keys | your gauges (waterdata.usgs.gov), your keys |
| `signals.html`, `society.html` copy | "within 40 km of Berne", "Helderbergs to the northern Catskills" | your geography |
| `calendar.html` `NEARBY_EXCLUDE_CATS`; `about.html` | category names; the about text | yours |
| `data/microseasons.md`, `climate_events.xlsx`, `folklore_legends.xlsx`, `stations/` | all content | start empty; build each in its own research chat |
| `data/water/` | the whole package | optional; only if the region wants a water page |
| `images/` | share card, favicon, mark | yours |

**Sources that transfer to any US location**
- Weather: Open-Meteo (forecast, ERA5 1940–, winds aloft) — no key. NOAA co-op/CoCoRaHS daily listings via xmACIS2 (NRCC) — export per station.
- Water: USGS Water Data API (api.waterdata.usgs.gov, free key); state environmental agency open-data portals for permits, spills, remediation, wells (NY had data.ny.gov; most states have an equivalent, or use EPA ECHO / TRI / Envirofacts nationally).
- Wildlife: iNaturalist API (no key, rate-limited), eBird API (free key).
- Places: Google Places for coordinates/hours/phone (verify, don't scrape); OpenStreetMap for the locate link.
- Basemaps: OpenFreeMap (vector, free), Esri World Topo / imagery / hillshade (raster, attribution required).
- Analytics: GoatCounter (privacy-preserving, no cookies). Hearts: a public counter API (abacus) — fine for a toy, fragile; consider dropping.

---

## 7. Phase plan for a new community

**Phase 0 — scope (one session).** Name the region, its centre, its radius, its towns. Decide the first three pages (calendar, atlas, directory). Pick 6–10 POI categories that match what the region actually has. Create `place.json`. Choose a domain and GitHub repo; enable Pages (source: GitHub Actions).

**Phase 1 — skeleton live (one to two sessions).** Kit build with empty masters → first deploy. Add 20 POIs by hand with verified coordinates to prove the pipeline. Set up the Action, the delivery ritual, the README header. Get the editor opening the xlsx and pushing.

**Phase 2 — events (parallel chat).** Stand up an events ingestor: ICS feeds from libraries, towns, venues; a Sources sheet; dated-row contract. First `events_01.xlsx` drop. Agenda-quiet and carryover files from day one.

**Phase 3 — the directory fills (ongoing).** Batches of 20–50 POIs per session, each with existence-guard, Places-verified coords, hours as stated, dated Notes. Tag style enforced from the start. Hide-don't-delete.

**Phase 4 — Signs + Signals.** Open-Meteo first (works anywhere, no data to collect). Then stations: find every co-op/CoCoRaHS station within ~30 mi on xmACIS2, export, register. Then USGS gauges with the new API. Then wildlife.

**Phase 5 — the slow layers.** Microseasons (needs the editor's own year of observation plus regional sources), the climate-event register (newspaper archives, NWS, state climatologist), folklore (library and historical-society sources), water (only if someone will research it properly).

**Phase 6 — polish.** Mobile, accessibility, design tokens, the share card, analytics.

Expect Phase 1–3 in a few weeks of part-time work; the Hilltowns took about six weeks to v300 and the rest was depth.

---

## 8. Questions to ask the editor before writing code

1. Centre point and radius? Which towns are "in"? (Decides every bounding box.)
2. What is the site for — visitors, residents, organisers? (Decides which page is the landing page.)
3. Which 6–10 categories? What does the region have that the Hilltowns didn't (coast, desert, a university, a reservation, a ski hill)?
4. Who feeds events, and from where? Any ICS feeds already?
5. Timezone, and does the region cross one?
6. Domain, GitHub account, who deploys?
7. Any existing brand, colours, logo, Instagram?
8. Which public-record layers matter locally (water, air, mines, wildfire, flood, agriculture)? Which state portals hold them?
9. What should never appear (private residences, sensitive sites, sacred places)?
10. How will corrections arrive (email, a form, the editor)?

---

## 9. First-session prompt for the new instance

> Attached is the community-field-guide starter kit (`starter-kit-v1.zip`) and its brief (`BRIEF.md`). Read `BRIEF.md` first, then `LOCALIZE.md` and `HANDOFF_README.md`. We are building a field guide for **[REGION]** centred on **[LAT, LNG]**, radius **[N] km**, timezone **[TZ]**, for **[audience]**. Step 1: create `config/place.json` with those values and make every file in `LOCALIZE.md` read from it. Step 2: rename the categories in `manifest.json` to **[list]** and empty the example rows. Step 3: build, confirm `BUILD OK`, package as v1 with the delivery ritual in the brief (README header, clean-room rebuild, full zip + CHANGED-ONLY zip). Then stop and show me the empty site before we add data.

---

## 10. Things that are easy to get wrong (a checklist from the log)

- Timezones: compute everything in the region's zone, not the viewer's (the Hilltowns stamps Eastern on every clock). Use `Intl.DateTimeFormat` with `timeZone`, never `Date.getHours()`.
- Hours text: "By appointment" ≠ "Closed" ≠ blank. Each has a pin state.
- Recurring meetings are not events; they are POIs with a window.
- Do not expand recurrence rules; render dated rows.
- `text-transform: uppercase` on a unit label turns "µg/L" into "MG/L" — a thousand-fold error in one CSS line.
- A 429 from an API looks exactly like "no results" unless the code checks `response.ok`.
- Square bounding boxes reach 1.4× further at the corners than the radius you meant; use a circle where the API allows.
- Public datasets name the *registrant*, not the *place* (a septage hauler's office, not the field). Say so on the page.
- Record counts drop every day as past events expire. Not a bug.
- The Pages queue blocks on a stuck deploy unless `concurrency.cancel-in-progress: true` and a job timeout are set.
- Never rebuild a file from a truncated tool result; re-read the source.
- A clean-room rebuild catches "works on my tree" every single time it is skipped.

---

*Package contents: `BRIEF.md` (this), `LOCALIZE.md`, `HANDOFF_README.md` (the Hilltowns log, for reference), the full source tree with empty masters and example rows, `scripts/`, harnesses, the GitHub workflow.*
