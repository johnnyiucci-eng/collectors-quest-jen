# CQ205 independent full-source peer review

Reviewer: early-episode lane, not CQ205's extractor. Read the complete [canonical transcript](../../../library/episodes/cq-205-sc-1360671826.md) **174/174 timestamp windows**, in seven ordered chunks, before opening the extraction. Range: 00:00:01 through 03:03:55/END. Source SHA256: `de30cbc3b2f0c8e3691dfbad2f4aafb9339b80bb861e12d7c0a82cc986976842`. No audio, external catalogs, market verification or network calls.

Then read all **329 span summaries**, **72 action rows**, **60 lore summaries**, all **12 full composed answers**, and the written brief/audit. This is an independent primary-source semantic peer pass, not a second audio transcription or a claim of perfect global entity recall. No CQ205 extractor artifact was edited by this reviewer.

Pre-repair snapshots inspected: record SHA256 `b12ec11c0c974874c6dd00f71a5a2c2bfc6476f8ecb32afa20412eaf40958dc1`; annotation SHA256 `b20a90beaaf8cc4062e239b1b44540b4f52b39da0ded22562a66d5c1be35e389`. Counts and failures below refer to these inputs, not an assumed repaired build.

## Findings requiring repair

### 1. Composite subjects hide known actors from actions queries

`cq205-action-015` uses subject **Stefan and April**. The source says “that and Rescue Rangers were the two games me and my sister played a bunch,” following Stefan's named Jaws/April account. Use canonical Stefan with `co_subjects: ["April"]`, or equivalent separate rows. [01:05:36–01:06:41 source](../../../library/episodes/cq-205-sc-1360671826.md#010641).

`cq205-action-032` uses **Johnny household / Carly**. Source: “those Carly collected Carly really liked Skylanders she was she was playing the game and so I own a … ton of Skylanders.” Keep Johnny as canonical owner, Carly as source-qualified co-subject/collector, and the household explanation in prose. Carly's played state is already separately captured in action033. [02:13:40 source](../../../library/episodes/cq-205-sc-1360671826.md#021340).

Actual read-only reproduction used the production `LoreStore.actions` method with the annotation claims as its in-memory items, avoiding a shared database rebuild. For the affected rows, `actions("Stefan","played")`, `actions("April","played")`, `actions("Johnny","owned")`, and `actions("Carly","owned")` each returned **zero matches**. This is **0/4 expected actor matches** before repair, not merely a style issue. The implementation does exact canonical subject/co-subject matching. [Query implementation](../../../scripts/lore_store.py).

### 2. Two explicit play reports are absent from action rows

At **00:52:51**, a host says “the only version I've played is the original Ghostbusters game,” continuing into the NES/Atari/Master System design debate. The existing action list has wants for the 2600 sequel but **no played Ghostbusters claim**. Add a source-qualified original-design/platform-unspecified played row; do not infer the speaker played every listed port. Exact speaker can remain unknown if the undiarized turn is insufficient. [Source](../../../library/episodes/cq-205-sc-1360671826.md#005251).

At **02:41:33**, first-person Last of Us II experience explains how detailed vistas “would take me out of the game” and prompted thoughts about production expense. Existing game/lore mapping captures the opinion but **no Last of Us II played action** exists. Add a contextual/unknown-subject played claim, not a completion or attribution to Johnny's distinct almost-finished remaster. [Source](../../../library/episodes/cq-205-sc-1360671826.md#024133).

These are **2/2 omitted action representations in the identified omission probes**, not a measured overall action-recall rate. All 72 stored rows were reviewed; absence is not cured by having the title in the general game index.

### 3. One explicit patron-name reference is missing

At **03:00:42**, the tail includes “the actual Shinobi just Sonic the kid.” Adjacent Shinobi and other patron allusions are indexed, but **Sonic has no game/reference bucket or span** in the inspected 196-reference map. Add a raw, series-level joke/patron reference, with no exact installment or actual gameplay inferred. [Source](../../../library/episodes/cq-205-sc-1360671826.md#030042).

The source-first notes retained ten explicit-title/franchise tail buckets before opening records: Pocky & Rocky with Becky, Shinobi, Sonic, Mad Dog McCree, Ghosts 'n Goblins, Mega Man, Zelda, Super Mario 64, Donkey Kong, Double Dragon. **9/10** have mapped records/spans; Sonic is the miss. This narrow denominator excludes inferred catchphrases/characters and is not a global 90% recall score. The full 174-window read revealed this tail gap; it does not justify claiming all 196 stored identities form a complete independent denominator.

### 4. Vampire Hunter D receives a movie-only supporting window

`cq205-span-125-2`, **02:01:04–02:02:07**, is marked SUPPORTING_EXAMPLE. After the generic “double check … prices change wildly” transition, the window is about anime films/generational gateways: “Akira ninja scroll … Vampire Hunter D … Ghost in the Shell” contrasted with “Naruto and Pokemon.” It gives no new material game-specific discussion until the next window's pricing/cover comparison.

Downgrade this window to PASSING_MENTION (or otherwise explicitly film-only), retaining the title lookup. This removes **63 seconds of coarse meaningful game credit** without changing the top three. Actual game-price/cover discussion at02:02:07 remains meaningful. [Source](../../../library/episodes/cq-205-sc-1360671826.md#020104).

## Ranking and type audit

Recomputed the union from all inspected spans, excluding non-video-game types. Current qualified leaders reproduce the extractor's table:

| Platform-specific record | Combined coarse coverage | Substantial | Supporting |
|---|---:|---:|---:|
| Ghostbusters — Atari 2600 | 445s | 125s | 320s |
| Arachnophobia — computer versions | 390s | 390s | 0s |
| Mary Shelley's Frankenstein — Genesis | 326s | 259s | 67s |
| Addams Family Values — SNES/Genesis | 322s | 189s | 133s |
| Ghostbusters — NES | 317s | 0s | 317s |

The top three's topic boundaries are defensible at the supplied caption-window resolution. Arachnophobia includes game packaging/novel-bundle distinctions rather than only gameplay. Its all-substantial classification is generous: a later calibration pass could split packaging comparisons into supporting roles, but these are still material collecting details, so I do not call the entire interval an omission or invalid boundary. Frankenstein includes a real physical sticker check and price deliberation; the exclusive→special and printed→sticker corrections are preserved. Ghostbusters has a sustained design/mechanics dispute, not just name frequency. [Ghostbusters](../../../library/episodes/cq-205-sc-1360671826.md#005357), [Arachnophobia](../../../library/episodes/cq-205-sc-1360671826.md#012643), [Frankenstein](../../../library/episodes/cq-205-sc-1360671826.md#015114).

Important type controls pass this review: physical Magic and Warhammer products are tabletop; Gremlins print-shop is non-game software; Nightbreed RPG is cancelled; books are books; Addams pinball is physical pinball; Skylanders/Infinity figures are toys; Wata/VGA cases are packaging; Star Fox banner is promotional; Mario trailer/live-action movie are films; Nintendo Land here is an attraction; counselor VHS is archival media; ZombiU console box is hardware. None improperly outranks individual games.

Gremlins/Batman Returns/Blair Witch family comparisons are kept apart from specific designs. Atari Alien versus computer Alien, the multiple Gremlins 2 designs, Ghostbusters originals/sequels, and Jaws computer groups preserve source distinctions/uncertainty. Film-only Beetlejuice/Addams/Mario tangents are not generally inherited by game duration. The Vampire Hunter D window above is the identified exception.

The physical terminal window remains END; no fabricated03:04:50 final speech boundary is used. Coarse caption coverage is not stopwatch talk time. Combined and substantial-only ordering are different questions, and ports must not be silently summed as independent franchises.

## Roster, speakers and action semantics

Opening explicitly supplies Tyler, Johnny and Stefan; Stefan's exit at02:56:33 is preserved. Source01:04:31 retrospectively identifies Stefan as the opening dog-injury storyteller, so any later biography extraction should use that bridge rather than assuming Johnny. Current lore does not falsely assign that anecdote.

April is Stefan's sister, Carly a third-party Skylanders player/collector, Steve the Star Fox-banner auction winner, and Kelsey the helper with the counselor archive. Unknown turns remain unknown, including the Poltergeist purchase speaker and two sealed Infinity owners. No source evidence was found requiring a forced new attribution.

The central purchase/nonpurchase distinctions pass: Johnny buys the big-box Blair Witch trilogy and Quarry; Tyler wants the trilogy; the free Quarry exchange is explicitly fictional; novel-sticker Arachnophobia is wanted; missing Frankenstein variants not newly bought; Last of Us almost done is not finished; Jaws childhood failure is not a new victory; Divinity300hours is a target; Space Quest purchase does not imply affection; Maniac Mansion lust wording is rejected. The two missing played rows and composite-subject retrieval failures above remain real A4 gaps despite these successes.

## Twelve actual composed answers

All twelve prose answers were read after the full primary source, not inferred from keyword hits. This peer pass used **47 grouped material checks**, listed here to define the denominator; **47/47 supported, 12/12 answers source-supported**. This is a source-adjudicated answer review, not an end-to-end query test or live delivery score.

| Case | Grouped checks | Result |
|---|---:|---|
| Frankenstein stickers | 5: wording, inner/outer placement, no-text form, existing/missing copies, rejected price/no purchase | 5/5 |
| Quarry free-copy story | 4: fictional exchange, Johnny purchase, ~40minutes, future longer session | 4/4 |
| Blair Witch buyers | 4: Johnny's three volumes, big-box CIB, Tyler wants, not DVD/outer-box substitution | 4/4 |
| Space Quest purchase | 5: first-print grid box, condition/inserts, only first played, late dead end, collecting vs liking | 5/5 |
| Accomplishments | 3: Tyler sets, Johnny community, Stefan museum | 3/3 |
| Ghostbusters wants/labels | 4: both want, tentative lastness, picture/blue distinction, uncertain chronology | 4/4 |
| Arachnophobia bundle | 4: wanted sticker/novel, current copy different, sleeves/formats/inserts, not every component assumed | 4/4 |
| Jaws history | 3: Stefan/April, failed stab, possible retry not completion | 3/3 |
| QVC/Gaia | 4: acquired/digitized archive, earlier window, not T-shirt, exact date absent | 4/4 |
| Gremlins map | 4: two originals, multiple sequel designs, print-shop exclusion, unverified complete counts | 4/4 |
| Maniac Mansion | 3: Apple copy acquired, lust rejected, other wants not purchases | 3/3 |
| Magic randomness | 4: randomized999product, older complete/direct alternatives, different backs, nonguaranteed outcomes | 4/4 |

Exact evidence windows are retained with each [actual answer case](205-annotations.json). I found no material prose answer requiring revision. Corrections and forbidden-inference controls are effective: no release date invented for Gaia, no guarantee of random card pulls, no verified licensing-afterthought history for Blair Witch, no false free-copy gift. The actor-filter failures show why prose checks alone are not enough.

## Practical brief review and disposition

The [extractor's brief](205-audit.md) is useful: it leads with tangible packaging distinctions, separates each host's collecting priorities, retains the Ghostbusters disagreement instead of flattening it, and warns about buyer/state confusion. It cites real episode examples and does not pretend to have rehearsed live delivery.

Two useful editorial additions, clearly proposals rather than history: ask how a source can establish a pre-release sales window without supplying an exact calendar date; contrast the live-auction communal experience with Stefan's future concern about phone-mediated bidding. Do not convert his prior Game On experience into an observed Portland outcome.

**Disposition:** answers and main ranking/type design pass this peer review, but A2/A4 and one role need the repairs above before unconditional acceptance. Owner/root must rebuild, rerun actor queries and retain these pre-repair metrics. This reviewer changed only this Markdown report. Research skill guided the primary-source-first read and durable cited findings; no live rehearsal or external fact verification is claimed.

## Owner repair verification — read-only follow-through

After the owner reported repairs, this reviewer inspected the current inputs and reran the actual LoreStore.actions method against the updated claims. All **4/4** canonical actor probes now return the correct affected row: Stefan/April → action015; Johnny/Carly → action032. The pre-repair 0/4 result above remains part of the record.

New action073 captures original Ghostbusters play with unknown actor/platform, and action074 captures Last of Us II play with unknown actor; both use the exact source windows and avoid false completion or blanket port-play claims. Sonic g197/span197-1 is a series-level patron joke with no meaningful game duration, bringing the explicit-title tail check to **10/10 after repair** (9/10 before). Vampire Hunter D span125-2 is now passing, removing the identified 63 seconds of movie inheritance. All six reported repairs are present in durable owner artifacts.

The updated record has **197 references, 330 spans and 74 actions**. Independent literal traversal of the actual current record plus annotation verifies **1,304/1,304 quoted evidence objects**, across the unchanged 174-window source. No extractor artifact was edited by this reviewer. Root's persistent rebuild/regressions and final A7/A8 acceptance remain separate; this verifies repaired inputs and action-method behavior, not a claimed full integrated database acceptance.
