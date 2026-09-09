"""Validate generated archive integrity and public-source boundaries."""

import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "library"


def main():
    manifest = json.loads((LIBRARY / "manifest.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    errors = []
    keys, paths = set(), set()
    available, words = 0, 0
    for entry in entries:
        label = entry["title"]
        if entry["key"] in keys or entry["path"] in paths:
            errors.append(f"Duplicate source key or page: {label}")
        keys.add(entry["key"])
        paths.add(entry["path"])
        page = (LIBRARY / entry["path"]).resolve()
        if not page.is_relative_to(LIBRARY.resolve()) or not page.is_file():
            errors.append(f"Missing or out-of-library page: {label}")
            continue
        content = page.read_text(encoding="utf-8")
        if not content.startswith("# " + label + "\n"):
            errors.append(f"Page title mismatch: {label}")
        if urlparse(entry["source_url"]).hostname != "soundcloud.com":
            errors.append(f"Unexpected publisher domain: {label}")
        if entry["transcript_status"] == "available":
            available += 1
            words += entry["transcript_words"]
            blocks = re.split(r"\n### [^\n]+\n\n", content)[1:]
            actual_words = sum(len(block.split()) for block in blocks)
            if actual_words != entry["transcript_words"] or actual_words < 1:
                errors.append(f"Transcript word count mismatch or implausibly short text: {label}")
            if not entry["transcript_sources"]:
                errors.append(f"Transcript lacks provenance: {label}")
        elif "No usable transcript has been ingested" not in content:
            errors.append(f"Missing-source page fails to disclose gap: {label}")
        if re.search(r"https?://[^\s)<>]*(?:airtableusercontent|dl\.airtable|airtable-attachments)", content):
            errors.append(f"Temporary attachment URL in public page: {label}")
    coverage = manifest["coverage"]
    if (available, words, len(entries) - available) != (coverage["transcripts_available"], coverage["transcript_words"], coverage["transcripts_missing"]):
        errors.append("Manifest coverage totals disagree with entries")
    actual_paths = {"episodes/" + p.name for p in (LIBRARY / "episodes").glob("*.md")}
    if actual_paths != paths:
        errors.append(f"Unreferenced/missing generated pages: {sorted(actual_paths ^ paths)}")
    # Check relative Markdown links throughout the repository; ignore fenced examples.
    for file in ROOT.rglob("*.md"):
        if ".git" in file.parts:
            continue
        content = re.sub(r"```.*?```", "", file.read_text(encoding="utf-8"), flags=re.S)
        for target in re.findall(r"\]\(([^)\s]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            destination = (file.parent / target.split("#")[0]).resolve()
            if not destination.exists():
                errors.append(f"Broken local link in {file.relative_to(ROOT)}: {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(entries)} source entries, {available} transcript pages, {words:,} words, provenance and local links.")


if __name__ == "__main__":
    main()
