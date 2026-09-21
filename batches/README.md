# Post-pilot episode batches

The [fixed ten-episode pilot](../pilot/PROGRESS.md) remains a regression corpus. New episodes use separate, source-hashed collections so growing the archive does not silently change the pilot's denominators.

| Collection | Episodes | Status |
| --- | --- | --- |
| [002](002/PROGRESS.md) | 8, 75, 201 | Captured-text review complete; all 24 A1–A8 checks passed |
| [003](003/PROGRESS.md) | 9, 76, 202 | Captured-text review complete; all 24 A1–A8 checks passed |
| [004](004/PROGRESS.md) | 10, 77, 203 | Captured-text review complete; all 24 A1–A8 checks passed |
| [005](005/PROGRESS.md) | 11, 78, 204 | Captured-text review complete; all 24 A1–A8 checks passed |
| [006](006/PROGRESS.md) | 12, 79, 205 | Captured-text review complete; all 24 A1–A8 checks passed |
| [007](007/PROGRESS.md) | 13, 80, 206 | Captured-text review complete; all 24 A1–A8 checks passed |
| [008](008/PROGRESS.md) | 14, 81, 207 | Captured-text review complete; all 24 A1–A8 checks passed |
| [009](009/PROGRESS.md) | 15, 82, 208 | Captured-text review complete; all 24 A1–A8 checks passed |
| [010](010/PROGRESS.md) | 16, 83, 209 | Captured-text review complete; all 24 checks and exact binding passed |
| [011](011/PROGRESS.md) | 17, 84, 210 | Captured-text review complete; all 24 checks and exact binding passed |
| [012](012/PROGRESS.md) | 18, 85, 211 | Captured-text review complete; all 24 checks and exact binding passed |
| [013](013/PROGRESS.md) | 19, 86, 212 | All24 checks passed; exact review binding |
| [014](014/PROGRESS.md) | 20, 87, 213 | All24 checks passed; exact review binding |
| [015](015/PROGRESS.md) | 21, 88, 214 | All24 checks passed; exact review binding |
| [016](016/PROGRESS.md) | 22, 89, 215 | All24 checks passed; exact review binding |
| [017](017/PROGRESS.md) | 23, 90, 216 | All24 checks passed; exact review binding |
| [018](018/PROGRESS.md) | 24, 91, 217 | All24 checks passed; exact review binding |
| [019](019/PROGRESS.md) | 218 | All8 checks passed; exact review binding |
| [020](020/PROGRESS.md) | 25, 26 | All16 checks passed; exact review binding; two fresh episodes |
| [021](021/PROGRESS.md) | 102 | All8 checks passed; exact review binding; Halloween Games #1 |
| [022](022/PROGRESS.md) | 130 | All8 checks passed; exact review binding; Halloween Games #2 |

Every episode repeats [A1–A8](../pilot/WORKFLOW.md). All supplied text is read, omissions and identities are reviewed, speakers and action states are qualified, multiple complete answers are checked, and a practical brief is desk-reviewed. Fresh source-first samples are frozen before extraction-record comparison. Source defects remain visible.

## Reproduce and query a batch

For one read-only query across all reviewed collections, use the [archive query guide](QUERYING-THE-LORE-ARCHIVE.md). The catalog currently contains66 reviewed episodes; unfinished or stale reviews are excluded. Exact review bindings and database freshness are separate checks: rebuilding does not renew approval.

```powershell
python scripts/process_lore_batch.py build --collection batches/002
python scripts/process_lore_batch.py check --collection batches/002
python scripts/process_lore_batch.py answers --collection batches/002
python scripts/process_lore_batch.py sample --collection batches/002
python scripts/process_lore_batch.py gate --collection batches/002
python scripts/lore_store.py search "Metroid" --collection batches/002 --episode 8
python scripts/lore_store.py answer-evidence "Maxi 15" --collection batches/002 --episode 201
python scripts/lore_store.py top --collection batches/002 --episode 75
python scripts/lore_store.py actions --collection batches/002 --speaker Johnny --state played
```

Omitting `--collection` queries only the pilot. Batch results are not implicitly merged into pilot statistics or live Jen. A result's collection/episode/source scope must travel with any answer; no hit in one collection does not mean archive absence.

Explicitly typed series discussion is reported separately in `top` output's `series_results`, not mixed into individual-game `results`. Pinball, hardware and standalone accessories do not earn video-game ranking credit. Same-game edition coverage can be unioned while preserving distinct source records and variant qualifications. Action queries match canonical subjects and explicitly stored co-subjects, not just reporting speakers; a trade is not encoded as a cash sale. Explicit returns are searchable separately from historical purchase/receipt, so buying a copy does not imply it is still owned. These are recurring A1/A3/A4/A7 checks, not exemptions for previously processed episodes.

The build requires records and maps for all selected episodes. Generated databases/evidence bundles stay local and rebuildable. Nothing here publishes to GitHub, synchronizes Airtable, imports private history or purchases processing.

For ongoing processing, use the [efficient workbench workflow](EFFICIENT-PROCESS.md): whole-window source pages, concise answer/list/failure views, and exact-input reuse of successful local checks. All eight episode requirements and exact review bindings remain mandatory. Shared-code changes and final handoff still require the full regression suite.
