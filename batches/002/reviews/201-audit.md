# CQ201 source-first episode audit

Coordinator completion addendum (2026-09-13): integration, source-first checks, all 17 batch answer reviews and 56 regressions passed. A1–A8 are accepted at captured-text development level in the [final ledger](../episode-review-ledger.json). Pending-coordinator statements below preserve the extraction-stage history and are superseded by that ledger; no audio/live certification is implied.

Status: A1–A6 source review and authored artifacts complete. Root's independent source-window cross-audit, retrieval integration, regression checks and A8 acceptance ledger remain separate and pending. This document does not claim that the batch is accepted or that a live cohost rehearsal occurred.

## Source and method

The research skill was used for primary-source reading and this findings artifact. Only the locally supplied [CQ201 transcript](../../../library/episodes/cq-201-sc-1327980511.md) was used. It is dated 2022-08-21, titled *Reconsidering the List of 677 NES Games*, with supplied media duration 02:39:49. The text has 150 timestamp windows, ending at 02:38:48; all were read consecutively in bounded, untruncated chunks, then selected identity, action and boundary passages were rechecked. SHA-256: `eff28d3c954554ce99abdb4cae21c58ad70ee372fafa32e9d83ec27a97d1520c`.

No audio was checked and no network, paid transcription, paid model API or publication was used by this audit. Caption navigation times do not prove exact utterance timing or transcription accuracy. No game-release, price, print-run, ROM, hardware or licensing claims were externally verified.

The episode was inventoried from the source before a CQ201 record existed. The same agent subsequently checked its own inventory; that is not an independent review. Root froze its own source-window sample separately, and its results must not be pre-claimed here.

Artifacts:

- [Record](../records/sc-1327980511.json): 179 reference records, 33 lore items, four correction records and 30 explicit unresolved identity/allusion entries.
- [Annotations](201-annotations.json): 264 uniquely identified, source-hashed spans; 150 section-accounting rows; 46 action/negative/hypothetical claims with explicit subjects; six composed task cases.
- Every span uses an existing base game ID and exact heading bounds. No additional game overrides are required because this is the initial extraction.

## A1 — Coverage and prominence

Every source window has a section-accounting row with its disposition and applicable span references. There are 123 windows intersecting at least one mapped reference and 27 deliberately without game spans. The latter include the opening travel/health tangent, generic list and sticker discussion, PSVR hardware debate, and Coraline toy purchases. These are accounted for, not silently skipped. The broad discussion of list philosophy is not allocated wholesale to every named example.

The map distinguishes substantial coverage, supporting examples, passing mentions and joke asides; returns such as Sunday Funday, NWC, Punch-Out, Ninja Gaiden and the closing Silly Bandz correction are split. Original games, compilation containers, component games, series references and uncertain titles are not treated as a single release indiscriminately. Utilities, cleaning accessories and the Rocket Games publisher line have non-video-game kinds in the annotations and must be excluded from game rankings.

The leading substantial-window proxies are:

| Reference | Substantial windows | Caption-window union |
| --- | ---: | ---: |
| Cheetahmen II | 8 | about 8:30 |
| Nintendo World Championships 1990, gray/gold discussion | 7 | about 7:32 |
| The Last of Us Part II | 7 | about 7:19 |

These are coarse editorial coverage estimates, not measured speaking time. NWC is a combined gray/gold discussion entity with variant context; it is not a claim those are two unrelated games or one identical collectible. Cheetahmen II includes discussion of its original distribution and a later remake comparison; Cheetahmen inside Action 52 remains separate. Tetris, Menace Beach and Sunday Funday also receive substantial coverage. Rankings can change under a supporting-plus-substantial metric or finer utterance segmentation. Adjacent totals are too close to imply precise dominance. Sources: [CQ201 00:55:32](../../../library/episodes/cq-201-sc-1327980511.md#005532), [CQ201 01:12:31](../../../library/episodes/cq-201-sc-1327980511.md#011231), [CQ201 02:13:19](../../../library/episodes/cq-201-sc-1327980511.md#021319).

## A2 — Omission and identity audit

Actual denominators: 150/150 supplied windows accounted for; 179/179 inventoried reference IDs represented by at least one span; 264/264 unique span IDs have valid base references and ordered source-heading bounds. These counts demonstrate accounting and referential integrity, not statistical recall of all possible game references. There is no independently measured semantic-recall percentage in this document.

The source-first pass includes rapid examples, compilation lists, quiet/non-game sections and patron credits. Rechecks specifically repaired returns in the live arithmetic, split the generic sticker tangent away from Myriad, limited Action 52's substantial span to its actual discussion, separated collectors' preferences from list rules, and restored the Sunday Funday correction. The 13-title Tengen list contains a caption reading “alien storm”; it is not silently rewritten to Alien Syndrome. “After Burner” crosses a caption boundary, as does the Ghosts 'n Goblins nickname, so both adjacent windows remain attached. Sources: [CQ201 01:45:35](../../../library/episodes/cq-201-sc-1327980511.md#014535), [CQ201 01:46:40](../../../library/episodes/cq-201-sc-1327980511.md#014640), [CQ201 02:34:38](../../../library/episodes/cq-201-sc-1327980511.md#023438), [CQ201 02:35:43](../../../library/episodes/cq-201-sc-1327980511.md#023543).

Major identity controls:

- Aladdin the Disney game is distinct from the Aladdin Deck Enhancer and Dizzy pack-in.
- Stack-Up is distinct from the unresolved “stack M” component on Maxi 15.
- Cheetahmen I, Cheetahmen II and Action 52's container are distinguished.
- Nintendo/Tengen Tetris share a topical entity but retain explicit variant context and the hosts' disagreement.
- Namco/Tengen Ms. Pac-Man equivalence remains unresolved; a same-ROM fact is not manufactured.
- Temple of Doom's publisher variant is not confused with the immediately corrected Last Crusade two-game example.
- Sunday Funday is a compilation with exclusive Fish Fall under the hosts' correction; the early same-game removal is superseded.
- Hypothetical SNES Little Samson and Dinosaur Peak ports are not real-release records.
- Coraline is a film/toy discussion here, not evidence of the Coraline video game.
- Patron allusions are marked jokes or uncertain series candidates, not substantive coverage or proof of someone's achievements.

The record deliberately retains the following unresolved or non-explicit identities. These are represented uncertainty, not silently completed external research:

- cq201-g006: secret of Monkey Island 2 — Second Monkey Island installment identified contextually; exact subtitle is not supplied. ([CQ201 00:13:50](../../../library/episodes/cq-201-sc-1327980511.md#001350))
- cq201-g009: Castlevania X — Caption says Castlevania X; Dracula X is a candidate, not silently certified. ([CQ201 00:13:50](../../../library/episodes/cq-201-sc-1327980511.md#001350))
- cq201-g015: Hong Kong mang — Unresolved caption, likely mahjong title; do not certify exact spelling or rarity. ([CQ201 00:19:15](../../../library/episodes/cq-201-sc-1327980511.md#001915))
- cq201-g018: aster — Tentative Asterix example; no exact game or exclusivity established. ([CQ201 00:20:18](../../../library/episodes/cq-201-sc-1327980511.md#002018))
- cq201-g019: balloon world — Unresolved inexpensive unlicensed example; do not substitute a known title. ([CQ201 00:22:25](../../../library/episodes/cq-201-sc-1327980511.md#002225))
- cq201-g020: Earth Defense Force — Unlicensed example; caption title may be wrong for the discussed game. ([CQ201 00:22:25](../../../library/episodes/cq-201-sc-1327980511.md#002225))
- cq201-g024: power strike two — Promotional example; possible title-number mismatch left unresolved. ([CQ201 00:27:43](../../../library/episodes/cq-201-sc-1327980511.md#002743))
- cq201-g034: Castlevania — Discussed as a prospective aftermarket release; exact title not given and not assumed released. ([CQ201 00:34:07](../../../library/episodes/cq-201-sc-1327980511.md#003407))
- cq201-g039: stack M — Unresolved spoken title of exclusive included game; retain component relationship without inventing exact spelling. ([CQ201 00:39:32](../../../library/episodes/cq-201-sc-1327980511.md#003932))
- cq201-g065: papon gals — Caption unresolved; compared to Galactic Crusader, no certified title or US release. ([CQ201 01:07:14](../../../library/episodes/cq-201-sc-1327980511.md#010714))
- cq201-g069: Donkey Kong competition — Competition/rental analogy; exact event and full title unspecified. ([CQ201 01:13:38](../../../library/episodes/cq-201-sc-1327980511.md#011338); [CQ201 01:14:39](../../../library/episodes/cq-201-sc-1327980511.md#011439))
- cq201-g107: alien storm — Source says alien storm; likely title error, Alien Syndrome candidate only. ([CQ201 01:46:40](../../../library/episodes/cq-201-sc-1327980511.md#014640))
- cq201-g131: Batman — Unspecified Batman game while browsing, no exact subtitle supplied. ([CQ201 02:08:01](../../../library/episodes/cq-201-sc-1327980511.md#020801))
- cq201-g138: Quest for thelda — Tyler buying update; title caption uncertain and Legend of Zelda port history unverified. ([CQ201 02:11:15](../../../library/episodes/cq-201-sc-1327980511.md#021115))
- cq201-g146: Rocket Games — Label/line of unlicensed games, not identified individual title. ([CQ201 02:12:16](../../../library/episodes/cq-201-sc-1327980511.md#021216))
- cq201-g158: Chris SNK — Patron nickname could be Capcom vs SNK allusion; no exact game identified. ([CQ201 02:33:32](../../../library/episodes/cq-201-sc-1327980511.md#023332))
- cq201-g159: Sonic — Patron nickname only, no installment inferred. ([CQ201 02:34:38](../../../library/episodes/cq-201-sc-1327980511.md#023438))
- cq201-g164: Zelda — Variant keeper, hero-of-time, timeline and Error nicknames; do not assign unspecified individual releases. ([CQ201 02:35:43](../../../library/episodes/cq-201-sc-1327980511.md#023543); [CQ201 02:36:46](../../../library/episodes/cq-201-sc-1327980511.md#023646))
- cq201-g165: what a horrible night — What a horrible night patron quotation, contextual allusion not direct title mention. ([CQ201 02:36:46](../../../library/episodes/cq-201-sc-1327980511.md#023646))
- cq201-g166: Pro Skater — Patron nickname, no installment supplied. ([CQ201 02:37:46](../../../library/episodes/cq-201-sc-1327980511.md#023746))
- cq201-g167: a bad enough dude to rescue the president — Rescue-the-president nickname, contextual candidate only. ([CQ201 02:37:46](../../../library/episodes/cq-201-sc-1327980511.md#023746))
- cq201-g168: all your base are belong to him — All your base quotation, contextual candidate only. ([CQ201 02:37:46](../../../library/episodes/cq-201-sc-1327980511.md#023746))
- cq201-g171: rip and tear — Rip and tear nickname, not a specific release or actual gameplay. ([CQ201 02:38:48](../../../library/episodes/cq-201-sc-1327980511.md#023848))
- cq201-g173: Mr Saturn — Mr. Saturn patron nickname only; contextual franchise candidate, not direct game title or host play. ([CQ201 02:33:32](../../../library/episodes/cq-201-sc-1327980511.md#023332))
- cq201-g174: Red Pyramid — Red Pyramid nickname only; no installment is explicitly named. ([CQ201 02:34:38](../../../library/episodes/cq-201-sc-1327980511.md#023438))
- cq201-g175: favorite store on the Citadel — Favorite store on the Citadel quote, contextual candidate only. ([CQ201 02:34:38](../../../library/episodes/cq-201-sc-1327980511.md#023438))
- cq201-g176: no gods or Kings — Patron quote, not a game discussion or endorsed philosophy. ([CQ201 02:35:43](../../../library/episodes/cq-201-sc-1327980511.md#023543))
- cq201-g177: a winner is him — A winner is him nickname; contextual candidate only. ([CQ201 02:36:46](../../../library/episodes/cq-201-sc-1327980511.md#023646))
- cq201-g178: strand type Game — Strand type game patron nickname, not actual play. ([CQ201 02:36:46](../../../library/episodes/cq-201-sc-1327980511.md#023646))
- cq201-g179: Order of No Quarter — Patron nickname group name, contextual candidate only. ([CQ201 02:36:46](../../../library/episodes/cq-201-sc-1327980511.md#023646))

## A3 — Participants and attribution

The introduction says Tyler is there with Johnny. Both are participants; Stefan is discussed but is not introduced as being on the episode. Joe, Pat, Nick Morgan, Mr. CIB, listeners and the barbecue attendee are mentioned people, not extra hosts. [CQ201 00:00:00](../../../library/episodes/cq-201-sc-1327980511.md#000000), [CQ201 01:16:48](../../../library/episodes/cq-201-sc-1327980511.md#011648), [CQ201 01:55:11](../../../library/episodes/cq-201-sc-1327980511.md#015511).

Named buying/playing handoffs and argument continuity support medium-confidence attribution for Johnny's Hellfire, Last of Us II and Silly Bandz accounts, and Tyler's MaxPlay, Ninja Gaiden and Golden Axe Warrior accounts. Undiarized shared exchanges retain an unknown speaker, including the Resident Evil 7 VR aside and the Mr. Dream non-play admission. Every attribution is text-contextual, not audio-verified.

The hosts repeatedly warn that this is devil's advocacy. Johnny's child-brain model is not his actual preference for collecting multicarts: he explicitly says his collector instinct is the opposite. NWC's aesthetic preference is distinct from whether it qualifies for a list. Stefan's older gray preference is not presented as current. [CQ201 00:18:09](../../../library/episodes/cq-201-sc-1327980511.md#001809), [CQ201 00:35:11](../../../library/episodes/cq-201-sc-1327980511.md#003511), [CQ201 01:56:19](../../../library/episodes/cq-201-sc-1327980511.md#015619), [CQ201 01:58:26](../../../library/episodes/cq-201-sc-1327980511.md#015826).

## A4 — Actions and non-actions

The 46 claims distinguish mentioned, wanted, purchased, received, owned, played, sold and hypothetical. No ordered state is manufactured where there is no explicit order. A negative statement remains negative, even when its storage state is “mentioned.” Action subjects are explicit; a reporter does not become the owner or buyer.

Important checks:

- Tyler's sealed Maxi 15 is historical ownership/purchase, not this week's pickup or evidence of playing the exclusive component.
- His loose Action 52 is owned; a CIB copy is wanted but explicitly not bought at the quoted cost.
- Impossible Mission II's two cartridges are owned/played by Tyler according to his report; identical-ROM status is not independently verified.
- Nick Morgan and Pat's NWC gold ownership is third-party reporting; neither becomes a host purchase. Stefan's possible future response is hypothetical.
- Johnny sold a cut-up Menace Beach box, not necessarily a cartridge or a complete-in-box game; approximate 2016 supersedes the earlier 2006 joke.
- Johnny bought Hellfire for its registration card while already owning a card-incomplete MUSHA. Discarding Hellfire and selling its remainder are uncompleted jokes/proposals.
- Quest for Thelda is a buying-segment mention but lacks an explicit transaction sentence here; its purchase is not certified.
- MaxPlay has two explicitly purchased platform copies, not one disc playable on both platforms.
- Last of Us II's New Game Plus replay is played but unfinished; no earned completion trophy or working repair.
- Johnny's Halloween games and Mr. CIB's Game Boy Color gift remain unnamed.
- Silly Bandz: two purchased copies, one intended for Tyler; contemplated bulk lot is not purchased and Tyler's receipt/play is not established.
- Dancing Blocks' sale and Poker III's asking price are not purchases by the hosts. Another attendee's Third Strike interest is not Tyler's gameplay.
- Patron score/completion jokes never become action records.

Sources: [CQ201 00:39:32](../../../library/episodes/cq-201-sc-1327980511.md#003932), [CQ201 00:43:49](../../../library/episodes/cq-201-sc-1327980511.md#004349), [CQ201 01:04:02](../../../library/episodes/cq-201-sc-1327980511.md#010402), [CQ201 01:09:25](../../../library/episodes/cq-201-sc-1327980511.md#010925), [CQ201 01:48:51](../../../library/episodes/cq-201-sc-1327980511.md#014851), [CQ201 02:09:09](../../../library/episodes/cq-201-sc-1327980511.md#020909), [CQ201 02:11:15](../../../library/episodes/cq-201-sc-1327980511.md#021115), [CQ201 02:13:19](../../../library/episodes/cq-201-sc-1327980511.md#021319), [CQ201 02:22:46](../../../library/episodes/cq-201-sc-1327980511.md#022246), [CQ201 02:29:16](../../../library/episodes/cq-201-sc-1327980511.md#022916).

## A5 — Composed real-task answers

These are actual answers written and checked against the source, not just keyword expectations. The same answer prose and forbidden-inference lists are in annotation JSON for root's retrieval checks. Search execution is a separate A7 integration step, not claimed here.

### 1. Why did Sunday Funday end up counting after they called it the same as Menace Beach?

They initially treated Sunday Funday as a reskin of Menace Beach, but later remembered that the Sunday Funday cartridge also contains Fish Fall, an exclusive game. Under Tyler's rule, a compilation with unique content counts, so he restores Sunday Funday and adds one back to his subtotal. This is the episode's own correction, not a claim that all religious reskins are distinct games. (CQ201 00:50:11; 01:47:48–01:48:51; 01:50:55.)

Source check: [CQ201 00:50:11](../../../library/episodes/cq-201-sc-1327980511.md#005011); [CQ201 01:47:48](../../../library/episodes/cq-201-sc-1327980511.md#014748); [CQ201 01:48:51](../../../library/episodes/cq-201-sc-1327980511.md#014851); [CQ201 01:50:55](../../../library/episodes/cq-201-sc-1327980511.md#015055). Expected boundary: Fish Fall exclusive restores Sunday Funday to Tyler's list.

Forbidden inferences: Sunday Funday remains excluded; Menace Beach and Sunday Funday have identical complete cartridge contents; An authoritative final 677-game replacement list was published.

Result: the composed answer is supported at the stated confidence by the supplied transcript. This is the extraction agent's desk check, not an independent reviewer or an executed retrieval pass.

### 2. Does Johnny liking gold NWC mean he counts it, and how does Tyler differ?

No. Johnny says gold NWC is cooler than gray but excludes promotional cartridges from his list. Tyler counts gold because a consumer could obtain it as a prize, while rejecting gray competition cartridges under his criteria. Their aesthetic preferences and inclusion rules differ. Stefan is discussed, but the hosts explicitly do not know his current opinion. (CQ201 01:12:31–01:15:42; 01:55:11–01:56:19.)

Source check: [CQ201 01:12:31](../../../library/episodes/cq-201-sc-1327980511.md#011231); [CQ201 01:13:38](../../../library/episodes/cq-201-sc-1327980511.md#011338); [CQ201 01:14:39](../../../library/episodes/cq-201-sc-1327980511.md#011439); [CQ201 01:15:42](../../../library/episodes/cq-201-sc-1327980511.md#011542); [CQ201 01:55:11](../../../library/episodes/cq-201-sc-1327980511.md#015511); [CQ201 01:56:19](../../../library/episodes/cq-201-sc-1327980511.md#015619). Expected boundary: Johnny prefers gold aesthetically but excludes it; Tyler counts consumer-prize gold, not gray.

Forbidden inferences: Johnny counts NWC gold; Tyler bought NWC gold; Stefan currently owns or is ordering NWC gold; All gray copies were definitively stolen.

Result: the composed answer is supported at the stated confidence by the supplied transcript. This is the extraction agent's desk check, not an independent reviewer or an executed retrieval pass.

### 3. What did Johnny buy Hellfire for?

Johnny says he finally bought Genesis Hellfire with its registration card after a long saved search. His MUSHA lacks a card, and he says Hellfire uses the same card, so it was a cheaper way to fill that gap than buying another MUSHA. Throwing Hellfire away and selling the remainder are jokes or proposals, not completed disposal or resale. The matching-card claim is his report, not independently authenticated here. (CQ201 02:09:09–02:11:15.)

Source check: [CQ201 02:09:09](../../../library/episodes/cq-201-sc-1327980511.md#020909); [CQ201 02:10:14](../../../library/episodes/cq-201-sc-1327980511.md#021018); [CQ201 02:11:15](../../../library/episodes/cq-201-sc-1327980511.md#021115). Expected boundary: Johnny purchased Hellfire with registration card to complete existing MUSHA card gap; no completed resale.

Forbidden inferences: Tyler bought Hellfire as his pickup; Johnny bought another MUSHA; Hellfire was actually thrown away; A resale was completed; Current market price certified.

Result: the composed answer is supported at the stated confidence by the supplied transcript. This is the extraction agent's desk check, not an independent reviewer or an executed retrieval pass.

### 4. Did Johnny buy a whole case of Silly Bandz and did they play it?

Johnny reports buying two sealed Nintendo DS copies, one for himself and one for Tyler. He considered a cheap bulk lot because handing them out would be funny, but does not report buying the case. No actual play is established; Tyler says not until Portland. The initial Scribblenauts comparison is corrected to Angry Birds because the game launches rubber bands. (CQ201 02:29:16–02:32:27.)

Source check: [CQ201 02:29:16](../../../library/episodes/cq-201-sc-1327980511.md#022916); [CQ201 02:30:18](../../../library/episodes/cq-201-sc-1327980511.md#023018); [CQ201 02:31:23](../../../library/episodes/cq-201-sc-1327980511.md#023123); [CQ201 02:32:27](../../../library/episodes/cq-201-sc-1327980511.md#023227). Expected boundary: Two sealed DS copies purchased; bulk lot considered only; no play; corrected Angry Birds comparison.

Forbidden inferences: Purchased fifty copies; Bulk lot acquired; Both hosts played it; Scribblenauts comparison was the final account; Tyler already received the gift.

Result: the composed answer is supported at the stated confidence by the supplied transcript. This is the extraction agent's desk check, not an independent reviewer or an executed retrieval pass.

### 5. Which Wario Land II version does Tyler favor for collecting versus playing?

Tyler says he would rather own the original Game Boy version but would probably rather play the Game Boy Color version. He explains that the older box and original-development context can appeal more to him as a collector. He frames cross-generation comparisons case by case, not as a rule that older versions are always better games or guaranteed to rise in value. (CQ201 01:59:27–02:01:40.)

Source check: [CQ201 01:59:27](../../../library/episodes/cq-201-sc-1327980511.md#015927); [CQ201 02:00:35](../../../library/episodes/cq-201-sc-1327980511.md#020035); [CQ201 02:01:40](../../../library/episodes/cq-201-sc-1327980511.md#020140). Expected boundary: Original Game Boy for collection, Game Boy Color for playing; case-by-case preference, not a transaction.

Forbidden inferences: Tyler purchased either version in this episode; Older release always plays better; Guaranteed future appreciation.

Result: the composed answer is supported at the stated confidence by the supplied transcript. This is the extraction agent's desk check, not an independent reviewer or an executed retrieval pass.

### 6. Did Johnny finish his Last of Us Part II New Game Plus replay?

No completion is reported. Johnny says he reached the final compound near the shore but could not climb a train-car ladder: his character became stuck in an animation pose. Reloading did not fix it, and his earlier save was about nine hours back. He stopped without the desired New Game Plus completion or trophy. His report does not establish a universal bug or a working fix. (CQ201 02:13:19–02:18:36.)

Source check: [CQ201 02:13:19](../../../library/episodes/cq-201-sc-1327980511.md#021319); [CQ201 02:14:22](../../../library/episodes/cq-201-sc-1327980511.md#021422); [CQ201 02:15:28](../../../library/episodes/cq-201-sc-1327980511.md#021528); [CQ201 02:16:29](../../../library/episodes/cq-201-sc-1327980511.md#021629); [CQ201 02:17:33](../../../library/episodes/cq-201-sc-1327980511.md#021733); [CQ201 02:18:36](../../../library/episodes/cq-201-sc-1327980511.md#021836). Expected boundary: Near-end New Game Plus ladder bug stopped Johnny; not completed, no fix proven.

Forbidden inferences: Finished New Game Plus; Earned the desired trophy; Confirmed patch fixes the bug; All players encounter this bug; This is Johnny's first-ever playthrough.

Result: the composed answer is supported at the stated confidence by the supplied transcript. This is the extraction agent's desk check, not an independent reviewer or an executed retrieval pass.

## A6 — Practical pre-show brief

**Episode frame:** “What should one of every NES game mean?” Open with criteria, not a replacement number. Tyler's proposed US, licensing-neutral, consumer-obtainable, original-lifespan list differs from Johnny's official-channel/childhood-familiarity countermodel. Neither resolves a universal definition. [CQ201 00:25:34](../../../library/episodes/cq-201-sc-1327980511.md#002534), [CQ201 00:33:06](../../../library/episodes/cq-201-sc-1327980511.md#003306), [CQ201 01:40:20](../../../library/episodes/cq-201-sc-1327980511.md#014020).

**Useful callback:** “The list rule met its own counterexample with Sunday Funday.” Cue the Menace Beach exclusion, then reveal Fish Fall and the on-air restoration. This demonstrates why corrected later context must travel with an early quote. [CQ201 00:50:11](../../../library/episodes/cq-201-sc-1327980511.md#005011), [CQ201 01:47:48](../../../library/episodes/cq-201-sc-1327980511.md#014748), [CQ201 01:48:51](../../../library/episodes/cq-201-sc-1327980511.md#014851).

**Host-sensitive contrast:** “You can think gold NWC is cooler without saying it belongs in the set.” Attribute Johnny's preference separately from Tyler's inclusion rule; do not bring Stefan in as a current witness. [CQ201 01:55:11](../../../library/episodes/cq-201-sc-1327980511.md#015511), [CQ201 01:56:19](../../../library/episodes/cq-201-sc-1327980511.md#015619).

**Collecting-detail callback:** Johnny's Hellfire saved search was about the registration card missing from MUSHA, not a new enthusiasm for disposing of games. Follow with Silly Bandz' rubber-band pack-in: the collectible packaging can be the hook. [CQ201 02:10:14](../../../library/episodes/cq-201-sc-1327980511.md#021018), [CQ201 02:31:23](../../../library/episodes/cq-201-sc-1327980511.md#023123).

**Playing callback:** Tyler repeats Ninja Gaiden for comfort, not to improve a speedrun; Johnny's Last of Us II run stalls at a ladder. Keep the latter as his dated experience, not current technical advice. [CQ201 02:13:19](../../../library/episodes/cq-201-sc-1327980511.md#021319), [CQ201 02:26:03](../../../library/episodes/cq-201-sc-1327980511.md#022603).

**Possible open loops:** Joe guest idea; “baller in 2008” NES collectibles episode; then-future Portland meetup. These are proposals or historical plans, not confirmed upcoming events. [CQ201 01:16:48](../../../library/episodes/cq-201-sc-1327980511.md#011648), [CQ201 01:37:08](../../../library/episodes/cq-201-sc-1327980511.md#013708), [CQ201 02:32:27](../../../library/episodes/cq-201-sc-1327980511.md#023227).

**Do not say:** “The true NES set is 755”; “Johnny wants the multicart set”; “Ms. Pac-Man ports are proven identical”; “Stefan is getting a gold NWC”; “Johnny bought fifty Silly Bandz”; or “CQ201 identifies the best SMB3 edition.” SMB3 is only an embedded-minigame counting analogy here. [CQ201 01:21:08](../../../library/episodes/cq-201-sc-1327980511.md#012108), [CQ201 01:22:13](../../../library/episodes/cq-201-sc-1327980511.md#012213), [CQ201 01:39:14](../../../library/episodes/cq-201-sc-1327980511.md#013914), [CQ201 01:50:55](../../../library/episodes/cq-201-sc-1327980511.md#015055).

Desk-usefulness result: the artifacts can support six concrete source-bound answers, correction-aware callbacks, variant/action distinctions and explicit abstentions. The longest topic remains a policy debate rather than a deterministic game list. The brief avoids current valuations, unverified hardware claims and an invented final checklist. This is a document-level rehearsal by the extraction agent, not a timed/live cohost session. Root must still prove retrieval returns the right evidence and verify its independent sample before accepting the episode.

## Verification and remaining work

Local source checks passed: 1018 quote validations across game occurrences, lore, actions, spans and accounting excerpts; source SHA-256 matches; all 264 span IDs are unique and source bounds ordered; all 179 references exist. Authored JSON is UTF-8 via apply_patch. These are structural/source-literal checks, not proof that every semantic interpretation is correct.

Still separate and required: root's A7 database/retrieval/regression integration, independent frozen-window omission comparison and A8 episode/batch acceptance ledger. Any mismatches found there require durable repair in these artifacts and regression coverage. Audio verification, external licensing/history research, precise utterance timing and live-cohost evaluation have not been performed and are not implicitly promised by this source audit.


## Final bounded Stadium Events prominence recheck

Root's default meaningful metric (substantial plus supporting) initially gave Stadium Events 892 seconds, despite only 129 substantial seconds. A fresh primary-source recheck found role inflation: isolated benchmarks were receiving entire supporting caption windows. The following are now passing mentions, retained for retrieval but excluded from meaningful prominence:

- 00:19:15–00:20:18: one rarity benchmark in video-signal terminology discussion.
- 01:01:56–01:04:02: a short distribution contrast straddling a caption boundary amid Cheetahmen II/lifespan/Action 52 discussion.
- 01:36:04–01:37:08: one same-game analogy inside Athletic World naming.
- 01:40:20–01:41:21: brief choose-one shorthand in the general countermodel setup.
- 01:56:19–01:58:26: closing desirability and controversial-game shorthand, not developed Stadium Events discussion.

The developed backstory/gameplay comparison at 00:59:46–01:01:56, destruction report at 01:34:59–01:36:04 and bundle-exclusion example at 01:42:26–01:44:33 remain supporting; the main 01:23:16–01:25:25 variant debate remains substantial. All are still coarse whole-window proxies. [Source: Stadium Events comparison](../../../library/episodes/cq-201-sc-1327980511.md#005946), [manufacturing and Athletic World](../../../library/episodes/cq-201-sc-1327980511.md#013459), [countermodel](../../../library/episodes/cq-201-sc-1327980511.md#014020), [closing comparisons](../../../library/episodes/cq-201-sc-1327980511.md#015619).

Durable repair: base occurrence roles/evidence and annotation roles/bounds were changed together; two mixed-role spans were split and three affected section-accounting references updated. Stadium Events now has nine spans, 451 meaningful seconds (7:31), of which 129 are substantial. The episode has 264 spans, not 262. The substantial-only leaders above do not change. This repair should be included in root's final rebuild and ranking regression; it is not a claim of a full independent prominence audit of all games.

After repair, 1,018 exact-source quote checks passed, all 264 span IDs are unique, and all section-accounting references resolve. JSON parsing and scoped diff whitespace checks passed.
