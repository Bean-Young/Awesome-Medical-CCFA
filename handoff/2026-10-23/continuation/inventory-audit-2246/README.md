# ICML inventory selector regression and frozen evidence

This is a staged, read-only inventory audit. It does not change scientific fields, canonical IDs, source IDs, rights decisions, credits, application code, or deployment. It does not establish that ICML has been exhausted or reapprove every existing scope inclusion.

## Two separately identified snapshots

- Baseline v325: commit `f4e40dfdae8b946111ce8547447115d7afdba956`, papers SHA-256 `1a89c684bf8d16da15b8e4c43edde14dcdf089c623d377335bedb976aa9f19a5`. The 403 ICML records include 42 with metadata_ready=false: 2020=16, 2021=7, 2022=2, 2023=1, 2024=7, 2025=8, 2026=1.
- Later saved v326: commit `f7d117696cf28ee40781f269d2df989660ddf314`, papers SHA-256 `8ad448e88dee4620d832457bf7d9f6a80663ea98c2880ffae04c979c7b1a10e0`. Separately observed 40 incomplete, with only Laforgue2020 and Wang2020w changing from false to true. This audit did not integrate those profiles. Later counts are metadata observations, not a mixture with the frozen v325 guard results.

## Frozen baseline findings

- All 403 current ICML records have literal venue ICML and track Main. The selector imposes no year/track/publication-type restriction. Four of the 42 incomplete records lack publication_type; no value is inferred. The report preserves paper_type separately.
- 27 incomplete records have an absent asset: 26 lack both paths, and Langbein2025 lacks the first-page path while its figure is cleared. There are 53 absent paths, zero referenced-but-missing files, and zero invalid/nonlocal references.
- The other 15 records have both files present but at least one guard hold. Across all 84 incomplete asset slots: 53 absent, 26 present but held, and 5 present and cleared. Five records have one cleared and one held asset; four of those have both files, while Langbein has the mixed physical-presence case.
- The narrower older-packet inventory covers 26 ICML 2020–2023 records, not all 42: 5 component-rights holds, 6 access holds, 10 scope holds/proposals, 3 unscreened records, and 2 selected reviews still incomplete at baseline. Its separate two NeurIPS records are excluded from all ICML counts.
- The three previously missed canonical IDs remain unchanged: ICML2020-chen20h, ICML2020-brennan20a, ICML2020-bao20b. Their indexed inclusion is not a new scope approval.
- Actual committed media-rights guard execution matches the metadata flag and cached media decisions for all 403 ICML records. Asset existence is not treated as permission evidence.
- Candidate collision checks report no exact/casefold catalogue-ID collision, normalized-title/article-URL/PDF-URL collision touching ICML, PMLR source-identity collision, or conflicting PMLR IDs across the two source URL fields. Canonical and source IDs are preserved independently; no rows are merged.

## What the tests establish

Run from this packet directory:

    PYTHONDONTWRITEBYTECODE=1 python test_inventory_regression.py

The 19 offline tests cover case-insensitive venue equality, independence from ID prefixes, all years/tracks, exact boolean-false selection, case-sensitive canonical/source-ID preservation, collision reporting without merging, distinct publisher IDs, and the frozen report's counts/partitions. They do not claim to rerun the source guard without the repository and assets.

The browser's current filter expression is `(!venue||p.venue===venue)`: it is exact venue equality, not an ID-prefix filter. This packet tests the staged inventory selector only. It is not a deployed browser case-folding fix and contains no browser/runtime test claim.

## Reproduce the full evidence

The supplied audit script imports the exact committed `scripts/media_rights.py` with bytecode writing disabled. It reconstructs the v325 papers from the commit's hash-bound shard manifest, verifies the exact papers digest, and copies only exact committed ICML asset blobs into an external frozen fixture before guard execution. It reads later active metadata separately and verifies whether its digest matches the saved HEAD manifest. It makes no network requests and refuses an output directory inside the active repository.

    PYTHONDONTWRITEBYTECODE=1 python audit_icml_inventory.py --root REPOSITORY --output EXTERNAL_AUDIT_DIRECTORY --holds NARROW_PACKET_INVENTORY_JSON

The repository and narrow-packet source are inputs, not included in this small packet. Raw source data, image assets, and the private reproducibility fixture are deliberately excluded. Public JSON contains no absolute workstation paths. `SHA256SUMS` pins every included evidence/code/test file; it is not a signature.

No new-paper, scientific-reading, or core-completion credit is claimed by this audit.
