# Medical CCFA saved-source handoff index

This compact index describes saved v335 (commit 8e2016b4a600569919c3e25f23f9e0b06c81bd59), NOT the live website. It contains 2,008 case-sensitive included paper IDs, 999 recorded strict core-complete profiles and cleared media pairs, and 1,521 licensed original-abstract flags. No abstracts, full text, PDFs, contact details or clinical record text are included.

Read manifest.json first for column definitions, recorded conference/edition/track stages and caveats. Ordered papers shards are compact row arrays. Ordered url_entries shards and url_prefixes.json reconstruct exact existing source URLs using a lossless prefix dictionary. Manifest ordering is mandatory. Media hashes are independently calculated from the current asset bytes and match every recorded gate hash present. Permission holds remain holds. Source URLs and historical reading claims are not newly revalidated by this export.

changes_since_v296.json compares exact saved source records, not live/hourly growth. The four added IDs comprise three ACL 2026 records and one separately listed old-scope restoration. Core-complete changes are NOT comparable across the older and stricter current permission definitions. Existing paper metadata, asset or permission work must not be counted as new papers or new science reads.

NeuJoRN (2021.acl-long.219) and AMR489 (2021.acl-long.489) are separately recorded as reviewed but unintegrated material packets, with zero saved/live completion increment. Do not merge them merely because their recovery evidence exists.

This index covers current INCLUDED records only. The prior published historical decision ledger remains needed for excluded/pending decisions and evidence details. An absent per-paper reading flag means unrecorded here, not unread. Recorded conference-stage completion does not independently recertify the unavailable original complete per-paper ledger.

checksums.json gives SHA-256 of each deliverable. Concatenating ordered shard arrays exactly reconstructs the canonical arrays whose hashes are recorded in manifest.json. Export creation makes no source changes, publication, integration or new reading claim.
