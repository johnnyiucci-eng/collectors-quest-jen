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
    patterns = [re.compile(r"\b" + re.escape(term) + r"\b", re.I) for term in terms]
    phrase = re.compile(r"\W+".join(re.escape(term) for term in terms), re.I)
    results = []
    for entry in entries:
        if args.episode is not None and entry["episode_number"] != args.episode:
            continue
        body = (ROOT / "library" / entry["path"]).read_text(encoding="utf-8")
        for section in re.split(r"\n### ", body)[1:]:
            heading, _, passage = section.partition("\n")
            if all(pattern.search(passage) for pattern in patterns):
                source = entry["primary_transcript_source"]
                location = heading.strip()
                if "youtube.com/watch?" in source and re.fullmatch(r"\d+:\d{2}:\d{2}", location):
                    hours, minutes, seconds = map(int, location.split(":"))
                    source += f"&t={hours * 3600 + minutes * 60 + seconds}s"
                score = 4 * bool(phrase.search(passage)) + 2 * sum(bool(p.search(entry["title"])) for p in patterns) + sum(min(3, len(p.findall(passage))) for p in patterns)
                results.append({"episode": entry["title"], "date": entry["date"], "location": location, "file": entry["path"], "text_url": "https://raw.githubusercontent.com/johnnyiucci-eng/collectors-quest-jen/main/library/" + entry["path"], "source": source, "passage": passage.strip(), "score": score})
    results.sort(key=lambda result: result["score"], reverse=True)
    for result in results:
        result.pop("score")
    print(json.dumps(results[:args.limit], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
