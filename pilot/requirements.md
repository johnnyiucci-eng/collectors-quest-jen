# Lore Master requirement traceability

Authority: `handoffs/Collectors_Quest_Default_Jen_Lore_Master_Handoff.docx`, read in full September 12, 2026; latest user-approved process refinements add discussion-span rankings and persistent queries. This matrix groups requirements without replacing the source document.

| Requirement / handoff heading | Stored evidence or behavior | Acceptance check |
| --- | --- | --- |
| Privacy boundary; architecture | Public episode sources only; persona and private history excluded from lore inputs | Index input allowlist; no private-directory traversal |
| Corpus processing strategy | Canonical episode/source keys; end-to-end batch ledger; existing Airtable relationships reused conceptually | Duplicate upload does not add an episode; input provenance retained |
| Canonical episode record | Existing ten records retain metadata, participants, topics, references, claims, flags | Hash, locator, quote and schema validation |
| Game mention index | Raw title, identity confidence, edition/platform, occurrence classification | Generic Halloween/Clowns words do not resolve game identities; sequels remain distinct |
| Meaningful coverage; user top-three task | Reviewed spans and union duration/paragraph coverage, split by depth | Returns ranks only within declared mapped scope; no name-count substitution |
| Speaker attribution; retrieval behavior | Speaker candidate and confidence independently preserved | Uncertain speaker retains topic hit; strict speaker filter is opt-in |
| Provenance and lore types | Claim type, source, timestamp/paragraph, evidence, external verification state | Joke, interpretation and reported claim never become verified fact |
| Person-specific anecdotes | Explicit action states linked to evidence | Wanted/ordered is not received/owned; mention is not purchase |
| Corrections / contradiction ledger | Original, replacement or counterpoint plus paired citations | Intra-episode repair and cross-episode opinion change remain available |
| Topic/theme index; heat map | Distinct canonical episode counts by depth; first/last date in processed scope | Passing hits do not inflate meaningful coverage; no archive-wide first/never claims |
| Timeline; open loops | Dated episode metadata and source-linked relationships/open-loop rows | No invented return date; delivery requires paired evidence |
| Pre-show lore brief | Retrieved history, corrections, jokes, open questions, freshness and research limits | Traceable brief; unknown saturation remains unknown; live usefulness scored separately |
| Clarification-needed system | Stable unresolved record IDs, reason, priority and status | Preserve raw forms; rebuilding retains reviewed annotations |
| Live retrieval behavior | Persistent query interface with source freshness checks | Relevant partial evidence and uncertainty returned; no audible checking narration added |
| Locked persona, improv, humor, biography, favorite game | Existing persona kept separate; no changes authorized by extraction | Persona files unchanged; no fictional biography imported as episode history |
| Active episode state | Existing approved tips and unresolved fifth preserved | Lore development does not silently approve/reorder episode material |
| North star / chemistry | Actual rehearsal required in addition to retrieval tests | No claim of successful live cohosting from database tests alone |

See `PROGRESS.md` for implementation and test status. Unimplemented or unmeasured capabilities must remain visible there.
