"""Read-only pilot integrity checks. No network, API calls, or data writes."""

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate():
    manifest = read_json(ROOT / 'pilot/manifest.json')
    errors = []
    quote_count = 0
    record_count = 0
    accepted = 0
    source_passages = {}
    keys = [entry['key'] for entry in manifest['episodes']]
    if len(keys) != 10 or len(set(keys)) != 10:
        errors.append('Expected ten distinct selected source keys')
    for entry in manifest['episodes'] + manifest['duplicate_controls']:
        path = (ROOT / 'library' / entry['path']).resolve()
        if not path.is_relative_to(ROOT / 'library'):
            errors.append(f"Unsafe source path: {entry['key']}")
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            errors.append(f"Source changed: {entry['key']}")
        sections = re.split(r'^### (.+)\n', path.read_text(encoding='utf-8'), flags=re.M)
        source_passages[entry['key']] = dict(zip(sections[1::2], sections[2::2]))
        if not entry.get('record_path'):
            continue
        record_path = (ROOT / 'pilot' / entry['record_path']).resolve()
        if not record_path.is_relative_to(ROOT / 'pilot'):
            errors.append(f"Unsafe record path: {entry['key']}")
            continue
        record = read_json(record_path)
        record_count += 1
        accepted += record['review']['status'] == 'accepted'
        if record['source'] != {k: entry[k] for k in record['source']}:
            errors.append(f"Record source metadata mismatch: {entry['key']}")
        if entry['status'] != record['review']['status']:
            errors.append(f"Review status mismatch: {entry['key']}")
        passages = source_passages[entry['key']]

        def inspect(value):
            nonlocal quote_count
            if isinstance(value, list):
                for child in value:
                    inspect(child)
            elif isinstance(value, dict):
                if 'quote' in value and 'location' in value:
                    quote_count += 1
                    passage = passages.get(value['location'])
                    if passage is None or not value['quote'] or value['quote'] not in passage:
                        errors.append(f"Unsupported excerpt {entry['key']} {value['location']}: {value['quote']}")
                for child in value.values():
                    inspect(child)

        inspect(record)
        for collection in ('games', 'lore', 'review_queue', 'corrections'):
            ids = [item['id'] for item in record.get(collection, [])]
            if len(ids) != len(set(ids)):
                errors.append(f"Duplicate IDs in {entry['key']} {collection}")
        for item in record['lore']:
            if not item['evidence']:
                errors.append(f"Lore has no evidence: {item['id']}")
        for game in record['games']:
            for group in game['occurrence_groups']:
                if group['type'] not in {'SUBSTANTIAL_COVERAGE', 'SUPPORTING_EXAMPLE', 'PASSING_MENTION', 'JOKE_ASIDE'}:
                    errors.append(f"Invalid coverage type: {game['id']}")
                if not group['evidence']:
                    errors.append(f"Game has no evidence: {game['id']}")
        for topic in record['topic_coverage']:
            for location in topic['locations']:
                if location not in passages:
                    errors.append(f"Missing topic location: {location}")
    relationships = read_json(ROOT / 'pilot/relationships.json')['relationships']
    for relationship in relationships:
        for evidence in relationship['evidence']:
            quote_count += 1
            passage = source_passages.get(evidence['source_key'], {}).get(evidence['location'], '')
            if not evidence['quote'] or evidence['quote'] not in passage:
                errors.append(f"Unsupported relationship evidence: {relationship['id']}")
    questions = read_json(ROOT / 'pilot/questions.json')['questions']
    if len(questions) != 25 or len({q['id'] for q in questions}) != 25:
        errors.append('Expected 25 distinct development questions')
    print(json.dumps({'selected_episodes': len(keys), 'draft_records': record_count - accepted,
                      'accepted_records': accepted, 'evidence_excerpts_checked': quote_count,
                      'development_questions': len(questions), 'errors': errors}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(validate())
