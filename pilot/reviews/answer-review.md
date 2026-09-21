# Composed-answer development review — 2026-09-12

Nineteen actual answers, spanning every pilot episode, were checked against full source windows retrieved from the persistent database. The ten coordinator answers are in [answer-cases.json](../answer-cases.json); nine additional answers and their forbidden inferences are in the CQ248/259 and CQ299 companion task cases. `evaluate_lore_answers.py` reproduces the evidence bundles in `pilot/generated/answer-evidence.json`.

## What was measured

- Integration: all explicitly required windows must be present in the returned context, not merely a relevant title hit.
- Manual answer review: the complete answer must preserve supported subject, object, action, qualifications and source limits; any material unsupported claim or listed forbidden inference fails the answer.
- Final results: **19/19 integration checks; 19/19 manually reviewed, appropriately qualified answers**, with no identified forbidden inference in those answers. This is same-team, source-adjudicated development evaluation, not automated truth scoring or held-out accuracy.

| Episode | Answer cases reviewed | Key qualification checked |
| --- | ---: | --- |
| 6 | 1 | Box/cellophane is not factory-sealed; test-device identity uncertain |
| 7 | 1 | Kat's spouse John is not Johnny; sealed Fallout not played; no Tyler |
| 146 | 1 | Bleakness is not a shared negative verdict; Stefan did not review it |
| 200 | 1 | Played 1978 edition distinct from purchased 1982 edition |
| 222 | 1 | Xbox/PS5 packaging comparison; no claim about PC or literal caption PS3 |
| 248 | 3 | Specific refund; original soundtrack, not Origins; catalog purchase, not games |
| 259 | 3 | Regretted purchase versus ownership; withdrawn Poltergeist buy; Stone Prophet not played |
| 263 | 1 | Rusty purchased but still awaiting arrival |
| 299 | 3 | Matte Mario ownership; unresolved auction; one Dracula bundle, not three purchases |
| 300 | 4 | Blasty music versus gameplay; Witchaven pending; reverse-floppy correction; Manhole not owned |

## Failures retained, not erased

Initial integration was 15/19. CQ6's later cartridge inspection and CQ146's qualification were missed by raw lexical context selection; Witchaven's caption spelling also hid its purchase window. CQ263's expected timestamp contained a one-second transcription error in the test itself (02:56:20 corrected to the actual heading 02:56:21). These were three retrieval/context gaps and one invalid test expectation, not four incorrect host answers.

Repair: combine full-window lexical retrieval with structured aliases, quoted record evidence, reviewed return spans and neighboring windows. Required evidence now includes CQ146's actual pacing/length passages and CQ222's explicit PS5 comparison, not just introductory mentions. The older Beneath Apple Manor regression now uses occurrence group 1: group 0 became the earlier reference when the complete occurrence list was restored. No answer target was silently weakened to obtain a pass.

This retrieval method returns an evidence bundle for adjudication. It does not automatically write or certify a live answer, and selected cases are not a guarantee about unseen questions. Short extracts still need context; timestamps are caption headings, not precise utterance boundaries. Every future episode requires fresh complete-answer cases, including negative/action/attribution pitfalls, under A5.
