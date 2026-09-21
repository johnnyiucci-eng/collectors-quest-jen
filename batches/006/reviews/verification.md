# Batch006 verification

Rebuilt on2026-09-13 after peer and runtime repairs:575 structured rows plus246 full-source passages,432 spans and144 action claims. All950 base and996 fragment quote/location checks pass (1946 checks, not unique excerpts). All246 windows have complete section/reference accounting and consistent explicit entity kinds.

28/28 complete composed answers retrieve all required contexts and match manually source-adjudicated snapshots. Frozen source-first sample22/22 across nine windows, three with no game titles. No denominator change. The shared regression suite passes106 tests, including six new source-bound batch006 checks.

Initial runtime27/28 missed Space Quest's02:50:01; semantic query expansion repaired it. Independent CQ205 peer read found missing Sonic, two absent played actions, four failed canonical/co-subject probes and63seconds movie-inflated game credit. Current actor probes4/4 and peer tail10/10 pass; original failures remain in205-peer-review.md and integration-history.json. No perfect global recall claim follows.

Reproduce build/check/answers/sample/gate with scripts/process_lore_batch.py --collection batches/006; run python -m unittest discover -s tests -p "test_lore*.py". Source timestamps are coarse windows, not stopwatch speech time. Captured-text acceptance is not audio, external catalog, market or live performance certification.
