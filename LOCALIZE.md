# LOCALIZE — every place-specific value in the kit, by file and line

> **Status v1 (2026-10-06): DONE for every file below except the water package** (`waterwip.html`, `water.js`, `build/water.py` — unlinked, optional, a research project of its own) and the stock sample cards in `bulletin.html`. Line numbers below are from the pre-patch kit and no longer match; the list is kept as the checklist it was. Values now live in `config/place.json`; see `HANDOFF_README.md` for what reads what. Two items this list missed and v1 also moved: the Onondaga moon-name table in `skyline.js` and the atlas epigraph in `index.template.html`.

Generated from the kit source. Replace each with a value from `config/place.json` (or make the file read place.json). Line numbers are for this kit version.

## `index.template.html` — 21 line(s)

| line | what | snippet |
|---|---|---|
| 6 | page titles and descriptions | `<title>Hilltowns Field Guide — NY Helderberg-Hudson Hilltowns</title>` |
| 7 | page titles and descriptions | `<meta name="description" content="An interactive atlas of folklore, history, and daily life in the NY Helderbe` |
| 8 | page titles and descriptions | `<meta property="og:title" content="Hilltowns Field Guide">` |
| 9 | page titles and descriptions | `<meta property="og:description" content="Folklore, history &amp; daily life in the NY Helderberg-Hudson Hillto` |
| 461 | place names in copy | `(sunset→sunrise at Berne, NY) or by the header sun/moon toggle. Tokens are` |
| 540 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 550 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 577 | place names in copy | `<button class="iconbtn" id="modeToggle" title="Night mode follows sunset and sunrise in Berne, NY. Tap to swit` |
| 607 | place names in copy | `<div class="sidefoot"><a href="about.html">About this atlas</a> &middot; <a href="https://instagram.com/NYHill` |
| 635 | place names in copy | `<h2>Hilltowns Field Guide</h2>` |
| 636 | place names in copy | `<div class="field"><div class="fv story">A living atlas of the NY Helderberg-Hudson` |
| 637 | place names in copy | `Hilltowns &mdash; folklore and legends gathered from historical sources, alongside` |
| 642 | place names in copy | `<a class="weblink" href="https://instagram.com/NYHilltowners" target="_blank"` |
| 643 | place names in copy | `rel="noopener">@NYHilltowners</a></div></div>` |
| 681 | centre point / sky point | `var HOME = [-74.1436, 42.5145]; /* Rensselaerville, NY (lng,lat) */` |
| 684 | place names in copy | `The atlas keeps Hilltowns time: night mode runs from sunset to sunrise at` |
| 685 | place names in copy | `Berne, NY for every visitor, wherever they are. Coordinates are Berne Town` |
| 686 | place names in copy | `Hall's own POI row (1656 Helderberg Trail). The sunrise equation below is` |
| 689 | centre point / sky point | `var BERNE = {lat:42.624848, lng:-74.135036};` |
| 805 | place names in copy | `/* "today" pinned to the atlas's home timezone so events expire on Catskill time */` |
| 1319 | place names in copy | `the Helderberg relief, then an ember wash so the gray reads warm. */` |

## `calendar.html` — 11 line(s)

| line | what | snippet |
|---|---|---|
| 6 | page titles and descriptions | `<title>Event Calendar — Hilltowns Field Guide</title>` |
| 7 | page titles and descriptions | `<meta name="description" content="Upcoming events across the NY Helderberg-Hudson Hilltowns — a community even` |
| 8 | page titles and descriptions | `<meta property="og:title" content="Event Calendar — Hilltowns Field Guide">` |
| 308 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 317 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 778 | place names in copy | `that SHOULD show (Hilltown Commons itself is out; The Pub at Hilltown Commons stays) */` |
| 806 | place names in copy | `"hamlet ny",   /* 2026-09-16 (Laurie) — Hamlet NY, Rensselaerville */` |
| 842 | category names / title | `var NEARBY_EXCLUDE_CATS = ["Natural History", "Mines & Quarries", "Spills", "Fuel & Chemical Storage", "Cleanu` |
| 921 | place names in copy | `at Hilltown Commons must still show for a Commons event) */` |
| 1031 | place names in copy | `// boundaries so "Berne" doesn't match "Bernese" and "Knox" is whole-word.` |
| 1033 | place names in copy | `"Rensselaerville","Berne","Knox","Westerlo","Oak Hill",` |

## `directory.html` — 14 line(s)

| line | what | snippet |
|---|---|---|
| 6 | page titles and descriptions | `<title>Directory — Hilltowns Field Guide</title>` |
| 7 | page titles and descriptions | `<meta name="description" content="An A–Z directory of the organizations and businesses on the Hilltowns Field ` |
| 8 | page titles and descriptions | `<meta property="og:title" content="Directory — Hilltowns Field Guide">` |
| 165 | place names in copy | `/* Hilltowns-proper highlight: gold sidebar + faint warm tint, for orgs physically` |
| 166 | place names in copy | `located in Berne/Knox/Westerlo/Rensselaerville/Preston Hollow/Potter Hollow/Oak Hill */` |
| 305 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 314 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 398 | place names in copy | `/* ---- physically-in-the-Hilltowns highlight ----` |
| 400 | place names in copy | `search would false-positive on street names like "Berne-Altamont Rd" in Altamont,` |
| 401 | place names in copy | `which is not itself a Hilltown. Whole-word/phrase match so "East Berne" and` |
| 402 | place names in copy | `"South Westerlo" (real hamlets within Berne/Westerlo) still count. */` |
| 405 | place names in copy | `function isHilltownOrg(town){` |
| 458 | place names in copy | `o.inHilltowns = isHilltownOrg(o.town);` |
| 548 | place names in copy | `var h = '<div class="org'+(o.inHilltowns?' htown':'')+'">';` |

## `about.html` — 10 line(s)

| line | what | snippet |
|---|---|---|
| 6 | page titles and descriptions | `<title>About — Hilltowns Field Guide</title>` |
| 7 | page titles and descriptions | `<meta name="description" content="About the Hilltowns Field Guide — a living field guide to the NY Helderberg-` |
| 8 | page titles and descriptions | `<meta property="og:title" content="About — Hilltowns Field Guide">` |
| 178 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 187 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 206 | place names in copy | `<h1>Hilltowns Field Guide</h1>` |
| 208 | place names in copy | `<p>A living atlas of the NY Helderberg-Hudson Hilltowns &mdash; folklore and legends gathered from historical ` |
| 210 | place names in copy | `<p>Additions, suggestions, corrections, complaints about the universe? Message us on Instagram at <a class="li` |
| 212 | place names in copy | `<p>Local organization, business, interesting bit of folklore, or something else you think should be on the map` |
| 236 | place names in copy | `<p>We always welcome new perspectives and civil discourse. Please DM us on Instagram at <a href="https://insta` |

## `signals.html` — 8 line(s)

| line | what | snippet |
|---|---|---|
| 6 | page titles and descriptions | `<title>Signs + Signals — Hilltowns Field Guide</title>` |
| 7 | page titles and descriptions | `<meta name="description" content="Sun, moon, weather, winds aloft and degree days for the Hilltowns — the natu` |
| 8 | page titles and descriptions | `<meta property="og:title" content="Signs + Signals — Hilltowns Field Guide">` |
| 383 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 392 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 421 | place names in copy | `<p class="sg-det" style="margin:0 0 8px">For Berne, NY, ~1,700 ft. Sun and moon are computed here; today's for` |
| 450 | place names in copy | `<!-- v954 (2026-09-28, Laurie): ONE picker — Berne reanalysis (default) or an active observed station — govern` |
| 515 | place names in copy | `<p class="sg-note" id="dd-note"><b>Sources.</b> Sky computed locally for Berne, NY (~1,700 ft). Today, air, wi` |

## `society.html` — 8 line(s)

| line | what | snippet |
|---|---|---|
| 6 | page titles and descriptions | `<title>Society Pages — Hilltowns Field Guide</title>` |
| 7 | page titles and descriptions | `<meta name="description" content="Who's getting noticed in the Hilltowns this fortnight — iNaturalist observat` |
| 8 | page titles and descriptions | `<meta property="og:title" content="Society Pages — Hilltowns Field Guide">` |
| 383 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 392 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 416 | place names in copy | `<p class="sg-det sg-intro" style="margin:4px 0 22px">Who's been getting noticed in the Hilltowns lately! Submi` |
| 420 | place names in copy | `<p class="sg-det" style="margin:0 0 10px">Research-grade observations within about 40 km of Berne — Helderberg` |
| 427 | place names in copy | `<p class="sg-det" style="margin:0 0 10px">Reported within 25 km of Berne in the last 14 days, newest first. Th` |

## `waterwip.html` — 12 line(s)

| line | what | snippet |
|---|---|---|
| 2 | place names in copy | `<!-- waterwip.html — v982 (2026-09-29, Laurie): Helderberg–Hudson water-quality dashboard. Unlinked (no nav li` |
| 9 | page titles and descriptions | `<title>Water — Hilltowns Field Guide</title>` |
| 10 | page titles and descriptions | `<meta name="description" content="Helderberg–Hudson water: what the public record says about the water at each` |
| 12 | page titles and descriptions | `<meta property="og:title" content="Water — Hilltowns Field Guide">` |
| 179 | place names in copy | `Helderberg–Hudson water-quality master. White on ink, gold for headings/live pills, the four validated` |
| 343 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 352 | place names in copy | `<span><span class="tg">𓅓</span> Suggestions? Hit us up NYHilltowners@Gmail.com</span>` |
| 402 | place names in copy | `<h2 class="sg-sec">4 · Basic Creek Reservoir <span class="n">— impaired for phosphorus (TMDL 2013) and dissolv` |
| 403 | place names in copy | `<h3 class="sg-h3">Summer phosphorus, lake by lake <span class="sub">DEC summer means (June–September), log sca` |
| 459 | place names in copy | `<p class="sg-note">The Basic Creek Reservoir catchment (USGS StreamStats, 11,318 ac) runs north into Berne; bo` |
| 468 | place names in copy | `<div>· City of Albany AWQR 2022 and 2024 not obtained; Berne-Knox-Westerlo CSD report not pulled.</div>` |
| 469 | place names in copy | `<div>· A "Westerlo Southside Water Coop" appears in EPA ECHO and is not yet confirmed with the town.</div>` |

## `signals.js` — 62 line(s)

| line | what | snippet |
|---|---|---|
| 2 | place names in copy | `Phenology / natural-cycles dashboard for Berne, NY. Reuses skyline.js (loaded first)` |
| 12 | centre point / sky point | `var LAT = (window.BERNE¦¦{}).lat ¦¦ 42.6248, LNG = (window.BERNE¦¦{}).lng ¦¦ -74.1350;` |
| 115 | place names in copy | `/* v954 (Laurie): Berne reanalysis first and default; then the active stations. This one picker drives Rain & ` |
| 116 | place names in copy | `var ob=document.createElement('option'); ob.value='berne'; ob.textContent='Berne reanalysis \u00b7 ERA5 grid c` |
| 167 | place names in copy | `var _winterBerne=null;` |
| 199 | place names in copy | `source happens to contain. 1956 is the same violet on every station and on Berne; only the real` |
| 321 | place names in copy | `var rn=$('ch-rain-note'); if(rn) rn.textContent = (_curSrc==='berne') ? '' : 'Rain alone is not recorded at a ` |
| 325 | place names in copy | `var _yearsBerne=null;` |
| 331 | place names in copy | `_yearsBerne=yearSeries(j); _winterBerne=winterFromDaily(j.daily.time, j.daily.snowfall_sum¦¦[], j.daily.temper` |
| 369 | place names in copy | `if(src==='berne'¦¦!ALL¦¦!ALL.stations[src]){ years=_yearsBerne; _curWinter=_winterBerne; note=''; }` |
| 374 | place names in copy | `var ntn=$('no-temp-note'); if(ntn){ ntn.style.display=noTemp?'':'none'; ntn.textContent=noTemp?('This station ` |
| 376 | place names in copy | `_curSrc=src; _curYears=years; _curNote=(src==='berne'?'ERA5 reanalysis for Berne via Open-Meteo':'NOAA GHCN-Da` |
| 403 | place names in copy | `/* Albany observed (station_dd.js), same date, same formulas */` |
| 409 | place names in copy | `/* water + extremes for the chosen source - v954: Berne reanalysis (default) computed from the same ERA5 serie` |
| 425 | place names in copy | `var stn=$('st-note'); if(stn) stn.textContent='ERA5 reanalysis for the Berne grid cell via Open-Meteo, 1940 to` |
| 504 | place names in copy | `/* ---------- iNaturalist: research-grade observations in the Hilltowns box, newest observed first ---------- ` |
| 505 | radii and API keys | `var INAT_DIST_KM = 40;   /* v927 shrank this to 25 km to match the birds; v939 (2026-09-27, Laurie): widened t` |
| 530 | place names in copy | `around Berne, several parameter codes at once; USGS returns whatever each site actually has. */` |
| 541 | radii and API keys | `var USGS_KEY='imM50bTg9Hd7VWPGYA0fRs73FcFYLN8UchnfbZZO';   /* v1011 (2026-10-05, Laurie): api.waterdata.usgs.g` |
| 603 | radii and API keys | `var WATER_BBOX_KM = 50;` |
| 639 | USGS gauges, river chains, named waters | `var WELL_SITES = ['421821074012701','421746074180201','422241073274601','424560074274101','424115073495301','4` |
| 640 | place names in copy | `/* v940 (2026-09-27, Laurie): the stream row is a curated transect, not a nearest-N sweep - Schoharie Creek fr` |
| 642 | place names in copy | `tidal Hudson at the Port of Albany, the Esopus at Mount Marion (the big Catskill drainage, entering at` |
| 644 | place names in copy | `Catskill Creek has no active gauge (Oak Hill 01361500 is dead). */` |
| 647 | USGS gauges, river chains, named waters | `var WELL_NOTE = {'424115073495301':'Glacial Lake Albany \u00b7 Pine Bush sand', '424311073423901':'Glacial Lak` |
| 648 | USGS gauges, river chains, named waters | `var WATER_CHAIN = {` |
| 649 | place names in copy | `'01347000':'Mohawk \u00b7 above the Schoharie', '01349705':'Schoharie headwaters \u2192 Mohawk \u2192 Hudson',` |
| 650 | place names in copy | `'01350212':'Schoharie \u00b7 below Blenheim-Gilboa pumped storage', '01351298':'Cobleskill Creek \u2192 Schoha` |
| 652 | place names in copy | `'01350000':'Schoharie \u2192 Mohawk \u2192 Hudson', '01350100':'Schoharie Reservoir \u00b7 Gilboa Dam', '01350` |
| 653 | place names in copy | `'01350480':'Little Schoharie \u2192 Schoharie', '01350500':'Schoharie \u2192 Mohawk \u2192 Hudson', '01350750'` |
| 654 | place names in copy | `'01351200':'Fox Creek \u2192 Schoharie', '01351450':'Schoharie \u2192 Mohawk \u2192 Hudson', '01351500':'Schoh` |
| 656 | place names in copy | `'01359525':'Normans Kill \u2192 Hudson', '01362230':'Schoharie Reservoir \u2192 Shandaken Tunnel \u2192 Esopus` |
| 658 | place names in copy | `/* v946 (2026-09-28, Laurie): + 01350100 Schoharie Reservoir (the impoundment between Prattsville and Gilboa D` |
| 660 | place names in copy | `Schoharie Reservoir' = the Shandaken Tunnel outlet at Allaben - the water the reservoir sends OUT of the` |
| 661 | place names in copy | `Schoharie basin to the Esopus and New York City (~170 ft\u00b3/s tonight). Its number sorts just before Esopus` |
| 662 | place names in copy | `Mount Marion, which is right: that gauge sees Schoharie water too. */` |
| 663 | place names in copy | `/* v947 (2026-09-28, Laurie's list): + Schoharie near Lexington 01349705 (headwater), Batavia Kill at Red Fall` |
| 664 | place names in copy | `(enters at Prattsville), Schoharie near North Blenheim 01350212 (below the Blenheim-Gilboa pumped-storage plan` |
| 666 | place names in copy | `BEFORE the Schoharie joins), Mohawk at Freeman's Bridge 01354500 (after), Normans Kill at Albany 01359528 (nea` |
| 670 | place names in copy | `Patroon Creek (unrelated), the small Schoharie tributaries (West Kill, East Kill, Bear Kill, Manor Kill, Platt` |
| 671 | place names in copy | `Kill, Mine Kill), Beaver Kill at Mt Tremper, Schoharie AT North Blenheim (duplicate of NEAR). Optional if want` |
| 673 | USGS gauges, river chains, named waters | `var STREAM_SITES = ['01347000','01349705','01349950','01350000','01350100','01350101','01350212','01350355','0` |
| 682 | USGS gauges, river chains, named waters | `var CHAINS = [` |
| 683 | place names in copy | `{key:'schoharie', name:'Schoharie Creek \u2192 Mohawk', light:'#2a78d6', dark:'#3987e5', sites:['01349705','01` |
| 686 | place names in copy | `{key:'esopus',    name:'Esopus Creek \u2192 Hudson (Catskills)', light:'#eda100', dark:'#c98500', sites:['0136` |
| 693 | place names in copy | `var WATER_CAP = {stream:99, lake:3, well:9};   /* v948/v959: pinned wells count toward the cap; 7 so the three` |
| 698 | USGS gauges, river chains, named waters | `var NAMED_WATERS = [` |
| 699 | place names in copy | `{key:'catskill', re:/catskill creek/i, label:'Catskill Creek'},` |
| 706 | place names in copy | `/* USGS names wells with no descriptive name like "Local number, So-528, Westerlo NY" - strip the ID. */` |
| 867 | place names in copy | `runs Schoharie headwaters -> Schoharie at Schoharie -> Hudson at Green Island -> Normans Kill.` |
| 976 | page titles and descriptions | `var svg='<svg viewBox="0 0 '+W+' 96" role="img" aria-label="'+waterEsc(title)+'"><title>'+waterEsc(title)+'</t` |
| 1004 | place names in copy | `(Gilboa Dam, N. Blenheim, Little Schoharie, Cobleskill, Esperance…) are simply absent. Not live: re-check year` |
| 1084 | place names in copy | `/* v963 (Laurie): Schoharie, Mohawk, Esopus, then wells, lakes, the tidal Hudson, and the Hudson head-of-tide ` |
| 1175 | place names in copy | `local waters (Normans Kill, Hudson, Catskill Creek...) are still guaranteed a card when a gauge` |
| 1223 | place names in copy | `/* v958 (2026-09-28, Laurie): one chart per river chain, each with its own axis - the Schoharie's storm rise w` |
| 1279 | place names in copy | `/* v1007 (2026-10-02, Laurie): a 40 km circle around Berne instead of the square box, whose corners reached ~5` |
| 1433 | place names in copy | `$('inat-list').innerHTML = olderHtml.length ? '<p class="sg-eye" style="margin:14px 0 4px">Hilltown Hotties: S` |
| 1442 | place names in copy | `/* ---------- eBird: recent + notable sightings near Berne (key per Laurie, 2026-09-20) ---------- */` |
| 1445 | radii and API keys | `'function fetchEBird' marker — which is what made fetchEBird() throw 'EBIRD_DIST is not defined'. */` |
| 1446 | radii and API keys | `var EBIRD_KEY='dce779eb-603d-4505-9113-a04103e6d8d5', EBIRD_DIST=25, EBIRD_BACK=14;` |
| … | | 2 more lines match place names — search the file for the names above |

## `skyline.js` — 10 line(s)

| line | what | snippet |
|---|---|---|
| 1 | place names in copy | `/* NY Hilltowners — shared Skyline widget (weather + sunrise/sunset + moon).` |
| 8 | centre point / sky point | `var BERNE = (typeof window.BERNE !== 'undefined') ? window.BERNE : {lat:42.624848, lng:-74.135036};` |
| 32 | place names in copy | `/* ============ SKYLINE: Hilltowns weather + today's sun ============` |
| 34 | place names in copy | `Preserve's coordinates (a central Hilltowns point; the Preserve isn't named` |
| 38 | centre point / sky point | `var HUYCK = {lat:42.5155081667906, lng:-74.1401693189751};` |
| 89 | place names in copy | `document.getElementById('skyWx').title = kind[1]+asOf+' \u2014 modeled current conditions for the Hilltowns (d` |
| 92 | place names in copy | `/* ---- Stratospheric wind at 10 hPa over Berne (Laurie, 2026-09-16). ~26-31 km up, the` |
| 107 | place names in copy | `document.getElementById('skyStrat').title = 'Wind at the 10 hPa pressure level over Berne, NY \u2014 the strat` |
| 256 | place names in copy | `{id:'wjff', name:'Radio Catskill', sub:'WJFF 90.5 · Jeffersonville / Sullivan County', url:'https://stream1.rc` |
| 257 | place names in copy | `{id:'wamc', name:'WAMC', sub:'Northeast Public Radio · Albany', url:'https://playerservices.streamtheworld.com` |

## `water.js` — 23 line(s)

| line | what | snippet |
|---|---|---|
| 1 | place names in copy | `/* water.js — v982 (2026-09-29, Laurie): the Helderberg–Hudson water-quality dashboard (waterwip.html).` |
| 22 | place names in copy | `var TXNAME = { north: 'North · Basic Creek → Alcove → Hannacroix → Hudson at Coeymans', south: 'South · Myosot` |
| 23 | place names in copy | `var ZONECOL = { 'plateau (Hilltowns)': '#199e70', 'Catskill Creek valley / Greene': '#c98500', 'Albany lowland` |
| 44 | place names in copy | `function txOf(s) { if (/comparison/i.test(s.symbol_hint ¦¦ '') ¦¦ s.site_id === 'NYC_DEP_PWS') return 'compare` |
| 213 | place names in copy | `if (rows.length) { var draw = function () { var on = {}; $('cp-med').querySelectorAll('input').forEach(functio` |
| 226 | USGS gauges, river chains, named waters | `var CHAINS = {` |
| 256 | place names in copy | `Object.keys(pos).forEach(function (k) { var p = pos[k], s = p.s, col = COL[p.tx], hl = headline(s), yr = lates` |
| 258 | place names in copy | `$('tx').innerHTML = '<svg class="tx-svg" viewBox="0 0 ' + Wd + ' ' + H + '" role="img" aria-label="Two transec` |
| 277 | page titles and descriptions | `if (yrs.length) o += '<text class="m" x="0" y="22">2012–18</text>' + yrs.map(function (yr) { var r = hist.filt` |
| 283 | place names in copy | `front += '<div class="row">' + (t === 'compare' ? '<span class="chip na">comparison · 33 km W, across the Scho` |
| 325 | place names in copy | `var STREAM_NOTE = { BASIC_CREEK_STREAM: 'Basic Creek — north transect; mile 4.7 is below the reservoir, mile 1` |
| 354 | place names in copy | `var LAKE_NAME = { VLY_CREEK_RES: 'Vly Creek Reservoir', HELDERBERG_LAKE: 'Helderberg Lake' };` |
| 372 | place names in copy | `/* v998: the NYC comparison — Schoharie Reservoir, annual mean TP (all seasons, DEP), against DEP's 15 µg/L be` |
| 374 | place names in copy | `var B = (W.nyc_bench ¦¦ []).filter(function (r) { return r.reservoir === 'Schoharie'; }); var tp = B.filter(fu` |
| 382 | place names in copy | `tp.forEach(function (r) { var t = tb[r.report_year]; o += '<circle cx="' + xs(r.report_year) + '" cy="' + ys(r` |
| 384 | place names in copy | `return '<div class="sg-chart" style="border:1px dashed ' + col + ';border-left:4px dashed ' + col + '"><div cl` |
| 423 | page titles and descriptions | `years.forEach(function (y, i) { var yy = T + i * rowH; o += '<text class="lbl dim" x="' + (L - 8) + '" y="' + ` |
| 472 | page titles and descriptions | `o += '<rect x="' + L + '" y="' + y + '" width="' + (xs(2011.5) - L) + '" height="' + ROW.bl + '" fill="url(#ix` |
| 592 | place names in copy | `var col = COL[txOf(S[Object.keys(SITE_PERMIT).filter(function (k) { return SITE_PERMIT[k] === p.npdes_id; })[0` |
| 605 | place names in copy | `$('outfalls').innerHTML = render(near) + (far.length ? '<details class="sg-more"><summary>' + far.length + ' m` |
| 667 | place names in copy | `$('tri-near').innerHTML = '<div class="tri-scroll"><table class="ddtab tri-tab"><thead><tr><th>Facility</th><t` |
| 710 | place names in copy | `$('prov-summary').innerHTML = 'Workbook <code>helderberg_hudson_water_quality.xlsx</code>, built ' + esc(W.gen` |
| 712 | place names in copy | `$('wq-foot').innerHTML = '<b>Sources.</b> NYSDEC Waterbody Inventory / Priority Waterbodies List factsheets; N` |

## `build/build.py` — 37 line(s)

| line | what | snippet |
|---|---|---|
| 128 | stations, cache URLs, hearts namespace | `PREVIEW_CACHE_URL = "https://nyhilltowners.com/" + PREVIEW_CACHE_FILE` |
| 173 | stations, cache URLs, hearts namespace | `headers={"User-Agent": "Mozilla/5.0 (compatible; AtlasBuild/1.0)"})` |
| 215 | stations, cache URLs, hearts namespace | `url, headers={"User-Agent": "Mozilla/5.0 (compatible; AtlasBuild/1.0)"})` |
| 1131 | stations, cache URLs, hearts namespace | `HEARTS_NS = "nyhilltowners-explore-hills"` |
| 1133 | stations, cache URLs, hearts namespace | `HEARTS_URL = "https://nyhilltowners.com/" + HEARTS_FILE` |
| 1142 | stations, cache URLs, hearts namespace | `headers={"User-Agent": "Mozilla/5.0 (compatible; AtlasBuild/1.0)"})` |
| 1164 | stations, cache URLs, hearts namespace | `req = urllib.request.Request(HEARTS_URL, headers={"User-Agent": "Mozilla/5.0 (compatible; AtlasBuild/1.0)"})` |
| 1268 | page titles and descriptions | `html = html.replace("<title>", "<title>WIP map — ", 1)` |
| 1284 | stations, cache URLs, hearts namespace | `req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (HilltownsAtlas preview)"})` |
| 1331 | place names in copy | `# Albany Intl AP, 1938→) → site/station_dd.js. Per year, cumulative HDD/CDD (base 65 on the` |
| 1336 | stations, cache URLs, hearts namespace | `DAILY_STATIONS = {"alcove_dam", "albany_ap", "slide_mountain", "cobleskill_2ese", "indian_lake_2sw", "old_forg` |
| 1337 | stations, cache URLs, hearts namespace | `STATIONS = [   # (slug, display name, elevation ft, active?)  — see data/stations/README.md` |
| 1346 | place names in copy | `("albany_ap",       "Albany Intl Airport (ALB)",            285,  True),` |
| 1364 | place names in copy | `("berne_2s",              "Berne 2 S (co-op) · Albany Co. — elev. approx.",                 1300, False),  # 1` |
| 1365 | place names in copy | `("berne_5sw",             "Berne 5 SW (co-op) · Albany Co. — elev. approx.",                1500, False),  # 1` |
| 1366 | place names in copy | `("east_berne",            "East Berne 2.7 NE (CoCoRaHS) · Albany Co. — elev. approx.",      1200, True),   # 2` |
| 1369 | place names in copy | `("rensselaerville_21nnw", "Rensselaerville 2.1 NNW (CoCoRaHS) · Albany Co. — elev. approx.", 1550, True),   # ` |
| 1370 | place names in copy | `("rensselaerville_2nw",   "Rensselaerville 2 NW (co-op) · Albany Co. — elev. approx.",       1550, False),  # ` |
| 1371 | place names in copy | `("westerlo_2",            "Westerlo (co-op) · Albany Co. — elev. approx.",                  1550, False),  # 1` |
| 1372 | place names in copy | `("clarksville",           "Clarksville 2.7 S (CoCoRaHS) · Albany Co. — elev. approx.",        600, False),  # ` |
| 1380 | place names in copy | `("altamont_29sw",   "Altamont 2.9 SW (CoCoRaHS) · Albany Co. — elev. approx.",        900, False),  # 2019-05 ` |
| 1381 | place names in copy | `("altamont_04se",   "Altamont 0.4 SE (CoCoRaHS) · Albany Co. — elev. approx.",        700, True),   # 2023-06 ` |
| 1382 | place names in copy | `("altamont_35nw",   "Altamont 3.5 NW (CoCoRaHS) · Albany Co. — elev. approx.",       1100, True),   # 2021-07 ` |
| 1383 | place names in copy | `("altamont_27ssw",  "Altamont 2.7 SSW (CoCoRaHS) · Albany Co. — elev. approx.",       800, True),   # 2007-11 ` |
| 1386 | place names in copy | `("berne_2nw",       "Berne 2 NW (co-op) · Albany Co. — elev. approx.",               1400, False),  # 1963-08 ` |
| 1387 | place names in copy | `("catskill_41nnw",  "Catskill 4.1 NNW (CoCoRaHS) · Greene Co. — elev. approx.",       500, True),   # 2024-06 ` |
| 1388 | place names in copy | `("fleischmanns_57n","Fleischmanns 5.7 N (CoCoRaHS) · Delaware Co. — elev. approx.",  2000, False),  # 2015-01 ` |
| 1389 | place names in copy | `("knox",            "Knox (co-op, historic) · Albany Co. — elev. approx.",           1600, False),  # 2000-01 ` |
| 1390 | place names in copy | `("ravena_14nnw",    "Ravena 1.4 NNW (CoCoRaHS) · Albany Co. — elev. approx.",         200, True),   # 2018-10 ` |
| 1391 | place names in copy | `# 2026-09-27 (v910, atlas session) (Laurie): third batch. Two exceptional finds — West Berne is the oldest and` |
| 1393 | place names in copy | `# Hilltowns, both in DAILY_STATIONS. Freehold 2 NW is a solid mid-century real-temp record too.` |
| 1398 | place names in copy | `("middleburgh_63ese", "Middleburgh 6.3 ESE (CoCoRaHS) · Schoharie Co. — elev. approx.",  1000, False),  # 2021` |
| 1400 | place names in copy | `("preston_hollow",    "Preston Hollow (co-op) · Albany Co. — elev. approx.",              900, False),  # 1948` |
| 1401 | place names in copy | `("voorheesville",     "Voorheesville (co-op, historic) · Albany Co. — elev. approx.",     300, False),  # 1950` |
| 1402 | place names in copy | `("west_berne",        "West Berne (co-op, historic) · Albany Co. — elev. approx.",       1300, False),  # 1898` |
| 1474 | place names in copy | `"""v982 (2026-09-29, Laurie): the Helderberg–Hudson water-quality master (data/water/) → site/data_water.js.` |
| 1560 | place names in copy | `# of Albany Hill") → site/phenology_expected.js. One record per "### N. Name — Mon D–D" heading` |

## `build/water.py` — 6 line(s)

| line | what | snippet |
|---|---|---|
| 2 | place names in copy | `water.py — v982 (2026-09-29, Laurie): the Helderberg–Hudson water-quality emitter.` |
| 618 | place names in copy | `# the AWQR PDF, or the data.ny.gov dataset. Distance from Rensselaerville computed here (equirectangular).` |
| 688 | place names in copy | `# v998: NYC DEP reservoir benchmarks (comparison node) — Schoharie (nearest, 33 km W) and Kensico (terminal), ` |
| 694 | place names in copy | `if r.get("reservoir") in ("Schoharie", "Kensico") and r.get("analyte") in ("Total phosphorus", "Turbidity", "C` |
| 725 | place names in copy | `"ref": {"name": "Rensselaerville hamlet", "lat": 42.515, "lon": -74.145, "elev_ft": 1500,` |
| 726 | place names in copy | `"note": "every km_from_ref column measures from here (Hannacroix / Catskill Creek divide)"},` |

## `partials/header.html` — 2 line(s)

| line | what | snippet |
|---|---|---|
| 8 | place names in copy | `<span class="stack"><span class="l1">Hilltowns</span><span class="l2">Field Guide</span></span>` |
| 15 | place names in copy | `<div class="sky-g sky-sun" title="Today's sunrise and sunset, Berne time">` |

## `partials/footer.html` — 2 line(s)

| line | what | snippet |
|---|---|---|
| 3 | place names in copy | `<div>A community project of the NY Hilltowners.</div>` |
| 14 | place names in copy | `<a href="https://instagram.com/NYHilltowners" target="_blank" rel="noopener">@NYHilltowners</a>` |

## `manifest.json` — 1 line(s)

| line | what | snippet |
|---|---|---|
| 2 | category names / title | `"site_title": "Explore These Hills — Catskill & Beyond",` |

## Content files to replace entirely

- `data/points_of_interest.xlsx` — example rows only; your categories (rename sheets AND manifest.json together).
- `data/events.xlsx` — example rows; ingestor-owned once the events chat exists.
- `data/folklore_legends.xlsx`, `data/climate_events.xlsx`, `data/microseasons.xlsx` + `data/microseasons.md` — templates; each is a research project of its own.
- `data/stations/` — empty; export from xmACIS2 (see README there) and register in `build/build.py STATIONS`.
- `data/water/` — empty; only if the region wants a water page (needs its own research chat and workbook with cell-colour provenance).
- `images/` — Hilltowns share card, favicons and raccoon mark are still here; replace.
- `HANDOFF_README.md` — the Hilltowns log, kept for reference. Start your own `HANDOFF_README.md` from its "Where things stand" / log / delivery-ritual structure and cut the Hilltowns history.
