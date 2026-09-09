"""Fill selected RSS source gaps with local Whisper; requires faster-whisper.

Usage: python scripts/transcribe_rss_audio.py sc-2233221167 --device cuda
Raw recordings and outputs stay outside the public repository.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_keys", nargs="+")
    parser.add_argument("--raw-dir", type=Path, default=ROOT.parent / "research-local")
    parser.add_argument("--model", default="large-v3")
    parser.add_argument("--device", choices=("cuda", "cpu"), default="cuda")
    args = parser.parse_args()
    raw = args.raw_dir.resolve()
    registry = raw / "audio-transcripts.json"
    existing = json.loads(registry.read_text(encoding="utf-8")) if registry.exists() else []
    feed = ET.parse(raw / "collectors-quest.rss").findall("./channel/item")
    inventory = {}
    for item in feed:
        match = re.search(r"tracks/([0-9]+)", item.findtext("guid", ""))
        if match:
            inventory["sc-" + match[1]] = item
    if any(key not in inventory for key in args.source_keys):
        parser.error("Every source key must identify an item in the local publisher RSS")
    # Scope Windows DLL lookup to this environment; no system settings changed.
    handles = []
    if os.name == "nt" and args.device == "cuda":
        paths = list(Path(sys.prefix, "Lib/site-packages/nvidia").glob("*/bin"))
        handles = [os.add_dll_directory(str(path)) for path in paths]
        os.environ["PATH"] = os.pathsep.join(map(str, paths)) + os.pathsep + os.environ["PATH"]
    from faster_whisper import WhisperModel, BatchedInferencePipeline
    precision = "int8_float16" if args.device == "cuda" else "int8"
    print(f"Loading {args.model} on {args.device}", flush=True)
    model = WhisperModel(args.model, device=args.device, compute_type=precision, cpu_threads=4)
    pipeline = BatchedInferencePipeline(model=model)
    version = importlib.metadata.version("faster-whisper")
    for key in args.source_keys:
        item = inventory[key]
        url, title = item.findtext("link"), item.findtext("title")
        if any(record.get("source_url") == url and record.get("status") == "success" for record in existing):
            print(f"Already captured: {title}", flush=True)
            continue
        audio = raw / (key + ".mp3")
        if not audio.exists():
            print(f"Downloading publisher audio: {title}", flush=True)
            pending = audio.with_suffix(".download")
            urllib.request.urlretrieve(item.find("enclosure").get("url"), pending)
            pending.replace(audio)
        started = time.monotonic()
        segments, info = pipeline.transcribe(str(audio), batch_size=8, language="en", beam_size=5, vad_filter=True, initial_prompt="Collector's Quest. Johnny and Tyler discuss video game collecting. Nintendo, Sega, PlayStation, Xbox.")
        rows = []
        with (raw / (key + "-whisper-progress.jsonl")).open("w", encoding="utf-8") as progress:
            for segment in segments:
                row = {"start": segment.start, "duration": segment.end-segment.start, "text": segment.text.strip(), "avg_logprob": segment.avg_logprob, "no_speech_prob": segment.no_speech_prob}
                rows.append(row)
                progress.write(json.dumps(row, ensure_ascii=False) + "\n")
                progress.flush()
                if len(rows) % 100 == 0:
                    print(f"{key}: {segment.end/60:.1f} audio minutes; elapsed {time.monotonic()-started:.0f}s", flush=True)
        if not rows:
            raise RuntimeError(f"No recognized text for {title}; not marking complete")
        filename = key + "-whisper.json"
        (raw / filename).write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        record = {"title": title, "source_url": url, "path": filename, "method": f"Local faster-whisper {version} {args.model} {precision} {args.device}, batched beam5, English, VAD; no speaker diarization", "source_duration_seconds": info.duration, "retrieved_at": datetime.now(timezone.utc).isoformat(), "audio_sha256": hashlib.sha256(audio.read_bytes()).hexdigest(), "status": "success", "quality": "Machine-generated text; proper names and speaker attribution require verification"}
        existing.append(record)
        pending = registry.with_suffix(".tmp")
        pending.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        pending.replace(registry)
        print(f"Complete {title}: {len(rows)} segments, {sum(len(r['text'].split()) for r in rows)} words, {time.monotonic()-started:.0f}s", flush=True)


if __name__ == "__main__":
    main()
