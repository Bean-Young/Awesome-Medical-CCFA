# Complete-catalogue paging prototype: review handoff

**UNINTEGRATED. Conditional technical pass only. Real-browser QA has NOT passed. Hold source integration/save. Production remains v299; no deployment is authorized.**

This is a small code-and-status packet for repository review, not a deployable website, full repository, or current generated-data package. No source integration, upload, push, or deployment was performed to prepare it.

The patch is relative to the recorded v324 repository baseline and requires the complete repository context. Patch/overlay consistency was verified, but conflict-free application to v326 has not been certified. Inspect and dry-run it in an isolated checkout; do not treat this packet as a self-contained runnable site.

## What is included

- `runtime-paging.patch`: the exact frozen reviewed patch, unchanged.
- `reviewed-overlay-manifest.json`: the original byte counts and SHA-256 identities, unchanged.
- `VALIDATION.md`: compact evidence summary and explicit gaps.
- `MIGRATION.md`: conditions for validation, integration, and rollback.
- `STATUS.json` and `HASHES.json`: machine-readable status, baselines, and identities.
- `SHA256SUMS`: checksums for all packet content except the checksum file itself and its distribution archive.

No research datasets, generated page snapshots, raw PDFs, large build archives, private reports, credentials, or concrete private filesystem locators are included. Generic forbidden-path patterns in privacy regression tests are intentional and retained exactly. Public project URLs and synthetic test URLs are not private endpoints. No sanitization changed functional code. Optional full-file copies are omitted because one unchanged source file contains an environment-specific packager locator outside the patch diff. The exact patch and all 12 full-file identities remain included; do not silently rewrite that source locator during migration. Any portability change needs separate review and new hashes.

## Baselines: do not mistake old evidence for current validation

- Patch-generation baseline: v324, commit `a458d71212a81dd771e7c5f6b7e00f6ccf98626d`. This is the baseline retained in the original overlay manifest, not the latest data.
- Independent validation baseline: v325, commit `f4e40dfdae8b946111ce8547447115d7afdba956`: 2,008 records, 981 complete core profiles, 1,518 licensed abstracts.
- Latest saved source identified for this handoff: v326, commit `f7d117696cf28ee40781f269d2df989660ddf314`: 2,008 records, 983 complete core profiles, 1,520 licensed abstracts.
- Production: v299. The paging prototype is not integrated into the saved source or production.

**Regenerate on v326 or whichever clean source baseline is latest at integration time.** Repeat all data-dependent equivalence, science, privacy, asset-closure, build, capacity, and real-browser checks. Never reuse the v325 generated pages or package as validation of v326.

## API and completeness contract

The prototype uses the versioned `medical-ccfa-papers-v1` interface. Discovery is `/data/papers-v1/manifest.json`; the generated loader pins a hash-addressed manifest and ordered, bounded, content-addressed pages. Complete snapshot keys, scalar metadata, records, coverage, and scope are assembled before the catalogue or global Insights starts. No partial Atlas dataset or partial Insights is an acceptable fallback.

The legacy `/data/papers.json` keeps its existing **32 MiB raw / 8 MiB gzip** caps. Below both caps, the original complete bytes and GET/HEAD/range/ETag behavior remain exact. Above either cap, the Worker returns an explicit bounded HTTP 409 `catalogue_requires_paging` response with manifest and complete-download alternatives, including for old conditional/range requests. HEAD is bodyless; unsupported methods return 405. No subset, stale response, redirect, or 200 error object substitutes for the original array.

`/data/papers-v1/download.html` assembles a complete client-side download and verifies its final byte length and SHA-256 before saving. This preserves exact original JSON bytes, including whitespace and Unicode, rather than reserializing or exporting a subset. Native-browser execution of this download remains unverified.

New collection limits are 4 MiB raw / 2 MiB measured gzip per page, 16 pages, 5,000 records, a 64 KiB manifest, 2 MiB per sidecar, and 48 MiB aggregate page-plus-sidecar bytes. These do not raise any legacy response or deployment limit. No dependency, credential, binding, permission, or scientific-data omission is added.

Above the legacy caps, generic static hosting, including GitHub Pages, is unsupported without a separately reviewed equivalent non-200 error route. A GitHub repository upload is not a deployment solution. Do not publish the preparatory static output as if it provides the Worker contract.

## Capacity warning

At v325, the complete raw JSON was 32,869,134 bytes. The official package expanded tar stream was 254,822,400 bytes against the unchanged 268,435,456-byte cap, leaving 13,613,056 bytes. The legacy raw endpoint had only 685,298 bytes of headroom. These are historical v325 measurements, not v326 capacity approval. Paging is a bounded bridge, not unlimited growth; remeasure every actual baseline.

## Browser blocker

A test listener could fetch its own loopback endpoint successfully (HTTP 200), but a separate command received connection refused while that listener was still running. Installed Chromium also failed before navigation because socket creation was denied. No supported reachable alternative preview/browser environment was available during review. These observations are environment limitations, not browser passes and not proof that all preview routes are impossible.

Required evidence still includes actual loading/rendering, complete/global Insights, every-page failure with no partial publication, retry and late-abort isolation, native complete-download hash, no-JavaScript recovery, and peak memory/responsiveness at current and over-cap sizes. Node VM tests do not satisfy these gates.

See `MIGRATION.md` before applying any change. Source save and production publication are separate decisions; neither is authorized by this packet.
