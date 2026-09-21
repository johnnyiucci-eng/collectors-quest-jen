# Pilot review verification — 2026-09-12

Local, standard-library checks. No network processing, publication or live cohost mutation.

- Durable merge: seven review fragments cover all ten canonical source keys exactly once; original partial seed maps replaced, not duplicated.
- Database build: 1,492 structured retrieval rows, 1,237 discussion spans, 365 action facts, 129 guarded overrides and 49 additional reference records. Repeated action states are not extra purchases. Full caption windows are indexed separately for answer-context retrieval.
- All annotation quotes match the recorded source windows; span bounds, source hashes, referenced game IDs and override expected values passed build checks.
- Structural validator: ten base drafts, 1,616 original evidence excerpts, zero errors. Original extraction status remains draft; completed captured-text review is recorded separately in the episode ledger.
- Behavioral regressions: 43 tests passed, including new cases for attribution subject versus reporter, non-game exclusion, missing-reference persistence, unknown timing, split returns and hybrid answer context.
- Composed-answer integration: 19/19 required-window checks; manual semantic review documented in answer-review.md, not inferred from the automated result.
- Frozen omission test: repaired map covers 52/52 reference-window buckets; original pre-repair 51/52 is retained. Donkey Kong's inflated boundary is narrowed. `validate_lore_workflow.py` checks this against the built database and checks all 80 mandatory ledger entries.

Reproduce from repository root:

```powershell
python scripts/merge_lore_reviews.py
python scripts/lore_store.py build
python scripts/validate_lore_pilot.py
python scripts/evaluate_lore_answers.py
python scripts/validate_lore_workflow.py
python -m unittest discover -s tests -p "test_lore*.py"
git diff --check
```

No test establishes audio accuracy, independent historical truth, archive-wide recall, live latency or human usefulness. Review fragments and the consolidated annotations are durable; generated SQLite/evidence bundles are rebuildable and ignored by Git.
