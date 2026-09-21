# Efficient Lore Master processing

Current checkpoint (2026-09-14):021/022 add the user-selected Halloween episodes CQ102/130, bringing the reviewed archive to66 sources. This pair covers33,407 words, about3.3 times the prior CQ25/26 pair's10,132 words. It took roughly75 minutes including separate full reads, artifact/answer review, input cleanup, a shared retrieval repair, regressions and final handoff. See [the Halloween pair report](022/PROGRESS.md) for exact phase times. The [prior short pair](020/PROGRESS.md) took about25 minutes; different source density and repair work prevent a controlled speed-multiplier claim. Earlier017-failure/55-source reports below are historical measurements, not current blockers.

The local workbench reduces avoidable model context and repeated machine execution. It does not replace any A1–A8 requirement, source reading, independent adjudication, full answer evaluation or exact review binding. It makes no paid model calls and does not select a different model.

## Read once per reviewer, resume precisely

```powershell
python scripts/lore_workbench.py source --collection batches/016 --episode 215
```

The response contains whole source windows, their exact text, a source SHA and `next_start`. Use the returned cursor and hash for the next page:

```powershell
python scripts/lore_workbench.py source --collection batches/016 --episode 215 --start 5 --source-sha HASH_FROM_PREVIOUS_PAGE
```

The5 is only an example: always use the actual returned `next_start`. Default item budget is12,000 serialized characters, not tokens. If a single window is too large, the command refuses to truncate it and reports the required budget; pass `--budget` explicitly. Changed source content invalidates the resume hash, even if the manifest was updated. Displaying a page does not mark it read. Record each reviewer's actual completed range and next cursor in the handoff; extraction and independent review still require distinct full reads. Once a reviewer has finished the full source, reread only passages needed to resolve a specific issue, plus their context.

## Inspect answers and lists without recursive evidence dumps

```powershell
python scripts/lore_workbench.py answers --collection batches/016 --episode 89
python scripts/lore_workbench.py actions --collection batches/018 --episode 24
python scripts/lore_workbench.py lists --collection batches/016 --episode 215
python scripts/lore_workbench.py references --collection batches/019 --episode 218
python scripts/lore_workbench.py spans --collection batches/019 --episode 218
python scripts/lore_workbench.py failures --collection batches/016
```

All views paginate with `--start` and `--budget`. Answers retain full prose, original question, tuned query, forbidden inferences and required locations. Lists retain owner, purpose, membership, status and reasons, but do not repeat every full transcript quote. Failure views return only missing evidence locations and identifying question fields. Follow locations back to the source when evaluating support. Omitted nested evidence is a display optimization, not permission to omit evidence from stored records or reviews. No hidden character truncation or ten-item list cutoff is allowed.

Keep normal word boundaries in every searchable title, context and summary. Shorter output is achieved by selecting fields and deduplicating repeated explanations, never by joining prose words. Under each episode's existing A4/A7 review, inspect mixed purchase/want/play questions and negative qualifications; "wanted to buy" is one intention, not evidence of a completed acquisition. CQ130's durable routing tests preserve this boundary. Broad returned context still has a cost: a coverage pass is not proof of retrieval precision.

Actions retain reporting speaker, canonical subject/co-subjects, action state, summary, source locations and explicit qualifiers (including polarity, custody, uncertainty and household scope). The episode is resolved from the canonical source key. Do not substitute the speaker for the actor. Saved failure views now include **both original and tuned wording**, label each row, and warn that saved reports can be stale.

Reference and span views read authored drafts without building a database. References retain raw/canonical names, candidate identities, uncertainty and whole occurrence groups; spans retain explicit entity kind, role, exact endpoints, reason and evidence locations. They use the same item cursor/budget and compact JSON output to avoid indentation bloating dense inventories. Full source quotes remain in the artifacts. Any extra unprojected fields are named in `additional_fields` and must be inspected when relevant; this display is not a complete semantic approval. Action views also preserve hypothetical intended states and pet-recovery return context. Use bounded pages rather than recursive full-record/ranking dumps; do not count clipped output as reviewed.

## Tight repair loop before full verification

```powershell
python scripts/lore_workbench.py triage --collection batches/017 --case cq090-task-physics --case cq216-zero
```

This executes both unchanged wordings of only the selected cases against the current fresh database. It reports missing windows, returned-context size, routing and the ranks of up to50 lexical lore candidates that contain the missing windows. Full diagnostics are saved in unique `generated/workbench-triage/` files; console results paginate without truncating an item. No answer key is injected into retrieval. Missing wordings are excluded and fail the focused check, not silently replaced with tuned text. Unknown IDs/locations and stale databases fail explicitly. After record/map changes, rebuild the collection before triage; it never repairs a stale database automatically.

During repair, use this focused loop instead of repeatedly running every batch question. When the repair is ready, run the full verification, source sample, fresh questions and final required checks. A triage pass cannot approve an episode. Candidate crowding is a diagnostic, not permission to pad summaries with test wording, widen every context window or relax required evidence.

## Reuse machine checks only on unchanged inputs

```powershell
python scripts/lore_workbench.py verify --collection batches/015
```

Runs build, structural checks, tuned answers, original questions and the existing acceptance gate when a ledger exists. Processes run sequentially to avoid SQLite replacement conflicts on Windows. Full outputs stay in timestamped `generated/workbench-runs/` logs; console output is a compact status/count/path summary. Initial failures are not overwritten by later runs. A failed build stops downstream queries; answer failures still allow original-wording diagnostics.

A second call reuses a successful machine result only if all collection inputs, source bytes, referenced review artifacts, shared scripts/tests and workflow requirements match, and the generated database/evidence outputs still match their recorded hashes. A failed result is never reused. Missing or altered outputs, new review files, changed source or shared code all force checks to run again. `--force` explicitly reruns them. Receipts are local performance bookkeeping, not a security attestation or semantic approval. No ledger or review binding is created, renewed or repaired by this command. Pilot checks remain separate.

Merged `annotations.json` is a deterministic build output: build/check validate it, and successful receipts hash its bytes with the database/reports. Its expected regeneration no longer falsely counts as a concurrent authored-input change. Edits to source records, review fragments, requirements or other authored inputs during checks still invalidate the run; altered merged outputs invalidate reuse. Existing exact acceptance bindings remain enforced by the gate. Each verification step now reports measured elapsed seconds.

## Choosing verification scope

### Early validation, archive preservation and measurements

Run `python scripts/lore_workbench.py preflight --collection batches/016` immediately after draft records/maps land, before detailed answer integration. `--episode` checks one ready episode while others are unfinished. Missing topic locations/review notes, duplicate spans, broken section accounting and list/mapping problems fail early without building or approving anything. This is a limited readiness check; full exact evidence/build checks remain required.

An explicit baseline of the52 reviewed source identities was captured in `batches/generated/archive-baseline.json`. `python scripts/lore_workbench.py archive-check --collection batches/016` checks that none disappeared or changed identity, then opens each expected collection's fresh database and exercises search. Equal counts cannot conceal a substituted episode. New approved episodes are allowed, but the baseline is never lowered or overwritten automatically. On a fresh installation, explicitly run `archive-baseline` before edits; it refuses to overwrite an existing baseline. Preserve the baseline file in handoffs. Only an explicitly reviewed baseline update may add future accepted episodes to its protected set.

CLI `verify` now performs preflight and archive preservation before running expensive checks, and rechecks preservation afterward—even if successful machine results were reused. A stale database, stale approval or missing baseline is not repaired by silently replacing the baseline. Restore the intended reviewed inputs or perform the required review/rebuild steps. Keep the old bound pilot workflow unchanged; these operating additions live in this companion document.

Workbench CLI operations now record observed elapsed execution time and exact console character count in unique local `generated/workbench-metrics/` event files. Source displays also record source SHA, window locations and `--reviewer` (use `root`, or a distinct researcher ID). `python scripts/lore_workbench.py metrics --collection batches/016` reports measured operations, output size and repeated window displays for the same reviewer/source. Separate reviewers do not count as repeats. These are observed displays—not proof of reading, total active work time, tokens or subscription billing. Earlier work and calls outside the workbench are unmeasured. Supply reviewer IDs to avoid conflating independent readers under `unspecified`.

| Change | Required work |
| --- | --- |
| One draft episode's record or annotation | Review affected claims/ranks/lists; run that batch's workbench verification. Keep earlier full-source reading unless the source changed. |
| Source transcript changes | Reconcile source differences and affected mappings; invalidate prior read cursor and affected semantic review; rerun batch checks. |
| Question routing, schema, shared code or tests | Full shared suite and affected behavior tests; recheck accepted batches and pilot. Workbench receipts invalidate conservatively. |
| Only an unrelated batch changes | Do not repeat unchanged episodes' semantic reads. Existing exact bindings still govern acceptance. |
| Batch acceptance | All eight checks, every actual answer, frozen omissions, fresh/original questions, independent review and an explicit exact binding. A cache hit is not acceptance. |
| Work-block handoff | Run the full shared suite once after final edits; record actual result and remaining draft failures. |

Run cheap local checks early, before long semantic integration. Reuse generated rankings rather than asking the model to recalculate every unchanged span. Keep full evidence on disk and pull only the fields needed for the current review. Finish a bounded batch and preserve a clean handoff instead of repeatedly rebuilding or rereading to fill a wall-clock target. Honor user-requested work duration with useful pending work, not idle time or redundant checks.

Required task-case and fresh-question source locations are now validated during preflight. A missing or mistyped timestamp must fail as an authoring defect before retrieval; preserve its initial result and document the corrected literal heading rather than silently deleting the requirement. This applies to every episode's questions.

These changes reduce avoidable output and repeated local execution. Exact subscription savings are not measured and must not be inferred from character counts. Full-source review remains the principal model-usage cost; local SQLite and test computation are comparatively cheap.

## Throughput discipline — required for subsequent episode work

These operating rules apply to every episode without removing A1–A8 or the separate full-source independent review:

1. **Finish before expanding.** Keep one active extraction/review batch. Resolve its acceptance work before starting another; if genuinely blocked, save the exact reason and next action rather than building an expanding queue of nearly finished batches. Existing018 drafts are preserved; finish017 first.
2. **Size by work, not episode count.** Initially aim for about30,000–35,000 supplied transcript words per batch. A single episode over20,000 words should normally be its own batch. Treat this as a scheduling heuristic to measure, not a speed guarantee or a reason to omit material. Rotate early/middle/later lanes across consecutive batches rather than requiring three very unequal episodes in every batch. Count windows, references, list memberships and answers as additional workload indicators.
3. **Combine extraction tasks in one full pass.** Capture A1–A4 and brief/open-loop material together. The separate reviewer still reads the full source, but then revisits only disputed passages and relevant neighboring context. Retain precise reviewer/hash/cursor state. Do not rerun unchanged semantic reviews after a formatting-only edit.
4. **One authoritative answer set, one concise audit.** Keep complete answers in task-case JSON and the exact reviewed snapshots required by the gate. Do not manually paste the entire answer set into the audit, brief, progress file and work-session log. A practical brief remains distinct and useful; the audit records coverage, material findings, repairs and per-check evidence links. Generate projections from stored data. Do not rewrite bound historical reviews merely to adopt this format.
5. **Validate early; diagnose narrowly.** Preflight once a draft lands, build when retrieval inputs change, then triage failures during repair. Run complete batch checks when repairs are ready and the full shared suite once after final edits at handoff, plus required shared-behavior regressions. No repeated full runs merely to fill a requested duration. Preserve first failures and later results.
6. **Measure human-work phases honestly.** In the single current progress record, note UTC boundaries for extraction, independent review, repair and acceptance, along with source words and completed episode IDs. Record interruptions and distinguish concurrent reviewer intervals; do not add overlapping agent durations and call them elapsed session time. Existing workbench timings measure commands only. Compare the next two completed batches on accepted words/hour, accepted episodes/hour, first-pass failures, review-output size and repair time. Do not promise a throughput multiplier before measuring it.

### Observed baseline and limits (September13)

The17:38:15–18:38:15UTC session accepted three episodes, while drafting/reviewing three more and drafting CQ24. This is not equivalent to processing only three fresh episodes end to end. The accepted archive remains55 while017/018 are unaccepted.

Recorded workbench events within that hour:60 source displays (832,176 console characters),13 list displays (140,959),7 answer displays (61,008),24 preflights,3 verification calls and2 archive checks. These event categories total about55.70 seconds of measured command execution. Direct shell reads, separate tests and thinking/review time are not included; console characters are not tokens. Thus command timing does **not** establish that testing consumed most of the hour, or how much manual review was redundant. Broad earlier statements assigning most time to repeated checks were not measured.

The two unchanged017 problem questions reproduce in0.378 seconds in a direct focused loop. The new triage command also exposes candidate ranks: relevant pinball lore is fourth, the1982 narrative tenth. A measured complete017 verification takes about16.55 seconds across build/check/tuned/original steps, excluding archive guards. This demonstrates a substantially smaller **repair loop**, not a proven end-to-end episode speedup. Regression fixtures separately verify that first-build annotation generation no longer requires an unnecessary second verification, while real concurrent input changes and tampered outputs still invalidate reuse.

The two remaining017 retrieval failures are deliberately still failures. This change improves the processing loop and its observability; it does not claim to have fixed ranking, accepted new episodes, verified audio or reduced the user's bill.

Verification of this process update: all223 shared tests passed in63.969 seconds (`batches/017/generated/process-improvements-tests.log`). The real triage CLI measured0.796 seconds for both original/tuned versions of the two selected cases, versus17.736 seconds for full017 verification including archive guards. These run sizes differ by design: focused checks are for iterative repair, and full verification remains mandatory. The real018 action view was checked against source-key-based claims, including actor/ownership qualifiers. The diagnostic regression also confirms that exposing a missing evidence candidate does not inject it into retrieval or turn a failing question into a pass.
