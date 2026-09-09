"""Build the portable Jen profile from its authoritative Markdown sources."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "persona/DEFAULT_JEN.md",
    "SHOW_CONTEXT.md",
    "LIBRARY_GUIDE.md",
    "episodes/001-five-ways-ai-can-help-you-collect/EPISODE.md",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sections = [
        "# Default Jen — start here\n\n"
        "Use this document as the cohost profile when Johnny asks you to be Jen. "
        "Read the full profile before responding. Start in casual conversation "
        "unless Johnny cues preparation or recording. The episode section is "
        "reference material, not a script to deliver all at once.\n\n"
        "Generated from the source files listed below; edit those files and "
        "rebuild this bundle to update it."
    ]
    for source in SOURCES:
        sections.append(f"Source: `{source}`\n\n" + (ROOT / source).read_text(encoding="utf-8-sig").strip())
    content = "\n\n---\n\n".join(sections) + "\n"
    destination = ROOT / "JEN_START_HERE.md"
    if args.check:
        if not destination.exists() or destination.read_text(encoding="utf-8") != content:
            raise SystemExit("Chat bundle is missing or stale. Run python scripts/build_chat_bundle.py")
        print("Chat bundle matches all source files.")
    else:
        destination.write_text(content, encoding="utf-8", newline="\n")
        print(f"Built {destination.name}")


if __name__ == "__main__":
    main()
