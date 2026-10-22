# Redesign build helper

`index.html` and `services/*/index.html` are generated from `content.py` (copy) and `build.py` (templates).

    python3 _build/build.py

The free guide PDF is printed from `_build/guide/lead-magnet.html`:

    bash _build/guide/print-pdf.sh

Shared styles/scripts: `assets/redesign/site.css`, `assets/redesign/site.js`.
Public prices live only in `assets/pricing.js` (AIOS sheet, 27 Sep 2026). The build reads that file. Leave `published` false until Billy says the figures are a final public offer.
This folder starts with `_`, so GitHub Pages (Jekyll) does not publish it.
