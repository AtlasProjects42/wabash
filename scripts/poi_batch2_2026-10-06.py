#!/usr/bin/env python3
"""POI batch 2 (2026-10-06): preserves & trails. NICHES Land Trust properties (Tippecanoe + Carroll county pages,
nicheslandtrust.org), DNR/Purdue/city/county trail sites. Coordinates from Google Places lookups today (place_id in
Notes). NICHES hours: "open dawn to dusk Dec 1 – Oct 31" (nicheslandtrust.org/properties) → Dawn-Dusk + Season
12-01 → 10-31 where the county page says 'closed November for deer-control hunt'. No-trail NICHES tracts go in as
directory-only (Anchor Type none, no coords) so no one is sent into a floodplain. Descriptions from NICHES pages."""
import sys, re
from openpyxl import load_workbook
WB = sys.argv[1]; D = "2026-10-06"
H = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
def hrs(*c): assert len(c)==7; return dict(zip(H, c))
DD = hrs(*(["Dawn-Dusk"]*7)); NONE = hrs(*([""]*7))
NICHES = "https://www.nicheslandtrust.org/"; NPH = "+1 765-423-1605"
def row(sheet, name, tags, addr, lat, lng, desc, hours, site="", phone="", notes="", anchor="premise", s_start=None, s_end=None, display="Yes", source="Google Places lookup " + D):
    return dict(sheet=sheet, Name=name, Tags=tags, Address=addr, Latitude=lat, Longitude=lng, Description=desc, **hours, Website=site, Phone=phone,
                Notes=f"{D}: added by atlas assistant; {notes}".rstrip("; "), Display=display, **{"Anchor Type": anchor, "Season Start": s_start, "Season End": s_end, "Source": source})
def niches(name, tags, addr, lat, lng, desc, notes="", hunt=True, hours=DD, anchor="premise", display="Yes", site=NICHES):
    return row("Adventures", name, tags, addr, lat, lng, desc, hours, site, NPH,
               ("closed November for the deer-control hunt (NICHES county page); " if hunt else "") + "NICHES: open dawn–dusk; " + notes,
               anchor=anchor, s_start="12-01" if hunt else None, s_end="10-31" if hunt else None, display=display,
               source="nicheslandtrust.org; Google Places " + D)
def tract(name, tags, desc, county, notes="", display="Yes"):
    return row("Adventures", name, tags + "; NICHES; No Trails", f"NICHES Land Trust property, {county} County", None, None, desc, NONE, NICHES, NPH,
               "no public trails — directory listing only, no pin; " + notes, anchor="none", display=display, source="nicheslandtrust.org")

ROWS = [
 niches("Clegg Memorial Garden", "Adventures; Nature Preserve; NICHES; Trails; Wildcat Creek; Overlook; Natural Playground",
        "1782 N 400 E, Lafayette, IN 47905", 40.444554, -86.8285507,
        "NICHES' flagship preserve on a ridge above Wildcat Creek — a mile-plus of narrow trails through oak woodland, prairie and savanna, overlooks, steps down to the creek, and a natural playground. Shares the drive with the NICHES office.",
        "place_id ChIJ36DYbFwDE4gRtarAkFwJjaU; Google lists 8am–8pm, NICHES says dawn–dusk", hunt=False),
 niches("Granville Sand Barrens & Roy Whistler Wildlife Area", "Adventures; Nature Preserve; NICHES; Sand Barrens; Trails; Wabash River; State Dedicated",
        "8044 W 75 S, West Point, IN 47992", 40.400985, -87.056271,
        "Two adjoining NICHES preserves on the Wabash terrace west of Lafayette — rare sand-barrens habitat (a state-dedicated nature preserve) and the Whistler woods, on one loop trail from a shared lot.",
        "place_id ChIJa1duCADlEogRVsn9r2ww-QY (Whistler); DNR factsheet secure.in.gov/dnr/nature-preserves/files/np-Granville_Sand_Barrens.pdf"),
 niches("Black Rock Nature Preserve", "Adventures; Nature Preserve; NICHES; Bluff; Wabash River; Geology; Trails",
        "11598 E 350 N, Otterbein, IN 47970", 40.3666249, -87.1003024,
        "A sandstone bluff over the Wabash — the 'black rock' of the river name — with a grassy trail on top and a short rugged scramble to the cliff face. Two parking spaces; best in leaf-off seasons.",
        "place_id ChIJk1d3MSPvEogRFRs76fDhmok; not on the Tippecanoe county list — hunt closure unconfirmed, no season set", hunt=False),
 niches("Black Rock Barrens — Heischman-McAdams Reserve", "Adventures; Nature Preserve; NICHES; Barrens; Trails",
        "E Independence Rd, Otterbein, IN 47970", 40.3590263, -87.1159434,
        "Short loop of moderate grade through recovering barrens and woods next to Black Rock; shares its lot with Weiler-Leopold.",
        "place_id ChIJjwVEBgDvEogRtAjhgH7IMqg; hunt closure unconfirmed", hunt=False),
 niches("Weiler-Leopold Nature Preserve", "Adventures; Nature Preserve; NICHES; Meadow; Woods; Overlook; Trails",
        "E Independence Rd, Otterbein, IN 47970", 40.3589923, -87.1160191,
        "Single-loop trail through native meadow and woods with a short spur to an overlook and memorial; the gentle companion to Black Rock next door.",
        "place_id ChIJ5Rq2IszuEogRSH1zU2RYEX8; hunt closure unconfirmed", hunt=False),
 niches("Mulvey Pond", "Adventures; Nature Preserve; NICHES; Birding; Wetland; Blind; Trails",
        "4998 US-231, West Lafayette, IN 47906", 40.4900728, -87.0365315,
        "NICHES birding hotspot northwest of West Lafayette — a mown loop around the pond with a bird blind; sandhill cranes and waterfowl in season. Three-car lot.",
        "place_id ChIJe4RLK0n6EogRLzTXI8pBwU4", hunt=False),
 niches("The Howell Woods", "Adventures; Nature Preserve; NICHES; Old Growth; Little Pine Creek; Trails",
        "4450 US-231, West Lafayette, IN 47906", 40.4831091, -87.0299685,
        "Small NICHES preserve on Little Pine Creek near Mulvey Pond — two out-and-back trails, one each side of the creek, under some old trees.",
        "place_id ChIJJbTzWwD7EogRF8zkWA0IHQU", hunt=False),
 niches("Potawatomi Trail", "Adventures; Nature Preserve; NICHES; Trails; Wabash Valley",
        "2330 S 950 W, West Lafayette, IN 47906", 40.3727917, -87.0916781,
        "Fifty-nine NICHES acres between Ross Hills Park and Black Rock with hiking trails; few parking spaces; muddy after floods.",
        "place_id ChIJeeGFohPvEogRcYIKdipp-3w"),
 niches("Berkshire-Tarnowski Forest Preserve", "Adventures; Nature Preserve; NICHES; Deer Creek; Trails; Carroll County",
        "4284 IN-75, Camden, IN 46917", 40.5976087, -86.5406368,
        "NICHES forest preserve on Deer Creek south of Camden in the Tipton Till Plain — about 1.6 miles of mown trail along the creek.",
        "place_id ChIJE46XW0qeE4gRSWSx5g_JZLc"),
 niches("Frogs' Glory", "Adventures; Nature Preserve; NICHES; Prairie; Tippecanoe River; Accessible Walking; Trails",
        "W Tippecanoe Ranch Rd, Delphi, IN 46923", 40.6108343, -86.7604826,
        "Flat prairie-and-woods preserve on the Tippecanoe River bottoms above Delphi — easy mown trails, a little free library, river access across the road.",
        "place_id ChIJkSp_wGqoE4gRMlZZHtEe8Yg"),
 niches("Fall Creek Gorge Nature Preserve", "Adventures; Nature Preserve; NICHES; Gorge; Potholes; Big Pine Creek; Trails; Warren County",
        "78 W Twin Bridges Rd, Williamsport, IN 47993", 40.3408137, -87.318938,
        "'The Potholes' — a sandstone gorge on Fall Creek above Big Pine Creek, with swirl-carved potholes and a small falls; two loop trails, ~100 acres. Southwest edge of the guide's radius.",
        "place_id ChIJw7CofgCXEogRIBSNVP5h4wM; Warren County page not fetched — hunt closure unconfirmed", hunt=False),
 niches("Crow's Grove Nature Preserve", "Adventures; Nature Preserve; NICHES; Trails; Warren County",
        "3300 N 050 W, Williamsport, IN 47993", 40.3670732, -87.326771,
        "Short, scenic NICHES trail near Williamsport.", "place_id ChIJVckVOxSREogRQmruVACFz2A; hunt closure unconfirmed", hunt=False),

 # ---- non-NICHES trail sites
 row("Adventures", "Ross Hills Park", "Adventures; County Park; Trails; Lodge; Waterfall",
     "8815 W 50 S, West Lafayette, IN 47906", 40.4091501, -87.0704699,
     "Tippecanoe County park west of West Lafayette — about 2.5 miles of nature trails, a small waterfall and stream, open field and a rentable lodge.",
     hrs(*(["8am-11pm"]*7)), "https://www.tippecanoe.in.gov/", "+1 765-463-2306", "hours as listed on Google today; place_id ChIJe0jRq4fuEogR2z6U2IZOU40"),
 row("Adventures", "Peters Mill Access", "Adventures; River Access; Wildcat Creek; Canoe; Kayak; Fishing; DNR",
     "1635 Eisenhower Ct, Lafayette, IN 47905", 40.4414848, -86.8299566,
     "DNR public access on Wildcat Creek across from Clegg Memorial Garden — gravel lot, a small dock for canoes and kayaks, sand bars. Lot fills on summer weekends.",
     NONE, "https://www.in.gov/dnr/", "+1 317-232-4200", "phone is IDNR Indianapolis; NICHES' separate 'Peter's Mill Landing' (downstream of the bridge, no trails) is not this pin; place_id ChIJw3tnAlsDE4gRS4b7PruUVoA"),
 row("Adventures", "Wabash & Erie Canal Park", "Adventures; Historic Site; Canal; Museum; Trails; Campground; Boat Rides; Pioneer Village",
     "1030 N Washington St, Delphi, IN 46923", 40.5914024, -86.6812699,
     "Delphi's canal park — a restored stretch of the Wabash & Erie Canal with an interpretive center, replica lock, pioneer village, the Reed Case House, canal-boat rides in season, towpath trails and a small campground. Links to the Monon High Bridge Trail.",
     hrs("10am-4pm","10am-4pm","10am-4pm","10am-4pm","10am-4pm","1pm-4pm","Closed"), "https://www.wabashanderiecanal.org/", "+1 765-564-2870",
     "hours are the interpretive center's as listed on Google today; grounds/trails open longer; place_id ChIJQ02UoGCnE4gRIwdSjEBRVFY"),
 row("Adventures", "Martell Forest", "Adventures; Research Forest; Purdue; Hiking; Trails; Hills",
     "1007 N 725 W, West Lafayette, IN 47906", 40.4313121, -87.0379442,
     "Purdue's forestry research forest west of town — a hilly loop (about 6–7 miles if you do all of it, with a creek crossing near the start) open to walkers; little parking, few people.",
     NONE, "https://ag.purdue.edu/department/fnr/", "", "Purdue property — confirm public-access rules on the FNR site before promoting; place_id ChIJYQM9SgDlEogRaFNv4xsrI0A"),
 row("Adventures", "Happy Hollow Park", "Adventures; City Park; Ravine; Trails; Playground; Shelters",
     "1301 Happy Hollow Rd, West Lafayette, IN 47906", 40.4394561, -86.9014063,
     "West Lafayette's ravine park — a wooded valley with the Ravine Trail (stairs, creek, narrow paths), connections into the city trail system, two playgrounds and shelters.",
     hrs(*(["8am-8:40pm"]*7)), "https://www.westlafayette.in.gov/", "+1 765-775-5110", "place_id ChIJJVI66Fn9EogRLkD_FD_0mCY"),
 row("Adventures", "Trailhead Park", "Adventures; City Park; Trailhead; Trails; Shelter",
     "1485 W 350 N, West Lafayette, IN 47906", 40.4683347, -86.9332886,
     "Hub of the West Lafayette trail system on the north side — parking, a shelter, and trail links through meadow and woods.",
     hrs("8am-8pm","8am-8pm","8am-8pm","8am-8pm","8am-8pm","8am-9pm","10am-6:30pm"), "https://www.westlafayette.in.gov/", "+1 765-775-5110", "hours as listed on Google today; place_id ChIJ5TsBFgb9EogRS1a5DfIj0G8"),

 # ---- NICHES tracts without trails: directory only
 tract("Frank and Ada Beineke Memorial Forest", "Adventures; Nature Preserve; Indian Creek", "NICHES forest on Indian Creek; no trails; closed November for the deer hunt.", "Tippecanoe"),
 tract("Laura Hare Bend of the Wabash", "Adventures; Nature Preserve; Sand Barrens; Wabash River", "Two Wabash floodplain tracts with about 30 acres of sand-barrens habitat; no trails; closed November.", "Tippecanoe"),
 tract("Parker's Indian Creek Basin", "Adventures; Nature Preserve; Restoration; Wabash River", "Wabash floodplain under restoration; no trails; closed November.", "Tippecanoe"),
 tract("Wabash Bottoms: Janssen Tract", "Adventures; Nature Preserve; Wabash River", "45 NICHES acres of a 70-acre Wabash bottomland property; no trails; closed November.", "Tippecanoe"),
 tract("Wabash Breaks & Carter's Point", "Adventures; Nature Preserve; Gravel Hill Prairie; State Dedicated", "Rare gravel hill prairies above the Wabash, state-dedicated nature preserves with limited road access.", "Tippecanoe"),
 tract("Wise Island", "Adventures; Nature Preserve; Island; Wabash River; Eagles", "Two-acre island in the Wabash near Americus kept for birds and eagles; no access.", "Tippecanoe"),
 tract("Herb and Dortha Parker's Hickory Grove Farm", "Adventures; Nature Preserve; Trails", "Woods, pond and pasture with trails; a private residence is on the property; closed November.", "Tippecanoe", "HAS trails per NICHES but no Google listing — needs coordinates from NICHES' map before it gets a pin"),
 tract("Heron Bottoms", "Adventures; Nature Preserve; Owasco Creek", "NICHES tract on Owasco Creek; no trails; open with restrictions.", "Carroll"),
 tract("McAllister Woods", "Adventures; Nature Preserve; Wildcat Creek", "Woods on Wildcat Creek; no trails; closed November.", "Carroll"),
 tract("Mussel Shoals", "Adventures; Nature Preserve; Gravel Bar", "Creek-side tract with a gravel bar; no trails.", "Carroll"),
 tract("Sixbey", "Adventures; Nature Preserve; Wildcat Creek; Scenic Waterway", "NICHES tract on Wildcat Creek, an Indiana State Scenic Waterway; no trails; closed November.", "Carroll"),
 tract("Weaver Family Nature Reserve", "Adventures; Nature Preserve; Island; Wabash River; Nesting", "Island in the Wabash north of Delphi; no trails; avoid the nesting season (late March – June).", "Carroll"),
 tract("Whistler Woods", "Adventures; Nature Preserve; Deer Creek; Trails", "NICHES woods on Deer Creek with trails; closed November.", "Carroll", "HAS trails per NICHES but no Google listing — needs coordinates from NICHES' map before it gets a pin"),
 tract("Moyer-Gould Woods", "Adventures; Nature Preserve; Trails", "NICHES woods with trails, closed since June 2026 for storm damage.", "Carroll", "CLOSED for storm damage per NICHES (June 2026); hidden until it reopens", display="No"),
]

wb = load_workbook(WB)
def norm(s): return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()
added = 0; skipped = []
for r in ROWS:
    ws = wb[r["sheet"]]; headers = [c.value for c in ws[1]]
    existing = {norm(rw[headers.index("Name")]) for rw in ws.iter_rows(min_row=2, values_only=True) if rw[headers.index("Name")]}
    if norm(r["Name"]) in existing: skipped.append(r["Name"]); continue
    ws.append([r.get(h, None) if r.get(h, None) != "" else None for h in headers]); added += 1
wb.save(WB); print(f"added {added}; skipped {skipped}")
