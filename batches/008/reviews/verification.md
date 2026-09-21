# Batch 008 verification

Rebuilt from durable inputs on 2026-09-13: 511 structured rows plus 226 full-source passages; 367 spans and 161 action claims. All 721 base and 912 fragment quote/location checks pass (1633 checks, not unique quotations). Every source window is accounted for, each reference has a mapped role, span types are explicit and spoken forms occur literally in the supplied source.

31/31 complete composed answers retrieve all required contexts and match manually reviewed snapshots. Frozen sample: 8/8 references across nine windows, with three no-title windows retained. All 122 shared regressions pass, including source-bound action/identity checks and nine cross-episode continuity cases with 24 source checks.

Initial runtime29/31 missed guest-history and market qualifications. First query repair reached30/31 but lost other required market windows; compact meaningful query finally reached31/31. CQ81 peer found one product-type error and four missing ownership states, repaired and independently verified. CQ207 unspoken sentimental interpretation was removed from prose/lore/action summary.

See integration-history.json and episode audits for initial failures and limits. Reproduce build/check/answers/sample/gate with scripts/process_lore_batch.py --collection batches/008; run python -m unittest discover -s tests -p "test_lore*.py". Captured-text acceptance is not audio, external catalog/price verification, independent archive recall or live cohosting certification.
