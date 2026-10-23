# Migration and rollback gates

Keep this prototype unintegrated until all required gates pass. The packet authorizes no source save, upload, push, or production deployment.

1. Pin the latest clean source commit and record exact source-shard/raw/snapshot hashes, record/core/abstract counts, media-rights state, and native-media verification. The independent evidence baseline was v325; saved v326 is newer. Regeneration against v326 or the later actual integration baseline is mandatory.
2. Use an isolated validation checkout. Apply only the exact reviewed patch there after a dry-run/conflict check. The recorded full-file hashes identify the reviewed code; they are not permission to overwrite newer source. Optional full-file copies are not included. Do not copy old generated chunks, pages, snapshots, media, or research evidence. Any conflict resolution or functional code change requires an explicit reviewed delta and new hashes.
3. Hydrate current sources with the existing source workflow. Verify sources and run paging/generator tests. Run the static build before static asset-closure and privacy tests, because the framework build replaces that preparatory layout. Run targeted scientific/core/assets/scope/counters/resource/Insights tests, the official framework build, Worker privacy, and legacy routing tests. Report the known baseline assertion failure separately and unchanged.
4. Regenerate manifests/pages deterministically. Independently reconstruct every original raw byte and compare every snapshot field, scalar, record, coverage, and scope value. Check source guards. Retest both raw-over-32-MiB and gzip-over-8-MiB transitions, old conditionals/ranges, 409/HEAD/405 behavior, and absence of stale raw/gzip assets. Explicit generic-static over-cap builds must refuse.
5. Run the official packager for the actual framework output. Measure expanded tar stream and regular-file totals, not just compressed archive size. Stay below the unchanged 268,435,456-byte expanded cap and demonstrate useful growth headroom. Stop if insufficient; do not raise caps, discard evidence, change native-media rules, or claim v325 headroom applies to a newer baseline.
6. Obtain supported real-browser evidence against this exact current artifact and representative over-cap fixtures. Verify:
   - successful loading/rendering and complete global Insights independent of card filters;
   - failure of each page with no partial Atlas data, app, or Insights publication;
   - clean retry, retained-retry app-once protection, and late-abort isolation;
   - the actual saved complete Blob download length and SHA-256;
   - accessible loading/error states and no-JavaScript recovery with every ordered page and sidecar;
   - load time, peak memory, and responsiveness at current and over-cap sizes.
   Node VM results are not a substitute. Do not bypass browser or environment restrictions to manufacture a pass.
7. Only after the independent review and all integration gates are accepted should the designated source maintainer perform an authorized source merge/save. Re-pin and rerun if the baseline changed during validation. Keep source save distinct from production publication. No deployment follows automatically.

## Rollback

Restore code without rolling back newer scientific data, source shards, licensed content, or verified media. Keep the previous source version as a code reference. If current data exceed the old legacy raw or gzip cap, an old-code rollback must refuse the legacy response rather than publish oversized, truncated, partial, or stale JSON. Generic static hosting above the caps remains unsupported without a separately reviewed explicit error route.

## Minimal repeatable checks

In an isolated full repository containing current source, the included scripts support:

```sh
python3 scripts/catalogue_source.py hydrate
python3 scripts/catalogue_source.py verify
node scripts/test_paged_runtime.cjs
python3 scripts/build_static.py
python3 scripts/test_build_assets.py
python3 scripts/test_public_data_privacy.py
npm run build
python3 scripts/test_public_data_privacy.py --worker
node scripts/test_catalogue_routing.mjs
```

This command list is a subset, not a release recipe: add the repository's source-storage and scientific suites, independent equivalence checks, official expanded-package measurement, and the mandatory real-browser matrix above. The handoff alone is not runnable as the full site and contains no current research data.
