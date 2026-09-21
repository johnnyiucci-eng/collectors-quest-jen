"""Reproduce the consolidated annotations from durable, reviewed source fragments."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAGMENTS = ['early', 'middle', '222', '248-259', '263', '299', '300']


def merge(root=ROOT):
    result = dict(schema_version='1', review_status='source_reviewed_not_audio_certified',
                  note='Complete caption-window review; timing approximate, identities and speakers retain uncertainty.',
                  episodes=[], claims=[], overrides=[], new_games=[])
    for name in FRAGMENTS:
        part = json.loads((root / f'pilot/reviews/{name}-annotations.json').read_text(encoding='utf-8'))
        for field in ('episodes', 'claims', 'overrides', 'new_games'):
            result[field].extend(part.get(field, []))
    keys = [e['source_key'] for e in result['episodes']]
    expected = [e['key'] for e in json.loads((root / 'pilot/manifest.json').read_text(encoding='utf-8'))['episodes']]
    if len(set(keys)) != len(keys) or set(keys) != set(expected):
        raise ValueError('Reviews must cover each canonical episode exactly once')
    return result


if __name__ == '__main__':
    target = ROOT / 'pilot/annotations.json'
    target.write_text(json.dumps(merge(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Consolidated reviewed annotations; run lore_store.py build next.')
