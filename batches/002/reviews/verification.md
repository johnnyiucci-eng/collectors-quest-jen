# Batch 002 — verification, 2026-09-13

Scope: CQ8, CQ75 and CQ201; 48,965 supplied transcript words and 236 source windows. All three full-source maps and desk-reviewed briefs are complete at captured-text development level.

Final rebuilt collection: 488 structured search rows, 236 full-source passage rows, 394 discussion spans and 117 action claims. Base records contain 271 reference records, 93 lore entries and nine dedicated corrections; inline corrections create additional indexed correction rows. These counts are different representations, not additive unique facts.

Executed checks:

- Build and freshness check: 765 base-record and 842 review-fragment quote checks passed (1,607 validations, not unique quotations).
- Complete-answer retrieval: 17/17; all 17 separately source-adjudicated in answer-review.json.
- Frozen coordinator source-first sample: 27/27 reference-window buckets across nine windows, including one no-title window.
- Additional CQ201 reviewer sample: 11/11 across three windows, reported separately.
- Unit/regression suite: 56 tests passed.
- Fixed pilot: 1,616 excerpt checks, zero structural errors; 19/19 development answer checks; all 80 recurring ledger checks and 52/52 frozen references still pass.

Durable changes: separate collection manifests/builds and guarded database paths; source-warning retrieval without counting damaged transcript repetitions as discussion; corrected action/host and game-versus-series representations; Stadium Events role repair (892→451 meaningful seconds); and regressions protecting the pilot, source evidence, required answer context and repaired rankings.

Reproduce:

```powershell
python scripts/process_lore_batch.py build
python scripts/process_lore_batch.py check
python scripts/process_lore_batch.py answers
python scripts/process_lore_batch.py sample
python scripts/process_lore_batch.py gate
python -m unittest discover -s tests -p "test_lore*.py"
python scripts/validate_lore_pilot.py
python scripts/evaluate_lore_answers.py
python scripts/validate_lore_workflow.py
git diff --check
```

The [individual ledger](../episode-review-ledger.json) requires A1–A8 for every episode. Gate acceptance is captured-text development review only. Contextual speaker identities, unresolved titles, coarse timing, damaged source text and historical claims remain qualified. No audio review, live rehearsal, external factual certification, publication, paid processing or live Jen connection occurred. Generated databases and answer bundles remain rebuildable local artifacts.
