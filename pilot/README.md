# CQ lore pilot

Started September 12, 2026 from the Lore Master handoff and Johnny's accepted refinements. The pilot tests whether source-linked episode analysis can support useful cohost retrieval. It does not activate persona changes or replace the existing archive.

## Current state

The process-hardening implementation is tracked in [PROGRESS.md](PROGRESS.md), with the handoff mapped in [requirements.md](requirements.md) and the operating process in [WORKFLOW.md](WORKFLOW.md). The persistent query interface below is the preferred local entry point. It does not activate Jen or connect her live chat automatically.

## Persistent local queries

From the repository root:

```powershell
python scripts/merge_lore_reviews.py
python scripts/lore_store.py build
python scripts/lore_store.py search "Mega Man refund" --episode 248
python scripts/lore_store.py search "Virtual Boy" --speaker Johnny --require-phrase "Virtual Boy"
python scripts/lore_store.py top --episode 300
python scripts/lore_store.py actions --speaker Johnny --state ordered
python scripts/lore_store.py topics
python scripts/lore_store.py timeline
python scripts/lore_store.py brief "inserts"
python scripts/lore_store.py answer-evidence "Witchaven" --episode 300
python scripts/evaluate_lore_answers.py
python scripts/validate_lore_workflow.py
python -m unittest discover -s tests -p "test_lore*.py" -v
python scripts/validate_lore_pilot.py
```

`build` creates `pilot/generated/lore.sqlite3` from the checked source records and `annotations.json`; no network calls are made. Changed inputs require a rebuild. Durable overrides preserve their expected original values and reject silent base drift. Never repair the generated database by hand. Close query sessions before rebuilding on Windows.

Search retains uncertain/other-speaker context, labels that fallback, and preserves evidence links. The older search script below offers a strict speaker filter. Action queries cover 365 reviewed action facts; an empty result does not establish that a host never performed the action. A reporting speaker is not necessarily the actor. Topic normalization is currently exact case-folded labels, not full synonym reconciliation. Timeline returns the three recorded cross-episode relationships, not an exhaustive history.

The store has 1,237 reviewed spans across all ten episodes. `top` returns a mapped estimate, with complete mapping distinguished from incomplete final-window timing. It unions overlaps, separates returns and excludes passing/joke and non-video-game spans. Untimed episodes retain paragraphs; near ties are not decisive rankings. See [qualified leaders](reviews/top-games.md). The brief command remains an evidence packet; completed written briefs and desk reviews are in each episode audit. Live use remains untested.

## Pilot corpus and earlier checks

Ten distinct episodes are selected in `manifest.json`: 6, 7, 146, 200, 222, 248, 259, 263, 299 and 300. CQ 263's old upload is an additional comparison source, not an eleventh episode. This deliberately difficult sample includes long episodes and previously studied material; its timings must not be treated as an unbiased archive average.

All ten episodes have been read end to end and have structured draft extractions, covering 254,821 transcript words in 1,279 windows. Their captured-text review is now complete in the separate [A1–A8 ledger](episode-review-ledger.json); original extraction files remain drafts rather than silently changing their provenance. Original audio has not been certified. Source hashes identify the exact transcript versions used. The older [pilot-review.md](pilot-review.md) records the initial extraction-stage findings; current results are in [PROGRESS.md](PROGRESS.md).

Current records contain 884 game/software/reference records, 514 lore items and eight dedicated correction entries. These are not unique game counts or utterance counts. Search exposes 49 correction rows, including 41 corrections embedded in lore. There are 93 open review flags. `relationships.json` links the Portland follow-up, Johnny's Wii completion milestone and his changing view of manuals. `host-context.md` preserves Johnny's clarification about the host eras.

Read-only local search is available with `python scripts/search_lore_pilot.py "Mega Man refund" --kind game`. It preserves source excerpts, timing limits, draft status and attribution confidence. Twelve behavior tests pass. Five queries, each run five times across the ten records, had median local load/index/search times of about 24–31 ms. This excludes model/voice latency and is not a full-archive speed estimate. Use `--require-phrase "Virtual Boy"` to require a complete phrase, and `--speaker Tyler` to filter a contextual speaker candidate without upgrading confidence. See `metrics-2026-09-12.json` and rerun `python scripts/report_lore_pilot.py` for measurements.

The three reserved questions received an evaluation-stage lookup after all ten draft records existed. Results and limitations are in `johnny-evaluation.json`: one partial candidate and two insufficient-evidence results, all unscored because expected answers are not established. The coordinator saw the questions before extraction; this is not fully blinded. The sample was not changed to chase answers. A broad-query false positive prompted phrase filtering; that repair is development work, not an untouched holdout result.

## Cost and execution boundary

Use local tools and the included ChatGPT/Codex subscription allowance only. Do not run paid API extraction, embeddings, transcription, voice, hosting, or the API-backed Jen agent. Work is resumable across allowance resets. No model-time or dollar estimate is measured yet; the earlier conversation's token estimates are not benchmark results.

## Existing structures reused

The library manifest supplies episode keys, numbers, dates, public source links, source paths and timing quality. Keys, rather than episode numbers alone, identify uploads. `research/ARCHIVE_FINDINGS.md` documents the observed Airtable Episodes, Games, People, Platforms and Topics relationships. Local Airtable parent-transcript metadata was also inspected. A complete Q-index/breakout schema is not present in the inspected material; exact field mapping remains pending before any Airtable synchronization. These local records extend the existing source model provisionally; they are not a replacement Airtable schema.

## Processing and acceptance

1. Read an episode end to end, using bounded consecutive sections for long transcripts. Extract all dimensions together and reconcile repeated entities and cross-section context.
2. Review for omitted game mentions, unsupported speaker assignments, mismatched quotes, missing topics and overly broad interpretations. Keep raw wording when identification is unresolved. Source hashes must still match.
3. Resolve important ambiguities against audio or stronger evidence when available within the spending boundary. Otherwise preserve them in the review queue.
4. Run the evaluation questions with source-backed expected answers. Questions used to guide extraction or inspected during development are development checks, not independent accuracy evidence. Johnny's reserved questions were visible to the coordinator and remain unscored; do not describe them as a blinded or completed independent check.
5. Produce a pre-show brief and measure whether it is useful. Test live delivery separately once a subscription-supported interaction route is established.

The bounded development gate is measured: 51/52 source-first reference-window buckets before final repair (52/52 after), and 19/19 manually adjudicated qualified development answers with required database context retrieved. All episode checks and 43 regressions pass. These exceed the proposed 90% thresholds on this disclosed sample, not on unseen questions or the whole archive. Repeat fresh source-first selection and complete-answer checks in every batch; do not relabel repaired samples as holdouts.

Record extraction/review time, transcript words, record counts, ambiguity counts, and retrieval timings separately. Time local lookup separately from model answer latency. Subscription usage must come from an available usage display, not inferred from a word count. Do not extrapolate a full schedule until several differently sized episodes have been measured.

## Data contract version 0.1

Each record includes the existing source key, metadata, source SHA-256, extraction version and review state. Evidence has an exact transcript heading and verbatim supporting excerpt. Untimed sources use paragraph headings; never manufacture timestamps. A whole paragraph can contain multiple speakers.

Games have a local entity ID, raw spoken forms, candidate/normalized name, entity granularity, platform/edition when supported, identification confidence, and occurrence groups. Each group has SUBSTANTIAL_COVERAGE, SUPPORTING_EXAMPLE, PASSING_MENTION or JOKE_ASIDE, evidence, and independently stated speaker confidence. Groups may cover repeated references within one exchange; their count is not a raw utterance count. Regional equivalents and series must not be silently collapsed into individual releases. Local IDs are provisional until the existing game index can be mapped.

Lore items have a kind (reported factual claim, host opinion, show discussion, anecdote, joke, interpretation, lead, correction or open loop), scope, interpretation confidence and independent attribution. A statement in a transcript is evidence of what was said, not independent verification of its factual accuracy. Do not assign SHOW OPINION merely because one host spoke. Do not promote colloquial psychological language into diagnosis.

Topic depth and game coverage counts count distinct canonical episodes. Report substantial and supporting counts separately. Unknown aliases and unreviewed material remain gaps. No search result supports an unqualified 'never covered' or 'first ever' claim. Saturation is editorial judgment supported by depth, recency and fresh angles, not a mandatory numerical score.

Corrections distinguish factual repair, changed host opinion, disagreement and identification repair. Preserve the original record and link the replacement or counterpoint; do not erase history. A joke is not recurring until separate occurrences support that label. Open loops distinguish an explicit promised follow-up from an analyst's suggested research question.

## Review and publication

Review queues are embedded in each record and use stable IDs, priority, evidence, reason and resolution state. Prioritize upcoming-show impact, then attribution and identity errors. Durable development-review overrides are now stored in `annotations.json`, separately from base records and the generated database. These corrections do not mark whole episodes accepted. A stale source hash or changed override base blocks rebuilding rather than silently rewriting reviewed data.

Only public CQ episode material belongs here. Fictional Jen canon and private conversation notes remain separate. This pilot does not import the private conversation databases or broad personal analyses. No GitHub publication or Airtable write is performed by the pilot scripts.

Run `python scripts/validate_lore_pilot.py` for structural/source checks. Passing it does not establish semantic completeness, factual truth, retrieval quality or independent review.

Run `python -m unittest discover -s tests -p "test_lore*.py" -v` for behavior regressions and `python scripts/validate_lore_workflow.py` for the recurring episode ledger and frozen omission repairs. Captured-text review, answer adjudication and brief desk review are complete; live/human usefulness and broader product integration remain separate. There is no queued user clarification. No pilot data has been published to GitHub or synchronized to Airtable.
