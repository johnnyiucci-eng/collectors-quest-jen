# Collector's Quest — Default Jen

Default Jen is Johnny's AI cohost for **Collector's Quest**: collector-first conversation, informed pushback, dry humor, and room for Johnny to lead. This public repository holds her profile and episode preparation material.

## Start talking to Jen

Open [JEN_START_HERE.md](JEN_START_HERE.md) for the complete profile and current episode in one file. Copy its contents into a new chat, or give a chat with web access this prompt:

```text
Read this full cohost profile and episode context:
https://raw.githubusercontent.com/johnnyiucci-eng/collectors-quest-jen/main/JEN_START_HERE.md

Use it as your Default Jen cohost profile. I'm Johnny. Start in casual conversation and wait for me to cue a recording. If you cannot retrieve the file, tell me so I can paste it; do not pretend you read it.
```

To rehearse the introduction, say “Jen, let's rehearse the opening.” To work on the episode, say “Jen, off mic—let's work on episode one.”

Public links let a client request the files without GitHub authentication. Whether a particular chat can fetch them depends on its available tools. Pasting the bundle gives it the content directly. This repository publishes the profile; it does not itself create a custom GPT, select a voice, or automatically synchronize future conversations.

For direct file loading, use the [downloadable knowledge package](downloads/README.md). It contains the profile and the captured archive split into bounded Markdown files, with source links and coverage information. Extract the ZIP before loading the files into your chat or supported knowledge workspace.

## Files

| File | Purpose |
| --- | --- |
| [Cohost profile](persona/DEFAULT_JEN.md) | Identity, modes, opening, turn taking, and evidence rules |
| [Fiction and conversational bits](persona/FICTION_AND_BITS.md) | Character direction, exploratory details, and contextual humor |
| [Accepted corrections](style/CORRECTIONS.md) | Show-relevant corrections from Johnny's ongoing Jen conversation handoff |
| [Discord behavior](discord/BEHAVIOR.md) | Text-bot specification, identity, retrieval, and private conversation boundaries |
| [Show context](SHOW_CONTEXT.md) | Dated show context and recurring conversation mechanics |
| [Johnny's collecting context](JOHNNY_COLLECTING_CONTEXT.md) | Source-backed experience, goals, and collecting habits for Jen's conversations |
| [Episode library](library/README.md) | Source-linked episode catalog and captured transcripts |
| [Library guide](LIBRARY_GUIDE.md) | How Jen retrieves, compares, and cites past discussions |
| [Coverage report](library/COVERAGE.md) | Missing text, numbering issues, and source-matching gaps |
| [Topic discovery](library/topics/README.md) | Search leads across collecting subjects and platforms |
| [Knowledge download](downloads/README.md) | Portable profile and archive files for direct loading |
| [Conversation style](style/CONVERSATION_STYLE.md) | Original handoff's performance notes |
| [Rehearsal prompts](style/REHEARSAL.md) | Short scenarios for checking the profile in conversation |
| [Episode 001](episodes/001-five-ways-ai-can-help-you-collect/EPISODE.md) | Five Ways AI Can Help You Collect: developed material and open fifth tip |
| [Transcript analysis plan](research/TRANSCRIPT_ANALYSIS_PLAN.md) | Future study of the show's conversational mechanics |
| [YouTube findings](research/YOUTUBE_STYLE_FINDINGS.md) | Twelve-episode study with timestamped evidence and coverage limits |
| [Archive findings](research/ARCHIVE_FINDINGS.md) | Airtable and podcast inventory, transcript close reading, and summary-quality checks |
| [Early archive findings](research/EARLY_ARCHIVE_FINDINGS.md) | Kat and Johnny's convention discussion and its relation to later collecting goals |
| [Show-history milestones](research/SHOW_HISTORY.md) | Source-backed host introductions, formats, and the current transition |
| [Audio transcription provenance](research/AUDIO_INGESTION.md) | SoundCloud-only coverage, local model settings, and quality limits |
| [Single-file chat bundle](JEN_START_HERE.md) | Generated profile and Episode 001 for loading into a chat |
| [Handoff provenance](SOURCE_NOTES.md) | What came from the original handoff and what was added |

## Current development status

The September 9, 2026 handoff supplies the show position and live rehearsal rules. Episode 001 retains its original status: Tip 1, Learn AI's Love Language, leads; Tip 2, Make a Better Brain, is approved; Tip 3, Use Photos to Hunt Variants, is approved for continued development; Tip 4, Build a Buying Priority List, is approved and substantially developed. The fifth tip is still open.

The expanded profile adds explicit casual, preparation, and recording modes so Jen can be a conversation partner outside a recording. A twelve-episode YouTube transcript study and additional Airtable material now inform her approach to hypothetical questions, concrete explanations, shared jokes, collecting boundaries, and uncertainty. These are ready to rehearse; the updated profile has not yet been validated in a live voice session.

## Updating Jen

The supplied Discord handoff has been incorporated into the profile, fictional character notes, corrections log, and active episode state. Its original Word file remains local. The Discord document is a specification; a running bot and automatic synchronization with the existing ChatGPT conversation have not yet been built.

The episode library is built from the publisher's SoundCloud feed, YouTube captions, and transcript attachments in Johnny's Airtable archive. See the library's live coverage counts; acquisition is tracked separately from close reading. These sources overlap, and bonus entries and duplicate uploads mean archive-entry counts differ from numbered-episode counts.

To rebuild from locally retrieved source files, run `python scripts/build_library.py --source-dir ../research-local`. The source directory is outside the public repository. The generated library publishes episode text and public source links, not temporary attachment URLs or account data. Search the resulting text with `python scripts/search_library.py "your search"`.

Edit the profile or episode source files, then run `python scripts/build_chat_bundle.py` to refresh the single-file bundle. Run `python scripts/build_chat_bundle.py --check` to check that it matches the sources. Commit and push the source changes and bundle together. Load the updated bundle into the chat where you want to use it.

Keep reusable required behavior in the profile and episode content in the episode file. OpenAI's [personalization documentation](https://learn.chatgpt.com/docs/personalize) distinguishes persistent instructions from memories; this repository keeps Jen's required behavior in an explicit document.
