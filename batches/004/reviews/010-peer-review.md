# CQ10 — separate source-first peer review

Reviewer: middle-lane agent, not CQ10's extractor. The full supplied [CQ10 transcript](../../../library/episodes/cq-010-sc-237478983.md) was read before opening the extraction. The first display omitted part ofP16–17; those paragraphs were then read completely before the inventory was frozen. This is a distinct reviewer within the same team, not a blinded statistical or external independent validation.

Source hash independently checked: `2bfc63dbf212e2904a0881f00b2661a93d07189e6de4217580e693c6c5d60adc`. Source scope is34 untimed paragraphs; no audio, network, database writes or extractor-file edits.

## Findings requiring coordinator repair

1. **Outgoing trade is returned as a sale.** `cq010-action-26` uses `sold` for the empty N64 boxes. SourceP16 explicitly introduces an Instagram trade: “we did a trade. I sent him a bunch of empty N64 boxes.” The summary correctly says trade-not-cash-sale, but the enum still makes a sold-state query return it. Prefer `mentioned` plus an explicit traded disposition under the current enum, or a supported separate trade state. This mirrors the need not to encode donations as sales. [P16](../../../library/episodes/cq-010-sc-237478983.md)

2. **Joint ownership is missed by canonical-person action retrieval.** `cq010-action-29` uses subject `Kat and John`. SourceP25 supports joint ownership—“we built so much of it together”—but the real `LoreStore.actions` exact-subject predicate returns no Kat-owned rows. Represent canonical Kat as an actor with a separate co-owner/joint qualifier, or linked canonical actor rows, without conflating husband John with Johnny. [P24–25](../../../library/episodes/cq-010-sc-237478983.md)

Read-only reproduction used the real `LoreStore.actions` method against the authored claim list through an input-backed object, not a generated database:

- `actions('Kat','owned')` → `[]`
- `actions('Nick Morgan','sold')` → `cq010-action-26`
- Joint row subject is literally `Kat and John`.

These are observed pre-repair behavioral gaps. Repairs and post-repair rebuild/results are pending coordinator. No extractor files were changed by this reviewer.

## Source-first inventory and real denominators

Before comparison, the reviewer froze the following seven windows containing31 raw reference-window pairs. NWC gray/gold were counted separately at raw-variant level; the extraction legitimately groups them under one underlying game, so31 raw references map to30 stored buckets/spans. The31 denominator must not be silently changed to30 or described as31 distinct games.

| Source window | Frozen raw reference inventory | Comparison |
| --- | --- | --- |
| P8 | “reproductions of Earthbound”; “Battle Kid games” | 2/2 |
| P9 | “stadium events” North American CIB; “NWC gray”; “NWC gold”; “GameCube interactive multi-game demo disc set” | 4/4, NWC variants share one bucket |
| P10 | “January 2002 disc”; “Oddworld, Munch of Saddusy”; “Grand Theft Auto 3” | 3/3 |
| P11 | “International Superstar Soccer 99” | 1/1 |
| P13 | “Super Metroid”; “original Harvest Moon”; “Super Mario World”; “Zelda Link to the Past”; “Donkey Kong Country series”; “Luffy 1 and 2” | 7/7 |
| P17 | “Zelda franchise”; “Mega Man 1 through 6”; “Mega Man X2, X3” | 9/9 |
| P32 | “Mario Kart 7”; “Fallout 4”; “Super Mario Maker”; “Smash Bros.”; “Splatoon” | 5/5 |

All excerpts/locations refer to the [primary transcript](../../../library/episodes/cq-010-sc-237478983.md). The raw numbered Mega Man range supports six references, not six substantive reviews.

Results:34/34 source paragraphs read and considered,31/31 frozen raw pairs present in base records and mapped at their source occurrences,30/30 existing spans examined, and27 windows without a newly identifiable named-game reference. The additional P10 continuation of the demo-set object is correctly included even though the initial raw inventory separately names its January2002 member there. No named-reference miss was found. This is full-source peer inventory coverage for this episode, not estimated archive recall.

Exclusions: Star Wars introductory/closing media quotes are not specific game titles; Skynet is a joke; platform collection totals are not thousands of itemized games; Magic cards are a tabletop/trading-activity reference. Generic social media, succession discussion, unnamed transactions and closing music remain useful source sections without game-ranking credit.

## Span precision and identity

All30 stored span records were inspected. Six are supporting,24 passing; the demo-set span alone extends across two source paragraphs. No obvious inflated meaningful span was found. Rapid SNES examples inP13 and Mega Man/Zelda examples inP17 correctly earn no meaningful coverage. P10's first sentences genuinely complete the January2002 demo-set anecdote, so the two-paragraph set span is justified despite other subjects following within the same coarse paragraph.

The extractor's qualified ranking is sound: Oddworld, GTAIII, ISS99 and Mario Kart7 each have one supporting paragraph; no unique top three exists. The two-paragraph demo collection must remain excluded from individual-game rankings, and neither collection size nor interview length should make every owned game a leading topic. [P9–13, P17, P32](../../../library/episodes/cq-010-sc-237478983.md)

Identity safeguards pass: NES Earthbound reproduction remains unresolved; Battle Kid and DKC stay collective; raw Luffy1/2 remain separate uncertain candidates; Oddworld normalization is provisional; no contents are invented for the January2002 demo disc. Gray/gold NWC variants remain retrievable as separate owned objects while sharing one game identity. The canonical NWC1990 year and Wii U Smash title are contextual normalizations, not verbatim full source titles; they should not be described as external catalog verification.

## Actions, speakers and future plans

All51 existing action rows were checked against their source context.49/51 did not require a semantic/filter repair in this review; the two exceptions are listed above. This is a denominator of existing rows checked, not a claim that51 is the only possible segmentation of all source actions. Full-source omission review did not find a missing positive named-game purchase/ownership/play event beyond information already represented.

Johnny, Kat and guest Nick Morgan are directly introduced. Signed-copy anecdotes and10,000-game milestone belong to Nick, not Johnny; Kat's husband John, Nick's brother Matt and Johnny's card-selling friend remain different people. Structured speaker objects preserve the reporter even where a separate reporter field is null; filling that field consistently would improve the contract but is not an additional observed attribution error.

Plans versus receipts are handled well: the GBC lot initially lacks ISS99 and the later “since gotten” statement supports acquisition; no separate ISS99 price or delivery date is invented. The delayed Instagram item is shipped, not upgraded to a documented receipt. Mario Maker/Wii U are intentions, Mario Kart7 is actual recurring play, and the digital bundle is considered then probably rejected. Oral succession conversations and market-value hypotheticals are not completed sales, wills, paid commissions or accepted offers. [P11, P16–19, P24–33](../../../library/episodes/cq-010-sc-237478983.md)

## Actual composed-answer review

All seven stored full prose answers and all36 attached evidence checkpoints were read against their complete source windows.7/7 answers are substantively supported with no material false attribution or forbidden inference found:

- Signed copies: correctly Nick, with respectful personal encounter distinct from hostile general commentary.
- GBC purchase: initial missing game versus later completion, no invented standalone price.
- Instagram trades: Kat has not traded; Nick and Johnny have; shipment not a dated receipt.
- Succession plans: oral/hypothetical, distinct relatives and declined15% offer.
- Market-value offers: different hosts and qualified positions, not actual sale.
- Playing: Mario Kart7 actual; Mario Maker future; digital bundle not purchased.
- VGDB: dated searchable-database features, not a fresh website audit.

This peer check is manual source adjudication of authored answers, not a new retrieval benchmark. The two action-query defects do not make these prose answers false; they still require repair because a structured action request can return different results.

## Handoff

No game-reference or span repair requested. Two action-representation repairs requested; coordinator owns their implementation and post-repair verification. Keep the pre-repair results above when recording improvements. A7/A8 acceptance is not granted by this peer note.

