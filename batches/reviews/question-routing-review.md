# Question routing development review

The frozen original-wording baseline remains112/116 in original-question-diagnostic.json. Generic routing now recovers116/116 without rewriting those questions or dropping required locations. The73 cases lacking a distinct original question remain unmeasured. The shared suite passes138 tests after the first routing implementation and whole-word ranking guard.

`answer_evidence` remains the caller interface. It now exposes effective/omitted lexical terms, the16-term limit, collection scope, selected route, added seed windows and returned/total context counts. Rank requests use typed game prominence (including ties and close runners-up), open-loop requests use recorded leads/wants/orders, and biography/event-work requests add a disclosed generic lexical pass. No episode IDs, answer keys or known target locations appear in routing code. Ordinary title queries retain lexical behavior.

The design skill kept this behavior behind the existing small interface and tests across that same interface. Results remain evidence packets, not automatically certified answers. The search budget was not silently enlarged; omitted terms are now visible. New paraphrases are being independently authored without consulting implementation details and will be tested before being tuned.

Important load measurement: median returned context is two-thirds of a short untimed episode.35/116 questions return at least75% of source windows; one returns the whole episode. These coverage passes are therefore not evidence of high precision or low conversational context cost. Future compact retrieval work must preserve qualifications rather than simply deleting context to improve a size metric.

Reproduce with `python scripts/evaluate_lore_questions.py --collection batches/007 --collection batches/008 --collection batches/009`. Rebuild collections after shared query code changes; source fingerprints deliberately reject stale databases.

## Three-hour continuation checkpoint, September13, 13:28 UTC

The preceding138-test result and116-case context measurement are historical checkpoints, not current totals. The shared suite now passes195 tests. Batches010–015 have282 manually checked answers, with all original wordings and required evidence locations retained; final original and tuned retrieval pass for each batch. Their42 source-informed fresh wordings also pass, but are development cases after use, not blind tests.

Generic routes now cover origin/correction, ports, hypothetical releases, collecting process, preorders, actual acquisitions and additional natural prominence phrasings. The acquisition route preserves person-identification questions such as “Which collector bought this game?” as lexical queries. One shared-suite failure exposed that distinction; it was fixed rather than changing the test. A separate small lore channel keeps multi-game explanations from being crowded out by repeated title occurrences. No episode IDs or answer-specific target locations were added to routing logic.

The interface remains evidence retrieval, not generated-answer certification. Broad context remains a known cost: coverage success alone is not retrieval precision. Final original-wording and fresh-question result files under010–015 retain context diagnostics. Every accepted batch002–015 was rebuilt and re-gated after the final code change. Exact review bindings are distinct from database freshness; a rebuild cannot grant semantic approval. Batch016 remains excluded pending its full review.
