"""Read-only pilot coverage and lookup timings; no model or network calls."""

from collections import Counter
import json
from pathlib import Path
import re
import statistics
import time

from search_lore_pilot import ROOT, load_records, search, searchable_rows


def report():
    records = load_records()
    episodes = []
    for record in sorted(records, key=lambda r: r['source']['episode_number']):
        source = record['source']
        body = (ROOT / 'library' / source['path']).read_text(encoding='utf-8')
        actual = len(re.findall(r'^### ', body, flags=re.M))
        declared = re.search(r'All (\d+)', record['review']['read_coverage'])
        episodes.append({'episode': source['episode_number'], 'words': source['words'],
                         'source_windows': actual,
                         'declared_windows_match': bool(declared and int(declared[1]) == actual),
                         'game_reference_records': len(record['games']),
                         'lore_records': len(record['lore']),
                         'open_review_flags': sum(q['status'] == 'open' for q in record['review_queue']),
                         'status': record['review']['status']})
    queries = ['Mega Man refund', 'Tyler return timetable', 'Terror Jack Ripper floppy',
               'Wii complete set', 'outback joy']
    timings = []
    for query in queries:
        samples = []
        for _ in range(5):
            start = time.perf_counter()
            results = search(load_records(), query)
            samples.append((time.perf_counter() - start) * 1000)
        timings.append({'query': query, 'runs': 5, 'median_load_index_search_ms': round(statistics.median(samples), 2),
                        'min_ms': round(min(samples), 2), 'max_ms': round(max(samples), 2),
                        'top_result_ids': [r['id'] for r in results['results']]})
    rows = searchable_rows(records)
    return {'episodes': episodes,
            'totals': {'episodes': len(episodes), 'transcript_words': sum(e['words'] for e in episodes),
                       'game_reference_records': sum(e['game_reference_records'] for e in episodes),
                       'lore_records': sum(e['lore_records'] for e in episodes),
                       'open_review_flags': sum(e['open_review_flags'] for e in episodes),
                       'search_rows_by_kind': dict(Counter(r['kind'] for r in rows))},
            'lookup_timings': timings,
            'limits': ['Reference records are not unique games or raw utterance counts.',
                       'Window counts check declared bookkeeping, not reading or omission recall.',
                       'Timings include local loading, hash checking, indexing and lookup only.',
                       'No model response latency, subscription consumption or all-archive throughput is measured.',
                       'Structural validity is not semantic acceptance.']}


if __name__ == '__main__':
    print(json.dumps(report(), indent=2))
