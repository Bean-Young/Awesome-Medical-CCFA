# Current frozen snapshot archive

This archive contains the sanitized 2,004-record saved-source snapshot, rights inventory, media metadata and missing-field queue, not the live website. Run `python restore_current.py` in this directory with Python 3. It verifies all part hashes, base64/gzip/tar hashes and each decoded JSON file before restoring to `restored_current/`.

The frozen public version is v295 with 2,001 records; saved v296 with 2,004 records was not published. Of the 2,513 frozen media assets, six belong only to the saved unpublished source. Their website URLs are not confirmed live; URL/hash metadata does not prove availability. This handoff contains logs/data, not the complete website code or media deployment.

Read `../continuation/CONTINUATION.md` before repeating any of the old 54 body checks: the separate continuation has resolved them. Historical research events are supplied separately; completing this current snapshot does not imply complete historical source coverage.
