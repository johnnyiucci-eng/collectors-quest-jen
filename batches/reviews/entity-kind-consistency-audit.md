# Cross-collection entity-kind consistency audit

## Scope and outcome

Read-only snapshot of **37 extracted records, 3,134 reference buckets and 1,452 lore rows** in the pilot and batches 002–010. Compared record `entity_granularity` with all joined annotation-span `entity_kind` values by source key and game reference. The research skill required primary-artifact investigation and this durable report. No accepted record, annotation, generated index or review binding was changed.

**Search has a real classification gap:** [searchable_rows](../../scripts/search_lore_pilot.py) emits `kind: game` for every occurrence in `record.games`, regardless of its granularity or the reviewed span kind. There are **276 buckets whose joined spans are exclusively known non-video-game object kinds**, producing **450 rows still labelled game**. Four additional buckets mix video-game and non-game spans; all 280 buckets together produce 460 coarse game rows. The latter number must not be presented as 460 individually adjudicated non-game occurrences. Physical pinball, tabletop and electronic toys are games in ordinary language, but remain outside this collection's individual-video-game ranking contract.

Changing record granularity alone will not fix that coarse search filter. The span-based ranking already separates these types. A future repair needs explicit object-kind propagation or filtering in searchable evidence, while retaining meaningful references to products and media. Hardware or music should not disappear from general lore search.

The mismatch-oriented candidate scan found **218 record buckets** detailed below: 193 use `title_unspecified_release`, three `unresolved_game_or_variant`, eight generic `unresolved`, thirteen `series`, and one `edition`. This is a review queue, **not 218 proven semantic extraction failures**. The generic unresolved and series labels can be correct on their own axis while failing to express the known object kind. One additional clear wrong-category example outside that filter is **cq082-g036**, an EP labelled accessory.

## Checks and interpretation limits

- All **1,452/1,452 lore.topics** values are nonempty arrays of nonblank strings. No malformed topic row was found. This checks structure, not ontology quality, synonym duplication or completeness of topics.
- For the 280 buckets with a non-game span, **489/489 occurrence evidence quote/location pairs** matched the supplied raw source window exactly. This is mechanical source fidelity, not a fresh semantic rereading of all those windows.
- I inspected contextual evidence for ten risk examples: cq222-g038/g041, cq259-g081, cq263-g134, cq078-g007, cq082-g036, cq209-g168, and cq016-g030/g043/g044. The broader candidate table is a cross-artifact type review, not a claim to have independently re-read every episode end to end during this task.
- **160 legacy pilot buckets** have joined spans without an explicit kind. Those are not counted as definite non-game mismatches. Missing legacy metadata is a separate coverage limitation; blindly calling them hardware or games would manufacture an answer.
- Broad series synonyms are not automatically bugs. `series` and `game_series` are compatible. A comic/book/music series can also correctly be a series, provided its object kind is carried separately. Similarly, unresolved identity is not unresolved object type: an unknown cookbook can still be a book.
- Compilations, hypothetical games and unrecognized references were not automatically treated as hardware/media errors. The report does not normalize their identity or adjudicate their ranking policy.

## Source-confirmed priority examples

| ID | Evidence and required review |
| --- | --- |
| cq222-g038 | [CQ222 01:42:55](../../library/episodes/cq-222-sc-1517354524.md): buying the Lightening Force **manual**, not the software. Record title/granularity alone misrepresent the acquired object; accessory span is already correct. |
| cq222-g041 | [CQ222 01:51:04](../../library/episodes/cq-222-sc-1517354524.md): an Animal Crossing **Switch** not bought, not an unspecified Animal Crossing game. Preserve the negative purchase state. |
| cq263-g134 | [CQ263 03:37:45](../../library/episodes/cq-263-sc-1993480675.md): Tyler's Sears home Pong console; the hardware span disambiguates the generic Pong title. |
| cq016-g030/g043/g044 | [CQ16 P16/P33/P34](../../library/episodes/cq-016-sc-243666752.md): controller designs and controllers. Exact model ambiguity does not justify `unresolved_game_or_variant`; preserve uncertain models while typing accessory/hardware. |
| cq082-g036 | [CQ82 P13–14](../../library/episodes/cq-082-sc-381157055.md): Super Madness Clockwork EP, music and band support. `accessory` is wrong; `music_release` spans already supply the correct object kind. |
| cq078-g007 | [CQ78 P11–12](../../library/episodes/cq-078-sc-349518307.md): haunted-house collectible, with a hypothetical controller function. Review as a collectible/edition-product context, not evidence that a Resident Evil 7 software edition was played or purchased. Do not convert the imagined controller function into a real hardware specification. |
| cq209-g168 | [CQ209 02:16:30](../../library/episodes/cq-209-sc-1391155801.md): Rock Band 2 bundle price example, not a purchase. Bundle typing may need both software and hardware context rather than unconditional single-game or hardware-only flattening. |
| cq259-g081 | [CQ259 02:01:54 and reviewed spans](../../pilot/annotations.json): Blood Bowl has both tabletop and video-game kinds. A global per-bucket replacement would lose that distinction; review occurrences separately. |

Also review cq082-g034/g038/g039 for accessory-versus-console specificity, not a false game identity: Nintendo PlayStation prototype, Omega console and PS4 prize console are already non-game on both broad axes. cq015-g023 remains an incoming unresolved item, not enough evidence here to force either a game or hardware. cq016-g051's broad Star Fox comparison remains an intended series/unspecified-reference distinction, not an automatic synonym error.

## Exact candidate IDs

Each row links the owning record. Span kinds are the current reviewed categories, not newly invented canonical identities. For `series`, `unresolved` and `edition` rows, examine object-kind propagation before changing a valid granularity. Mixed kinds require occurrence-level review. This table preserves all 218 initial candidates rather than silently deleting inconvenient cases.

| Collection | ID / current title | Record granularity | Span kind(s) |
| --- | --- | --- | --- |
| pilot | [cq200-g036](../../pilot/records/sc-1316628157.json) — Logo | title_unspecified_release | non_video_game_reference |
| pilot | [cq200-g064](../../pilot/records/sc-1316628157.json) — Magic: The Gathering | title_unspecified_release | non_video_game_reference |
| pilot | [cq222-g038](../../pilot/records/sc-1517354524.json) — Lightening Force: Quest for the Darkstar | title_unspecified_release | accessory |
| pilot | [cq222-g041](../../pilot/records/sc-1517354524.json) — Animal Crossing | title_unspecified_release | hardware |
| pilot | [cq222-g042](../../pilot/records/sc-1517354524.json) — Unresolved raw identity | title_unspecified_release | interactive_attraction |
| pilot | [cq222-g043](../../pilot/records/sc-1517354524.json) — Unresolved raw identity | title_unspecified_release | interactive_attraction |
| pilot | [cq259-g081](../../pilot/records/sc-1943435095.json) — Blood Bowl | title_unspecified_release | tabletop, video_game |
| pilot | [cq259-g084](../../pilot/records/sc-1943435095.json) — Warhammer Fantasy Battle | title_unspecified_release | tabletop |
| pilot | [cq259-g085](../../pilot/records/sc-1943435095.json) — Warhammer 40,000 | title_unspecified_release | tabletop |
| pilot | [cq259-g086](../../pilot/records/sc-1943435095.json) — Warhammer Age of Sigmar | title_unspecified_release | tabletop |
| pilot | [cq263-g134](../../pilot/records/sc-1993480675.json) — Pong | title_unspecified_release | hardware |
| pilot | [cq299-g059](../../pilot/records/sc-2387089140.json) — Deck Demon | title_unspecified_release | non_game_software |
| pilot | [cq146-g033](../../pilot/records/sc-852741172.json) — Magic: The Gathering | title_unspecified_release | non_video_game_reference |
| pilot | [cq146-g034](../../pilot/records/sc-852741172.json) — Pokémon | title_unspecified_release | trading_card_brand |
| batches/002 | [cq201-g026](../../batches/002/records/sc-1327980511.json) — Dreamcast Web Browser | title_unspecified_release | non_game_software |
| batches/002 | [cq201-g028](../../batches/002/records/sc-1327980511.json) — Compton's Interactive Encyclopedia | title_unspecified_release | non_game_software |
| batches/002 | [cq201-g029](../../batches/002/records/sc-1327980511.json) — Game Genie | title_unspecified_release | hardware |
| batches/002 | [cq201-g030](../../batches/002/records/sc-1327980511.json) — Action Replay | title_unspecified_release | hardware |
| batches/002 | [cq201-g031](../../batches/002/records/sc-1327980511.json) — NES Cleaning Kit | title_unspecified_release | hardware |
| batches/002 | [cq201-g032](../../batches/002/records/sc-1327980511.json) — Eliminator | title_unspecified_release | hardware |
| batches/002 | [cq201-g141](../../batches/002/records/sc-1327980511.json) — HD Loader | title_unspecified_release | non_game_software |
| batches/003 | [cq202-g032](../../batches/003/records/sc-1335372241.json) — Haunted House | title_unspecified_release | physical_pinball |
| batches/003 | [cq202-g112](../../batches/003/records/sc-1335372241.json) — Warhammer | title_unspecified_release | tabletop |
| batches/004 | [cq203-g034](../../batches/004/records/sc-1343296345.json) — Unresolved raw identity | unresolved | electronic_toy |
| batches/004 | [cq203-g035](../../batches/004/records/sc-1343296345.json) — Simon | title_unspecified_release | electronic_toy |
| batches/004 | [cq203-g036](../../batches/004/records/sc-1343296345.json) — Frogger | title_unspecified_release | electronic_toy |
| batches/004 | [cq203-g037](../../batches/004/records/sc-1343296345.json) — Donkey Kong tabletop | title_unspecified_release | electronic_toy |
| batches/004 | [cq203-g038](../../batches/004/records/sc-1343296345.json) — Pac-Man tabletop | title_unspecified_release | electronic_toy |
| batches/004 | [cq203-g072](../../batches/004/records/sc-1343296345.json) — Panzer Dragoon R-Zone | title_unspecified_release | electronic_toy |
| batches/004 | [cq203-g098](../../batches/004/records/sc-1343296345.json) — Unresolved raw identity | unresolved | historical_apparatus |
| batches/004 | [cq203-g099](../../batches/004/records/sc-1343296345.json) — Practical Cinematography and Its Applications | title_unspecified_release | book |
| batches/004 | [cq203-g119](../../batches/004/records/sc-1343296345.json) — Dungeons & Dragons | title_unspecified_release | tabletop |
| batches/004 | [cq203-g147](../../batches/004/records/sc-1343296345.json) — Unresolved raw identity | unresolved | non_game_software |
| batches/004 | [cq203-g156](../../batches/004/records/sc-1343296345.json) — The Last of Us: American Dreams | series | comic |
| batches/005 | [cq204-g025](../../batches/005/records/sc-1350766930.json) — Collector Protector box protectors | title_unspecified_release | packaging |
| batches/005 | [cq204-g026](../../batches/005/records/sc-1350766930.json) — RetroProtection box protectors | title_unspecified_release | packaging |
| batches/005 | [cq204-g027](../../batches/005/records/sc-1350766930.json) — Video Game Box Protectors | title_unspecified_release | packaging |
| batches/005 | [cq204-g034](../../batches/005/records/sc-1350766930.json) — Super Nintendo New 3DS XL edition | title_unspecified_release | hardware |
| batches/005 | [cq204-g035](../../batches/005/records/sc-1350766930.json) — Super Nintendo Super Set | title_unspecified_release | hardware |
| batches/005 | [cq204-g038](../../batches/005/records/sc-1350766930.json) — Zelda special-edition handhelds | title_unspecified_release | hardware |
| batches/005 | [cq204-g039](../../batches/005/records/sc-1350766930.json) — Original Game Boy boxed / Zelda-sticker bundle | title_unspecified_release | hardware |
| batches/005 | [cq204-g040](../../batches/005/records/sc-1350766930.json) — Persona special-edition handheld | title_unspecified_release | hardware |
| batches/005 | [cq204-g041](../../batches/005/records/sc-1350766930.json) — Metroid special-edition handheld | title_unspecified_release | hardware |
| batches/005 | [cq204-g045](../../batches/005/records/sc-1350766930.json) — Batman: Knightfall | series | comic |
| batches/005 | [cq204-g061](../../batches/005/records/sc-1350766930.json) — Nintendo Deluxe Set / pre-Deluxe test-market bundle | title_unspecified_release | hardware |
| batches/005 | [cq204-g073](../../batches/005/records/sc-1350766930.json) — Pokemon Pico/Beena console | title_unspecified_release | hardware |
| batches/005 | [cq204-g074](../../batches/005/records/sc-1350766930.json) — Pikachu-face handheld | title_unspecified_release | hardware |
| batches/005 | [cq204-g091](../../batches/005/records/sc-1350766930.json) — The Hitchhiker's Guide to the Galaxy signed book | title_unspecified_release | book |
| batches/005 | [cq204-g102](../../batches/005/records/sc-1350766930.json) — Unresolved raw identity | unresolved | non_game_software |
| batches/005 | [cq078-g007](../../batches/005/records/sc-349518307.json) — Resident Evil 7: Biohazard | edition | accessory |
| batches/006 | [cq205-g001](../../batches/006/records/sc-1360671826.json) — Magic: The Gathering | title_unspecified_release | tabletop |
| batches/006 | [cq205-g002](../../batches/006/records/sc-1360671826.json) — Magic 30th Anniversary Edition | title_unspecified_release | tabletop |
| batches/006 | [cq205-g003](../../batches/006/records/sc-1360671826.json) — Magic Secret Lair | series | tabletop |
| batches/006 | [cq205-g004](../../batches/006/records/sc-1360671826.json) — Warhammer 40,000 Commander decks | title_unspecified_release | tabletop |
| batches/006 | [cq205-g005](../../batches/006/records/sc-1360671826.json) — Magic Alpha / Beta | title_unspecified_release | tabletop |
| batches/006 | [cq205-g006](../../batches/006/records/sc-1360671826.json) — Black Lotus | title_unspecified_release | tabletop |
| batches/006 | [cq205-g007](../../batches/006/records/sc-1360671826.json) — Ancestral Recall | title_unspecified_release | tabletop |
| batches/006 | [cq205-g008](../../batches/006/records/sc-1360671826.json) — Magic Collector's Edition | title_unspecified_release | tabletop |
| batches/006 | [cq205-g009](../../batches/006/records/sc-1360671826.json) — Magic dual lands | title_unspecified_release | tabletop |
| batches/006 | [cq205-g010](../../batches/006/records/sc-1360671826.json) — Mox Jet | title_unspecified_release | tabletop |
| batches/006 | [cq205-g011](../../batches/006/records/sc-1360671826.json) — Wurmcoil Engine | title_unspecified_release | tabletop |
| batches/006 | [cq205-g012](../../batches/006/records/sc-1360671826.json) — Contract from Below | title_unspecified_release | tabletop |
| batches/006 | [cq205-g013](../../batches/006/records/sc-1360671826.json) — Crusade | title_unspecified_release | tabletop |
| batches/006 | [cq205-g014](../../batches/006/records/sc-1360671826.json) — Invoke Prejudice | title_unspecified_release | tabletop |
| batches/006 | [cq205-g015](../../batches/006/records/sc-1360671826.json) — Earthbind | title_unspecified_release | tabletop |
| batches/006 | [cq205-g056](../../batches/006/records/sc-1360671826.json) — Gremlins 2 print-shop add-on | title_unspecified_release | non_game_software |
| batches/006 | [cq205-g099](../../batches/006/records/sc-1360671826.json) — Arachnophobia novel | title_unspecified_release | book |
| batches/006 | [cq205-g100](../../batches/006/records/sc-1360671826.json) — Bram Stoker's Dracula novelization | title_unspecified_release | book |
| batches/006 | [cq205-g114](../../batches/006/records/sc-1360671826.json) — The Addams Family pinball | title_unspecified_release | physical_pinball |
| batches/006 | [cq205-g131](../../batches/006/records/sc-1360671826.json) — Blair Witch: Rustin Parr novel | title_unspecified_release | book |
| batches/006 | [cq205-g134](../../batches/006/records/sc-1360671826.json) — Skylanders figures | series | toy_collection |
| batches/006 | [cq205-g136](../../batches/006/records/sc-1360671826.json) — Amiibo | title_unspecified_release | toy_collection |
| batches/006 | [cq205-g137](../../batches/006/records/sc-1360671826.json) — Disney Infinity figures | title_unspecified_release | toy_collection |
| batches/006 | [cq205-g139](../../batches/006/records/sc-1360671826.json) — Wata cases | title_unspecified_release | packaging |
| batches/006 | [cq205-g140](../../batches/006/records/sc-1360671826.json) — VGA slide-bottom cases | title_unspecified_release | packaging |
| batches/006 | [cq205-g141](../../batches/006/records/sc-1360671826.json) — Retro Boxed acrylic cases | title_unspecified_release | packaging |
| batches/006 | [cq205-g142](../../batches/006/records/sc-1360671826.json) — Star Fox banner | title_unspecified_release | promotional_item |
| batches/006 | [cq205-g143](../../batches/006/records/sc-1360671826.json) — Super Mario Bros. movie | title_unspecified_release | film |
| batches/006 | [cq205-g144](../../batches/006/records/sc-1360671826.json) — Super Mario animated movie trailer | title_unspecified_release | film |
| batches/006 | [cq205-g145](../../batches/006/records/sc-1360671826.json) — Nintendo Land | title_unspecified_release | attraction |
| batches/006 | [cq205-g148](../../batches/006/records/sc-1360671826.json) — Nintendo gameplay-counselor VHS collection | title_unspecified_release | archival_media |
| batches/006 | [cq205-g167](../../batches/006/records/sc-1360671826.json) — ZombiU Deluxe Wii U set | title_unspecified_release | hardware |
| batches/007 | [cq206-g001](../../batches/007/records/sc-1369678939.json) — Magic: The Gathering | title_unspecified_release | tabletop |
| batches/007 | [cq206-g018](../../batches/007/records/sc-1369678939.json) — Limited Run collector cards | title_unspecified_release | packaging |
| batches/007 | [cq206-g026](../../batches/007/records/sc-1369678939.json) — Unresolved raw identity | unresolved | book |
| batches/007 | [cq206-g047](../../batches/007/records/sc-1369678939.json) — Garfield and Friends themes / specials | series | television |
| batches/008 | [cq207-g022](../../batches/008/records/sc-1377327931.json) — Action Comics #1 | title_unspecified_release | comic |
| batches/008 | [cq207-g023](../../batches/008/records/sc-1377327931.json) — Action Comics | series | comic |
| batches/008 | [cq207-g024](../../batches/008/records/sc-1377327931.json) — Sensation Comics | series | comic |
| batches/008 | [cq207-g025](../../batches/008/records/sc-1377327931.json) — Flash Comics | series | comic |
| batches/008 | [cq207-g026](../../batches/008/records/sc-1377327931.json) — Captain America | title_unspecified_release | comic |
| batches/008 | [cq207-g027](../../batches/008/records/sc-1377327931.json) — Superman #1 | title_unspecified_release | comic |
| batches/008 | [cq207-g042](../../batches/008/records/sc-1377327931.json) — Tecmo Super Hockey | title_unspecified_release | packaging |
| batches/008 | [cq207-g043](../../batches/008/records/sc-1377327931.json) — NHL 98 | title_unspecified_release | packaging |
| batches/008 | [cq207-g044](../../batches/008/records/sc-1377327931.json) — Madden NFL 93 | title_unspecified_release | packaging |
| batches/008 | [cq207-g065](../../batches/008/records/sc-1377327931.json) — M.A.C.S. rifle | title_unspecified_release | hardware |
| batches/008 | [cq207-g068](../../batches/008/records/sc-1377327931.json) — Nintendo Power #1 | title_unspecified_release | magazine |
| batches/008 | [cq207-g073](../../batches/008/records/sc-1377327931.json) — Metal Gear Solid 2 signed plaque | title_unspecified_release | promotional_item |
| batches/008 | [cq207-g074](../../batches/008/records/sc-1377327931.json) — CGC game case | title_unspecified_release | packaging |
| batches/008 | [cq207-g075](../../batches/008/records/sc-1377327931.json) — Wata new case | title_unspecified_release | packaging |
| batches/008 | [cq207-g076](../../batches/008/records/sc-1377327931.json) — VGA game case | title_unspecified_release | packaging |
| batches/008 | [cq207-g084](../../batches/008/records/sc-1377327931.json) — Generic Nintendo inserts and Tengen registration cards | title_unspecified_release | packaging |
| batches/008 | [cq207-g094](../../batches/008/records/sc-1377327931.json) — Switch Collector books | title_unspecified_release | book |
| batches/008 | [cq207-g095](../../batches/008/records/sc-1377327931.json) — Game manuals bulk lot | title_unspecified_release | packaging |
| batches/008 | [cq207-g096](../../batches/008/records/sc-1377327931.json) — Super Mario World manual | title_unspecified_release | packaging |
| batches/008 | [cq207-g097](../../batches/008/records/sc-1377327931.json) — Super Mario Kart manual | title_unspecified_release | packaging |
| batches/008 | [cq207-g098](../../batches/008/records/sc-1377327931.json) — Super Metroid manual | title_unspecified_release | packaging |
| batches/008 | [cq207-g099](../../batches/008/records/sc-1377327931.json) — The Adventures of Batman & Robin manual | title_unspecified_release | packaging |
| batches/009 | [cq208-g004](../../batches/009/records/sc-1381920739.json) — PlayStation Classic | title_unspecified_release | hardware |
| batches/009 | [cq208-g005](../../batches/009/records/sc-1381920739.json) — God of War cookbook | title_unspecified_release | book |
| batches/009 | [cq208-g006](../../batches/009/records/sc-1381920739.json) — Hyrule Historia | title_unspecified_release | book |
| batches/009 | [cq208-g007](../../batches/009/records/sc-1381920739.json) — The Legend of Zelda Encyclopedia | title_unspecified_release | book |
| batches/009 | [cq208-g008](../../batches/009/records/sc-1381920739.json) — Bitmap Books JRPG book | title_unspecified_release | book |
| batches/009 | [cq208-g012](../../batches/009/records/sc-1381920739.json) — Hardcore Gaming 101 retro horror guide | series | book |
| batches/009 | [cq208-g013](../../batches/009/records/sc-1381920739.json) — Hardcore Gaming 101 Japanese obscurities books | series | book |
| batches/009 | [cq208-g014](../../batches/009/records/sc-1381920739.json) — Hardcore Gaming 101 translation books | series | book |
| batches/009 | [cq208-g015](../../batches/009/records/sc-1381920739.json) — Game Engine Black Book: Doom | title_unspecified_release | book |
| batches/009 | [cq208-g016](../../batches/009/records/sc-1381920739.json) — Game Engine Black Book: Wolfenstein 3D | title_unspecified_release | book |
| batches/009 | [cq208-g019](../../batches/009/records/sc-1381920739.json) — The Making of Prince of Persia | title_unspecified_release | book |
| batches/009 | [cq208-g021](../../batches/009/records/sc-1381920739.json) — A History of Video Games in 64 Objects | title_unspecified_release | book |
| batches/009 | [cq208-g023](../../batches/009/records/sc-1381920739.json) — Sierra Collector's Quest I | title_unspecified_release | book |
| batches/009 | [cq208-g024](../../batches/009/records/sc-1381920739.json) — Ultima collecting reference | title_unspecified_release | book |
| batches/009 | [cq208-g025](../../batches/009/records/sc-1381920739.json) — Ultima Online collecting reference | title_unspecified_release | book |
| batches/009 | [cq208-g028](../../batches/009/records/sc-1381920739.json) — Sierra Collector's Quest Zero | title_unspecified_release | book |
| batches/009 | [cq208-g032](../../batches/009/records/sc-1381920739.json) — Family Bits Volume One | title_unspecified_release | book |
| batches/009 | [cq208-g033](../../batches/009/records/sc-1381920739.json) — Masters of Doom | title_unspecified_release | book |
| batches/009 | [cq208-g034](../../batches/009/records/sc-1381920739.json) — Jeffrey Wittenhagen black-box guide | title_unspecified_release | book |
| batches/009 | [cq208-g035](../../batches/009/records/sc-1381920739.json) — NES Oddities | title_unspecified_release | book |
| batches/009 | [cq208-g036](../../batches/009/records/sc-1381920739.json) — Console Wars | title_unspecified_release | book |
| batches/009 | [cq208-g037](../../batches/009/records/sc-1381920739.json) — The Ultimate History of Video Games | title_unspecified_release | book |
| batches/009 | [cq208-g038](../../batches/009/records/sc-1381920739.json) — Super Mario Encyclopedia | title_unspecified_release | book |
| batches/009 | [cq208-g040](../../batches/009/records/sc-1381920739.json) — Limited Run history-book imprint | title_unspecified_release | book |
| batches/009 | [cq208-g041](../../batches/009/records/sc-1381920739.json) — The Art of Super Mario Galaxy | title_unspecified_release | book |
| batches/009 | [cq208-g044](../../batches/009/records/sc-1381920739.json) — PlayStation retrospective book | title_unspecified_release | book |
| batches/009 | [cq208-g045](../../batches/009/records/sc-1381920739.json) — History of Sunsoft | title_unspecified_release | book |
| batches/009 | [cq208-g046](../../batches/009/records/sc-1381920739.json) — Chris Kohler Square history book | title_unspecified_release | book |
| batches/009 | [cq208-g052](../../batches/009/records/sc-1381920739.json) — Garbage Pail Kids movie | title_unspecified_release | film |
| batches/009 | [cq208-g054](../../batches/009/records/sc-1381920739.json) — Cuphead merchandise | title_unspecified_release | merchandise |
| batches/009 | [cq208-g055](../../batches/009/records/sc-1381920739.json) — Gimmick pin | title_unspecified_release | merchandise |
| batches/009 | [cq208-g057](../../batches/009/records/sc-1381920739.json) — Conker pin | title_unspecified_release | merchandise |
| batches/009 | [cq208-g058](../../batches/009/records/sc-1381920739.json) — Battletoads pin | title_unspecified_release | merchandise |
| batches/009 | [cq208-g059](../../batches/009/records/sc-1381920739.json) — Teenage Mutant Ninja Turtles pins | title_unspecified_release | merchandise |
| batches/009 | [cq208-g060](../../batches/009/records/sc-1381920739.json) — Penny Arcade / PAX pins | title_unspecified_release | merchandise |
| batches/009 | [cq208-g080](../../batches/009/records/sc-1381920739.json) — RetroTINK 2X Pro | title_unspecified_release | hardware |
| batches/009 | [cq208-g081](../../batches/009/records/sc-1381920739.json) — RetroTINK 5X Pro | title_unspecified_release | hardware |
| batches/009 | [cq208-g082](../../batches/009/records/sc-1381920739.json) — Modded Game Boy / GBA IPS screen | title_unspecified_release | hardware |
| batches/009 | [cq208-g083](../../batches/009/records/sc-1381920739.json) — Analogue Pocket | title_unspecified_release | hardware |
| batches/009 | [cq208-g084](../../batches/009/records/sc-1381920739.json) — NESmaker development kit | title_unspecified_release | development_tool |
| batches/009 | [cq208-g086](../../batches/009/records/sc-1381920739.json) — Nerdy Nights | title_unspecified_release | development_tool |
| batches/009 | [cq208-g087](../../batches/009/records/sc-1381920739.json) — Nintendo Switch Pro Controller | title_unspecified_release | hardware |
| batches/009 | [cq208-g088](../../batches/009/records/sc-1381920739.json) — Xbox controller and Windows wireless adapter | title_unspecified_release | hardware |
| batches/009 | [cq208-g089](../../batches/009/records/sc-1381920739.json) — 8BitDo controller | title_unspecified_release | hardware |
| batches/009 | [cq208-g090](../../batches/009/records/sc-1381920739.json) — Xbox 360 wired controller | title_unspecified_release | hardware |
| batches/009 | [cq208-g092](../../batches/009/records/sc-1381920739.json) — Super Mario Bros. soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g093](../../batches/009/records/sc-1381920739.json) — OutRun soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g094](../../batches/009/records/sc-1381920739.json) — Undertale piano soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g095](../../batches/009/records/sc-1381920739.json) — Stardew Valley soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g096](../../batches/009/records/sc-1381920739.json) — Turnip Boy Commits Tax Evasion soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g098](../../batches/009/records/sc-1381920739.json) — Disco Elysium soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g099](../../batches/009/records/sc-1381920739.json) — The Messenger soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g100](../../batches/009/records/sc-1381920739.json) — Battletoads soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g101](../../batches/009/records/sc-1381920739.json) — Warhammer soundtrack | series | soundtrack |
| batches/009 | [cq208-g102](../../batches/009/records/sc-1381920739.json) — World of Warcraft soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g103](../../batches/009/records/sc-1381920739.json) — Persona 5 soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g104](../../batches/009/records/sc-1381920739.json) — Persona soundtracks | series | soundtrack |
| batches/009 | [cq208-g105](../../batches/009/records/sc-1381920739.json) — Unresolved raw identity | unresolved | soundtrack |
| batches/009 | [cq208-g106](../../batches/009/records/sc-1381920739.json) — Perfect Dark soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g107](../../batches/009/records/sc-1381920739.json) — Halo soundtrack | title_unspecified_release | soundtrack |
| batches/009 | [cq208-g108](../../batches/009/records/sc-1381920739.json) — Unresolved raw identity | unresolved | soundtrack |
| batches/009 | [cq208-g109](../../batches/009/records/sc-1381920739.json) — Sega Genesis Mini 2 | title_unspecified_release | hardware |
| batches/009 | [cq208-g110](../../batches/009/records/sc-1381920739.json) — NES Classic Mini | title_unspecified_release | hardware |
| batches/009 | [cq208-g112](../../batches/009/records/sc-1381920739.json) — Playdate | title_unspecified_release | hardware |
| batches/009 | [cq208-g113](../../batches/009/records/sc-1381920739.json) — Super Mario Game & Watch | title_unspecified_release | hardware |
| batches/009 | [cq208-g114](../../batches/009/records/sc-1381920739.json) — Zelda Game & Watch | title_unspecified_release | hardware |
| batches/009 | [cq208-g117](../../batches/009/records/sc-1381920739.json) — Steam Deck | title_unspecified_release | hardware |
| batches/009 | [cq208-g119](../../batches/009/records/sc-1381920739.json) — LEGO Mighty Bowser | title_unspecified_release | toy |
| batches/009 | [cq208-g120](../../batches/009/records/sc-1381920739.json) — LEGO Nintendo Entertainment System | title_unspecified_release | toy |
| batches/009 | [cq208-g121](../../batches/009/records/sc-1381920739.json) — LEGO Atari | title_unspecified_release | toy |
| batches/009 | [cq208-g122](../../batches/009/records/sc-1381920739.json) — LEGO Super Mario question block | title_unspecified_release | toy |
| batches/009 | [cq208-g124](../../batches/009/records/sc-1381920739.json) — LEGO Sonic packs | title_unspecified_release | toy |
| batches/009 | [cq208-g126](../../batches/009/records/sc-1381920739.json) — LEGO Super Mario course sets | title_unspecified_release | toy |
| batches/009 | [cq208-g128](../../batches/009/records/sc-1381920739.json) — Hallmark Super Nintendo ornament | title_unspecified_release | merchandise |
| batches/009 | [cq208-g130](../../batches/009/records/sc-1381920739.json) — Hallmark Genesis ornament | title_unspecified_release | merchandise |
| batches/009 | [cq208-g131](../../batches/009/records/sc-1381920739.json) — Hallmark Nintendo / Sega character ornaments | title_unspecified_release | merchandise |
| batches/009 | [cq208-g132](../../batches/009/records/sc-1381920739.json) — Fortnite llama ornament | title_unspecified_release | merchandise |
| batches/009 | [cq208-g134](../../batches/009/records/sc-1381920739.json) — Hallmark Animal Crossing musical ornament | title_unspecified_release | merchandise |
| batches/009 | [cq208-g138](../../batches/009/records/sc-1381920739.json) — Fortnite Magic Secret Lair | title_unspecified_release | tabletop |
| batches/009 | [cq208-g140](../../batches/009/records/sc-1381920739.json) — Arcade1Up cabinets | title_unspecified_release | hardware |
| batches/009 | [cq208-g141](../../batches/009/records/sc-1381920739.json) — Killer Instinct Arcade1Up Pro | title_unspecified_release | hardware |
| batches/009 | [cq208-g143](../../batches/009/records/sc-1381920739.json) — Star Wars Arcade1Up sit-down | title_unspecified_release | hardware |
| batches/009 | [cq208-g144](../../batches/009/records/sc-1381920739.json) — Street Fighter Arcade1Up | title_unspecified_release | hardware |
| batches/009 | [cq208-g146](../../batches/009/records/sc-1381920739.json) — Game Room Classics Taito counter unit | title_unspecified_release | hardware |
| batches/009 | [cq208-g147](../../batches/009/records/sc-1381920739.json) — Dragon's Lair Arcade1Up | title_unspecified_release | hardware |
| batches/009 | [cq208-g149](../../batches/009/records/sc-1381920739.json) — Tron Arcade1Up | title_unspecified_release | hardware |
| batches/009 | [cq208-g151](../../batches/009/records/sc-1381920739.json) — Gaming chairs / racing seats | title_unspecified_release | furniture |
| batches/009 | [cq208-g152](../../batches/009/records/sc-1381920739.json) — Stream Deck | title_unspecified_release | hardware |
| batches/009 | [cq208-g153](../../batches/009/records/sc-1381920739.json) — Streamer LED lights / effects | title_unspecified_release | hardware |
| batches/009 | [cq208-g154](../../batches/009/records/sc-1381920739.json) — Packing puzzle with ball bearings | title_unspecified_release | physical_puzzle |
| batches/009 | [cq208-g155](../../batches/009/records/sc-1381920739.json) — The Untold History of Japanese Game Developers | title_unspecified_release | book |
| batches/009 | [cq208-g156](../../batches/009/records/sc-1381920739.json) — History of Digital Games: Developments in Art, Design and Interaction | title_unspecified_release | book |
| batches/009 | [cq208-g157](../../batches/009/records/sc-1381920739.json) — Seeking Redemption: The Real Story of the Beautiful Game of Skee-Ball | title_unspecified_release | book |
| batches/009 | [cq208-g158](../../batches/009/records/sc-1381920739.json) — The Bingo Pinball War: United versus Bally, 1951–1957 | title_unspecified_release | book |
| batches/009 | [cq208-g165](../../batches/009/records/sc-1381920739.json) — X-Men Game Gear Cable card | title_unspecified_release | packaging |
| batches/010 | [cq209-g007](../../batches/010/records/sc-1391155801.json) — Super Nintendo Super Set | title_unspecified_release | hardware |
| batches/010 | [cq209-g008](../../batches/010/records/sc-1391155801.json) — Super Nintendo Control Set | title_unspecified_release | hardware |
| batches/010 | [cq209-g056](../../batches/010/records/sc-1391155801.json) — Dragon Ball | title_unspecified_release | other_media |
| batches/010 | [cq209-g091](../../batches/010/records/sc-1391155801.json) — Mother 3 GBA console | title_unspecified_release | hardware |
| batches/010 | [cq209-g093](../../batches/010/records/sc-1391155801.json) — Super Nintendo Classic | title_unspecified_release | hardware |
| batches/010 | [cq209-g094](../../batches/010/records/sc-1391155801.json) — PlayStation Classic | title_unspecified_release | hardware |
| batches/010 | [cq209-g140](../../batches/010/records/sc-1391155801.json) — Fun 'n Games manual | title_unspecified_release | packaging |
| batches/010 | [cq209-g143](../../batches/010/records/sc-1391155801.json) — 3 Ninjas Kick Back poster | title_unspecified_release | packaging |
| batches/010 | [cq209-g168](../../batches/010/records/sc-1391155801.json) — Rock Band 2 bundle | title_unspecified_release | hardware |
| batches/010 | [cq209-g169](../../batches/010/records/sc-1391155801.json) — Unresolved raw identity | unresolved | merchandise |
| batches/010 | [cq209-g217](../../batches/010/records/sc-1391155801.json) — Nintendo DS handheld collection | title_unspecified_release | hardware |
| batches/010 | [cq209-g218](../../batches/010/records/sc-1391155801.json) — Action Max | title_unspecified_release | hardware |
| batches/010 | [cq016-g030](../../batches/010/records/sc-243666752.json) — Hello Mac / Jeffrey / Mario Kart controller designs | unresolved_game_or_variant | accessory |
| batches/010 | [cq016-g043](../../batches/010/records/sc-243666752.json) — Hori Wii classic SNES controller — as spoken | unresolved_game_or_variant | accessory |
| batches/010 | [cq016-g044](../../batches/010/records/sc-243666752.json) — Dreamcast / Saturn 3D controller comparison | unresolved_game_or_variant | accessory |

## Integration recommendation and completion

Repair clear hardware/media record categories with explicit source context, then address coarse search-kind propagation and mixed occurrences separately. Preserve raw aliases, canonical uncertainty, negative states, span roles, source hashes and initial failure history. Re-run affected answer/actor/ranking regressions and renew only the affected review bindings after actual source adjudication. Do not bulk-label every `unresolved` bucket as a game or every franchise synonym as a defect.

The source scan initially used a wider candidate output that was truncated; I discarded that output and reran a bounded structured scan before computing these counts. No truncated content was used to edit records. A separate first PowerShell projection returned no result and was replaced by a read-only structured Python scan. Neither failure changed any file.

This task completes a bounded read-only consistency audit, not the repairs, fresh full-source acceptance of 37 episodes, or an automatic revocation/renewal of their existing bindings.

