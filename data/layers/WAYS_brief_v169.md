# WAYS → CARTOGRAPHER — v169-B169 shipment

**From:** ways-researcher instance · **Base of record:** v169-B169
**Lineage this session:** v153-B153 (547 routes, prior cartographer handoff) → v169-B169 (560 routes)

---

## 1. What's in this package

| File | bytes | md5 |
|---|---|---|
| `ways_layer.json` | 1590915 | `a76948fb7d77a0b895d7415532bf0fec` |
| `ways_lore.json` | 53547 | `f369a33f1c72006031af9eb21b85a43c` |

**Disposition: PIN-REPLACE** — both replace the copies handed off after the v153-B153 shipment (or any earlier snapshot on the cartographer side). Tier: SOURCE (`ways_layer.json`) and DERIVED-but-durable (`ways_lore.json`), same convention as before.

Schema unchanged (`_meta.schema: "v2"`). No renderer changes needed to read this file.

---

## 2. Headline numbers

- **560 routes** (was 547 at last handoff), **13 net new this session**, plus a larger number of note-only upgrades to existing routes (no geometry change, just stronger sourcing — flagged below since they may be worth a second look if you cache route metadata separately from geometry).
- **122 lore entries** (was 115), all reconciled, 0 pending.
- Guard: **CLEAN**. Census vs. inherited baseline: **CLEAN, nothing disappeared**. Near-miss sweep (600 m): **1 open case**, unchanged from last handoff and still deliberately unresolved (see §5).
- Manual duplicate/degenerate-segment/orphaned-group_id audit run this session (the `audit_layer.py` substitute) — clean on all axes.

---

## 3. What's new, by source

### 3a. Beauchamp's "Perch Lake Mounds" trails section — fully mined
The prior handoff noted this NY primary source was half-mined; it's now finished (six new routes: the Owego–Onondaga Trail complex, the Cold Spring Creek Trail, two Madison County trails, a Canandaigua branch onto the existing Lake Ridge Trail, and the Esopus–Neversink Trail). The companion "rich" scan of the same book was checked and confirmed a duplicate — no separate mining needed there. Two lower-priority Beauchamp texts (`Aboriginal Occupation of New York`, `Indian Names in New York`) were checked and confirmed to be archaeological-site and place-name catalogs respectively, with no route-level material — that finding is now closed out, not just deferred.

### 3b. The Moravian Journals (Beauchamp, ed., 1916) — fully worked
The previously-untouched primary source. Five separate journals (Spangenberg 1745, Cammerhoff/Zeisberger 1750, Mack/Zeisberger/Rundt 1752, Zeisberger/Frey 1753, Zeisberger/Frederick 1754–5) were read in full. **One genuinely new route** came out of this (AW-556, Cammerhoff's Cayuga Road — the documented *alternative* to the Owego route, diverging at the same fork Tioga, both preserved). Everything else in the five journals resolved to **corroboration of already-drawn ground**: two existing routes (AW-401, AW-550) turned out to be independently confirmed down to physical evidence — Zeisberger recognized a lake from a prior trip and found the names his party had carved into trees eight years earlier. Full detail in the routes' own notes.

**A note on method, since you may see it reflected in unusually long notes this session:** partway through this work the person running the session asked for a stricter test before drawing anything from a travel diary — was the diarist following a known, named path, or improvising through open country with a guide who was also unsure? That test was applied retroactively to what had already been drawn and prospectively to everything after. One near-miss was caught by this: a Zeisberger/Frey water route that looked like new territory turned out, once properly identified against the diary's own editorial notes, to already be AW-079. No geometry was drawn on the strength of the test alone — every route in this shipment still has an independent citation.

### 3c. Simms, *History of Schoharie County* (1845) — new source, three routes plus two upgrades
Found via web search after the on-disk Catskill/hilltowns material was exhausted (see §3d). Judge Brown, interviewed by Simms in 1837 at nearly ninety, enumerated five named foot-paths from before white settlement; three were genuinely new (AW-557, AW-558, AW-559) and two were confirmations of already-drawn routes (AW-452, AW-454 — the latter gained a properly-named waypoint, "the Vlaie," where it previously had an unnamed shaping node).

### 3d. Manhattan and the lower Hudson — new territory for this layer entirely
In response to a question about historical antecedents of the modern "Long Path" hiking trail (which is a 1930s recreational route, **not** an indigenous trail — flagged clearly to the user and worth flagging to you too in case it comes up), three new routes were drawn: the Wickquasgeck Trail (AW-560, Manhattan's spine, now Broadway — a direct 1642 primary-source citation), the Bloomingdale Trail (AW-561, a second, genuinely distinct Manhattan trail with unusually precise legislative evidence of pre-existence), and the Wiccoppe–Wappinger Trail (AW-562, Kingsbridge to Fishkill Creek, connecting Manhattan to the already-existing AW-082 Mahican-Wappinger River Trail toward Albany). AW-562 was drawn at tier C initially, then **upgraded to tier B this same session** after finding C.G. Hine's 1906 walked account, which gave real Native place-names at nearly every stop and an explicit period statement that the road was converted from an Indian trail to a wagon road under Lord Loudoun before the French and Indian War.

**Net effect: a continuous, honestly-graded indigenous-trail-based route now exists from the Battery to Albany.** It was never one named path historically — it's three separate trail traditions a colonial road later stitched together — and the notes say so explicitly rather than presenting it as more unified than the sources support.

### 3e. Six more hub joins caught by the near-miss sweep
Same pattern as every prior batch: Schoharie Crossing/Fort Hunter, Cayuga (a third route through an existing 2-way junction), New Amsterdam/Bowling Green, and three others across the session. All snapped and cross-cited; none required overwriting anything.

---

## 4. Rendering notes — no changes from the last brief

Everything in §4 of the v153 brief (node types, segment kinds, tidal handling, confidence-tier semantics, polyline-length caveat, sensitivity flag, verify-flag convention) still applies unchanged. Not repeating it here; flag if you'd like it re-sent.

One addition: this session's Manhattan routes (AW-560, AW-561) sit at a much finer geographic scale than anything else in the layer — street-level rather than regional. If your renderer has a zoom-dependent simplification pass, these two routes are worth checking don't get over-simplified into a single line, since the whole point of drawing both is that they're genuinely distinct parallel trails a few blocks apart.

---

## 5. Open item, unchanged: the Marklesburg near-miss

Same as last handoff — two nodes 556 m apart (AW-428/AW-430 vs. AW-505), deliberately left unresolved per the `duplicate_place_gap` standing test (one node is explicitly "north of" the town, which the layer treats as legitimate for a town/region touch-point, distinct from a single physical object). Still a candidate for cosmetic generalization on your end if it renders as an artifact; the layer itself still leaves them apart on purpose.

---

## 6. What's still outstanding on the research side

- The Westchester-to-Albany stretch of the new NYC corridor (AW-082, Fishkill Creek to Schodack) is still tier C — no Hine-quality walked primary source was found for that piece specifically, though one may exist and wasn't searched for exhaustively.
- The three open Ways-layer rulings still waiting on Laurie: Kula ring bidirectionality, sites appearing in both the ways and sacred layers, AW-062 tier-C alignment.
- No new PA/western-NY source work this session — it was NY/lower-Hudson focused throughout.

None of the above touches any route ID or coordinate already in this shipment.

---

## 7. Protocol compliance (per Writer Protocol v5)

- **R8**: ships as `v169-B169`, layer's own batch namespace.
- **R9**: both files tagged **PIN-REPLACE**.
- **R10**: this brief cites `_meta` fields and route IDs by name throughout.
- **R11**: fingerprints in §1; verify before treating as current.
