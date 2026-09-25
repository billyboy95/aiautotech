# Redesign build helper

`index.html` and `services/*/index.html` are generated from `content.py` (copy) and `build.py` (templates).

    python3 _build/build.py

Shared styles/scripts: `assets/redesign/site.css`, `assets/redesign/site.js`.
This folder starts with `_`, so GitHub Pages (Jekyll) does not publish it.
