"""Search episode transcripts and return source-linked passages without dependencies."""

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Words to find together in a passage")
    parser.add_argument("--episode", type=int)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    entries = json.loads((ROOT / "library/manifest.json").read_text(encoding="utf-8"))["entries"]
    terms = re.findall(r"\w+", args.query.casefold())
    if not terms:
        parser.error("query must contain a word")
    results = []
    for entry in entries:
        if args.episode is not None and entry["episode_number"] != args.episode:
            continue
        body = (ROOT / "library" / entry["path"]).read_text(encoding="utf-8")
        for section in re.split(r"\n### ", body)[1:]:
            heading, _, passage = section.partition("\n")
            if all(term in passage.casefold() for term in terms):
                results.append({"episode": entry["title"], "date": entry["date"], "location": heading.strip(), "file": entry["path"], "source": entry["primary_transcript_source"], "passage": passage.strip()})
                if len(results) >= args.limit:
                    print(json.dumps(results, ensure_ascii=False, indent=2))
                    return
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
