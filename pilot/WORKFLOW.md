# Lore Master processing workflow

Use [requirements](requirements.md) and [progress](PROGRESS.md) together. The ten-episode pilot is the fixed evaluation corpus, not the final archive boundary.

## Mandatory additions — every episode, every batch

The following additions were explicitly required by Johnny after the pilot. They are recurring episode-completion requirements, not one-time pilot improvements. Record each separately in the episode review ledger with evidence/artifact links; no blanket “tests pass” substitutes for them.

- **A1 — Full discussion map:** account for every transcript section; map meaningful game discussion, separate returns, incidental references and uncertain identities. Produce a qualified top-three result or explicitly explain why the source cannot support one.
- **A2 — Omission and identity audit:** check the transcript against extracted mentions, including rapid lists and quiet sections; reconcile game/series/edition identity; report actual audited denominator, misses and repairs.
- **A3 — Speaker and host-era audit:** verify participants and contextual attribution. Preserve uncertainty; do not apply a later host to an early episode.
- **A4 — Action-state audit:** cover supported purchases, orders, receipt, returns, ownership, play, wants and sales throughout the episode. A mention is not a purchase; a purchase is not delivery or continued ownership after a return. Keep canonical subjects and explicit co-subjects separate from reporting speakers and household qualifiers. Explicitly mark no applicable events only after checking.
- **A5 — Complete-answer evaluation:** compose and check multiple useful answers, not only search hits. Check every material claim and citation, correction history and forbidden inferences. Include uncertainty/negative evidence cases. Record failures before repairing them.
- **A6 — Practical brief and usefulness review:** prepare an episode-grounded pre-show brief with prior conclusions, examples, corrections, jokes/open loops, uncertainties and fresh angles. Separate editorial proposals from documented history. Review its actual usefulness; do not label a written review as a live rehearsal.
- **A7 — Durable repair and regression checks:** store reviewed corrections in reproducible inputs, rebuild, run evidence and behavioral checks, and confirm previous fixes survive.
- **A8 — Explicit completion ledger:** record each check as pending, partial, passed, failed, or not applicable with a reason and evidence. Keep unresolved item-level flags. An episode cannot be accepted while a required check is pending/partial/failed; isolated uncertainty may pass only when safely represented and evaluated.

These requirements apply retroactively to all ten pilot episodes and prospectively to every additional episode. Live delivery rehearsal is an additional integration check; repeat it when retrieval/persona/delivery behavior materially changes, without pretending every archive episode needs a recorded voice session.

## One episode through the process

1. Resolve its canonical episode and source versions; inspect existing episode/game/person/platform/topic mappings before adding fields. Preserve source hashes and transcription limits.
2. Read end to end. Map conversation sections, then game discussion spans, references, topics, speakers, claims, action states, jokes, corrections and open loops in the same pass. Repeated returns get separate spans. Never seed spans merely by expanding name matches.
3. Preserve raw names and unresolved candidates. Spoken-form fields must contain literal source wording, not substituted canonical catalog names; keep normalized titles separately. Automated source-presence checks are a minimum, not proof of correct identity or attribution. Link identities only where evidence warrants it; keep a series distinct from a particular game and a regional variant distinct from a new title.
4. Store exact evidence and independent labels for attribution, interpretation, external verification and review state. Do not convert every first-person quotation into the same host's memory.
5. Review separately for omitted references, unsupported claims, identity collisions and span inflation. Include quiet windows, rapid lists, negative examples and interruptions. Mark same-agent review honestly; it is not independent.
6. Record corrections in the separate annotation/override inputs, with reasons and source versions. Rebuild the index; never manually repair only the generated database.
7. Run task tests and regressions. Test actual questions through the same query interface used for retrieval, with explicit expected facts, forbidden inferences and citations. Record pre-repair failures; repaired cases become development tests.
8. Update the batch ledger. Complete records may advance while isolated uncertain titles remain flagged. Do not certify an episode-wide ranking while span mapping is incomplete.

## Ranking rules

Timed sources use the union of annotated caption-window intervals, an estimate rather than precise speech time. Untimed sources use the union of annotated paragraphs. Never compare seconds to paragraph counts. Substantial and supporting coverage are reported separately. Passing mentions and jokes do not earn discussion duration. Overlapping spans of the same game count once; comparisons can legitimately credit more than one game but totals then exceed episode runtime. Uncertainty and incomplete mapping accompany every ranking.

Every new-batch span requires an explicit entity kind. Report series coverage separately from individual games; do not let physical pinball, accessories, films, card games or compilations silently enter individual-game rankings. Preserve useful excluded-category evidence instead of deleting it.

Discussion prominence is not a recommendation, favorites, ownership or purchase ranking. A question with an actor, action or preference constraint must not silently receive a whole-episode prominence result. Preserve ties and state what the metric actually measures.

When an episode presents selection lists, A1/A2/A5 also require checking explicit membership, owner, purpose and exclusions against the source. Starter choices, aspirational choices, considered alternatives and jokes remain separate. Use source-backed `selection_lists` when those groups need direct retrieval; never reconstruct membership from duration or wanted states. Missing typed list data is a retrieval limitation, not evidence that the episode contained no list. Older accepted prose reviews are not automatically a complete typed-list archive.

## Review and evaluation

Keep three distinct suites: source/structure checks, synthetic query-behavior regressions, and source-adjudicated functional cases. A fourth evaluation, live brief usefulness and conversational delivery, requires an actual rehearsal result; a generated brief is not proof of that result.

For game recall, annotate source passages before consulting extracted records, report numerator/denominator and identity ambiguities, and freeze selection rules. Evaluate more than title recall: assess claim support, speaker correctness, action state and false confident answers. Do not claim independence when the same coordinator saw extraction and answer keys.

Preserve original question wording separately from tuned lexical queries. Missing original wording must be counted as excluded from that evaluation, not silently copied from a tuned query. Record required-window recall and returned-context size separately: retrieving most of an episode can pass recall while remaining inefficient. Fresh reviewer wordings become development regressions once inspected or used for repair.

A8 acceptance must be bound to the exact reviewed local source, record, annotations, review inputs and evidence artifacts using `review_binding`. A database rebuild does not renew human review. If those inputs change, inspect the changes, repeat affected checks and explicitly refresh the binding; archive queries exclude missing or stale bindings. The hash proves input identity, not independent semantic truth or live readiness.

Before full-production scale, all critical behavior regressions must pass and the pilot's semantic gate must have actual measurements against the agreed 90% recall/qualified-answer targets. Read-only archive inventory and preparation can proceed while that gate remains open. Thereafter process manageable batches across eras, repeating the same checks. No unrelated record needs to wait for one obscure title's resolution.

## Operating discipline

Keep progress here in the repository, not in conversational memory. Continue normal implementation/review steps without requesting repeated restart permission. Report meaningful findings and genuine blockers, not every internal checkpoint. Do not publish, synchronize private data, activate a persona change or purchase services as a side effect of processing.
