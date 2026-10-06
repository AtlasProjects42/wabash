# WAYS / ANCIENT WAYS LAYER — data dictionary & export manifest
Exported 2026-10-06 for carry-over to another project.

## Source of record
- File: ways_layer_v169-B169.json
- Version: v169-B169 | schema: v2
- md5: a76948fb7d77a0b895d7415532bf0fec
- bytes: 1590915
- routes: 560 | networks (group_id): 96 | sensitive routes: 14

## Structure
Top level: { "_meta": {...}, "routes": [ ... ] }

### route object
- id            frozen route ID, "AW-###" — the only safe join key (names are mutable)
- name          display name
- class         one of: indigenous, trade, pilgrimage, post-road, caravan, drover, military
- confidence    tier A / B / C (A=strongest sourcing; C=plausible but thinner). NOTE: the field
                is **confidence**, not "tier" — the v169 brief calls them tiers but the JSON key is confidence.
- group         human network name (e.g. "Hudson Valley trails")
- group_id      frozen network slug (e.g. "hudson-valley-trails") — join key for networks
- era           free-text dating / usage-period string
- sensitive     bool — if true, coordinates are deliberately generalized (see sensitivity_rule in _meta)
- note          long-form sourced prose (the scholarship; some are several hundred words)
- segments      ordered list of segment objects

### segment object
- kind          land | river | sea | ferry | tidal  (controls how it's drawn)
- confidence    per-segment A/B/C (a route can be firmer in some stretches than others)
- nodes         ordered list of node objects (the polyline)

### node object
- lon, lat      coordinates (decimal degrees, WGS84)
- n             name (absent/blank on shaping nodes)
- t             node type: terminus, station, town, pass, shrine, oasis, ford, port,
                portage, caravanserai, wall-gate, shaping (shaping = geometry-only, unnamed)
- s             sensitivity/secondary flag (present on some nodes)
- v             verify flag (coordinate independently verified vs. inferred)

## Field value counts (this export)
- class: {'post-road': 33, 'pilgrimage': 84, 'caravan': 28, 'trade': 204, 'drover': 8, 'indigenous': 202, 'military': 1}
- confidence: {'A': 54, 'C': 175, 'B': 331}
- segment kinds: {'land': 535, 'ferry': 16, 'river': 100, 'sea': 29, 'tidal': 2}
- node types: {'terminus': 1027, 'station': 697, 'town': 2297, 'pass': 179, 'shrine': 377, 'shaping': 852, 'oasis': 101, 'ford': 367, 'wall-gate': 10, 'caravanserai': 8, 'port': 335, 'portage': 155}

## _meta
Carries ~70 named rules/conventions (the layer's accumulated editorial law) plus group_registry
(the 96 networks) and lore_store pointer. All preserved in the JSON. Read _meta._RULES_INDEX for the map.

## NOT in this export (get from the ways chat)
- ways_lore.json — the companion lore store. v169 ships **122 entries**; the copy that reached the
  cartographer was one version behind (115, v153-era) and the v169 upload omitted it. For a complete,
  current carry-over, request ways_lore.json (122 entries, md5 f369a33f1c72…) from the ways researcher.
