# Batch 002 — qualified discussion leaders

Coverage is the per-entity union of substantial discussion plus supporting examples, excluding passing mentions. CQ8/CQ75 use paragraph counts; CQ201 uses coarse caption-window seconds, not exact speaking time. Shared windows can count for multiple games, so totals must not be summed as episode duration.

| Episode | Meaningful coverage leaders | Substantial-only perspective |
| --- | --- | --- |
| 8 | Metroid 6 paragraphs; Panic Restaurant and Tonic Trouble tied at 3 | Metroid 6; Panic Restaurant 2; other individual-game ties retained in query output |
| 75 | Bloodborne 4 paragraphs; Rondo of Blood, Castlevania, Donkey Kong Country Competition Cartridge and Gamma Attack tied at 3 | Bloodborne 3; Rondo of Blood and Crusader of Centy tied at 2 |
| 201 | Nintendo World Championships 1990 646s; Cheetahmen II 570s; Mike Tyson's Punch-Out!! and Punch-Out!! tied at 567s | Cheetahmen II 510s; Nintendo World Championships 1990 452s; The Last of Us Part II 439s |

There is no defensible exclusive top three where ties exist. CQ201's three-second difference between Cheetahmen II and the Punch-Out versions is much smaller than a caption window and is not decisive. Substantial-only results answer a different question from substantial-plus-supporting results.

CQ8's trilogy is explicitly a series discussion, not all credited to the first Mario Party release (2 meaningful paragraphs separately). CQ75's repeated tail contributes no meaningful coverage. CQ201's final X-Men window has an unknown endpoint and no invented duration; the Double Dragon credit joke is not a host's game assessment.

Shared-type recheck: Mario Party trilogy/series has five meaningful paragraphs in the separate `series_results` output, not the individual-game ranking. CQ201's broader Punch-Out series has 255 supporting seconds separately; it is not assigned to every installment. CQ75 individual leaders are unchanged.

Stadium Events was initially inflated to 892s by passing comparisons labeled supporting. After the source-bound repair it has 451 meaningful seconds, including 129 substantial. This correction preserves all nine reference spans. [Source audit and repair](201-audit.md).

Reproduce with `python scripts/lore_store.py top --collection batches/002 --episode 201`. [CQ8 map](008-annotations.json), [CQ75 map](075-annotations.json), [CQ201 map](201-annotations.json).
