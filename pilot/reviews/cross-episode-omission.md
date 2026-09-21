# Cross-episode source-first omission check

Selection rule frozen before new record/map comparison, 2026-09-12: for each of the ten canonical manifest episodes, split the supplied transcript at `###` headings, number windows from zero and select indices `floor(N * .25)`, `floor(N * .5)`, and `floor(N * .75)`. Add CQ300 01:34:38 as a separately labeled purposive rapid-list stress case. Do not include the old CQ263 upload as another episode. Retain no-hit windows. Read selected raw passages first, freeze reference-window buckets and exact quotes, then compare existing records and reviewed additions/maps.

Independence limit: deterministic selection and a secondary-agent source-first pass, not a fully blinded or externally independent evaluation. This reviewer previously read CQ146/CQ200 and saw surrounding project context. Do not generalize a small deterministic sample into archive-wide recall.

## Results before repair

Read all 31 selected raw windows before inspecting records/maps for this check, then froze 52 reference-window buckets with raw excerpts and per-window exclusions in [the JSON ledger](cross-episode-omission.json). Compared base records, original partial maps and all seven reviewed annotation companions. All ten episodes had reviewed maps available by comparison time. Sixteen windows have no identifiable game title; they remain in the sample.

| Sample | Reference-window buckets | Base title exists somewhere in episode | Base exact-window occurrence | Original partial-map coverage | Reviewed-map coverage before repair |
| --- | ---: | ---: | ---: | ---: | ---: |
| Deterministic quartiles: 30 windows | 28 | 28/28 | 18/28 (64.3%) | 2/28 (7.1%) | 28/28 (100%) |
| Separately selected CQ300 rapid list | 24 | 24/24 | 21/24 (87.5%) | 0/24 | 23/24 (95.8%) |
| Combined, with different selection methods disclosed | 52 | 52/52 | 39/52 (75%) | 2/52 (3.8%) | 51/52 (98.1%) |

The important difference is title presence versus occurrence recall: every sampled title/raw bucket already existed somewhere in its episode, but 13 selected-window occurrences were not linked there. Maps repaired twelve before this check. The sole remaining map omission is original **Final Fantasy**, explicitly in the first sentence of CQ300 01:34:38. It has base ID `cq300-g061`, but the reviewed map covered only Alpha and King's Knight from that sentence, then the 21-entry modern list. Add a passing occurrence without assigning it the entire Square history discussion. [CQ300 source 01:34:38](../../library/episodes/cq-300-sc-2396296749.md).

## Exact-window gaps in the baseline

| Episode/window | Game reference omitted at that location | Reviewed map before this audit |
| --- | --- | --- |
| CQ200 00:42:17 | Turbo Turtle Adventure | Covered |
| CQ222 01:29:43 | Super Mario World | Covered |
| CQ248 01:07:22 | Mega Man 2 | Covered |
| CQ263 00:55:51 | Hogan's Alley | Covered |
| CQ263 02:46:42 | Cosmology of Kyoto; Ren & Stimpy Buckeroo$ manual | Covered |
| CQ300 00:58:07 | Pokémon Red; Green; Blue | Covered |
| CQ300 02:55:05 | Super Mario World | Covered |
| CQ300 01:34:38 | Alpha; King's Knight; Final Fantasy | First two covered; Final Fantasy missing |

Exact snippets, baseline IDs and reviewed span IDs are stored per reference in the ledger. The raw-source locations above support these findings: [CQ200](../../library/episodes/cq-200-sc-1316628157.md), [CQ222](../../library/episodes/cq-222-sc-1517354524.md), [CQ248](../../library/episodes/cq-248-sc-1829470383.md), [CQ263](../../library/episodes/cq-263-sc-1993480675.md), [CQ300](../../library/episodes/cq-300-sc-2396296749.md).

## Selected-window precision checks

- **Potential CQ222 duration inflation:** `cq222-audit-span-053` gives Donkey Kong supporting coverage from 01:28:43 to 01:30:43. The selected 01:29:43 window quickly moves from an unnamed old-game antecedent to explicit Super Mario World, then fictional VR fragfest and a future-world joke. Recommend ending meaningful Donkey Kong coverage at 01:29:43, with any residual mention separately passing unless adjacent context warrants otherwise. This is a boundary concern, not a missing title. [CQ222 01:29:43](../../library/episodes/cq-222-sc-1517354524.md).
- **CQ300 rapid-list depth is appropriately passing:** the mapped Square list does not award each name a minute of substantive duration. Preserve that behavior when repairing Final Fantasy. Seiken Densetsu 3 / Trials of Mana is one bucket in this historical list; that does not establish equivalence to every later remake. [CQ300 01:34:38](../../library/episodes/cq-300-sc-2396296749.md).
- **No obvious selected-window inflation in the other CQ300 examples:** Red/Green/Blue/Yellow/Emerald are actually being compared; Mario 3 manual condition and Castlevania variants are actual examples. Their one-window estimates still are not exact speech durations. [CQ300 00:58:07 and 01:57:04](../../library/episodes/cq-300-sc-2396296749.md).
- **No-hit windows are not automatic false-positive tests:** the selected CQ259 00:34:49 words concern Seven Gables/Dracula literature, while its companion map treats the surrounding game discussion as The House of Seven Gables. Context outside the isolated window is needed to adjudicate that continuation. Likewise, an unnamed “this game” in CQ6 may legitimately continue the prior game's discussion. Do not erase contextual spans just because a title was not spoken again. [CQ259 00:34:49](../../library/episodes/cq-259-sc-1943435095.md), [CQ6 Paragraph 8](../../library/episodes/cq-006-sc-232561251.md).

## Interpretation and limits

The numerator measures retrieval-ready source-window coverage of frozen recognizable reference buckets, not precise title normalization, speaker attribution, game-duration accuracy, factual accuracy or complete-answer success. Physical cards, literary references, hardware, Logo programming, fictional VR fragfest and character-only allusions are explicitly excluded from the exact-title denominator and preserved as exclusion notes. Clipped/transcribed labels such as Zenog, Tactics, Outback Joy and the Blockbuster cart retain qualified identity confidence rather than pretending audio verification.

This small deterministic/purposive sample exceeds 90% **reviewed source-window coverage** before the final repair, but it does not prove 90% archive-wide recall or answer quality. CQ146's three windows contain no identifiable titles, so they contribute no positive title-recall denominator. Previously read CQ146/CQ200 and project context prevent a fully blinded claim. Once used for repair, this sample is development/regression data, not an unseen holdout.

Coordinator added the CQ300 Final Fantasy passing occurrence at 01:34:38 and narrowed the CQ222 Donkey Kong span's end to 01:29:43. **Post-repair verified: 52/52 reference-window buckets covered in the rebuilt database**, using `validate_lore_workflow.py`. The frozen JSON preserves the pre-repair 51/52 measurement and original findings; it is not silently relabeled an unseen successful sample.
