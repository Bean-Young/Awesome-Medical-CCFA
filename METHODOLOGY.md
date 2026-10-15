# Methodology and limitations

## Population and scope

The intended population is main-conference full research papers published in 2021–2025 at the 58 A-ranked conferences in the CCF 2022 sixth edition. This fixed cohort is applied retrospectively. It is not the CCF 2026 list and does not claim every venue had the same historical rank in every year. Journal papers, workshops, posters without full papers, demonstrations, tutorials, short papers, and Findings volumes are excluded unless separately and explicitly justified. ACL currently includes main-track long papers only.

The complete conference list and catalogue provenance are in `data/scope.json`. ECCV, EMNLP, MICCAI, and ICLR are not silently added. ICCV is not held in even years.

## Sources and review

Primary proceedings and public bibliographic metadata provide titles, authors, years, abstracts, and paper links. Collectors record event-specific screening methods in `data/coverage.json`. Keyword screening has imperfect recall and precision. A title-negative paper can contain an important clinical application. Broad molecular, biological, or neural terms can also identify nonmedical papers.

Records explicitly marked as unreviewed candidates or pending abstract verification are excluded from the visible medical catalogue and preserved in `data/pending_candidates.json`. Record inclusion reflects the collectors' relevance review, not independent full-text clinical evaluation. Different sources may have different review depths.

## One-sentence introductions

Introductions are concise, title-derived descriptions unless a record has an independently prepared paraphrase. They do not imply validated findings or clinical efficacy. Full abstracts are kept in local research inputs only and are not redistributed in the website or public data. Readers should consult the full text before relying on scientific claims.

## Figures and affiliations

Missing main figures are explicitly marked "Figure not yet extracted". Only source-paper images may appear as research figures. A first extracted figure may be a preview rather than the paper's designated main figure; this must be labeled in its asset provenance. Decorative network art in the page header is interface artwork and is not presented as research evidence.

Affiliations can come from original papers or publication-linked OpenAlex metadata. Aggregated bibliographic affiliations may be imperfect and are not current-employment assertions. They are not represented as PDF-verified unless explicitly checked.

## Measurements

- Indexed papers: deduplicated included records, not all medical papers in the field.
- Conference counts and annual counts: selected indexed records only. No inference of true growth is justified from changing source coverage.
- Topic heatmap: selected records with each tag by year. Tags overlap; totals can exceed the number of papers.
- Observed venue-year share: selected indexed medical papers divided by eligible papers in the matched source event/track. This is not a recall-adjusted estimate of the true medical share. Unknown or invalid denominators have no percentage. Unreviewed events must not be interpreted as zero medical research.
- Citation-based popularity: source-reported citation counts for exact matched papers with a retrieval date. Missing counts are null, not zero. Sources can merge versions. Citation counts depend on publication age, field, and indexing; they are not an intrinsic quality or clinical-impact measure. No inferred popularity proxy is used.

## Reproducibility

`data/snapshot.json` contains the full reviewed snapshot and build time. `data/snapshot.js` embeds the same snapshot for dependency-free browser use. Individual JSON files expose papers, coverage, scope, and pending candidates. The filtered export records active controls, selected records, and export time. `scripts/build_data.py` recreates the snapshot from collector outputs.

## Coverage states

"Event collected" means source data exists for that venue-year; it does not mean exhaustive medical screening or full metadata completion. "Not yet audited" is an unknown state, not zero. "Not held" is used only for verified nonannual event gaps. The metadata completeness panel counts populated fields and does not equate population with independent verification.

## Responsible use

This research-discovery tool is not medical advice or a clinical decision system. Verify original claims, datasets, validation settings, and licenses before reuse.
