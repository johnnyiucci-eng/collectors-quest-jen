"""Build a source-linked episode library from local publisher metadata and transcripts.

Raw retrieval files stay outside the repository. This command publishes episode
text and public source links, never browser state or temporary attachment URLs.
"""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from email.utils import parsedate_to_datetime
import hashlib
import html
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
REVIEWED = {142, 146, 176, 204, 222, 236, 248, 252, 254, 271, 281, 288, 299, 300}
TOPICS = {
    "variants-and-completeness": ("Variants and completeness", ["variant", "insert", "complete in box", "cib", "first print", "greatest hits", "packaging", "reissue"]),
    "collecting-goals-and-psychology": ("Collecting goals and psychology", ["collecting goals", "empty slot", "sunk cost", "collecting sets", "full set", "burnout", "fomo", "collection envy"]),
    "prices-and-the-market": ("Prices and the market", ["price", "auction", "market", "graded", "grading", "rarity", "rarities", "wata", "vga"]),
    "research-and-documentation": ("Research and documentation", ["research", "document", "database", "spreadsheet", "catalog", "gamefaqs", "nintendo age", "videogamesage"]),
    "halloween-and-horror": ("Halloween and horror", ["halloween", "horror", "spooky", "castlevania", "resident evil", "elvira"]),
    "nintendo": ("Nintendo", ["nintendo", "nes", "snes", "game boy", "gamecube", "wii", "switch"]),
    "sega": ("Sega", ["sega", "genesis", "mega drive", "saturn", "dreamcast", "master system"]),
    "playstation-and-xbox": ("PlayStation and Xbox", ["playstation", "ps1", "ps2", "ps3", "ps4", "ps5", "psp", "vita", "xbox"]),
    "pc-and-obscure-platforms": ("PC and obscure platforms", ["pc games", "computer games", "big box", "atari", "intellivision", "odyssey", "3do", "neo geo", "turbografx"]),
    "collectibles-beyond-games": ("Collectibles beyond games", ["trading card", "comic", "book collecting", "viewmaster", "view master", "steelbook", "plush", "lenticular", "preorder bonus"]),
    "buying-selling-and-conventions": ("Buying selling and conventions", ["convention", "ebay", "buying", "selling", "shipping", "reproduction", "counterfeit"]),
    "show-history-and-format": ("Show history and format", ["new host", "announcement", "anniversary", "microcast", "sidequest", "editing", "podcast format"]),
}


def text(value):
    return html.unescape(re.sub(r"<[^>]+>", " ", value or "")).strip()


def normalized(value):
    return re.sub(r"[^a-z0-9]+", " ", text(value).lower()).strip()


def episode_number(title):
    legacy = re.match(r"Episode\s+\d+\s*\((\d+)\)", title, re.I)
    if legacy:
        return int(legacy[1])
    main = re.match(r"(?:CQ|Episode|Episide)\s*(\d+)(?:X)?\s*(?:[-:–]|\b)", title, re.I)
    return int(main[1]) if main else None


def stamp(seconds):
    value = int(seconds)
    return f"{value // 3600:02}:{value // 60 % 60:02}:{value % 60:02}"


def read_json(path, default):
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else default


def match_episode(entries, title, source_url=None):
    if source_url:
        same_url = [e for e in entries if e["source_url"].rstrip("/") == source_url.rstrip("/")]
        if len(same_url) == 1:
            return same_url[0]
    same_title = [e for e in entries if normalized(e["title"]) == normalized(title)]
    if len(same_title) == 1:
        return same_title[0]
    number = episode_number(title)
    candidates = [e for e in entries if e["episode_number"] == number] if number else []
    if len(candidates) == 1:
        # A numbered clip must not silently replace the full episode.
        score = SequenceMatcher(None, normalized(candidates[0]["title"]), normalized(title)).ratio()
        return candidates[0] if score >= 0.55 else None
    if candidates:
        scored = sorted(((SequenceMatcher(None, normalized(e["title"]), normalized(title)).ratio(), e) for e in candidates), key=lambda x: x[0], reverse=True)
        if scored[0][0] >= 0.7 and (len(scored) == 1 or scored[0][0] - scored[1][0] > 0.1):
            return scored[0][1]
    return None


def caption_paragraphs(segments):
    groups, current, beginning = [], [], None
    for segment in segments:
        start = float(segment["start"])
        spoken = text(segment["text"]).replace("\n", " ")
        if not spoken:
            continue
        if beginning is None:
            beginning = start
        if current and (start - beginning >= 60 or len(" ".join(current)) > 1800):
            groups.append((beginning, " ".join(current)))
            current, beginning = [], start
        current.append(spoken)
    if current:
        groups.append((beginning, " ".join(current)))
    return groups


def prose_paragraphs(raw):
    words = raw.split()
    return [(None, " ".join(words[i:i + 220])) for i in range(0, len(words), 220)]


def caption_coverage(segments, duration):
    """Flag conspicuously short captures without claiming ASR accuracy."""
    starts = [float(s["start"]) for s in segments]
    if any(not math.isfinite(s) or s < 0 for s in starts) or starts != sorted(starts):
        raise ValueError("Caption timestamps must be finite, nonnegative and ordered")
    end = max(float(s["start"]) + float(s.get("duration", 0)) for s in segments)
    if not isinstance(duration, (int, float)) or duration <= 0:
        return "duration unavailable", end
    # Intros/outros can be silent; a large missing span needs inspection.
    suspicious = starts[0] > max(120, duration * .05) or end < duration - max(120, duration * .05)
    return ("possible partial capture" if suspicious else "reaches near video end"), end


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=ROOT.parent / "research-local")
    args = parser.parse_args()
    source = args.source_dir.resolve()
    feed = ET.parse(source / "collectors-quest.rss").getroot()
    entries = []
    for item in feed.findall("channel/item"):
        title = text(item.findtext("title"))
        guid = item.findtext("guid") or item.findtext("link")
        track = re.search(r"tracks/(\d+)", guid)
        key = "sc-" + (track[1] if track else hashlib.sha256(guid.encode()).hexdigest()[:12])
        number = episode_number(title)
        filename = f"cq-{number:03}-{key}.md" if number is not None else key + ".md"
        entry = {
            "key": key, "title": title, "episode_number": number,
            "date": parsedate_to_datetime(item.findtext("pubDate")).date().isoformat(),
            "source_url": item.findtext("link"), "publisher_guid": guid,
            "inventory_source": "publisher RSS",
            "duration": item.findtext(ITUNES + "duration"),
            "description": text(item.findtext("description")),
            "path": "episodes/" + filename, "transcript_status": "missing",
            "analysis_status": "selected passages studied" if number in REVIEWED else "not closely analyzed",
            "transcript_words": 0, "video_urls": [], "transcript_sources": [],
        }
        entries.append(entry)

    publisher_count = len(entries)
    paragraphs = {}
    unmatched = []
    video_entries = {}
    for name in ("playlist.json", "channel-videos.json"):
        for video in read_json(source / name, {}).get("entries", []):
            if video.get("id") and video.get("title"):
                video_entries[video["id"]] = video
    for video_id, video in video_entries.items():
        match = match_episode(entries, video["title"])
        caption_path = source / (video_id + ".json")
        if not match:
            if caption_path.exists():
                unmatched.append({"kind": "youtube", "id": video_id, "title": video["title"], "reason": "No unambiguous publisher entry match"})
            continue
        video_url = "https://www.youtube.com/watch?v=" + video_id
        match["video_urls"].append(video_url)
        if not caption_path.exists():
            continue
        segments = read_json(caption_path, [])
        if not isinstance(segments, list) or not segments or not all(isinstance(s, dict) and "start" in s and "text" in s for s in segments):
            continue
        meta = read_json(source / (video_id + ".meta.json"), {})
        duration = meta.get("source_duration_seconds") or video.get("duration")
        coverage_check, last_end = caption_coverage(segments, duration)
        blocks = caption_paragraphs(segments)
        total_words = sum(len(p.split()) for _, p in blocks)
        match["transcript_sources"].append({"kind": "youtube", "url": video_url, "method": meta.get("method", "YouTube public caption retrieval"), "last_start_seconds": max(s["start"] for s in segments), "last_end_seconds": last_end, "source_duration_seconds": duration, "coverage_check": coverage_check, "segments": len(segments)})
        if total_words > match["transcript_words"]:
            match.update(transcript_status="available", transcript_words=total_words, primary_transcript_source=video_url, timing="YouTube caption timestamps")
            match["capture_check"] = coverage_check
            paragraphs[match["key"]] = blocks

    airtable = read_json(source / "airtable-transcripts.json", [])
    if isinstance(airtable, dict):
        airtable = airtable.get("records", airtable.get("entries", []))
    for number in (248, 252, 254):
        filename = source / f"airtable-cq{number}.txt"
        if filename.exists():
            existing = next(e for e in entries if e["episode_number"] == number)
            airtable.append({"path": str(filename), "title": existing["title"], "source_url": existing["source_url"], "status": "success"})
    for record in airtable:
        if record.get("status") not in (None, "success", "downloaded", "transcript") or not record.get("path"):
            continue
        filename = Path(record["path"])
        if not filename.is_absolute():
            filename = source / filename
        if not filename.exists():
            continue
        title = record.get("title", "")
        match = match_episode(entries, title, record.get("source_url"))
        if not match and record.get("source_url", "").startswith("https://soundcloud.com/"):
            public_url = record["source_url"]
            key = "archive-" + hashlib.sha256(public_url.encode()).hexdigest()[:12]
            number = record.get("episode_number") or episode_number(title)
            page_name = f"cq-{number:03}-{key}.md" if number is not None else key + ".md"
            match = {
                "key": key, "title": title, "episode_number": number,
                "date": record.get("publication_date") or record.get("date") or "Date not captured",
                "source_url": public_url, "publisher_guid": None,
                "inventory_source": "Airtable record with public publisher link",
                "duration": record.get("duration") or "Not captured",
                "description": "This archive entry was not unambiguously matched to the current publisher RSS feed. Its original title and source link are retained separately.",
                "path": "episodes/" + page_name, "transcript_status": "missing",
                "analysis_status": "not closely analyzed", "transcript_words": 0,
                "video_urls": [], "transcript_sources": [],
            }
            entries.append(match)
        if not match:
            unmatched.append({"kind": "airtable", "title": title, "record_id": record.get("record_id"), "reason": "No unambiguous publisher entry match"})
            continue
        raw = filename.read_text(encoding="utf-8-sig")
        blocks = prose_paragraphs(raw)
        total_words = sum(len(p.split()) for _, p in blocks)
        origin = {"kind": "airtable", "record_id": record.get("record_id"), "publisher_url": match["source_url"], "method": "User-provided archive transcript attachment"}
        if origin not in match["transcript_sources"]:
            match["transcript_sources"].append(origin)
        if match["transcript_status"] == "missing" or match.get("capture_check") == "possible partial capture":
            match.update(transcript_status="available", transcript_words=total_words, primary_transcript_source=match["source_url"], timing="No timestamps supplied; paragraph numbers are navigation aids")
            match["capture_check"] = "Full attachment text captured; untimed source completeness not independently verified"
            paragraphs[match["key"]] = blocks

    library = ROOT / "library"
    topic_matches = defaultdict(list)
    for entry in entries:
        lines = [f"# {entry['title']}", "", f"Published: {entry['date']} · Duration: {entry['duration']}", "", f"[Publisher episode]({entry['source_url']})"]
        if entry["video_urls"]:
            lines.append(" · ".join(f"[YouTube source {i + 1}]({url})" for i, url in enumerate(entry["video_urls"])))
        lines += ["", f"Transcript: **{entry['transcript_status']}** · Close reading: **{entry['analysis_status']}**", "", "## Publisher description", "", entry["description"] or "No description supplied.", "", "## Transcript", ""]
        blocks = paragraphs.get(entry["key"], [])
        if not blocks:
            lines.append("No usable transcript has been ingested for this entry yet. The publisher description is not a substitute for the episode's contents.")
        else:
            lines += [f"Source: {entry['primary_transcript_source']}", "", f"Timing: {entry['timing']}.", "", f"Capture check: {entry.get('capture_check', 'Not independently checked')}.", "", "Transcript wording may contain recognition errors, missing punctuation, or uncertain speaker attribution. Historical statements and prices are not current verified facts. Paragraph grouping is generated for navigation, not speaker labeling.", ""]
            for i, (seconds, paragraph) in enumerate(blocks, 1):
                label = f"{stamp(seconds)}" if seconds is not None else f"Paragraph {i}"
                lines += [f"### {label}", "", paragraph, ""]
        write(library / entry["path"], "\n".join(lines))
        # These are discovery leads, not semantic classifications or claims.
        entry["topic_leads"] = []
        for topic_id, (topic_name, terms) in TOPICS.items():
            patterns = [re.compile(r"\b" + re.escape(term) + r"\b", re.I) for term in terms]
            title_hit = any(p.search(entry["title"] + " " + entry["description"]) for p in patterns)
            hits = [(sec, para) for sec, para in blocks if any(p.search(para) for p in patterns)]
            if title_hit or len(hits) >= 3:
                entry["topic_leads"].append(topic_id)
                topic_matches[topic_id].append((entry, title_hit, hits[:2]))

    available = [e for e in entries if e["transcript_status"] == "available"]
    count = Counter(e["episode_number"] for e in entries if e["episode_number"] is not None)
    absent_numbers = [n for n in range(1, 301) if n not in count]
    manifest = {"built_at": datetime.now(timezone.utc).isoformat(), "publisher_feed": "https://feeds.soundcloud.com/users/soundcloud:users:183077381/sounds.rss", "entries": entries, "coverage": {"publisher_entries": publisher_count, "combined_entries": len(entries), "transcripts_available": len(available), "transcripts_missing": len(entries)-len(available), "transcript_words": sum(e["transcript_words"] for e in available), "numbered_episodes_not_in_inventory": absent_numbers, "duplicate_episode_numbers": {str(n): c for n, c in count.items() if c > 1}, "unmatched_transcript_sources": unmatched}}
    write(library / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    index = ["# Collector's Quest episode library", "", f"Combined inventory: **{len(entries)} entries** ({publisher_count} from the publisher feed). Transcripts ingested: **{len(available)}**. Still missing: **{len(entries)-len(available)}**. Transcript words: **{manifest['coverage']['transcript_words']:,}**.", "", "This library includes numbered episodes and bonus/special entries. A transcript being available does not mean every passage has been closely analyzed. See [coverage](COVERAGE.md), [topic discovery](topics/README.md), and [the full manifest](manifest.json).", "", "| Episode | Date | Transcript |", "| --- | --- | --- |"]
    index += [f"| [{e['title'].replace('|', '/')} ]({e['path']}) | {e['date']} | {e['transcript_status']} |" for e in entries]
    write(library / "README.md", "\n".join(index))
    coverage = ["# Ingestion coverage", "", f"Snapshot: {manifest['built_at']}", "", "The publisher RSS feed is the starting inventory. Airtable entries with a public publisher link can extend it. Episode numbering is preserved, including legacy titles with a parenthetical number and duplicates. Source matching uses exact public URLs, exact normalized titles, or a matching episode number with a title similarity check. Ambiguous matches are listed below rather than silently merged.", "", f"Numbered episodes 1–300 not represented in the combined inventory: {', '.join(map(str, absent_numbers)) or 'none'}.", "", f"Duplicate numbered labels: {json.dumps(manifest['coverage']['duplicate_episode_numbers'])}.", "", "## Sources awaiting a match", "", json.dumps(unmatched, ensure_ascii=False, indent=2), "", "## Entries still missing a transcript", ""]
    coverage += [f"- [{e['title']}]({e['source_url']}) — {e['date']}" for e in entries if e["transcript_status"] == "missing"]
    write(library / "COVERAGE.md", "\n".join(coverage))
    topic_index = ["# Topic discovery", "", "These indexes are generated keyword leads, not verified semantic summaries. Title/description matches are prioritized. Transcript matches require at least three paragraph hits, but a mention can still be incidental. Open the source passage and surrounding context before answering.", ""]
    for topic_id, (name, terms) in TOPICS.items():
        matches = sorted(topic_matches[topic_id], key=lambda row: (not row[1], row[0]["date"]), reverse=False)
        topic_index.append(f"- [{name}]({topic_id}.md) — {len(matches)} episode leads")
        lines = [f"# {name}", "", "Generated discovery leads. Verify relevance, context, speaker, and date in the linked episode. A keyword match is not a factual finding.", "", "Search terms: " + ", ".join(terms) + ".", ""]
        for entry, title_hit, hits in matches:
            lines += [f"## [{entry['title']}](../{entry['path']})", "", f"{entry['date']} · {'Title or publisher description match' if title_hit else 'Multiple transcript paragraph matches'} · Transcript {entry['transcript_status']}", ""]
            for seconds, paragraph in hits:
                label = stamp(seconds) if seconds is not None else "Untimed passage"
                lines.append(f"- {label}: {paragraph[:340].rstrip()}…")
            lines.append("")
        write(library / "topics" / (topic_id + ".md"), "\n".join(lines))
    write(library / "topics" / "README.md", "\n".join(topic_index))
    print(json.dumps(manifest["coverage"], indent=2))


if __name__ == "__main__":
    main()
