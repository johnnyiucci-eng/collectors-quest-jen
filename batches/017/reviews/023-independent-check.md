# CQ23 second-pass semantic check — same agent, not independent extraction

The filename follows the coordinator's requested review convention. This reviewer also extracted CQ23: this is **same-agent second-pass adjudication**, not an independent or blind check. Research used the unchanged supplied primary source, already read end-to-end (29/29 paragraphs, cursor 0 → 22 → EOF), followed by a fresh inspection of all 12 current complete answers, all 38 action summaries, and all 34 typed spans. P23 and P27–28 were reread exactly to resolve depth boundaries. No frozen sample, routing implementation, external source or audio was consulted.

Source SHA: `f317f278e4d35bc8cc5bb9871e5a290ac59a871cca41f049517e7c48e2095b30`.
Initial inspected record SHA: `e0fe3cbd1ad65ca8aedccbc2a830aa4af7779c6db68c8a7bcca9a569698d4e66`.
Initial annotations SHA: `aeeb3dc5c56c3e2390ac1cb2c25dd2b26048eed6ee1142014b5be79d11f38052`.

## Actual findings and authorized repairs

Two of the 34 span classifications had over-generous meaningful credit:

1. **Aerial Assault, P23, g010/span-010-1.** The passage says, “Just aerial assault for Master System.” The surrounding response is generic busy-week and something-better-than-nothing talk. This establishes the purchase/platform, but not meaningful game discussion. SUPPORTING_EXAMPLE → PASSING_MENTION; the purchased action is unchanged. [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23)
2. **LEGO Dimensions, P27, g022/span-022-1.** Johnny says, “I have been playing a little bit of Lego Dimension.” This is a brief recap, similar to Street Fighter V's adjacent passing return. The explanation of choosing LEGO with limited available time comes in P28 and retains supporting credit. P27 SUPPORTING_EXAMPLE → PASSING_MENTION. Played action remains unchanged. [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

These were reported to root before edits. Root agreed with both and authorized durable role, leaders, prominence-answer/checkpoint and audit-copy repair. This is a real ranking-precision failure, not an omitted title or quote failure.

The original 12-answer set had **11 answers without newly identified material errors and one prominence answer needing repair**. All 38 action summaries retained supported or explicitly qualified actors/actions; no action summary was changed. The first-pass 56/56 grouped checkpoint statement did not catch these depth errors and must not be treated as independent accuracy. After repair, the 12 current answers were checked again; the updated prominence answer matches the source-adjudicated map.

## Recalculated paragraph union, before and after

The calculation expands each span's start/end-exclusive bounds, unions substantial/supporting paragraphs by entity ID, and admits only `video_game` kinds. Passing spans contribute no units. There were no overlapping-window double counts to repair.

| Individual game | Initial meaningful union | Final meaningful union |
| --- | --- | --- |
| Life is Strange | P25–27: 3 | P25–27: 3 |
| LEGO Dimensions | P27–28: 2 | P28: 1 |
| Street Fighter V | P2: 1 | P2: 1 |
| Princess Tomato | P10: 1 | P10: 1 |
| Shadowgate | P20: 1 | P20: 1 |
| Aerial Assault | P23: 1 | none: passing |
| Minecraft | P25: 1 | P25: 1 |
| Little Mermaid II pinball | P28: 1 | P28: 1 |

The original ranking was Life is Strange 3, LEGO 2, with six games tied at 1 for third. **Final: Life is Strange 3, followed by a six-way tie at 1. There is no unique second or third game.** The digital Little Mermaid pinball is an eligible video game; its component tables are not standalone games. GTA/Zelda remain series-level and packaging/magazines remain non-game products. [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28)

## Complete-answer verdicts

| Case | Second-pass verdict and source |
| --- | --- |
| roster | Supported: two hosts, Johnny's first-round win and subsequent loss, recovery caveat. [P1](../../../library/episodes/cq-023-sc-251774783.md#paragraph-1), [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2) |
| mailers | Supported: cardboard rule, replaceable-case exceptions, three unnamed games returned, illustrative prices. [P4](../../../library/episodes/cq-023-sc-251774783.md#paragraph-4), [P5](../../../library/episodes/cq-023-sc-251774783.md#paragraph-5), [P6](../../../library/episodes/cq-023-sc-251774783.md#paragraph-6), [P7](../../../library/episodes/cq-023-sc-251774783.md#paragraph-7) |
| tomato | Supported: Kat's stickered copy, mixed affection/criticism, no completed removal. [P7](../../../library/episodes/cq-023-sc-251774783.md#paragraph-7), [P8](../../../library/episodes/cq-023-sc-251774783.md#paragraph-8), [P9](../../../library/episodes/cq-023-sc-251774783.md#paragraph-9), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P11](../../../library/episodes/cq-023-sc-251774783.md#paragraph-11) |
| photos | Supported: actual-item-photo exception and acknowledged gambles; no present-day policy claim. [P12](../../../library/episodes/cq-023-sc-251774783.md#paragraph-12), [P13](../../../library/episodes/cq-023-sc-251774783.md#paragraph-13), [P14](../../../library/episodes/cq-023-sc-251774783.md#paragraph-14), [P15](../../../library/episodes/cq-023-sc-251774783.md#paragraph-15), [P16](../../../library/episodes/cq-023-sc-251774783.md#paragraph-16), [P17](../../../library/episodes/cq-023-sc-251774783.md#paragraph-17) |
| sharpie | Supported: opposite preferences, Johnny's limited past removal, duplicate suggestion not performed. [P18](../../../library/episodes/cq-023-sc-251774783.md#paragraph-18), [P19](../../../library/episodes/cq-023-sc-251774783.md#paragraph-19) |
| shadowgate | Supported: discarded past copy; historical approximate value/date, no sale or return. [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20) |
| labels | Supported: conditional preferences and local constraints; Flintstones example hypothetical. [P21](../../../library/episodes/cq-023-sc-251774783.md#paragraph-21), [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23) |
| pickups | Supported: Aerial acquisition unchanged despite depth downgrade; magazines and box-only items distinguished; Empire wanted. [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) |
| life | Supported: Minecraft unplayed, Life is Strange started, tentative reaction and offer-versus-payment distinction. [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24), [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27) |
| time | Supported: LEGO played, generic Zelda deferred, available hour not an exact session. [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) |
| pinball | Supported: dislike, intended other-table trial, unnamed arrivals not yet tested. [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) |
| prominence | Initial depth-based answer failed; revised answer matches final union above. [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10), [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) |

## Action-state verdicts

All 38 action summaries were read individually. Grouped source anchors below cover the complete ID sequence, not a sample:

| Action IDs | Checked boundary |
| --- | --- |
| 001–002 | Johnny played the tournament and attended; not overall winner. [P1](../../../library/episodes/cq-023-sc-251774783.md#paragraph-1), [P2](../../../library/episodes/cq-023-sc-251774783.md#paragraph-2), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27) |
| 003–005 | Generic past returns versus three-game receipt/return; no retained ownership. [P5](../../../library/episodes/cq-023-sc-251774783.md#paragraph-5), [P6](../../../library/episodes/cq-023-sc-251774783.md#paragraph-6), [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23) |
| 006–009 | Kat's stickered possessions/wanted cleaning; Sega cleaning actor left unknown. [P8](../../../library/episodes/cq-023-sc-251774783.md#paragraph-8), [P9](../../../library/episodes/cq-023-sc-251774783.md#paragraph-9), [P10](../../../library/episodes/cq-023-sc-251774783.md#paragraph-10) |
| 010–013 | Past stock-photo purchasing; unspecified upgrades and future copy improvement, not invented transactions. [P15](../../../library/episodes/cq-023-sc-251774783.md#paragraph-15), [P17](../../../library/episodes/cq-023-sc-251774783.md#paragraph-17), [P21](../../../library/episodes/cq-023-sc-251774783.md#paragraph-21), [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22) |
| 014–016 | Kat's marked games/future cleaning versus Johnny's limited successful-removal report. [P18](../../../library/episodes/cq-023-sc-251774783.md#paragraph-18), [P19](../../../library/episodes/cq-023-sc-251774783.md#paragraph-19) |
| 017–019 | Shadowgate past ownership and explicit disposal; Flintstones hypothetical only. [P20](../../../library/episodes/cq-023-sc-251774783.md#paragraph-20), [P22](../../../library/episodes/cq-023-sc-251774783.md#paragraph-22) |
| 020–027 | Kat's actual purchase, Johnny magazines/packaging, existing THQ boxes, new Jedi JVC box and still-wanted Empire. [P23](../../../library/episodes/cq-023-sc-251774783.md#paragraph-23), [P24](../../../library/episodes/cq-023-sc-251774783.md#paragraph-24) |
| 028–032 | Minecraft negative/play intention, Life is Strange obtained/started/future play; no exact amount paid. [P25](../../../library/episodes/cq-023-sc-251774783.md#paragraph-25), [P26](../../../library/episodes/cq-023-sc-251774783.md#paragraph-26), [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27) |
| 033–038 | Johnny LEGO play, deferred Zelda, played Little Mermaid, planned other table, received but untested unnamed pinballs. [P27](../../../library/episodes/cq-023-sc-251774783.md#paragraph-27), [P28](../../../library/episodes/cq-023-sc-251774783.md#paragraph-28) |

Remaining limitations are safely represented: context-based attribution is not diarization; a `wanted` action may refer to future play or cleaning rather than buying, so its summary/purpose must accompany retrieval; Shadowgate's `owned` entry is explicitly historical and ended in disposal. No changes to these qualified summaries were necessary. No newly identified real purchase/return/receipt was omitted during this bounded action recheck.

## Settled local validation and handoff

All 12 original questions, queries and required evidence-location arrays remain identical at field level. The changed expected checkpoints remove unsupported ranking precision; they were not changed to satisfy a query result. Unrelated answer prose, evidence and all 38 actions were untouched.

The first audit-prose patch attempt failed because its hunks were ordered backward in the file; no partial Markdown edit landed. Reapplying in file order succeeded. This authoring failure is distinct from the two semantic span failures above.

Final preflight passes: 29 windows, 34 spans. Direct checks again passed 28 literal forms, 29 sections, 34 mappings, 34 explicit kinds and 242 exact proofs with zero failures. Final record SHA: `6544ff59b9eed6fc82a947e15b1f934097b7387acc71b5917e727a6dbb44dab6`; final annotations SHA: `9801d24e3219ba6c4fe2614402eac68ed89aab284bc55c18d55e843171207d62`. These identify the checked snapshots, not A8 acceptance. No global build, manifest edit, ledger or binding was performed here.

