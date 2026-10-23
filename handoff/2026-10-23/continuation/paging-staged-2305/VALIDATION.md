# Validation summary

## Verdict and scope

**Conditional technical pass for the exact frozen code; not a browser pass, integration approval, or deployment approval.** Existing evidence was checked and summarized for this handoff. No current-data build or real-browser run was performed while packaging it.

The independent v325 validation used commit `f4e40dfdae8b946111ce8547447115d7afdba956`, with 2,008 records / 981 complete core profiles / 1,518 licensed abstracts. It is superseded as a data baseline by saved v326 (2,008 / 983 / 1,520). All data-dependent checks must be rerun on the latest source.

## Passing evidence on the frozen code

- 34/34 paging loader/generator positive and adversarial tests, repeated on the isolated v325 checkout.
- 15/15 source-storage tests and exact source-byte/count verification.
- Independent runtime harness: complete typed snapshot assembly and original pretty/Unicode download bytes; 16 missing, corrupt, truncated, oversized, manifest, order/ID, UTF-8, sidecar, and cross-origin negative cases; fresh retry recovery and retained-retry app-once protection. These are Node VM tests, not browser tests.
- Loader failures did not publish partial global data or initialize the app/Insights. Tests cover later-page pending/failure, final download-hash failure, timeout/late completion, source-root/symlink refusal, and static over-cap refusal.
- Above-32-MiB raw and gzip-only-over-8-MiB transition fixtures. The gzip-only fixture used 13,422,058 raw / 10,109,313 gzip bytes and eight pages, each at most 1,677,758 raw / 1,263,708 gzip bytes. Over-cap legacy representations were omitted.
- Below-cap GET, HEAD, ranges/suffix, If-Range, ETag, and 405 equivalence; above either unchanged cap: bounded explicit 409, bodyless HEAD, 405, and no stale asset fetch. The unchanged legacy handler SHA-256 is `b093e922cacfcbaf283088f5b10bdf90b66d3a542bc63e1055a54a5d14309a64`.
- Static and full five-stage framework builds; targeted science/core/asset/scope/counter/resource/Insights checks; public and Worker privacy; exact referenced-asset closure. Original app.js and global Insights input were unchanged. All 36 guarded scientific/data/media/runtime paths were unchanged by the independent build/package run.
- Official package build and measurement under the unchanged expanded-artifact cap.

## Exact v325 reconstruction and package evidence

- Ordered pages: 8. Largest raw page: 4,191,954 bytes.
- Complete raw JSON: 32,869,134 bytes; SHA-256 `1a89c684bf8d16da15b8e4c43edde14dcdf089c623d377335bedb976aa9f19a5`.
- Aggregate page-plus-sidecar bytes: 33,209,670.
- Manifest SHA-256: `27bb410491d3954205d9327e41c2460b7088cb9f02ecabe902b8a4001f132e2e`.
- Legacy gzip: 5,453,921 bytes. Remaining raw legacy headroom: 685,298 bytes.
- Compressed official archive: 222,365,418 bytes; SHA-256 `86d3750c9af44d165afb4c2f781f310e0235335e120e52ab362c576b5c5f86da`.
- Expanded tar stream: 254,822,400 bytes; regular-file total: 253,946,281 bytes.
- Unchanged expanded-artifact cap: 268,435,456 bytes; measured headroom: 13,613,056 bytes.

The archive and generated data are deliberately not included. With other assets fixed, the projected headroom at the full 48 MiB aggregate bound after retiring legacy gzip was only 1,944,999 bytes. That is an approximation, not a capacity guarantee.

## Known failure, not waived

`validate_data.py` still fails the pre-existing `relevance_tier` assertion for the CVPR 2021 paper “Semantic Segmentation with Generative Models: Semi-Supervised Learning and Strong Out-of-Domain Generalization.” It was recorded unchanged. Do not describe the entire validation suite as passing or weaken the assertion to hide it.

## Missing mandatory evidence

No supported real-browser pass exists. Actual loading/rendering, complete/global Insights, each-page failure and no partial exposure, retry/late-abort isolation, native Blob download bytes/hash, accessible no-JS recovery, and current/over-cap peak memory and responsiveness are all still required. The interactive app retains the full parsed dataset; download hashing also materializes the complete file. Bounded network pages alone do not establish a browser-memory ceiling.

## Handoff integrity checks

All 12 source overlay files were checked against their frozen byte counts and SHA-256 hashes. The optional full files are not redistributed; their exact identities are included. The patch was reverse-checked, reversed, checked, and reapplied in a disposable directory; every resulting file matched the frozen overlay. This verifies patch/overlay consistency, not conflict-free application to v326. The exact patch and original manifest hashes are unchanged. A disclosure review of the final packet found no concrete private file locators, credentials, private reports, or raw paper files; intentional generic privacy-deny patterns were preserved. Optional full-file copies were excluded because an unchanged source file contains an environment-specific packager locator outside the patch diff. No functional code was edited to sanitize it.
