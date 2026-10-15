# Awesome Medical CCFA

[Open the public website](https://awesome-medical-ccfa.grandowlet6.chatgpt.site)

An English-language, responsive, source-backed catalogue of medical and biomedical research in the fixed CCF 2022 A-conference cohort, for publication years 2020–2025.

## Run locally

No npm packages, API keys, or build service are required.

```sh
python -m http.server 8000
```

Open http://localhost:8000. The embedded data snapshot also allows opening `index.html` directly.

## Features

- Full-text keyword search over titles, authors, affiliations, introductions, and tags
- Year, venue, and topic filters; newest, oldest, alphabetical, and citation sorting
- Original-source links, paper detail dialogs, provenance, missing-field disclosures
- Conference counts, yearly counts, topic heatmap, source-reported citation ranking
- Venue-year denominator ledger with qualified observed shares
- All 58 CCF A venues in a five-year coverage matrix
- Filtered JSON export and downloadable full data
- Responsive mobile layout, keyboard-accessible controls, native modal focus handling, reduced-motion support

## Update the snapshot

```sh
python scripts/build_data.py --source-dir /path/to/collector-output
```

Inputs: `vision_papers.json`, `language_papers.json`, `ml_papers.json`, corresponding `_coverage.json` files, `ccfa_scope.json`, optional `paper_enrichment.json` and `paper_assets.json`. Original collector records explicitly marked candidate/pending are excluded from the indexed catalogue and retained in `data/pending_candidates.json`.

The importer preserves original provenance while omitting full abstracts, normalizes common field names, deduplicates by normalized title and publication year, and matches enrichment by the same exact key. Citation nulls are never filled with zero.

## Deploy

Publish the contents of this directory to any static host. For GitHub Pages, select the repository's main branch and root folder in repository Settings → Pages. All assets and links use relative paths, so repository subpath hosting is supported. No personal data, secrets, tracking scripts, or external analytics are included.

## Research limitations

This is a partial, auditable catalogue, not an exhaustive census. Missing venue-years do not imply zero medical papers. Unreviewed ML title candidates are deliberately not displayed as confirmed medical papers. The fixed retrospective cohort is not the latest CCF ranking or a reconstruction of historical ranks. See [METHODOLOGY.md](METHODOLOGY.md).

## Reuse and attribution

Paper titles, author information, and extracted figures remain attributable to their original publishers/authors. Source links are included per record. The repository makes no blanket license claim over third-party paper content. Review original licenses before redistributing figures or full texts.

Year means the official conference edition label (e.g. CVPR 2020), regardless of the actual meeting or online publication date. 2020 screening is in progress. Resource links are taken from source-paper abstracts.
