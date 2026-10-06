# Community Field Guide — starter kit v1 (2026-10-06)

The NY Hilltowners Folk Atlas source tree (v1013) with the Hilltowns data removed. Read in this order:

1. `BRIEF.md` — what this is, how it was built, what to do differently, the phase plan, the first-session prompt.
2. `LOCALIZE.md` — every place-specific value still in the code, by file and line, and the content files to replace.
3. `config/place.json` — fill it in; make the files in LOCALIZE.md read from it.
4. `HANDOFF_README.md` — the Hilltowns build log (1,000 versions). Reference only: the delivery ritual, data rules, pin logic and schemas sections transfer; the version log does not.

Build (needs Python 3.10+ and `pip install openpyxl`):

    rm -rf site && python3 build/build.py      # expect: BUILD OK — 0 records … 0 errors (the kit ships empty)

Deploy: push to `main` on a GitHub repo with Pages source = GitHub Actions; `.github/workflows/build.yml` builds and publishes.

Harnesses (`scripts/signals_harness`, `scripts/water_harness`) need Node + Playwright + maplibre-gl; they mock every external feed so pages can be screenshot-tested offline.

Masters in `data/` carry one EXAMPLE row each (Display=No) showing the expected format — delete them when real rows exist.
