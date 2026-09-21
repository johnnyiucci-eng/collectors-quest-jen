# Pre-batch safeguards and batch016 restart

User authorized three additions: early draft validation, archive preservation and observed efficiency measurements, then resuming the next batch. Implemented in `scripts/lore_safeguards.py` and the workbench CLI. Design skill guided the small callable interfaces; research skill supplied a bounded same-agent CQ215 follow-up while coordinator implemented checks. No model change, paid API, private import, publication or persona activation.

## Checks implemented and exercised

- Preflight checks source/metadata, topic location arrays, review notes, span IDs/roles, full section accounting, reference mapping and list structure without building a database. Run per episode as soon as its draft lands. Actual016 passes for22/89/215,1097 spans and312 windows. This is readiness, not semantic approval.
- Archive baseline freezes the52 approved collection/episode/source/hash identities in `batches/generated/archive-baseline.json`. The guard detects disappearance or replacement even if total counts stay equal, opens each expected fresh database and exercises search. Baseline creation refuses overwrite; CLI verification runs the guard before and after work, including cache hits. Missing/stale approval cannot be fixed by lowering the baseline.
- Workbench events record elapsed command execution, output characters and source-window displays keyed by reviewer and source hash. Repeated display counts are observations, not reread certification. Distinct reviewers and changed source versions are separated. Only future workbench calls are measured; earlier work has no invented metrics.
- Eight new tests cover clean/no-write preflight, missing locations/note, duplicate spans, missing drafts, archive replacement/loss/additions, empty baseline and measured repeats. The full suite passed214/214 in90.231seconds. Archive guard passed52/52 with no database failures after that run. `git diff --check` passed.

## Actual next-batch work

Resumed016 rather than opening017 prematurely. CQ215 same-agent follow-up inspected25 answers and130 list members, rereading50 targeted windows, with concrete issues and citations in `016/reviews/215-followup-review.md`. Coordinator independently read source windows0–20,94–95 and163–166 this turn. The27 window displays were measured with reviewer root; they are not a claim of completing all179 windows.

Coordinator verified02:53:37 says Pac-Man Vs. has not arrived and does not confirm dispatch. The `cq215-pickups` answer now says “has not yet arrived; shipment is not confirmed.” Original question and required locations are unchanged. The unsupported specific Batman movie-ticket identity was independently confirmed at01:41:35 and remains a priority for durable record/span/list repair. Other pending findings include list owner, Animal Crossing paired-window proof, Resident Evil addendum, optional packaging examples and sale-versus-ask wording.

No batch016 ledger or acceptance binding was issued. The known57/62 tuned and56/62 original retrieval baseline remains preserved; episode acceptance requires the unfinished full independent CQ215 read, all affected semantic repairs, omission sample, answer snapshots, original/fresh retrieval and A1–A8 checks. The52 approved episodes remain the searchable reviewed scope.

Final settled-input verification: run20260913T173641747962Z passes build/structure and52/52 archive preservation, with the same57/62 tuned and56/62 original open failures and no stable-input error. No repeated command is credited as a semantic fix. Measured workbench sample now contains9 events,41.016seconds of command execution,34,394 output characters and27 source-window displays with zero same-reviewer/source repeats. This is a small forward-looking observation, not a claim about prior session usage or billing savings. Source read resumes at CQ215 cursor21; the remaining targeted already-read ranges are documented in the coordinator handoff.
