# Batch 003 verification

The collection was rebuilt from durable records and review fragments on 2026-09-13. Results: 428 structured rows, 183 full-source passage rows, 326 spans and 120 action claims. All 693 base and 706 fragment exact quote/location validations passed (1,399 checks, not unique quotations).

The original acceptance passed 79 regression tests; the later explicit-type/series reconciliation passed 99 shared regressions. Current counts above include four separately typed CQ202 returns added during that review. All 183 source windows are explicitly accounted for exactly once; every recorded reference evidence window has a mapped role. All 22 composed answers retrieve required source context and match their manually adjudicated answer snapshots. Frozen sample coverage was 23/24 initially and 24/24 after a separate Turok-series record was added. The original gold omitted an already captured Caveman reference; that limitation is not hidden by changing the denominator.

Observed integration failures and repairs are in [integration history](integration-history.json). A synthetic test initially rejected every title containing “remake”; it was narrowed to Final Fantasy VII Remake because the source genuinely reports playing other handheld remakes. That was a test-oracle defect, not an extraction repair.

Fixed pilot remains 10 episodes: 1,616 exact base checks, 19/19 development answers and 80 mandatory checks with 52/52 repaired frozen references. Batch002 regressions remain in the shared suite. No pilot denominator expansion.

Reproduce from repository root:

```powershell
python scripts/process_lore_batch.py build --collection batches/003
python scripts/process_lore_batch.py check --collection batches/003
python scripts/process_lore_batch.py answers --collection batches/003
python scripts/process_lore_batch.py sample --collection batches/003
python scripts/process_lore_batch.py gate --collection batches/003
python -m unittest discover -s tests -p "test_lore*.py"
python scripts/validate_lore_pilot.py
python scripts/evaluate_lore_answers.py
python scripts/validate_lore_workflow.py
```

Acceptance is captured-text development review only. Historical claims are not externally authenticated, undiarized speakers retain confidence qualifiers, caption durations are approximate, and no live cohosting rehearsal is claimed. Earlier audit handoff statements that A7/A8 were pending are superseded by the final ledger, not erased.
