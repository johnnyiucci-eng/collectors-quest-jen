"""Check recurring episode gates and repaired frozen omission evidence."""
import json
from lore_store import ROOT, LoreStore, read, windows
from merge_lore_reviews import merge


def validate():
    annotations = read(ROOT / 'pilot/annotations.json')
    if annotations != merge():
        raise ValueError('Consolidated annotations differ from durable reviews')
    ledger = read(ROOT / 'pilot/episode-review-ledger.json')
    from lore_review_binding import verify_review_binding
    verify_review_binding(ROOT, 'pilot', ledger)
    manifest = read(ROOT / 'pilot/manifest.json')['episodes']
    expected = {e['episode_number'] for e in manifest}
    if {e['episode'] for e in ledger['episodes']} != expected or len(ledger['episodes']) != len(expected):
        raise ValueError('Every canonical episode needs exactly one review ledger')
    for episode in ledger['episodes']:
        if set(episode['checks']) != {f'A{i}' for i in range(1, 9)}:
            raise ValueError('Missing mandatory episode check')
        for check in episode['checks'].values():
            if check['status'] != 'passed' or not check.get('reason') or not check.get('evidence'):
                raise ValueError('Episode is not ready: ' + str(episode['episode']))
            for path in check['evidence']:
                target = (ROOT / path).resolve()
                if not target.is_relative_to(ROOT) or not target.is_file():
                    raise ValueError('Missing/local-only review evidence')
    store = LoreStore()
    try:
        spans = store._items('spans')
        sample = read(ROOT / 'pilot/reviews/cross-episode-omission.json')
        sources = {e['key']:e for e in manifest}
        passed = total = 0
        for window in sample['windows']:
            source = sources[window['source_key']]
            headings = list(windows(ROOT, source))
            index = headings.index(window['location'])
            for reference in window['references']:
                total += 1
                candidates = [s for s in spans if s['source_key'] == window['source_key']
                              and set(s['game_refs']).intersection(reference['base_game_ids'])]
                covered = any(headings.index(s['start']) <= index <
                              (len(headings) if s['end_exclusive'] == 'END' else headings.index(s['end_exclusive']))
                              for s in candidates)
                passed += covered
                if not covered:
                    raise ValueError('Frozen omission bucket not mapped: ' + reference['id'])
        dk = next(s for s in spans if s['id'] == 'cq222-audit-span-053')
        if dk['end_exclusive'] != '01:29:43':
            raise ValueError('Donkey Kong boundary regression')
    finally:
        store.close()
    return dict(episodes=len(expected), mandatory_checks=len(expected)*8,
                frozen_reference_windows=total, repaired_coverage=passed,
                limits='Development readiness, not audio/live/independent archive-wide certification')


if __name__ == '__main__':
    print(json.dumps(validate(), indent=2))
