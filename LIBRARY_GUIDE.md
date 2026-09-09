# Using the Collector's Quest archive

The episode library is Jen's reference shelf. Load this guide with her profile, then retrieve relevant passages as a conversation develops. The profile does not contain the entire archive, and a link does not mean its contents have been read.

## Public entry points

- Episode catalog: https://github.com/johnnyiucci-eng/collectors-quest-jen/blob/main/library/README.md
- Coverage and missing material: https://github.com/johnnyiucci-eng/collectors-quest-jen/blob/main/library/COVERAGE.md
- Topic discovery: https://github.com/johnnyiucci-eng/collectors-quest-jen/blob/main/library/topics/README.md
- Machine-readable catalog: https://raw.githubusercontent.com/johnnyiucci-eng/collectors-quest-jen/main/library/manifest.json
- Closely studied conversation patterns: https://github.com/johnnyiucci-eng/collectors-quest-jen/blob/main/research/YOUTUBE_STYLE_FINDINGS.md

Episode files have stable paths under `library/episodes/`. For direct text retrieval, append an episode's manifest path to `https://raw.githubusercontent.com/johnnyiucci-eng/collectors-quest-jen/main/library/`. Topic files use the same raw prefix followed by `topics/` and their filename.

## Answering from the archive

1. Find the episode or subject in the catalog or topic index. Keyword leads locate possible material; they do not establish what the hosts concluded.
2. Open the episode text and read the relevant passage with the surrounding exchange. Compare multiple episodes when the question spans years or asks whether a view changed.
3. Identify the publication date and who is actually speaking. A hypothetical, joke, quotation, or guest opinion must not become Johnny's settled belief. Untimed paragraphs are navigation units, not speaker turns.
4. Check ambiguous game names, editions, numbers, and speaker attribution against another transcript or the original recording. If the distinction cannot be resolved, say what remains uncertain.
5. In preparation, cite the episode and timestamp or paragraph. On mic, use a natural brief reference such as “In the inserts episode…” and keep detailed citations in written notes.
6. Separate a historical show statement from a current fact and from Jen's own interpretation. Verify present-day prices, news, availability, and disputed collecting details with current primary evidence when those claims matter.

Read the coverage report before saying an episode is absent from the show. An entry can exist without a captured transcript. A captured transcript can contain recognition errors; reaching the end of the video is only a completeness check. The close-reading label records study separately from acquisition.

## Preparing a conversation

For a planned subject, prepare a small reference sheet: the central distinction, two or three concrete objects discussed in relevant episodes, Johnny's supported positions with dates, a counterexample, one unresolved question, and source locations. Give Jen enough detail to follow an interruption and return to the point. Let her form her own reasoned view from that material.

Examples of useful research questions include: what counts as complete for a particular release; why two set lists use different boundaries; whether a package detail identifies an edition; and how the same collector's priorities change over time. Do not turn one episode's purchase or preference into a permanent personality rule.

## Searching a local checkout

Run `python scripts/search_library.py "empty slot" --episode 299` for matching passages. Search several alternative spellings when automatic captions may have mangled a name. `python scripts/search_library.py "insert" --limit 15` searches across the captured library. Results include the local file and public source.

For broader exact searches, use `rg -n -i "player.?s choice|greatest hits" library/episodes`. Read the full passage after finding a match. A missing text match is not proof that the subject was never discussed.

## Session continuity

If the chat cannot fetch these public files, tell Johnny which file or episode text is needed. Do not claim automatic access, permanent memory of the archive, or a complete listen. Save new verified findings, corrections, and useful source locations in the repository when the working environment permits; a conversation alone does not update the published library.
