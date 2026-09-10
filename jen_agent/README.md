# Run the local Jen agent

This is the agent core for the existing Default Jen personality, with local archive search, private conversation history, and explicit saved notes. It uses the current profile and handoff work directly. It does not replace your existing ChatGPT conversation or import unseen parts of that thread.

## Start on your PC

Python 3.11 or newer with SQLite FTS5 support is required. No Python packages need installing. Open PowerShell in this repository and run:

```powershell
.\Start-Jen.ps1
```

If an API key is not already configured, the launcher asks for it using hidden input. It passes the key to the Python process and removes the prompted key from its environment when Jen closes. The key is never written into the repository. API usage is billed through your API account. Model availability depends on that account. The default is `gpt-5.5`; set `JEN_MODEL` or pass `--model` to select another Responses-compatible model with function calling.

A key is required for live model replies. These commands work entirely offline without one:

```powershell
python -m jen_agent --check
python -m jen_agent --search "empty slot" --episode 299
```

The first run builds a local search index of all 318 transcript entries. Subsequent starts verify source hashes and rebuild only when the source content changes. Search uses stemmed keywords and ranked passages; it is not semantic search. The model can choose alternate searches and read neighboring passages. Automatic transcript errors still require source checking.

## Preserve personality and continuity

The agent reads the existing persona, fictional status notes, original conversation-style notes, accepted corrections, show context, collecting context, library guide, and active episode on every turn. It has no tool that writes those files. `/profile` displays source hashes; each completed turn records its profile fingerprint locally. Human-approved repository edits remain the way to change canonical Jen. Preserving instructions does not guarantee identical delivery across models; rehearse against [the existing scenarios](../style/REHEARSAL.md).

Your normal session is `johnny-main`; restarting resumes its recent context. `/new` creates a separate session and prints its name. Resume one with `python -m jen_agent --session NAME`. The model receives up to 20 recent completed turns within a 24,000-character history budget. Older history remains on disk until cleared but is not automatically recalled or summarized.

| Command | Effect |
| --- | --- |
| `/remember TEXT` | Saves the exact note for this session, with explicit approval provenance. Keep it relevant to CQ. |
| `/notes` | Lists every saved note in this session. |
| `/forget ID` | Removes that note. Any original chat discussion remains in history until cleared. |
| `/clear-history` | Deletes this session's stored chat turns. Saved notes remain independently removable. |
| `/new` | Starts a separate session with no inherited history or notes. |
| `/quit` | Closes Jen. |

Saved notes are limited to 30 per session and 1,200 characters each. All saved notes for the current scope are supplied as reference data. A natural-language request to “remember” cannot write memory; the exact `/remember` command is required. This keeps conversations from silently becoming shared persona changes or public episode approvals.

## Private state and sharing

The default private directory is `jen-agent-private` beside the repository, outside GitHub. It contains a rebuildable archive index and a conversation database. You can override it with `JEN_DATA_DIR` or `--data-dir`, but paths inside the public repository are rejected. The database is local plaintext protected by the operating-system account, not encrypted storage. Do not publish or casually share it.

Live replies send the profile, your message, bounded recent history, saved notes for that session, and retrieved passages to OpenAI. Requests set `store: false`; this controls Responses storage and is not a promise of zero provider retention. No background loop, telemetry service, live web search, Discord connection, or automatic ChatGPT synchronization is included.

The Python core is reusable by a future Discord or hosted adapter. Every history/note query is scoped by owner and conversation. **The CLI assumes trusted local Johnny access and is not a multi-user authentication service.** A future adapter must authenticate identity, derive authorized scope server-side, serialize turns within each conversation, enforce access/usage limits, and avoid exposing this CLI directly to untrusted network users. Shared memory between ChatGPT and Discord is not implemented.

## Validation and implementation references

```powershell
python -m unittest discover -s tests -v
python -m jen_agent --check
```

Offline tests exercise retrieval, neighboring passages, source invalidation, user/session isolation, explicit memory deletion, preservation of personality sources, tool dispatch and reasoning continuation, bounded requests, and failure handling. They do not establish live model quality or API account access. Run the rehearsal scenarios with Johnny once an API key is available.

The connection uses OpenAI's [Responses function-calling workflow](https://developers.openai.com/api/docs/guides/function-calling), retaining returned reasoning items during tool continuation, and the [Responses storage controls](https://developers.openai.com/api/reference/cli/resources/responses/methods/create). Default model capabilities are documented for [GPT-5.5](https://developers.openai.com/api/docs/models/gpt-5.5). Documentation checked September 9, 2026.
