# Batch 002 — captured-text review complete

Completed 2026-09-13: CQ8 (holiday memories), CQ75 (system collecting costs), CQ201 (NES checklist boundaries). Three-era bounded continuation, 48,965 supplied transcript words. Thirteen episodes are now processed across separate pilot and batch collections. Pilot's ten episodes and evaluation set remain unchanged.

All [A1–A8 requirements](../../pilot/WORKFLOW.md) remain mandatory for every episode, every batch. See the [individual evidence ledger](episode-review-ledger.json). Completion means captured-text development review, not audio or live certification.

| Episode | Full source windows | Discussion spans | Action claims | Composed answers | A1–A8 |
| --- | --- | --- | --- | --- | --- |
| 8 | 27 | 30 | 30 | 5/5 | Passed |
| 75 | 59 | 100 | 41 | 6/6 | Passed |
| 201 | 150 | 264 | 46 | 6/6 | Passed |

The rebuilt batch has 488 structured search rows plus 236 full-source passage rows. All 17 complete development answers were source-adjudicated and retrieve required context. A fresh source-first sample of nine deterministic quartile windows was frozen before coordinator inspection of extraction records: 27/27 reference buckets are covered, with a no-title window retained. A separate reviewer sample covers 11/11. All 56 regression tests pass and the fixed pilot's checks still pass. These are bounded development checks, not archive-wide accuracy estimates.

Important repairs: CQ75's repetitive transcript tail is retrievable as a source warning but does not inflate discussion; intended play, donations, purchase/delivery and third-party actions remain distinct; CQ201's Stadium Events prominence fell from 892 to 451 meaningful seconds after passing comparisons were reclassified. All mentions remain searchable.

See [qualified game leaders](reviews/top-games.md), [answer review](reviews/answer-review.md), [source-first checks](reviews/source-first-sample.md), [host-era findings](reviews/host-era-findings.md) and [verification commands](reviews/verification.md). Each episode audit contains its practical preparation brief.

Query with `python scripts/lore_store.py search "Metroid" --collection batches/002 --episode 8`. Default queries still search only the pilot; see [collection commands and scope](../README.md). A miss in either collection is not proof of archive absence.

Base extraction records retain extracted_draft status; ambiguous titles/speakers, historical claims, coarse timing and damaged source text remain qualified. No audio/live certification, publication, private import, paid processing or live Jen connection occurred. This bounded batch is complete; no further episodes were started.
