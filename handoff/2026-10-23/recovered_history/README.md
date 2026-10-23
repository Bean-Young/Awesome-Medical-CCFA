Upload status: IN PROGRESS. Do not assume the full manifest is present until UPLOAD_COMPLETE.json exists and every manifest hash is verified.

# Recovered review facts, 2026-10-23

This is a selected-field reconstruction from saved Site source version `b2a08baf8e005a6931a7ebb31a11ed13598e1a27`, not the unavailable earlier export and not a claim that the entire project history has been delivered.

- Read `manifest.json` for the actual record counts, source version, omissions and hashes. Counts describe recovered records, not unique papers read or new work.
- Each JSONL event has an `event_id`, selected `record` fields and source file / JSON Pointer references. Exact-equal selected records are deduplicated, with all observed source references retained. Different records for the same paper are intentionally retained: they may be successive stages or conflicting judgments, not additional unique papers.
- Do not assume file order is chronology. Use the recorded timestamps and explicit supersessions. A record without a reading-completion field does not prove reading. Missing fields mean not exported or not present, not false.
- Sources inventory contains hashes and byte sizes for provenance only; source files themselves are not included. Raw abstracts, paper text, HTML, PDFs, media, credentials, request/response headers, private conversations and absolute filesystem paths are not part of this export.
- The source may contain inherited or candidate decisions. Current scientific decisions and later explicit corrections take precedence. In particular, read `../continuation/acl2026_body_continuation.json` before the old ACL 101–200 queue. That later continuation is separate from the recovered source snapshot.
- Some nested evidence structures and long/unsafe values are intentionally omitted. Retain a HOLD where the specific supporting evidence is not available; do not declare a conference or paper fully verified from aggregate counts.
- This export creates no new abstract/body reading credits, no new paper inclusions, and no website publication. Material rights, scientific inclusion, formal long-paper type and actual publication remain separate states.

Use line-oriented reading with `for line in file` or split on the literal newline character. Do not use Unicode-aware `splitlines()` on JSONL text: source titles may contain Unicode line-separator characters inside JSON strings.

Only files listed by the event provenance are included in source_inventory/. Broader intermediate inventories are not part of this deliverable.
