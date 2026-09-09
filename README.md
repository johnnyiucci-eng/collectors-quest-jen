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

## Files

| File | Purpose |
| --- | --- |
| [Cohost profile](persona/DEFAULT_JEN.md) | Identity, modes, opening, turn taking, and evidence rules |
| [Conversation style](style/CONVERSATION_STYLE.md) | Original handoff's performance notes |
| [Episode 001](episodes/001-five-ways-ai-can-help-you-collect/EPISODE.md) | Five Ways AI Can Help You Collect: developed material and open fifth tip |
| [Transcript analysis plan](research/TRANSCRIPT_ANALYSIS_PLAN.md) | Future study of the show's conversational mechanics |
| [Single-file chat bundle](JEN_START_HERE.md) | Generated profile and Episode 001 for loading into a chat |
| [Handoff provenance](SOURCE_NOTES.md) | What came from the original handoff and what was added |

## Current development status

The September 9, 2026 handoff supplies the show position and live rehearsal rules. Episode 001 retains its original status: Tip 1, Learn AI's Love Language, leads; Tip 2, Make a Better Brain, is approved; Tip 3, Use Photos to Hunt Variants, is approved for continued development; Tip 4, Build a Buying Priority List, is approved and substantially developed. The fifth tip is still open.

The expanded profile adds explicit casual, preparation, and recording modes so Jen can be a conversation partner outside a recording. These implementation defaults are ready to rehearse, not evidence of additional user-approved performance testing. No transcripts have been analyzed yet.

## Updating Jen

Edit the profile or episode source files, then run `python scripts/build_chat_bundle.py` to refresh the single-file bundle. Run `python scripts/build_chat_bundle.py --check` to check that it matches the sources. Commit and push the source changes and bundle together. Load the updated bundle into the chat where you want to use it.

Keep reusable required behavior in the profile and episode content in the episode file. OpenAI's [personalization documentation](https://learn.chatgpt.com/docs/personalize) distinguishes persistent instructions from memories; this repository keeps Jen's required behavior in an explicit document.
