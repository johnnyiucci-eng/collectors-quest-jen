# Download Jen's knowledge files

[Download the ZIP](https://raw.githubusercontent.com/johnnyiucci-eng/collectors-quest-jen/main/downloads/jen-knowledge.zip), extract it, and follow READ_ME_FIRST.txt. The profile and reference packs are ordinary Markdown files.

Snapshot: 2026-09-09T16:12:12.550069+00:00. **4 archive packs**, **205 captured transcript entries**, **3,920,364 transcript words**. Missing entries remain marked in the packs.

The public episode library remains the authoritative source. These files are a portable snapshot for clients that cannot fetch the public links reliably. Uploading does not automatically apply persona instructions or guarantee complete recall.

| File | o200k_base tokens | cl100k_base tokens |
| --- | ---: | ---: |
| CQ_ARCHIVE_01.md | 1,381,975 | 1,397,237 |
| CQ_ARCHIVE_02.md | 1,322,673 | 1,387,496 |
| CQ_ARCHIVE_03.md | 1,313,645 | 1,374,895 |
| CQ_ARCHIVE_04.md | 624,693 | 650,232 |

Counts use [OpenAI's tiktoken](https://github.com/openai/tiktoken) and leave room below the documented 2-million-token text-file limit. Your chat or workspace's actual acceptance is authoritative. See [OpenAI file limits](https://help.openai.com/en/articles/20001052-library-for-chatgpt) and [instructions versus knowledge](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts).

Rebuild with `python scripts/build_knowledge_export.py` in an environment with `tiktoken` installed, after rebuilding the library and chat bundle.
