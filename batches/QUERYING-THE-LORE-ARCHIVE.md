# Querying the reviewed Lore Master archive

Run these from the repository root. They use local SQLite files and make no model, network or paid-service calls.

```powershell
python scripts/query_lore_archive.py catalog
python scripts/query_lore_archive.py search "Super Mario Bros. 3"
python scripts/query_lore_archive.py search "Wii Sports" --entity-kind video_game
python scripts/query_lore_archive.py search "Wii Remote" --entity-kind hardware
python scripts/query_lore_archive.py answer-evidence "What were the two starter lists?" --episode 209
python scripts/query_lore_archive.py top --episode 84
python scripts/query_lore_archive.py actions --speaker Tyler --state purchased
```

`catalog` reports exactly which reviewed collections are included and why others are excluded. The fixed ten-episode pilot remains distinct from later batches; querying them together does not change the pilot test denominator. Duplicate source keys are rejected. If an episode has multiple reviewed versions, choose a collection explicitly with `lore_store.py` rather than silently combining them.

`search` returns lexical candidates, not certified answers. The archive merges separate database results by matched-term count, title/alias term count and within-collection position, not by pretending that their BM25 scores are comparable. Effective and omitted query terms are reported; the lexical budget is16unique terms. A speaker is a contextual candidate, not verified diarization; inspect `speaker_match` and evidence. Historical purchased/ordered/received/returned claims are not a resolved current inventory.

`--entity-kind` requires one explicit type across a reference row's evidenced windows. Examples include `video_game`, `game_series`, `hardware`, `software_utility`, and `publication`. Mixed and untyped legacy references are excluded from this strict filter, so no result does not establish absence. Default search keeps those useful uncertain references. The old coarse `kind='game'` label means a reference bucket and may include non-games; inspect `entity_kinds`, `entity_kind_status`, and the supplied warning. Do not globally retype a mixed reference such as tabletop/video-game Blood Bowl.

`answer-evidence` returns complete supporting windows and adjacent qualifications. Generic routes cover discussion prominence, explicitly typed lists, unfinished plans, collector origins, corrections, acquisitions and edition-integrity questions. List owners, purposes and selected/considered/rejected/joke states remain separate. The output is an evidence packet requiring claim-level review, not an automatically composed or certified answer. Some questions return much of an episode; complete coverage is not retrieval precision.

`top` estimates meaningful discussion from reviewed spans. Untimed episodes use paragraph coverage; timed episodes use caption-window seconds. Never compare those units across episodes. Passing mentions, jokes, series and hardware are separate. Explain exact ties and near-ties; a three-result display is not proof of a unique third place. For the full qualified ranking, use `LoreStore(collection=...).top_games(episode, limit=50)`.

## Rebuild and review boundaries

Generated indexes live under each collection's `generated/` directory and are ignored by Git. A stale index is deliberately rejected. For reviewed inputs that have not changed, rebuild the selected database:

```powershell
python scripts/lore_store.py build --collection pilot
python scripts/process_lore_batch.py build --collection batches/011
python scripts/process_lore_batch.py gate --collection batches/011
python scripts/evaluate_lore_questions.py --collection batches/011
```

Rebuilding is not approval. Each accepted collection has an exact review binding over its source, record, annotation, decision and review inputs. Changed inputs require actual re-review and an explicit renewed binding; a rebuild must never silently renew it. Every episode repeats A1–A8 in [the workflow](../pilot/WORKFLOW.md). Keep initial misses, current retrieval results, manual answer judgments and blind/source-informed test limitations separate.

This interface does not publish to GitHub, import private history, connect Airtable, activate a live persona or certify historical claims against external sources.
