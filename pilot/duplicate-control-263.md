# CQ 263 duplicate control

Both uploads remain preserved. Only `sc-1993480675` is an episode in pilot retrieval; `sc-1990205799` is a comparison source, not an additional coverage occurrence.

The caption bodies are not identical. After removing timestamp headings and comparing whitespace-delimited words with Python `difflib.SequenceMatcher(autojunk=False)`, the comparison found 956 non-equal blocks: 163 old-only insertions, 215 canonical-only deletions and 578 replacements. These alignment categories describe the old body relative to the canonical body, not proven edits to the audio.

The canonical transcript has 40,263 words; the old transcript has 39,028. Larger canonical-only sections include discussion of editing work, Jedi Survivor, the controller conversation and the closing. The largest old-only alignment is 37 words in the horror-mask conversation. Other old-only alignments include pickup-segment banter and reactions to disliked episodes.

Decision: retain both transcripts and their separate hashes. Do not discard the old upload or merge all differing text into a canonical quotation. Recognition errors, interruptions and alignment shifts can look like unique content. No conclusion that the audio is identical or different is established by this check. Adjudication of all 956 differences remains unfinished.

The old source's original `comparison_pending` state is retained until that adjudication is complete. This report records the comparison already performed, not a successful deduplication acceptance gate.
