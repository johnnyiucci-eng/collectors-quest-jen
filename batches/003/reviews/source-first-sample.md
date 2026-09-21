# Frozen source-first check — batch 003

Nine deterministic quartile windows were frozen before coordinator inspection of extraction records: 24 reference buckets across three episodes, including a no-title window. Initial result: 23/24. Final result: 24/24 after the missing Turok-series identity and span were added; individual games did not count as substitutes.

[Unchanged source text, rules and original denominator](source-first-sample.json) and [failure history](integration-history.json) are retained. A later inspection noticed that the gold itself omitted Caveman from the 01:02:54 window. Existing cq202-g027 already covered it in that window. This is an additional observation, not a newly repaired extraction miss or an independently frozen pass. The sample is bounded and deterministic, not an archive-wide accuracy estimate.
