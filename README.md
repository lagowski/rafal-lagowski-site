# rafal.lagowski.es

Personal expert profile of Rafał Łagowski, AI & Agentic Systems Architect.
Plain static HTML, CSS and vanilla JS, served by GitHub Pages straight from the
repository root. No build step, no framework, no trackers. Fonts are self-hosted.

Languages: EN (default), ES, PL. The switch sets a class on `<body>` and stores
the choice in `localStorage` under `lagowski-lang`; first visits follow the
browser language when it is Spanish or Polish.

## Editing

The pages are generated from `tools/gen.py` so the three languages stay in one
place, and the generated HTML is committed:

    python3 tools/gen.py
    python3 -m http.server 8765    # preview at http://localhost:8765

Values still to fill in sit at the top of `tools/gen.py`: `DAY_RATE`,
`LINKEDIN`, `VIDEO`. The CV button turns live once
`files/Rafal_Lagowski_CV.pdf` exists. Rerun the script after any change.

`tools/og.html` is the source of `assets/og.png` (1200x630 social card) and
`tools/icon.html` of the touch icon; both are rendered with headless Chrome.

The interactive demos and the starter-pack / workshop PDFs come from the
lagowski.es services site, which stays a separate project.
