# Batch 004 verification

Rebuilt after durable repairs on2026-09-13. 506 structured rows plus218 full-source passages;386 spans and125 action claims. All834 base and914 fragment quote/location checks pass (1748 checks, not unique excerpts). All218 windows accounted exactly once and every record reference evidence window has a mapped role; every span has a consistent explicit entity kind.

25/25 actual composed answers pass required runtime context and exact manual-review snapshots. Frozen sample:14/14 reference buckets across9 windows, including4 no-title windows. Selection preceded record comparison; not statistically representative or externally blind.99 regression tests pass, including purchase/unknown-actor, type and cross-episode controls.

Initial CQ10 trade/joint-owner filtering and CQ77 Maze-purchase/manual-actor certainty defects were repaired. Peer CQ77 initially6/7answers (31/33checkpoints), runtime24/25batch; repaired to25/25without dropping requiredintro. Series/non-game types and SpookySwamp union corrected; CQ203 specific titles split from series.

Reproduce: python scripts/process_lore_batch.py build --collection batches/004, then operations check, answers, sample, gate. Run python -m unittest discover -s tests -p "test_lore*.py" and python scripts/evaluate_lore_continuity.py. A7/A8 references durable artifacts, not ignored generated output. Captured-text acceptance is not audio, external history, current valuation or live cohost certification.
