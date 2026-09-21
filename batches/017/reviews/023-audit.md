# CQ23 primary-source extraction and same-agent desk audit

Source: [Episode 23 supplied transcript](../../../library/episodes/cq-023-sc-251774783.md), dated 2016-03-14. SHA-256: `f317f278e4d35bc8cc5bb9871e5a290ac59a871cca41f049517e7c48e2095b30`.

This is the extractor's source-first read and same-agent reconciliation, not an independent omission sample, audio check, live rehearsal or integration acceptance. The research skill required this durable cited report. Read cursor: all 29 windows completed in order, workbench start 0 → next 22 → EOF; no frozen coordinator sample was consulted. The supplied source is untimed. Paragraph coverage cannot be translated into seconds.

## Status and actual failures

A1–A6 are complete at same-agent extraction/desk-review level. A7/A8, independent adjudication, natural-question retrieval and exact review binding remain coordinator work.

Final local inventory: **28 reference buckets, 34 typed spans, 29 accounted paragraphs, 38 action claims, 29 lore rows, 6 correction/qualification rows, 9 safely qualified review flags and 12 full composed answers with 56 grouped material checkpoints.** No typed game-selection list was invented: the source has collecting complaints, illustrative condition examples and pickups, not a starter/favorites game selection exercise.

Initial failures are retained:

- The first record used the invalid role name `SUBSTANTIAL_DISCUSSION`. The schema check failed at g002. All such record/map labels were corrected to the existing `SUBSTANTIAL_COVERAGE` enum; no source boundaries were changed to make that test pass.
- First preflight failed `Record source metadata mismatch`: coordinator's manifest still said `selected_not_processed`, while the explicit delegation required record-only `extracted_draft`. No unauthorized manifest write was made. Coordinator transition/recheck remains necessary until confirmed.
- Before draft writing, the Little Mermaid candidate label briefly included an unsupported catalog subtitle. It was removed: the source supports a Little Mermaid II pinball game but not a supplied exact subtitle/platform. Raw caption forms were preserved. [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)
- Before draft writing, the Flintstones price example was adjudicated hypothetical, and the JVC/THQ variants were typed packaging. These are prevented false-positive interpretations, not discovered missing titles. [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22), [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24)

After role correction, direct checks passed: 28 literal spoken forms, 29 section entries, 34 reference mappings, 34 explicit span kinds and **242 exact quote/location checks, zero failures**. These machine counts do not establish independent semantic accuracy.

Coordinator subsequently updated the CQ23 manifest status; the settled episode preflight then passed with 29 windows and 34 spans. The initial metadata failure is retained above. Scoped whitespace/diff checks were also clean; no global database build was run by this extractor.

## A1/A2 — full reference and section reconciliation

The source-first inventory contains 28 buckets under the declared scope: identifiable games, series, named game products/platforms, component tables, a TV comparison and explicit unnamed game groups. All 28 are mapped (28/28; zero remaining unmapped buckets). This denominator is an episode-specific reference-bucket census, not every repeated word, an external title catalog or the coordinator's frozen sample. Occurrences/returns produce 34 spans. Generic unlabeled games, mailers/cases, cleaning supplies and damaged-cart examples remain in lore, not fictional individual titles.

| Bucket | Kind | Source map |
| --- | --- | --- |
| cq023-g001 — Street Fighter | series | [P1](../../../library/episodes/cq-023-sc-251774783.md#paragraph-1) passing |
| cq023-g002 — Street Fighter V | video_game | [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2) substantial; [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27) passing |
| cq023-g003 — PlayStation 2 | hardware | [P4](../../../library/episodes/cq-023-sc-251774783.md#paragraph-4) passing |
| cq023-g004 — Wii | hardware | [P4](../../../library/episodes/cq-023-sc-251774783.md#paragraph-4) passing |
| cq023-g005 — Unresolved three Game Boy games | game_collection | [P6](../../../library/episodes/cq-023-sc-251774783.md#paragraph-6) substantial; [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23) passing |
| cq023-g006 — Sega systems — unspecified | hardware | [P9](../../../library/episodes/cq-023-sc-251774783.md#paragraph-9) passing |
| cq023-g007 — Princess Tomato — exact subtitle not spoken | video_game | [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10) substantial |
| cq023-g008 — Shadowgate | video_game | [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20) substantial |
| cq023-g009 — Unresolved Flintstones | video_game | [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22) passing |
| cq023-g010 — Aerial Assault | video_game | [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23) passing |
| cq023-g011 — Master System | hardware | [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23) passing |
| cq023-g012 — Nintendo Power magazines | publication | [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) substantial |
| cq023-g013 — Super Star Wars — JVC box | accessory | [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) substantial |
| cq023-g014 — Super Star Wars: The Empire Strikes Back — THQ box | accessory | [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) substantial |
| cq023-g015 — Super Star Wars: Return of the Jedi — THQ box | accessory | [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) substantial |
| cq023-g016 — Super Star Wars: Return of the Jedi — JVC box | accessory | [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) substantial |
| cq023-g017 — Super Star Wars: The Empire Strikes Back — JVC box wanted | accessory | [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) substantial |
| cq023-g018 — Minecraft | video_game | [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25) supporting |
| cq023-g019 — Life is Strange | video_game | [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) passing; [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25) substantial; [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26) substantial; [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27) supporting |
| cq023-g020 — Grand Theft Auto | series | [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26) supporting |
| cq023-g021 — Twin Peaks | television | [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26) supporting |
| cq023-g022 — LEGO Dimensions | video_game | [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27) passing; [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) supporting |
| cq023-g023 — The Legend of Zelda — unspecified installment | series | [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) supporting |
| cq023-g024 — Little Mermaid II pinball game — exact edition unresolved | video_game | [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) substantial |
| cq023-g025 — Little Mermaid pinball table | game_component | [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) supporting |
| cq023-g026 — Little Mermaid II pinball table | game_component | [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) supporting |
| cq023-g027 — Unresolved couple other sweet pinballs | game_collection | [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) supporting |
| cq023-g028 — Game Boy systems | hardware | [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) passing |

Every paragraph was accounted for, including sections without game spans:

| Paragraph | Disposition |
| --- | --- |
| [P1](../../../library/episodes/cq-023-sc-251774783.md#paragraph-1) | Kat and Johnny host; schedule, recovery and small invited Street Fighter event. |
| [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2) | Johnny played Street Fighter V: first-round win over Nick then next-round loss; shop visit. |
| [P3](../../../library/episodes/cq-023-sc-251774783.md#paragraph-3) | Collecting frustrations and non-exhaustive rant setup; no game identity. |
| [P4](../../../library/episodes/cq-023-sc-251774783.md#paragraph-4) | Johnny ranks bubble mailers his worst annoyance; cardboard-box shipping rule and replaceable-case exceptions. |
| [P5](../../../library/episodes/cq-023-sc-251774783.md#paragraph-5) | Crushed returns, angry-email template, requests and offered shipping payment; no specific titles. |
| [P6](../../../library/episodes/cq-023-sc-251774783.md#paragraph-6) | Three unnamed Game Boy games received crushed and all returned; hypothetical cheap-return arithmetic. |
| [P7](../../../library/episodes/cq-023-sc-251774783.md#paragraph-7) | Time-cost emphasis and comic anger; Kat takes over with sticker complaints. |
| [P8](../../../library/episodes/cq-023-sc-251774783.md#paragraph-8) | Kat's price/name/rental stickers and label risk; metallic void stickers. |
| [P9](../../../library/episodes/cq-023-sc-251774783.md#paragraph-9) | Sticker-removal uncertainty, cleaning product mentions and unidentified Sega batch-cleaning speaker. |
| [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10) | Kat's stickered Princess Tomato as personal example; fondness and terrible-game judgment coexist. |
| [P11](../../../library/episodes/cq-023-sc-251774783.md#paragraph-11) | Invitation for removal advice or future remedies episode; no established universal method. |
| [P12](../../../library/episodes/cq-023-sc-251774783.md#paragraph-12) | Johnny's second complaint: stock-only photos and inadequate condition descriptions. |
| [P13](../../../library/episodes/cq-023-sc-251774783.md#paragraph-13) | Historical listing/photo-fee observations and desired views, not current platform rules. |
| [P14](../../../library/episodes/cq-023-sc-251774783.md#paragraph-14) | Stock photos acceptable alongside actual photos; hidden label damage and hypothetical small premium. |
| [P15](../../../library/episodes/cq-023-sc-251774783.md#paragraph-15) | Johnny accepts responsibility for stock-photo gambles; bubble shipping remains seller frustration. |
| [P16](../../../library/episodes/cq-023-sc-251774783.md#paragraph-16) | Missing before-shipping photos obscure whether damage was preexisting; subjective condition. |
| [P17](../../../library/episodes/cq-023-sc-251774783.md#paragraph-17) | Different condition standards, future upgrades and existing imperfect boxed copies. |
| [P18](../../../library/episodes/cq-023-sc-251774783.md#paragraph-18) | Kat fears Sharpie more than ordinary dirt; hypothetical ideal collection. |
| [P19](../../../library/episodes/cq-023-sc-251774783.md#paragraph-19) | Kat prefers stickers; Johnny prefers Sharpie and has removed it once or twice; duplicate-test suggestion. |
| [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20) | Johnny's mud-filled Shadowgate discarded in early collecting; remembered low value and damaged-game sightings. |
| [P21](../../../library/episodes/cq-023-sc-251774783.md#paragraph-21) | Kat accepts some common torn labels; Johnny usually passes to avoid paying twice. |
| [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22) | Flintstones rare-bargain hypothetical; Johnny online choices versus Kat local/exchange constraints. |
| [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23) | Listener cleaning-tip invitation; Kat bought Aerial Assault; Johnny returns recap. |
| [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) | Nintendo Power about forty, yesterday corrected; JVC/THQ Star Wars box consistency acquisitions and remaining want. |
| [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25) | Kat's Minecraft start postponed for Life is Strange; about fifteen minutes and tentative reaction; $10 Gold recommendation claim. |
| [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26) | Life is Strange linear outcomes versus GTA; Twin Peaks tonal comparison and corrected wording, not finished Kat verdict. |
| [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27) | Kat plans fair try; Johnny's Street Fighter V return and brief LEGO Dimensions play. |
| [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) | Zelda deferred, LEGO time choice, Little Mermaid pinball dislike/other-table plan and unnamed Game Boy arrivals. |
| [P29](../../../library/episodes/cq-023-sc-251774783.md#paragraph-29) | Ratings request and public handles; outro, no new game reference. |

### Qualified prominence

After the documented second-pass repair, Life is Strange leads at **three meaningful paragraphs (25–27)**. **Six games tie next at one paragraph**: Street Fighter V, Princess Tomato, Shadowgate, Minecraft, LEGO Dimensions and the Little Mermaid II pinball game. There is no unique second or third place. Life is Strange has two substantial paragraphs and one supporting; LEGO's P28 rationale is supporting while its P27 brief recap is passing. Aerial Assault's bare purchase/platform mention is passing. These are meaningful paragraph unions, not timed speech. The initial ranking and actual role errors are retained in [the second-pass report](023-independent-check.md). [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

GTA and Zelda remain series-level; the first Street Fighter event label is not automatically a specific installment before the next paragraph identifies V. Star Wars packaging, Nintendo Power, pinball component tables, TV comparison and unidentified game groups do not enter the individual-game leaders. The short P27 Street Fighter return is passing, not a second meaningful paragraph. The P24 anonymous setup for Life is Strange is also passing rather than inflated game discussion. [P1](../../../library/episodes/cq-023-sc-251774783.md#paragraph-1), [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

## A3 — participants and attribution

Kat and Johnny are the explicitly introduced hosts; no guest or Tyler is introduced. Johnny's tournament story is linked by the subsequent named handoff and first-person recap; Nick is a reported opponent, not a participant in this recording. Johnny's wife is mentioned only as his wife, without importing a personal name from elsewhere. [P1](../../../library/episodes/cq-023-sc-251774783.md#paragraph-1), [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2), [P3](../../../library/episodes/cq-023-sc-251774783.md#paragraph-3), [P4](../../../library/episodes/cq-023-sc-251774783.md#paragraph-4), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27)

Kat's sticker complaint follows the explicit handoff and anchors the Princess Tomato example. The later marker preference contrast and Johnny's once-or-twice removal are conversationally attributed, not audio diarization. The brief Sega batch-cleaning first-person passage remains actor-unknown because its turns are less securely anchored. [P7](../../../library/episodes/cq-023-sc-251774783.md#paragraph-7), [P9](../../../library/episodes/cq-023-sc-251774783.md#paragraph-9), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P18](../../../library/episodes/cq-023-sc-251774783.md#paragraph-18), [P19](../../../library/episodes/cq-023-sc-251774783.md#paragraph-19)

The closing pickup exchange anchors Kat's Aerial Assault and Johnny's magazine/box purchases. Minecraft/Life is Strange is Kat's story directed at Johnny, while LEGO and pinball follow the handoff asking what he has played. No household actor is silently substituted for either host. [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24), [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

## A4 — action audit and negative boundaries

All 38 typed actions were checked against their source paragraphs and adjacent handoffs. Most are host-reported and contextually attributed, not externally verified transactions. Critical distinctions:

- Three unnamed Game Boy games arrived crushed and **all went back**. The later pickup recap does not revive ownership. Generic repeated returns are separate from that three-game event; seven/four-dollar arithmetic is illustrative. [P5](../../../library/episodes/cq-023-sc-251774783.md#paragraph-5), [P6](../../../library/episodes/cq-023-sc-251774783.md#paragraph-6), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23)
- Kat owns the stickered Princess Tomato and some marked games; wanting cleanup is not performed cleanup. Johnny's removed-marker history is his, and a suggested duplicate experiment remains hypothetical. [P8](../../../library/episodes/cq-023-sc-251774783.md#paragraph-8), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P18](../../../library/episodes/cq-023-sc-251774783.md#paragraph-18), [P19](../../../library/episodes/cq-023-sc-251774783.md#paragraph-19)
- Shadowgate was **discarded**, not sold or returned. It is stored as a mentioned disposition with past ownership, not a fabricated sale enum. Approximate 2006/two-dollar context is historical memory. [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20)
- Flintstones at $200 is an illustrative rare-game exception; neither the installment nor a real acquisition is established. Conditional nicer-copy preferences are not completed upgrades. [P21](../../../library/episodes/cq-023-sc-251774783.md#paragraph-21), [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22)
- Kat bought Aerial Assault. Johnny bought about forty magazines and a JVC Jedi **box**. The existing JVC Super Star Wars and THQ Empire/Jedi packaging is distinct from the still-wanted JVC Empire box. No cartridge/CIB/new-set completion is inferred. [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24)
- Kat had not played Minecraft. She obtained Life is Strange and played about fifteen minutes, but the mentioned Gold offer is not proof of exactly what she paid. Continued play and final verdict remain open. [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27)
- Johnny played LEGO and the Little Mermaid pinball game, deferred unspecified Zelda, and received other unnamed Game Boy pinballs. The other table and those arrivals still await reported testing. No later photos, completion or recommendation is invented. [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

There is no explicit completed sale in this source. Potential resale in a label-upgrade argument is conditional, not a sale event. No title-specific order awaiting shipment is established; known returns and receipts are represented instead. [P21](../../../library/episodes/cq-023-sc-251774783.md#paragraph-21), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

## A5 — actual complete answers

All 12 answers below were composed and reread against the supplied passages. All 56 grouped material checkpoints are supported with the qualifications shown (56/56 same-agent checkpoint support; not independent atomic accuracy or retrieval performance). Original natural questions are stored separately from lexical queries. Their required locations are source requirements, not tuned after a retrieval failure. Forbidden-inference lists remain in the JSON.

The first-pass checkpoint review missed two overly generous span roles, which made the original prominence answer over-precise. A same-agent second pass found them; root agreed, and the current answer/map were repaired. Eleven of the original twelve answers needed no material correction; the prominence answer did. See [the second-pass report](023-independent-check.md) for the preserved initial ranking, exact findings and settled validation. The current 56 checkpoints are development review, not an independent score.

### cq023-roster

Who was hosting the collecting-rants episode, and how did Johnny's tournament go?

Kat and Johnny host this episode. Johnny says he attended a small invited Street Fighter event while still recovering from illness. In Street Fighter V he beat Nick in the first round and was then annihilated in the next round. His poor start to the conversation refers to how he felt afterward, not to having disliked the event.

Evidence: [P1](../../../library/episodes/cq-023-sc-251774783.md#paragraph-1), [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2). Checked 4/4 grouped material checkpoints; independent review and query execution pending.

### cq023-mailers

What exactly made bubble mailers Johnny's biggest complaint, and did he actually return any games?

Johnny's rule is that a game in a cardboard box should be shipped in a box. He allows more leeway for loose cartridges or inexpensive games in replaceable cases. He describes repeated crushed deliveries, a saved angry-email template and requests for better packing, including offers to pay more. Most concretely, three unnamed Game Boy games arrived crushed and all went back. His objection includes the time lost arranging returns; the seven-dollar game and four-dollar return examples are illustrative, not verified charges for those three games.

Evidence: [P4](../../../library/episodes/cq-023-sc-251774783.md#paragraph-4), [P5](../../../library/episodes/cq-023-sc-251774783.md#paragraph-5), [P6](../../../library/episodes/cq-023-sc-251774783.md#paragraph-6), [P7](../../../library/episodes/cq-023-sc-251774783.md#paragraph-7). Checked 5/5 grouped material checkpoints; independent review and query execution pending.

### cq023-tomato

Which stickered game was Kat especially reluctant to clean, and did she even like it?

Kat uses her Princess Tomato copy as the personal example: she wants its sticker gone but worries about removing part of the underlying label or leaving residue. She says she feels fondly about the game while also calling it terrible. The conversation does not report a successful removal. They ask listeners for methods; it supplies no demonstrated universal cleaning procedure.

Evidence: [P7](../../../library/episodes/cq-023-sc-251774783.md#paragraph-7), [P8](../../../library/episodes/cq-023-sc-251774783.md#paragraph-8), [P9](../../../library/episodes/cq-023-sc-251774783.md#paragraph-9), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P11](../../../library/episodes/cq-023-sc-251774783.md#paragraph-11). Checked 5/5 grouped material checkpoints; independent review and query execution pending.

### cq023-photos

Did Johnny reject every listing that used a stock photo?

No. He says a stock image alongside photos of the actual item is fine; his complaint is relying on it alone. He wants condition details and views that reveal damaged labels or hidden stickers. He admits gambling on stock-photo listings from half.com and Amazon, winning some and losing others, and takes responsibility for choosing that risk. Without before-shipping pictures, the hosts note that damage can be difficult to distinguish from an item's original condition. These are their dated observations, not present-day marketplace policy.

Evidence: [P12](../../../library/episodes/cq-023-sc-251774783.md#paragraph-12), [P13](../../../library/episodes/cq-023-sc-251774783.md#paragraph-13), [P14](../../../library/episodes/cq-023-sc-251774783.md#paragraph-14), [P15](../../../library/episodes/cq-023-sc-251774783.md#paragraph-15), [P16](../../../library/episodes/cq-023-sc-251774783.md#paragraph-16), [P17](../../../library/episodes/cq-023-sc-251774783.md#paragraph-17). Checked 5/5 grouped material checkpoints; independent review and query execution pending.

### cq023-sharpie

Which host preferred Sharpie to stickers, and had either proven a cleaning method?

Kat says Sharpie frightens her more and would take a sticker instead. Johnny leans the other way because stickers seem like more work, and says he has removed Sharpie once or twice. He suggests testing on a duplicate. That is not evidence Kat performed the experiment, and the exchange does not establish a universally safe cleaning method.

Evidence: [P18](../../../library/episodes/cq-023-sc-251774783.md#paragraph-18), [P19](../../../library/episodes/cq-023-sc-251774783.md#paragraph-19). Checked 4/4 grouped material checkpoints; independent review and query execution pending.

### cq023-shadowgate

What did Johnny do with the filthy Shadowgate, and is the two-dollar figure useful as a price today?

Johnny recalls opening a Shadowgate copy and finding what looked like dirt and mud inside, including around the board. He threw it away rather than dealing with it. The approximately two-dollar value and around-2006 setting are remembered historical context, not a current price or evidence of a sale or return.

Evidence: [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20). Checked 3/3 grouped material checkpoints; independent review and query execution pending.

### cq023-labels

Why did Kat and Johnny differ about accepting torn labels?

Kat says a torn label is not always a deal-breaker on common games and hopes to upgrade when a reasonably priced copy appears. Johnny usually passes because he expects to upgrade anyway and would rather spend a little more once. He recognizes that he is comparing online alternatives while Kat is constrained by what is locally available and by exchange and eBay costs. The two-hundred-dollar Flintstones line is a hypothetical rare-game exception, not a disclosed purchase.

Evidence: [P21](../../../library/episodes/cq-023-sc-251774783.md#paragraph-21), [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23). Checked 4/4 grouped material checkpoints; independent review and query execution pending.

### cq023-pickups

What were Kat and Johnny's actual pickups, and what was still missing from the matching Star Wars boxes?

Kat reports Aerial Assault for Master System. Johnny says he bought about forty Nintendo Power magazines at Game Swappers, correcting today to yesterday, and is getting close to finishing that set. He also bought a JVC box for Super Star Wars: Return of the Jedi. He already had a JVC Super Star Wars box and THQ packaging for Empire and Jedi; the JVC Empire box was still needed to make the shelf consistent. These are magazines and packaging acquisitions, not forty games or a newly purchased complete Jedi game.

Evidence: [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24). Checked 6/6 grouped material checkpoints; independent review and query execution pending.

### cq023-life

Did Kat finally play Minecraft, or did Johnny steer her toward something else?

Kat says she had never played Minecraft and still had not reached it. Johnny urged her to get Life is Strange instead, mentioning a ten-dollar Gold offer at the time. She got it and was only about fifteen minutes in, adjusting to its choice-based style. She neither loved nor hated it yet and planned to give it a fair try on her day off. Johnny describes its outcomes within a fairly linear track and a Twin Peaks-like strangeness; those are his comparisons, not Kat's completed verdict or proof of the exact price she paid.

Evidence: [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24), [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27). Checked 6/6 grouped material checkpoints; independent review and query execution pending.

### cq023-time

Why did Johnny play LEGO rather than more Zelda, and which Zelda was it?

Johnny says he played a little LEGO Dimensions and wanted more Zelda but only had about an hour, less time than he wanted for Zelda. The episode names Zelda generically; it does not establish the installment here. The hour describes available time, not an exact measured LEGO session.

Evidence: [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28). Checked 4/4 grouped material checkpoints; independent review and query execution pending.

### cq023-pinball

Did Johnny enjoy the Little Mermaid pinball, and had he tested the other Game Boy arrivals?

Johnny calls the Little Mermaid II pinball game awful, but says he probably will give it about five more minutes to try the other table. He describes Little Mermaid and Little Mermaid II table choices inside that game, not two separately purchased games. He also says a couple of other pinballs arrived for Game Boy systems and that he plans to check them out. Their titles, exact systems and later verdicts are not supplied.

Evidence: [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28). Checked 5/5 grouped material checkpoints; independent review and query execution pending.

### cq023-prominence

Which games received the most meaningful discussion in this episode?

Using meaningful untimed paragraph coverage, Life is Strange leads with three paragraphs (25–27). Six games tie next at one paragraph each: Street Fighter V, Princess Tomato, Shadowgate, Minecraft, LEGO Dimensions and the Little Mermaid II pinball game. There is no unique second- or third-place game. Aerial Assault is only a brief named pickup, and LEGO's P27 recap is passing; LEGO's meaningful time-allocation explanation is in P28. This is discussion coverage, not elapsed speech time or a recommendation. Series-level GTA and Zelda, boxes, magazines, component tables and unidentified game groups remain outside this individual-game ranking.

Evidence: [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28). Checked 5/5 grouped material checkpoints; independent review and query execution pending.

## A6 — practical pre-show brief

**Prior episode-grounded conclusions.** Lead with the contrast: Johnny's shipping anger is about irreplaceable time as much as cardboard damage, while Kat is anxious about making an already imperfect label worse. The three returned Game Boy games and Princess Tomato sticker make those complaints concrete. Do not turn the cleaning conversation into advice backed by testing. [P4](../../../library/episodes/cq-023-sc-251774783.md#paragraph-4), [P5](../../../library/episodes/cq-023-sc-251774783.md#paragraph-5), [P6](../../../library/episodes/cq-023-sc-251774783.md#paragraph-6), [P7](../../../library/episodes/cq-023-sc-251774783.md#paragraph-7), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10)

**Useful nuance.** Johnny is not simply demanding perfect-condition copies: he admits taking stock-photo risks and owns the decision. He also accepts that Kat's local selection and exchange costs alter the label-upgrade calculation. That makes a follow-up about differing constraints more grounded than repeating a generic rant. [P14](../../../library/episodes/cq-023-sc-251774783.md#paragraph-14), [P15](../../../library/episodes/cq-023-sc-251774783.md#paragraph-15), [P17](../../../library/episodes/cq-023-sc-251774783.md#paragraph-17), [P21](../../../library/episodes/cq-023-sc-251774783.md#paragraph-21), [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22)

**Continuity examples and corrections.** The shelf-matching Star Wars purchase was packaging, with Empire's JVC box still open; the magazine purchase date corrects to yesterday. Kat has started Life is Strange, not Minecraft, and has not rendered a final judgment. Johnny corrects his own playing-with/as wording. These are safe reminders with actual source boundaries, not a reconstructed biography. [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24), [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27)

**Jokes and tone.** The bubble-mailer rage and saved angry-email template are comic self-description, not an actionable threat. Kat can be fond of a game she calls terrible. The vegetable-game/pinball contrast closes the show, and Johnny's awful pinball verdict coexists with his intention to try the other table. [P4](../../../library/episodes/cq-023-sc-251774783.md#paragraph-4), [P5](../../../library/episodes/cq-023-sc-251774783.md#paragraph-5), [P7](../../../library/episodes/cq-023-sc-251774783.md#paragraph-7), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

**Open loops.** They invite good cleaning methods and possibly a remedies episode; Johnny still wants the Empire box; Kat promises a fair Life is Strange trial; Johnny plans other-table and unnamed pinball testing. The transcript does not close these loops. [P11](../../../library/episodes/cq-023-sc-251774783.md#paragraph-11), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

**Fresh editorial proposals, not documented past events.** Ask how collectors decide whether a cheap return is worth the time; whether condition preferences change when buying locally; or whether a disliked game earns a second short trial. A practical cleaning follow-up would require separately checked methods, not reuse of this episode's untested chemical mentions as safe instructions.

Desk usefulness review: the brief offers specific memory hooks, two-host contrast, source-backed corrections and four unresolved follow-up avenues. It avoids generic game trivia in an episode mostly about collecting condition. It is usable as written research context, but no live cohost rehearsal, latency test or spoken delivery result was performed. Root retains independent semantic review, all query/adjudication results and acceptance binding.
