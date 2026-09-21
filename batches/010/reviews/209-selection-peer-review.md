# CQ209 — selection-list extension peer review

Reviewed the [CQ209 source](../../../library/episodes/cq-209-sc-1391155801.md), [record selection lists](../records/sc-1391155801.json), [selection validator/filter](../../../scripts/lore_selections.py) and [question routing](../../../scripts/lore_store.py). Research-skill primary-source review produced this durable report. No files owned by the coordinator were edited, and no external or paid research was performed.

## Scope and independence

This is a bounded, separate-agent review, not a full independent extraction of the two-hour-plus episode. All **24 unique evidence windows** referenced by the four groups and 29 entries were read before inspecting their member labels, order or reasons. Opening criteria at **00:06:22 and 00:07:29**, and contextual windows **01:45:46 and 01:47:52**, were also read: **28 unique windows total**. Source locators were taken from the proposed extension, so window selection was not blinded or independently sampled. Generic routing code was inspected before the member comparison; no fresh-blinded-question claim applies to the code probes below.

## Source membership findings

The proposed **4 groups / 29 entries** contain **20 selected starter entries, 6 selected aspirational entries and 3 explicitly nonselected jokes**. All **29 membership/status assignments** are supported by the reviewed windows. The first four starter titles overlap, and Chrono Trigger occurs on both lists at different positions. That is not permission to collapse the lists into a joint ranking. Tyler's starter philosophy favors his games/platformers; Johnny aims at a recognizable representative collector shelf. The three-per-host strive segment is expressly introduced after completing ten picks. [00:04:17–00:06:22; 01:31:07–01:32:12](../../../library/episodes/cq-209-sc-1391155801.md).

Tyler's selected starter order is Mario World, Link to the Past, Super Metroid, Castlevania IV, Yoshi's Island, Chrono Trigger, Mega Man X, Super Ghouls 'n Ghosts, DKC2 and Contra III. Johnny's is the first four shared titles, Chrono Trigger, FFIII/VI, Super Mario Kart, EarthBound, SFII Turbo and Turtles in Time. Source handoffs and the explicit five/six exchange support this ordering; it is list order, not a mechanically measured quality score or joint consensus. [00:08:36–01:25:53, the 15 cited starter-introduction windows in the record](../../../library/episodes/cq-209-sc-1391155801.md).

Tyler's strive selections are Super 3D Noah's Ark, V Jump Chrono Trigger and Harvest Moon. Johnny's are Rendering Ranger R2, The Firemen and Fun 'n Games. V Jump is correctly distinct from the ordinary Chrono starter entry; Harvest Moon is not silently changed to Harvest Moon 64, which is only his preferred comparison. Selection does not establish acquisition, and Harvest Moon ownership is explicitly uncertain. [01:32:12, 01:34:15, 01:37:22, 01:39:30, 01:46:48](../../../library/episodes/cq-209-sc-1391155801.md).

Utopia, Vortex and Warlock correctly remain jokes without selected ordinals. Their placement in Johnny's list context does not prove Johnny uttered every line of the shared banter. UniRacers is another explicitly rejected guess at 01:24:49; omitting it is acceptable only if the extension does not claim an exhaustive inventory of every rejected candidate. No selected starter is missing in this review.

**Concrete evidence defect:** the Fun 'n Games entry reason requires the scarce manual, but its initial entry evidence cites only **01:46:48**, which names the pick and starts the explanation. The explicit requirement is in **01:47:52**: “very specifically not just funing games I want you to have the manual.” Add that window directly to the entry. Thus membership is **29/29 supported**, but the initial entry-local rationale audit is **28/29 fully supported**. The coordinator agreed to repair this; post-repair verification is not yet claimed here.

## Actual routing probes — initial failures

Five read-only calls to the generic route/filter functions produced these actual results:

| Natural query | Initial result | Problem |
| --- | --- | --- |
| What were both ten-game lists? | All four groups | Includes six aspirational selections despite ten-game constraint |
| What were Tyler's hot picks? | Tyler starter and aspirational | Route recognizes “hot” but purpose filter does not interpret it |
| What were Tyler's strive picks? | Lexical route | Misses the source's own term for aspirational lists |
| Show Johnny's starter list, not his aspirational list. | Both Johnny groups | Negated purpose is treated as a positive match |
| What was Stephan's starter list? | Both hosts' starter groups | Unknown named owner silently becomes unfiltered ownership |

These are candidate-routing failures, not proof that a final language answer already hallucinated. The returned labels/status fields remain valuable safeguards. Still, a cohost must not have to guess whether “both” means two starter lists or all four groups. Coordinator repair should preserve explicit purpose/owner constraints, report unsupported owners or ambiguity, and retain the original query. Purpose aliases and cardinality need source-independent generic tests rather than episode-specific game-name routing.

## Validator review

The initial validator accepts all **29 entries** and checks literal evidence, known/unique game references per group, explicit statuses, unique positive selected ordinals, and required metadata. Those are useful structural controls. It correctly allows the same underlying game in different hosts' groups and keeps joke entries without ordinals.

Two in-memory mutation probes also passed all 29 entries: changing a list subject to `Unrelated person`, and changing its first selected ordinal from 1 to 999. These expose current validation limits. Actor validity and contiguous ordinals are not enforced. A future generic format may legitimately support third-party owners or partial/unordered lists, so the remedy is an explicit ordering/completeness contract and source-backed actor policy, not indiscriminately rejecting all nonparticipant names. At minimum, this extension should state that its ordinals are source list order and that these four lists are complete.

Additional defensive limits from inspection: malformed non-object evidence/entries can raise incidental attribute/type errors instead of a consistent validation error; arbitrary purpose strings are accepted; literal quote containment cannot validate whether the quoted speaker actually selected the item. The latter necessarily remains a source-adjudication responsibility. A downstream answer must filter `status == selected` before calling Johnny's starter group a ten-item list; its raw entry count is thirteen because the jokes are preserved.

## Handoff

The separation of list membership from discussion prominence is sound and resolves a real semantic need. Preserve four distinct groups and status-aware entry handling. The missing manual evidence and five reproduced routing failures were reported to the coordinator before this report. Coordinator indicated repairs are underway; this document records the initial behavior, not an unrun post-repair pass. No starter/strive membership swaps or wrong selected-host assignments were found in the bounded source review.

## First repair probe round

After the coordinator's first routing changes, the same five queries were rerun unchanged. “Both ten-game lists” now returns just the two starter groups, and the unrepresented Stephan owner returns none. Three still fail: Tyler's hot picks, Tyler's strive picks, and Johnny's starter-not-aspirational query return no groups. Inspection identifies a new owner-parser defect: the optional two-word name pattern absorbs preceding words such as “were Tyler” or “Show Johnny,” treating those as unknown owners. The hot purpose is also not an alias for aspirational in the current filter, and negation does not allow the intervening pronoun in “not his aspirational.” These outcomes were reported to the coordinator; no final all-probes-pass claim is made.

## Second repair probe round

The same five probes were rerun after the owner-parser and intervening-pronoun repairs. Four now produce the intended constrained candidate result: the two ten-game starter groups; Tyler's single aspirational group for “strive”; Johnny's single starter group with the aspiration excluded; and no group plus an explicit unknown-owner warning for Stephan. “Hot” returns no group with no specific unresolved-purpose message. Treat that as an unmatched/ambiguous purpose boundary, not proof the episode contains no interesting collecting picks: the generic system may legitimately reserve `hot` for a distinct purpose in another episode rather than equating it with `aspirational`. The coordinator was told to make that unavailable-purpose scope clear.

Fun 'n Games entry evidence was verified to include **01:47:52** as well as 01:46:48. The full four-group validator still accepts all **29 entries**; the specific manual-rationale gap is repaired. Initial failure counts above remain preserved. No claim is made that these five development probes exhaust natural-language routing.
