# Verification record

## Checks completed

- JavaScript syntax checked with `node --check app.js`.
- Public-data validation passed with `python scripts/validate_data.py`.
- Verified unique title/year identities and IDs, 2021–2025 range, membership in the 58-venue CCF cohort, citation source/date presence, image path existence, matched-denominator bounds, exclusion of full abstracts from public records, and JSON/embedded snapshot equivalence.
- DOM-stub behavioral tests exercised initial render, unmatched search, year filter, conference filter, citation sorting, and construction of all analytics views.

## Browser verification status

Real rendered-browser verification is pending a reachable HTTP preview. The cloud browser could not reach the local preview server. Its file protocol restriction was respected. Local Playwright Chromium could not launch because this execution environment restricts sockets; the escalation failed due to an environment filesystem setup error. These are environment blockers, not evidence of successful visual verification.

Responsive breakpoints and accessible controls are implemented, but desktop/mobile screenshots, focus and keyboard flow, export downloads, and actual visual layout still require live-browser inspection. Do not describe the site as fully browser-tested until that inspection succeeds.

## Design

The original concept uses dark navy, ivory typography, cyan network lines, a compact metric band, two-column editorial paper cards, and paired analytical panels. The implemented composition intentionally avoids reproducing invented paper titles or chart values from the visual concept. All populated content comes from the source snapshot.
