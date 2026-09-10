# Local agent validation

September 9, 2026. The local core was built against the existing Jen profile and September 9 Discord handoff, without editing those personality sources.

- The real corpus indexed successfully: 318 entries and 30,950 searchable passages.
- Real searches found empty-slot passages in CQ 299, Probotector in CQ 199/201, Tableau in Episode 140 and Side Quest 3, and Tyler references in CQ 300. These are retrieval checks, not claims that every returned passage answers a full research question.
- Twelve offline tests passed for source indexing and updates, neighboring passages, user/session isolation, restart persistence, memory deletion, personality preservation, tool continuation, request limits, and failure handling.
- The PowerShell launcher passed its offline `-Check` path. The portable ChatGPT bundle remains current, and the existing library validator passed.
- No API key was configured, so no live model request was made and no API charges were incurred during this validation. Live response style, latency, model/account access, and end-to-end model tool selection remain untested.

Before adding Discord, connect the API key using the private launcher prompt and run the [rehearsal scenarios](../style/REHEARSAL.md) with Johnny. Confirm that Jen stops after the approved opening, riffs without losing the point, preserves exploratory fiction labels, retrieves a source for a CQ-specific answer, and gives useful pushback. Record any accepted correction in the authoritative profile; do not replace it with a freshly invented personality.
