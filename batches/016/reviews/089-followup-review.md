# CQ89 bounded source/retrieval follow-up

Status: source-backed record repairs stable; coordinator retrieval rerun and A7/A8 remain pending. This is the same extractor's follow-up, not an independent or blinded validation. The prior end-to-end reading of all 81 source paragraphs was reused; Paragraphs 16–18, 47, 50 and 51 were reread in full for this bounded review. Current research skill, WORKFLOW, requirements and EFFICIENT-PROCESS were read first. No external research, paid service, source modification or full batch build was performed.

## Preserved initial results

The frozen [original-wording results](initial-original-wording-results.json) report 56/62 batch cases passing: CQ89 passed 20/22, with scope missing Paragraph 18 and six-sets missing Paragraphs 50 and 51. The frozen [tuned results](initial-tuned-retrieval-results.json) report 57/62 batch cases passing: CQ89 passed 21/22, with rank missing Paragraph 47. These initial results remain unchanged. Missing context is not evidence that the actual prose is false, but it prevents treating that answer's retrieved bundle as complete.

## Source-backed changes

Only three lore aggregates in [the CQ89 record](../records/sc-419958968.json) were changed:

- `cq089-l002`: added the strict-completeness qualification and Paragraph 18 proof. The ordinary approximately 170/172 count, over-200 extras-inclusive collection and CIB claim already had Paragraphs 5, 16 and 17. The additional source explicitly says the mail-in fourth golf disc has no separate CIB copy and is added to the existing box. This connects a real exception to the set-scope explanation, not a new count or a claim that a boxed fourth-disc retail release exists. [Source, Paragraphs 16–18](../../../library/episodes/cq-089-sc-419958968.md#paragraph-16)
- `cq089-l018`: added Paragraph 47 and a sentence linking the authentic Stadium Events gift/provenance account to Stephan's explicit inclusion of it in his completed North American NES set. Existing gift evidence remains. This is a collecting discussion, not play evidence; no span role or ranking credit changed. [Source, Paragraph 47](../../../library/episodes/cq-089-sc-419958968.md#paragraph-47)
- `cq089-l024`: clarified the already-cited completion qualifications: two-and-a-half-month SNES completion did not mean every copy was CIB; shops and collector groups were major sources, with some eBay purchases rather than an all-eBay account. Paragraphs 50 and 51 were already attached, so this repairs aggregate wording/discoverability rather than inventing missing evidence. The six scoped collections, incomplete Turbo CDs and unspecified Virtual Boy region remain unchanged. [Source, Paragraphs 50–54](../../../library/episodes/cq-089-sc-419958968.md#paragraph-50)

No question, tuned query, required window, composed answer, action, entity identity, uncertainty, source metadata, list membership or discussion span was edited. In particular, Stadium Events remains five meaningful paragraphs, not six; its Paragraph 51 transition does not gain ranking credit. DinoPark Tycoon remains six and Mind Teaser four. Educational-software uncertainty for It's a Bird's Life remains intact.

## Before/after verification

Episode-only preflight passed before and after: 81 source windows and 339 spans. Literal proof checks increased from 1,160 to 1,162, all passing after the two added paragraph proofs. The record still has 168 reference buckets and 40 lore entries; annotations still have 22 actual answer cases. A first in-memory patch-construction attempt failed because `structuredClone` was unavailable; it made no file changes. The corrected scoped patch succeeded and preserved other record content.

Post-repair retrieval pass counts are deliberately not claimed: the coordinator must rebuild and rerun the unchanged questions against these record changes. No threshold or required context was relaxed. Structural preflight is not semantic approval or batch acceptance.

## Process suggestions

Keep broad completeness summaries linked to their explicit exceptions and format boundaries, rather than expecting a title-specific entry to supply them incidentally. For collecting prominence, connect explicit collection inclusion to provenance where the source does so, while keeping passing returns out of meaningful-discussion totals. When required evidence is already attached but its parent summary is difficult to retrieve, improve the substantive summary first; do not remove the requirement or stuff the query with an answer key. Preserve both original and tuned failures and measure the same cases again after integration.
