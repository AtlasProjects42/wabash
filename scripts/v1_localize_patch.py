#!/usr/bin/env python3
# v1 (2026-10-06): applied ONCE to turn the starter kit into the Navigators Guide v1 tree. Kept for the record; do not re-run (every substitution asserts the pre-patch text). The moon-name move (skyline.js → place.json moons) and the epigraph token were done by hand afterwards.
"""v1 localisation patch: make every file in LOCALIZE.md read config/place.json.
Each substitution asserts the original text is present exactly once (or `count` times),
so a miss is a loud failure, never a silent skip. Run once from the kit root."""
import re, sys, json
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
CHANGED = set()

def rd(p): return (ROOT / p).read_text(encoding="utf-8")
def wr(p, s): (ROOT / p).write_text(s, encoding="utf-8"); CHANGED.add(p)

def sub(p, old, new, count=1):
    s = rd(p)
    n = s.count(old)
    if n != count:
        raise SystemExit(f"PATCH FAIL {p}: expected {count} of {old[:70]!r}, found {n}")
    wr(p, s.replace(old, new))

def rsub(p, pattern, new, count=1, flags=0):
    s = rd(p)
    rx = re.compile(pattern, flags)
    n = len(rx.findall(s))
    if n != count:
        raise SystemExit(f"PATCH FAIL {p}: regex {pattern[:70]!r} expected {count}, found {n}")
    wr(p, rx.sub(lambda m: new, s))

def rsub_all(p, pattern, new, flags=0, min_count=1):
    s = rd(p); rx = re.compile(pattern, flags); n = len(rx.findall(s))
    if n < min_count:
        raise SystemExit(f"PATCH FAIL {p}: regex {pattern[:70]!r} expected >= {min_count}, found {n}")
    wr(p, rx.sub(lambda m: new, s))

PAGES = ["index.template.html", "calendar.html", "directory.html", "about.html", "signals.html",
         "society.html", "bulletin.html", "instagram.html", "tradingpost.html", "waterwip.html"]

# ---------------------------------------------------------------- build.py
B = "build/build.py"
sub(B, 'SITE = ROOT / "site"\n', '''SITE = ROOT / "site"

# ---------------------------------------------------------------------------
# v1 (2026-10-06, Laurie): config/place.json is the single source of every place-specific value.
# build.py reads it here; pages get {{place.a.b}} tokens stamped by stamp_place(); browser code
# reads window.PLACE from site/place.js (emitted by emit_place_js and injected into every page).
# ---------------------------------------------------------------------------
import html as _html
PLACE_FILE = ROOT / "config" / "place.json"
if not PLACE_FILE.exists():
    sys.exit("ERROR: config/place.json missing — it is the first file of a new build (see BRIEF.md §6)")
PLACE = json.loads(PLACE_FILE.read_text(encoding="utf-8"))

def pget(path, default=None):
    """Dotted lookup into PLACE: pget('center.lat')."""
    cur = PLACE
    for k in path.split("."):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur

def _place_derive():
    """Values pages need that are computed from the raw config (never typed twice)."""
    ig = (PLACE.get("instagram") or "").strip().lstrip("@")
    PLACE["instagram"] = ig
    PLACE["instagram_url"] = f"https://instagram.com/{ig}" if ig else ""
    PLACE["instagram_handle"] = f"@{ig}" if ig else ""
    PLACE["domain"] = (PLACE.get("domain") or "").strip()
    PLACE["share_card_url"] = PLACE["domain"].rstrip("/") + "/images/share-card.png" if PLACE["domain"] else ""
    landing = PLACE.get("landing", "calendar")
    if landing not in ("atlas", "calendar"):
        sys.exit(f"ERROR: place.json landing must be 'atlas' or 'calendar', got {landing!r}")
    PLACE["href_atlas"] = "index.html" if landing == "atlas" else "atlas.html"
    PLACE["href_calendar"] = "index.html" if landing == "calendar" else "calendar.html"
    c = PLACE["center"]
    for k in ("lat", "lng"):
        if not isinstance(c.get(k), (int, float)) or c[k] == 0:
            sys.exit(f"ERROR: place.json center.{k} is unset — fill config/place.json before building")
    if not (-90 <= c["lat"] <= 90 and -180 <= c["lng"] <= 180):
        sys.exit("ERROR: place.json center out of range")
    PLACE["center"]["elev_txt"] = f"~{int(c.get('elev_ft') or 0):,} ft"
    try:
        import zoneinfo; zoneinfo.ZoneInfo(PLACE["timezone"])
    except Exception as e:
        sys.exit(f"ERROR: place.json timezone {PLACE.get('timezone')!r} is not a valid IANA zone ({e})")
_place_derive()

def now_local():
    """Now, in the region's own zone — never the build machine's (BRIEF §10)."""
    import zoneinfo
    return datetime.datetime.now(zoneinfo.ZoneInfo(PLACE["timezone"]))

UA = PLACE.get("user_agent") or "Mozilla/5.0 (compatible; FieldGuideBuild/1.0)"

_TOKEN_RX = re.compile(r"\\{\\{place\\.([a-z0-9_.]+)\\}\\}")
_IF_RX = re.compile(r"<!-- @@if:([a-z0-9_.]+) -->(.*?)<!-- @@endif -->", re.S)
_TICKER_RX = re.compile(r"<!-- @@ticker -->")
_GOAT_RX = re.compile(r"<!-- GoatCounter[^\\n]*\\n?<script data-goatcounter=[^<]*</script>\\n?|<script data-goatcounter=[^<]*</script>\\n?")

def stamp_place(html, where):
    """{{place.x.y}} → HTML-escaped value; <!-- @@if:x -->…<!-- @@endif --> kept only when x is truthy;
    <!-- @@ticker --> → one <span> per PLACE.ticker line; unknown tokens are build warnings, never left in."""
    def _if(m):
        return m.group(2) if pget(m.group(1)) else ""
    html = _IF_RX.sub(_if, html)
    def _tok(m):
        v = pget(m.group(1))
        if v is None or isinstance(v, (dict, list)):
            WARNS.append(f"{where}: unknown or non-scalar place token {m.group(0)}")
            return ""
        return _html.escape(str(v), quote=True)
    html = _TOKEN_RX.sub(_tok, html)
    tick = "".join(f'<span><span class="tg">\\U00013153</span> {_html.escape(str(t))}</span>\\n    ' for t in PLACE.get("ticker", []))
    html = _TICKER_RX.sub(lambda m: tick, html)
    return html

def inject_place_runtime(html):
    """site/place.js before </head> (so every inline script can read window.PLACE), analytics before
    </body> only when place.json names a GoatCounter site."""
    if '<script src="place.js">' not in html:
        html = html.replace("</head>", '<script src="place.js"></script>\\n</head>', 1)
    gc = (pget("analytics.goatcounter") or "").strip()
    if gc:
        html = html.replace("</body>", f'<!-- GoatCounter: privacy-friendly analytics, no cookies, no personal data -->\\n<script data-goatcounter="https://{gc}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\\n</body>', 1)
    return html

def emit_place_js():
    pub = {k: v for k, v in PLACE.items() if not k.startswith("_")}
    for k in ("weather", "water", "towns", "calendar"):
        if isinstance(pub.get(k), dict):
            pub[k] = {kk: vv for kk, vv in pub[k].items() if not kk.startswith("_")}
    js = json.dumps(pub, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\\\/")
    (SITE / "place.js").write_text("window.PLACE = " + js + ";\\nwindow.CENTER = window.PLACE.center;\\nwindow.TZ = window.PLACE.timezone;\\n", encoding="utf-8")
    print(f"  place.js: {PLACE['brand']} · centre {PLACE['center']['lat']},{PLACE['center']['lng']} · {PLACE['timezone']} · landing {PLACE.get('landing')}")
''')

sub(B, 'PREVIEW_CACHE_URL = "https://nyhilltowners.com/" + PREVIEW_CACHE_FILE',
       'PREVIEW_CACHE_URL = (PLACE["domain"].rstrip("/") + "/" + PREVIEW_CACHE_FILE) if PLACE["domain"] else ""   # v1: from place.json')
sub(B, 'NO_PREVIEW_HOSTS = ("instagram.com", "greatnortherncatskills.com")',
       'NO_PREVIEW_HOSTS = tuple(PLACE.get("no_preview_hosts", ["instagram.com"]))   # v1: from place.json')
sub(B, 'headers={"User-Agent": "Mozilla/5.0 (compatible; AtlasBuild/1.0)"}', 'headers={"User-Agent": UA}', count=4)
sub(B, 'headers={"User-Agent": "Mozilla/5.0 (HilltownsAtlas preview)"}', 'headers={"User-Agent": UA}')
sub(B, 'HEARTS_NS = "nyhilltowners-explore-hills"', 'HEARTS_NS = PLACE.get("hearts_namespace") or "field-guide"   # v1: from place.json')
sub(B, 'HEARTS_URL = "https://nyhilltowners.com/" + HEARTS_FILE', 'HEARTS_URL = (PLACE["domain"].rstrip("/") + "/" + HEARTS_FILE) if PLACE["domain"] else ""')
sub(B, 'today = datetime.datetime.utcnow().strftime("%Y-%m-%d")', 'today = now_local().strftime("%Y-%m-%d")')
sub(B, '(SITE / HEARTS_FILE).write_text(json.dumps({"updated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),',
       '(SITE / HEARTS_FILE).write_text(json.dumps({"updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),')
# the preview-cache / hearts fetchers must not try to fetch from an empty domain
sub(B, 'def load_preview_cache():\n', 'def load_preview_cache():\n    if not PREVIEW_CACHE_URL:\n        print("  previews: no domain in place.json yet — cache not fetched (fine for a first build)")\n        return\n')

# stations → place.json
s = rd(B)
m = re.search(r'DAILY_STATIONS = \{.*?\nSTATIONS = \[.*?\n\]\n', s, re.S)
assert m, "stations block not found"
s = s[:m.start()] + '''# v1 (2026-10-06): the station register lives in config/place.json → weather.stations, one object per
# data/stations/<slug>.csv: {"slug","name","elev_ft","active","daily","lat","lng"}. daily=true ships raw daily
# highs/lows for the year charts (continuous records only); lat/lng only matter for closed stations with
# daily temps (a modeled current-year line is drawn at the place). See data/stations/README.md.
_ST = PLACE.get("weather", {}).get("stations", []) or []
DAILY_STATIONS = {st["slug"] for st in _ST if st.get("daily")}
STATIONS = [(st["slug"], st["name"], int(st.get("elev_ft") or 0), bool(st.get("active", True))) for st in _ST]
''' + s[m.end():]
wr(B, s)
s = rd(B)
m = re.search(r'STATION_COORDS = \{.*?\n\}\n', s, re.S)
assert m, "STATION_COORDS not found"
s = s[:m.start()] + 'STATION_COORDS = {st["slug"]: (st["lat"], st["lng"]) for st in _ST if st.get("lat") is not None and st.get("lng") is not None}\nSTATION_COORDS.update({k: tuple(v) for k, v in (PLACE.get("weather", {}).get("station_coords") or {}).items()})\n' + s[m.end():]
wr(B, s)

# emit_page: stamp tokens + runtime; main: landing page + place.js
sub(B, '''def emit_page(src, out_name: str) -> None:
    html = Path(src).read_text(encoding="utf-8")
    (SITE / out_name).write_text(apply_partials(html, out_name), encoding="utf-8")''',
'''def emit_page(src, out_name: str) -> None:
    html = Path(src).read_text(encoding="utf-8")
    html = apply_partials(html, out_name)
    html = stamp_place(html, f"{Path(src).name} -> {out_name}")   # v1: {{place.*}} tokens, @@if, @@ticker
    html = inject_place_runtime(html)
    (SITE / out_name).write_text(html, encoding="utf-8")''')
sub(B, '''    html = html.replace("<title>", "<title>WIP map — ", 1)
    (SITE / "wipmap.html").write_text(apply_partials(html, "atlas.html"), encoding="utf-8")''',
'''    html = html.replace("<title>", "<title>WIP map — ", 1)
    html = inject_place_runtime(stamp_place(apply_partials(html, PLACE["href_atlas"]), "index.template.html -> wipmap.html"))
    (SITE / "wipmap.html").write_text(html, encoding="utf-8")''')
sub(B, '''    emit_page(template, "atlas.html")      # 2026-09-18 (Laurie): the map now lives at atlas.html''',
'''    emit_place_js()                        # v1 (2026-10-06): window.PLACE for every page, from config/place.json
    emit_page(template, "atlas.html")      # 2026-09-18 (Laurie): the map now lives at atlas.html
    if PLACE.get("landing") == "atlas":
        emit_page(template, "index.html")  # v1: place.json "landing": "atlas" — the map is the front door''')
sub(B, '''            emit_page(ROOT / name, "index.html" if name == "calendar.html" else name)   # calendar (list view) is the landing page''',
'''            emit_page(ROOT / name, "index.html" if (name == "calendar.html" and PLACE.get("landing") == "calendar") else name)   # v1: landing page per place.json''')
# the nav highlight for the landing page: _mark_active is keyed on out_name, which is index.html — fine.

# ---------------------------------------------------------------- manifest.json
M = "manifest.json"
sub(M, '  "site_title": "Explore These Hills — Catskill & Beyond",\n', '  "_site_title": "moved to config/place.json (site_title) — v1 2026-10-06",\n')
sub(M, '''      "glyph": "🕳️",
      "color": "#5b4636",
      "default_on": false
    },''', '''      "glyph": "🕳️",
      "color": "#5b4636",
      "default_on": false,
      "nearby": false
    },''')

# ---------------------------------------------------------------- shared partials
H = "partials/header.html"
sub(H, '<span class="stack"><span class="l1">Hilltowns</span><span class="l2">Field Guide</span></span>',
       '<span class="stack"><span class="l1">{{place.brand_line1}}</span><span class="l2">{{place.brand_line2}}</span></span>')
sub(H, "Today's sunrise and sunset, Berne time", "Today's sunrise and sunset, {{place.center.short}} time")
NAV_OLD = '''        <a href="index.html">Calendar</a>
    <a href="atlas.html">Atlas</a>
'''
NAV_NEW = '''    <a href="{{place.href_atlas}}">Atlas</a>
    <a href="{{place.href_calendar}}">Calendar</a>
'''
sub(H, NAV_OLD, NAV_NEW)
sub(H, '<a href="instagram.html" class="ig hd-ig"', '<!-- @@if:instagram --><a href="instagram.html" class="ig hd-ig"')
s = rd(H)
# close the @@if after that anchor's closing tag
i = s.index('<!-- @@if:instagram --><a href="instagram.html" class="ig hd-ig"'); j = s.index("</a>", i) + 4
s = s[:j] + "<!-- @@endif -->" + s[j:]
wr(H, s)

F = "partials/footer.html"
sub(F, "<div>A community project of the NY Hilltowners.</div>", "<div>{{place.brand}} &mdash; a community project.</div>")
sub(F, NAV_OLD, NAV_NEW)
sub(F, '''    <a href="instagram.html">Instagram</a>
''', '''    <!-- @@if:instagram --><a href="instagram.html">Instagram</a><!-- @@endif -->
''')
sub(F, '''    <a href="https://instagram.com/NYHilltowners" target="_blank" rel="noopener">@NYHilltowners</a>
''', '''    <!-- @@if:instagram --><a href="{{place.instagram_url}}" target="_blank" rel="noopener">{{place.instagram_handle}}</a><!-- @@endif -->
''')

# ---------------------------------------------------------------- every page: tickers, email, goatcounter, timezone, instagram
TICK_ITEM = re.compile(r'    <span><span class="tg">\U00013153</span> (?!<a class="share-link)[^\n]*</span>\n')
for p in PAGES:
    s = rd(p)
    # ticker sets: collapse the editorial items to one marker per set (share-item stays)
    def _set(m):
        body = TICK_ITEM.sub("", m.group(0))
        return body.replace('<span class="ticker-set"', '<span class="ticker-set"', 1).replace("\n", "\n    <!-- @@ticker -->\n", 1)
    s2 = re.sub(r'<span class="ticker-set"[^>]*>\n(?:    <span[^\n]*\n)+?  </span>', _set, s)
    s2 = re.sub(r'<!-- GoatCounter[^\n]*\n\s*<script data-goatcounter=[^<]*</script>\n?', "", s2)
    s2 = re.sub(r'<script data-goatcounter=[^<]*</script>\n?', "", s2)
    s2 = s2.replace("timeZone:'America/New_York'", "timeZone:window.PLACE.timezone").replace('timeZone:"America/New_York"', "timeZone:window.PLACE.timezone")
    s2 = s2.replace("NYHilltowners@Gmail.com", "{{place.contact_email}}").replace("NYHilltowners@gmail.com", "{{place.contact_email}}").replace("nyhilltowners@gmail.com", "{{place.contact_email}}")
    s2 = s2.replace('https://instagram.com/NYHilltowners', '{{place.instagram_url}}').replace('@NYHilltowners', '{{place.instagram_handle}}')
    wr(p, s2)

# titles / og — per page
def head(p, title, desc, og_title=None):
    rsub(p, r'<title>[^<]*</title>', f'<title>{title}</title>')
    rsub(p, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">')
    rsub(p, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{og_title or title}">')
head("index.template.html", "{{place.brand}} — {{place.region_short}}", "{{place.tagline}}", "{{place.brand}}")
sub("index.template.html", '<meta property="og:description" content="Folklore, history &amp; daily life in the NY Helderberg-Hudson Hilltowns — mapped.">',
    '<meta property="og:description" content="{{place.tagline}}">')
sub("index.template.html", '<meta property="og:image" content="https://nyhilltowners.github.io/explore-the-hilltowns/images/share-card.png">\n<meta property="og:url" content="https://nyhilltowners.github.io/explore-the-hilltowns/">',
    '<meta property="og:image" content="{{place.share_card_url}}">\n<meta property="og:url" content="{{place.domain}}">')
head("calendar.html", "Event Calendar — {{place.brand}}", "Upcoming events across {{place.region_short}} — a community event calendar.")
head("directory.html", "Directory — {{place.brand}}", "An A–Z directory of the organizations and businesses on {{place.brand}} — {{place.region_short}}.")
head("about.html", "About — {{place.brand}}", "About {{place.brand}} — a living field guide to {{place.region_short}}.")
head("signals.html", "Signs + Signals — {{place.brand}}", "Sun, moon, weather, winds aloft and degree days for {{place.region_short}} — the natural cycles, on one dashboard.")
head("society.html", "Society Pages — {{place.brand}}", "Who's getting noticed in {{place.region_short}} this fortnight — iNaturalist observations and eBird sightings around {{place.center.short}}.")
head("bulletin.html", "Bulletin — {{place.brand}}", "{{place.short_name}} Bulletin — pin a card for your show, your sale, your haiku or your birthday shoutout.")
head("instagram.html", "Instagram — {{place.brand}}", "Our latest posts from {{place.instagram_handle}} on Instagram.")
head("tradingpost.html", "Trading Post — {{place.brand}}", "Shop locally, without leaving your nook — the {{place.short_name}} Trading Post.", "{{place.short_name}} Trading Post")
head("waterwip.html", "Water — {{place.brand}}", "Water: what the public record says about the water around {{place.region_short}}.")

# ---------------------------------------------------------------- index.template.html (atlas)
I = "index.template.html"
sub(I, "(sunset→sunrise at Berne, NY) or by the header sun/moon toggle.", "(sunset→sunrise at the place.json centre) or by the header sun/moon toggle.")
sub(I, 'title="Night mode follows sunset and sunrise in Berne, NY. Tap to switch until the next one."', 'title="Night mode follows sunset and sunrise at {{place.center.short}}. Tap to switch until the next one."')
sub(I, '''      <div class="sidefoot"><a href="about.html">About this atlas</a> &middot; <a href="{{place.instagram_url}}" target="_blank" rel="noopener">{{place.instagram_handle}}</a></div>''',
       '''      <div class="sidefoot"><a href="about.html">About this atlas</a><!-- @@if:instagram --> &middot; <a href="{{place.instagram_url}}" target="_blank" rel="noopener">{{place.instagram_handle}}</a><!-- @@endif --></div>''')
sub(I, '''        <h2>Hilltowns Field Guide</h2>
        <div class="field"><div class="fv story">A living atlas of the NY Helderberg-Hudson
        Hilltowns &mdash; folklore and legends gathered from historical sources, alongside
        the people making and telling stories today. Every tale lists its original teller
        and source, stories are only as reliable as their tellers.</div></div>
        <div class="field"><div class="fv story">Additions, suggestions, corrections,
        complaints about the universe? Message us on Instagram at
        <a class="weblink" href="{{place.instagram_url}}" target="_blank"
        rel="noopener">{{place.instagram_handle}}</a></div></div>''',
'''        <h2>{{place.brand}}</h2>
        <div class="field"><div class="fv story">{{place.about_text}}</div></div>
        <!-- @@if:instagram --><div class="field"><div class="fv story">Additions, suggestions, corrections,
        complaints about the universe? Message us on Instagram at
        <a class="weblink" href="{{place.instagram_url}}" target="_blank"
        rel="noopener">{{place.instagram_handle}}</a></div></div><!-- @@endif -->
        <!-- @@if:contact_email --><div class="field"><div class="fv story">Additions, suggestions, corrections? Email
        <a class="weblink" href="mailto:{{place.contact_email}}">{{place.contact_email}}</a></div></div><!-- @@endif -->''')
sub(I, 'var HOME = [-74.1436, 42.5145]; /* Rensselaerville, NY (lng,lat) */',
       'var HOME = [window.PLACE.map_home.lng, window.PLACE.map_home.lat]; /* v1: map centre (lng,lat) from config/place.json */')
sub(I, '''   The atlas keeps Hilltowns time: night mode runs from sunset to sunrise at
   Berne, NY for every visitor, wherever they are. Coordinates are Berne Town
   Hall's own POI row (1656 Helderberg Trail). The sunrise equation below is''',
'''   The atlas keeps the region's own time: night mode runs from sunset to sunrise at
   the place.json centre for every visitor, wherever they are. The sunrise equation below is''')
sub(I, 'var BERNE = {lat:42.624848, lng:-74.135036};', 'var CENTER = window.PLACE.center;   /* v1: sky point from config/place.json */')
sub(I, "center:HOME, zoom:10.9,   /* regional default: Cobleskill–Hudson River, Central Bridge–Windham (Laurie, Aug 29) */",
       "center:HOME, zoom:window.PLACE.map_home.zoom,   /* v1: from config/place.json */")
sub(I, "/* \"today\" pinned to the atlas's home timezone so events expire on Catskill time */", "/* \"today\" pinned to the region's timezone (place.json) so events expire on local time, not the viewer's */")
sub(I, "var LIKE_NS = 'nyhilltowners-explore-hills';", "var LIKE_NS = window.PLACE.storage_keys.likes_ns;   /* v1: from place.json */")
sub(I, "var TK='hilltowns_share_token';", "var TK=window.PLACE.storage_keys.share_token;")
sub(I, "it reuses this page's BERNE and", "it reuses this page's CENTER and")
sub(I, "the Helderberg relief, then an ember wash", "the hillshade relief, then an ember wash")
rsub_all(I, r"\bBERNE\b", "CENTER")
rsub_all(I, r"\bberneDateISO\b", "homeDateISO")

# ---------------------------------------------------------------- skyline.js
K = "skyline.js"
sub(K, "/* NY Hilltowners — shared Skyline widget", "/* Shared Skyline widget")
sub(K, "var BERNE = (typeof window.BERNE !== 'undefined') ? window.BERNE : {lat:42.624848, lng:-74.135036};",
       "var CENTER = window.CENTER || window.PLACE.center;   /* v1: from site/place.js (config/place.json) */")
sub(K, "/* ============ SKYLINE: Hilltowns weather + today's sun ============\n   Weather is Open-Meteo's modeled current conditions, sampled at the Huyck\n   Preserve's coordinates (a central Hilltowns point; the Preserve isn't named\n   in the UI and isn't affiliated).",
       "/* ============ SKYLINE: regional weather + today's sun ============\n   Weather is Open-Meteo's modeled current conditions, sampled at\n   place.json weather.open_meteo_point (a central point; not named in the UI).")
sub(K, "var HUYCK = {lat:42.5155081667906, lng:-74.1401693189751};", "var WX_POINT = window.PLACE.weather.open_meteo_point;   /* v1: from place.json */")
rsub_all(K, r"\bHUYCK\b", "WX_POINT")
sub(K, "modeled current conditions for the Hilltowns (data: Open-Meteo.com)", "modeled current conditions for '+window.PLACE.region_short+' (data: Open-Meteo.com)")
sub(K, "/* ---- Stratospheric wind at 10 hPa over Berne (Laurie, 2026-09-16).", "/* ---- Stratospheric wind at 10 hPa over the centre point (Laurie, 2026-09-16).")
sub(K, "'Wind at the 10 hPa pressure level over Berne, NY \\u2014 the stratosphere, '", "'Wind at the 10 hPa pressure level over '+CENTER.short+' \\u2014 the stratosphere, '")
sub(K, "&timezone=America%2FNew_York", "&timezone='+encodeURIComponent(window.PLACE.timezone)+'", count=2)
s = rd(K)
m = re.search(r"  var STATIONS = \[\n.*?\n  \];\n", s, re.S)
assert m and "Standing Wave" in m.group(0), "radio STATIONS block not found"
s = s[:m.start()] + "  var STATIONS = (window.PLACE.radio || []).filter(function(s){ return s && s.url; });   /* v1: presets live in config/place.json → radio */\n  if(!STATIONS.length) return;   /* no presets configured: no tuner */\n" + s[m.end():]
wr(K, s)
rsub_all(K, r"\bBERNE\b", "CENTER")
rsub_all(K, r"\bberneDateISO\b", "homeDateISO")
sub(K, "timeZone:'America/New_York'", "timeZone:window.PLACE.timezone", count=3)

# ---------------------------------------------------------------- signals.js
S = "signals.js"
sub(S, "Phenology / natural-cycles dashboard for Berne, NY. Reuses skyline.js (loaded first)\n   for BERNE,", "Phenology / natural-cycles dashboard for the place.json centre. Reuses skyline.js (loaded first)\n   for CENTER,")
sub(S, "var LAT = (window.BERNE||{}).lat || 42.6248, LNG = (window.BERNE||{}).lng || -74.1350;",
       "var CENTER = window.PLACE.center, LAT = CENTER.lat, LNG = CENTER.lng;   /* v1: from config/place.json */")
sub(S, "&timezone=America%2FNew_York", "&timezone='+encodeURIComponent(window.PLACE.timezone)+'", count=2)
sub(S, "/* v954 (Laurie): Berne reanalysis first and default;", "/* v954 (Laurie): centre-point reanalysis first and default;")
sub(S, "ob.value='berne'; ob.textContent='Berne reanalysis \\u00b7 ERA5 grid cell, ~1,700 ft \\u00b7 since 1940';",
       "ob.value='home'; ob.textContent=CENTER.short+' reanalysis \\u00b7 ERA5 grid cell, '+CENTER.elev_txt+' \\u00b7 since 1940';")
sub(S, "'ERA5 reanalysis for Berne via Open-Meteo'", "'ERA5 reanalysis for '+CENTER.short+' via Open-Meteo'")
sub(S, "'ERA5 reanalysis for the Berne grid cell via Open-Meteo, 1940 to yesterday.'", "'ERA5 reanalysis for the '+CENTER.short+' grid cell via Open-Meteo, 1940 to yesterday.'")
sub(S, "1956 is the same violet on every station and on Berne;", "1956 is the same violet on every station and on the reanalysis;")
sub(S, "/* Albany observed (station_dd.js), same date, same formulas */", "/* observed station (station_dd.js), same date, same formulas */")
sub(S, "v954: Berne reanalysis (default)", "v954: centre reanalysis (default)")
rsub_all(S, r"'berne'", "'home'", min_count=8)
rsub_all(S, r"_winterBerne\b", "_winterHome"); rsub_all(S, r"_yearsBerne\b", "_yearsHome")
sub(S, "in the Hilltowns box, newest observed first", "in the place.json box, newest observed first")
rsub(S, r"var INAT_DIST_KM = 40;   /\* v927[^\n]*\n", "var INAT_DIST_KM = window.PLACE.wildlife.inat_dist_km;   /* v1: from place.json. Half-width of a square box, not a radius. */\n")
sub(S, "around Berne, several parameter codes at once;", "around the centre, several parameter codes at once;")
rsub(S, r"var USGS_KEY='[^']*';   /\* v1011[^\n]*\n", "var USGS_KEY=window.PLACE.keys.usgs||'';   /* v1: api.waterdata.usgs.gov key from place.json; public in the page like EBIRD_KEY; blank still works */\n")
sub(S, "var WATER_BBOX_KM = 50;", "var WATER_BBOX_KM = window.PLACE.water.bbox_km;   /* v1: from place.json */")
rsub(S, r"  var WELL_SITES = \[[^\n]*\n", "  var WELL_SITES = window.PLACE.water.usgs_well_sites || [];   /* v1: pinned wells from place.json, always shown ahead of the nearest-N sweep */\n")
rsub(S, r"  var WELL_NOTE = \{[^\n]*\n", "  var WELL_NOTE = window.PLACE.water.well_notes || {};   /* v1: eyebrow context per well, from place.json */\n")
rsub(S, r"  var WATER_CHAIN = \{\n.*?\n  \};\n", "  var WATER_CHAIN = window.PLACE.water.water_chain || {};   /* v1: site number → drainage-path eyebrow, from place.json */\n", flags=re.S)
rsub(S, r"  var STREAM_SITES = \[[^\n]*\n", "  var STREAM_SITES = window.PLACE.water.usgs_stream_sites || [];   /* v1: the curated stream transect, from place.json */\n")
rsub(S, r"  var CHAINS = \[\n.*?\n  \];\n", "  var CHAINS = (window.PLACE.water.chains || []).map(function(c){ return {key:c.key, name:c.name, light:c.light, dark:c.dark, sites:c.sites||[]}; });   /* v1: river chains from place.json */\n", flags=re.S)
rsub(S, r"  var WATER_CAP = \{stream:99, lake:3, well:9\};[^\n]*\n", "  var WATER_CAP = window.PLACE.water.cap || {stream:99, lake:3, well:9};   /* v1: from place.json */\n")
rsub(S, r"  var NAMED_WATERS = \[\n.*?\n  \];\n", "  var NAMED_WATERS = (window.PLACE.water.named_waters || []).map(function(w){ return {key:w.key, re:new RegExp(w.pattern,'i'), label:w.label}; });   /* v1: from place.json; matched against each site's USGS name */\n", flags=re.S)
sub(S, "The specific local waters Laurie asked about by name,", "The specific local waters named in place.json,")
sub(S, '''    /* v963 (Laurie): Schoharie, Mohawk, Esopus, then wells, lakes, the tidal Hudson, and the Hudson head-of-tide chart last */
    var defs=[byKey.schoharie, byKey.mohawk, byKey.esopus,
      {id:'w7-wells', title:'Wells, last 7 days', color:KIND_COLOR.well.dark, sub:''},
      {id:'w7-lakes', title:'Lakes & reservoirs, last 7 days', color:KIND_COLOR.lake.dark, sub:''},
      {id:'w7-tidal', title:'Tidal Hudson, last 7 days', color:(byKey.hudson?byKey.hudson.color:KIND_COLOR.lake.dark), sub:'ft above NAVD88'}   /* v972 (Laurie): swatch was the lakes pink by mistake - tidal gauges are the Hudson chain */,
      byKey.hudson].filter(Boolean);''',
'''    /* v1 (2026-10-06): chart order from place.json water.chart_order (chain keys; wells/lakes/tidal appended), else every chain in CHAINS order */
    var order=(window.PLACE.water.chart_order&&window.PLACE.water.chart_order.length)?window.PLACE.water.chart_order:CHAINS.map(function(c){ return c.key; });
    var lastChain=CHAINS.length?CHAINS[CHAINS.length-1]:null;
    var defs=order.map(function(k){ return byKey[k]; }).concat([
      {id:'w7-wells', title:'Wells, last 7 days', color:KIND_COLOR.well.dark, sub:''},
      {id:'w7-lakes', title:'Lakes & reservoirs, last 7 days', color:KIND_COLOR.lake.dark, sub:''},
      {id:'w7-tidal', title:(window.PLACE.water.tidal_label||'Tidal gauges')+', last 7 days', color:(lastChain?lastChain.dark:KIND_COLOR.lake.dark), sub:'ft above NAVD88'}]).filter(Boolean);''')
sub(S, ">Hilltown Hotties: Species leaderboard \\u00b7 last '", ">Species leaderboard \\u00b7 last '")
sub(S, "var INAT_DAYS=14;", "var INAT_DAYS=window.PLACE.wildlife.inat_days||14;")
sub(S, "/* ---------- eBird: recent + notable sightings near Berne (key per Laurie, 2026-09-20) ---------- */", "/* ---------- eBird: recent + notable sightings near the centre (key in place.json) ---------- */")
rsub(S, r"var EBIRD_KEY='[^']*', EBIRD_DIST=25, EBIRD_BACK=14;", "var EBIRD_KEY=window.PLACE.keys.ebird||'', EBIRD_DIST=window.PLACE.wildlife.ebird_dist_km, EBIRD_BACK=window.PLACE.wildlife.ebird_back_days;   /* v1: from place.json */")
sub(S, "' km of Berne, most recent report of each shown.", "' km of '+CENTER.short+', most recent report of each shown.")
sub(S, "/* v1007 (2026-10-02, Laurie): a 40 km circle around Berne instead of the square box,", "/* v1007 (2026-10-02, Laurie): a circle around the centre instead of the square box,")
sub(S, "timeZone:'America/New_York'", "timeZone:window.PLACE.timezone", count=8)
assert "BERNE" not in rd(S)

# ---------------------------------------------------------------- signals.html / society.html copy
sub("signals.html", 'For Berne, NY, ~1,700 ft. Sun and moon are computed here;', 'For {{place.center.name}}, {{place.center.elev_txt}}. Sun and moon are computed here;')
sub("signals.html", '<!-- v954 (2026-09-28, Laurie): ONE picker — Berne reanalysis (default)', '<!-- v954 (2026-09-28, Laurie): ONE picker — centre reanalysis (default)')
s = rd("signals.html")
s = s.replace("Sky computed locally for Berne, NY (~1,700 ft). Today, air, winds and the Berne history:", "Sky computed locally for {{place.center.name}} ({{place.center.elev_txt}}). Today, air, winds and the {{place.center.short}} history:")
s = s.replace("these blocks are pinned to Berne;", "these blocks are pinned to the centre point;")
assert "Berne" not in s, [l for l in s.splitlines() if "Berne" in l]
wr("signals.html", s)
sub("society.html", "Who's been getting noticed in the Hilltowns lately!", "Who's been getting noticed in {{place.region_short}} lately!")
rsub("society.html", r'Research-grade observations within about 40 km of Berne — Helderbergs to the northern Catskills, Schoharie[^.]*\.',
     'Research-grade observations within about {{place.wildlife.inat_dist_km}} km of {{place.center.short}}.')
sub("society.html", 'id="hilltown-hotties"', 'id="leaderboard"')
sub("society.html", "Reported within 25 km of Berne in the last 14 days,", "Reported within {{place.wildlife.ebird_dist_km}} km of {{place.center.short}} in the last {{place.wildlife.ebird_back_days}} days,")

# ---------------------------------------------------------------- calendar.html
C = "calendar.html"
sub(C, 'var STANDING_FEATURES = ["kuhar family farm","sap bush hollow cafe","heather ridge farm","the pub at hilltown commons"];',
       'var STANDING_FEATURES = window.PLACE.calendar.standing_features || [];   /* v1: from place.json */')
rsub(C, r"  var NEARBY_EXCLUDE = \[\n.*?\]\.map\(function\(x\)\{ return x\.replace\(/\\u2019/g,\"'\"\); \}\);\n",
     "  var NEARBY_EXCLUDE = (window.PLACE.calendar.nearby_exclude || []).map(function(x){ return x.replace(/\\u2019/g,\"'\"); });   /* v1: from place.json */\n", flags=re.S)
sub(C, '''  /* exact-name exclusions — for places whose name is a prefix of something
     that SHOULD show (Hilltown Commons itself is out; The Pub at Hilltown Commons stays) */
  var NEARBY_EXCLUDE_EXACT = ["hilltown commons"];''',
'''  /* exact-name exclusions — for places whose name is a prefix of something that SHOULD show */
  var NEARBY_EXCLUDE_EXACT = window.PLACE.calendar.nearby_exclude_exact || [];''')
rsub(C, r"  var NEARBY_DEMOTE = \[\n.*?\n  \];\n", "  var NEARBY_DEMOTE = window.PLACE.calendar.nearby_demote || [];   /* v1: from place.json */\n", flags=re.S)
sub(C, '  var NEARBY_DEMOTE_LAST = ["maple on the lake"];', '  var NEARBY_DEMOTE_LAST = window.PLACE.calendar.nearby_demote_last || [];')
rsub(C, r"  var NEARBY_PRIORITY_EXACT = \[[^\n]*\n", "  var NEARBY_PRIORITY_EXACT = window.PLACE.calendar.nearby_priority_exact || [];\n")
rsub(C, r"  var NEARBY_PRIORITY = \[\n.*?\]\.map\(function\(x\)\{ return x\.replace\(/\\u2019/g,\"'\"\); \}\);\n",
     "  var NEARBY_PRIORITY = (window.PLACE.calendar.nearby_priority || []).map(function(x){ return x.replace(/\\u2019/g,\"'\"); });\n", flags=re.S)
rsub(C, r'  var NEARBY_EXCLUDE_CATS = \[[^\n]*\n',
     '  var NEARBY_EXCLUDE_CATS = ((window.ATLAS_DATA||{}).categories||[]).filter(function(c){ return c.wip || c.nearby === false; }).map(function(c){ return c.label; });   /* v1: any "wip" layer, plus manifest "nearby": false */\n')
sub(C, '''  // Core hilltowns — events in these get a gold highlight bar for prominence.
  // Matched against the event's address + venue text, case-insensitive, on word
  // boundaries so "Berne" doesn't match "Bernese" and "Knox" is whole-word.
  var CORE_TOWNS = [
    "Rensselaerville","Berne","Knox","Westerlo","Oak Hill",
    "Potter Hollow","Medusa","Preston Hollow","Preston-Potter Hollow",
    "Voorheesville",  /* added 2026-08-31 per Laurie — picks up Thacher State Park */
    "Thacher",        /* venue keyword, not a town: catches Thacher rows whose address omits the town */
    "Conkling Hall"   /* 2026-09-06 venue keyword — ingested rows sometimes arrive with no address */
  ];''',
'''  // Core towns (place.json towns.core) — events in these get a gold highlight bar for prominence.
  // Matched against the event's address + venue text, case-insensitive, on word boundaries.
  var CORE_TOWNS = window.PLACE.towns.core || [];''')
sub(C, "/* Core-hilltowns events get a gold left bar + faint wash for prominence. */", "/* Core-town events get a gold left bar + faint wash for prominence. */")
sub(C, "at Hilltown Commons must still show for a Commons event) */", "at a venue must still show for that venue's event) */")
s = rd(C); assert "CORE_RE = new RegExp" in s
if 'CORE_RE = new RegExp("\\\\b(" + CORE_TOWNS' in s:
    s = s.replace('CORE_RE = new RegExp("\\\\b(" + CORE_TOWNS', 'CORE_RE = CORE_TOWNS.length ? new RegExp("\\\\b(" + CORE_TOWNS')
    s = s.replace('''  }).join("|") + ")\\\\b", "i");
  function isCoreTown(ev){
    return CORE_RE.test(''', '''  }).join("|") + ")\\\\b", "i") : null;
  function isCoreTown(ev){
    return !!CORE_RE && CORE_RE.test(''')
    assert "!!CORE_RE" in s
wr(C, s)

# ---------------------------------------------------------------- directory.html
D = "directory.html"
sub(D, '''/* Hilltowns-proper highlight: gold sidebar + faint warm tint, for orgs physically
   located in Berne/Knox/Westerlo/Rensselaerville/Preston Hollow/Potter Hollow/Oak Hill */''',
       '''/* Core-town highlight: gold sidebar + faint warm tint, for orgs physically located in place.json towns.core */''')
sub(D, '''  /* ---- physically-in-the-Hilltowns highlight ----
     Matches against the parsed town only (never the raw street address) — a raw-address
     search would false-positive on street names like "Berne-Altamont Rd" in Altamont,
     which is not itself a Hilltown. Whole-word/phrase match so "East Berne" and
     "South Westerlo" (real hamlets within Berne/Westerlo) still count. */
  var HILLTOWN_NAMES = ["berne","knox","westerlo","rensselaerville",
    "preston hollow","potter hollow","oak hill","preston-potter hollow"];
  function isHilltownOrg(town){
    var t = String(town||"").toLowerCase().replace(/,\\s*(ny|new york)$/i,"").trim();
    if(!t) return false;
    return HILLTOWN_NAMES.some(function(name){''',
'''  /* ---- physically-in-a-core-town highlight ----
     Matches against the parsed town only (never the raw street address) — a raw-address
     search would false-positive on street names that carry a town's name. Whole-word/phrase
     match so "East <Town>" still counts. Towns from place.json towns.core; state suffix stripped. */
  var CORE_TOWN_NAMES = (window.PLACE.towns.core || []).map(function(t){ return String(t).toLowerCase(); });
  var STATE_RX = new RegExp(",\\\\s*(" + [window.PLACE.state_abbr, window.PLACE.state_name].filter(Boolean).map(function(x){ return x.replace(/[-/\\\\^$*+?.()|[\\]{}]/g,"\\\\$&"); }).join("|") + ")$", "i");
  function isCoreTownOrg(town){
    var t = String(town||"").toLowerCase().replace(STATE_RX,"").trim();
    if(!t) return false;
    return CORE_TOWN_NAMES.some(function(name){''')
sub(D, "o.inHilltowns = isHilltownOrg(o.town);", "o.inCore = isCoreTownOrg(o.town);")
sub(D, "(o.inHilltowns?' htown':'')", "(o.inCore?' htown':'')")
sub(D, "var LIKE_NS = 'nyhilltowners-explore-hills';", "var LIKE_NS = window.PLACE.storage_keys.likes_ns;")

# ---------------------------------------------------------------- about.html — minimal, tokenised; the Hilltowns FAQ was that site's editorial voice
A = "about.html"
s = rd(A)
i = s.index('<main class="wrap">'); j = s.index("</main>") + len("</main>")
s = s[:i] + '''<main class="wrap">
  <div class="eyebrow">About this guide</div>
  <h1>{{place.brand}}</h1>

  <p>{{place.about_text}}</p>

  <p>Sun, moon and weather are computed for {{place.center.name}} ({{place.center.elev_txt}}) in the region's own time zone, for every visitor wherever they are. Weather is Open-Meteo; wildlife is iNaturalist and eBird; water levels are USGS. Live feeds say when they fail — a gap means "no report," never "nothing happened."</p>

  <!-- @@if:contact_email --><p>Local organization, business, interesting bit of lore, or something else you think should be on the map? <a class="link" href="mailto:{{place.contact_email}}">{{place.contact_email}}</a>.</p><!-- @@endif -->
  <!-- @@if:instagram --><p>Additions, suggestions, corrections? Message us on Instagram at <a class="link" href="{{place.instagram_url}}" target="_blank" rel="noopener">{{place.instagram_handle}}</a>.</p><!-- @@endif -->

  <section class="faq">
    <div class="eyebrow">Infrequently Asked Questions</div>

    <h3>Who are you?</h3>
    <p>[Editor: who makes this guide, and why. The Hilltowns version of this page is in the starter kit's history if you want its shape.]</p>

    <h3>Do you track visitors?</h3>
    <p>[Editor: if analytics.goatcounter is set in place.json, say so here — GoatCounter sets no cookies and collects no personal data. If it is blank, nothing is counted.]</p>
  </section>

  <a class="backmap" href="{{place.href_atlas}}">Explore the Atlas &rarr;</a>
</main>''' + s[j:]
wr(A, s)

# ---------------------------------------------------------------- bulletin / instagram / tradingpost — light pages, tokens only
sub("bulletin.html", 'content:"From the kitchen of the Hilltowns";', 'content:"From the kitchen of {{place.region_short}}";')
sub("bulletin.html", "<h1>Hilltowns Bulletin</h1>", "<h1>{{place.short_name}} Bulletin</h1>")
sub("tradingpost.html", '<h1 class="tp-head">Hilltowns Trading Post</h1>', '<h1 class="tp-head">{{place.short_name}} Trading Post</h1>')

# ---------------------------------------------------------------- workflow: rebuild when config changes
W = ".github/workflows/build.yml"
sub(W, '      - "manifest.json"\n', '      - "manifest.json"\n      - "config/**"       # v1 (2026-10-06): place.json\n')

print("patched:", len(CHANGED), "files")
for p in sorted(CHANGED): print("  ", p)
