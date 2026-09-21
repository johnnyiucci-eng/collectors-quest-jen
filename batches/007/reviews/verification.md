# Batch 007 verification

Rebuilt from durable inputs on 2026-09-13: 386 structured rows plus 129 full-source passages; 290 spans and 131 action claims. All 509 base and 662 fragment quote/location checks pass (1171 checks, not unique quotations). Every source window is accounted for, each reference has a mapped role, span types are explicit and spoken forms occur literally in the supplied source.

25/25 complete composed answers retrieve all required contexts and match manually reviewed snapshots. Frozen sample: 26/26 references across nine windows, with three no-title windows retained. All 122 shared regressions pass, including source-bound action/identity checks and nine cross-episode continuity cases with 24 source checks.

Initial sample21/26 exposed Dragon Warrior series, Wii U Kart8 and Outlast returns/sequel gaps. Initial runtime24/25 missed six ranking windows; meaningful query repair retained them. Returned-copy state and literal aliases were repaired. A malformed intermediate CQ80 JSON from a truncated editing read was reconstructed and validated; source files were untouched.

See integration-history.json and episode audits for initial failures and limits. Reproduce build/check/answers/sample/gate with scripts/process_lore_batch.py --collection batches/007; run python -m unittest discover -s tests -p "test_lore*.py". Captured-text acceptance is not audio, external catalog/price verification, independent archive recall or live cohosting certification.
