"""Rebuild and verify a bounded post-pilot collection without changing the pilot."""
import argparse
import json
from lore_store import ROOT, LoreStore, build, collection_path, read, windows
from search_lore_pilot import DEPTH


def merged(base):
    result = dict(schema_version='1', episodes=[], claims=[], overrides=[], new_games=[])
    for path in sorted((base / 'reviews').glob('*-annotations.json')):
        part = read(path)
        for field in ('episodes', 'claims', 'overrides', 'new_games'):
            result[field].extend(part.get(field, []))
    expected = {e['key'] for e in read(base / 'manifest.json')['episodes']}
    keys = [e['source_key'] for e in result['episodes']]
    if set(keys) != expected or len(keys) != len(expected):
        raise ValueError('Every selected episode needs exactly one annotation map')
    return result


def check_records(base):
    checked = 0
    for entry in read(base / 'manifest.json')['episodes']:
        record_path = (base / entry['record_path']).resolve()
        if not record_path.is_relative_to(base):
            raise ValueError('Record path leaves collection')
        record = read(record_path)
        validate_record_schema(record)
        if any(entry.get(k) != value for k, value in record['source'].items()):
            raise ValueError('Source metadata mismatch: ' + entry['key'])
        source = windows(ROOT, entry)
        validate_spoken_forms(record, source)
        def inspect(value):
            nonlocal checked
            if isinstance(value, list):
                for child in value:
                    inspect(child)
            elif isinstance(value, dict):
                if 'quote' in value and 'location' in value:
                    checked += 1
                    if not value['quote'] or value['quote'] not in source.get(value['location'], ''):
                        raise ValueError('Unsupported excerpt: ' + entry['key'] + '/' + value['location'])
                for child in value.values():
                    inspect(child)
        inspect(record)
        for field in ('games', 'lore', 'corrections', 'review_queue'):
            ids = [i['id'] for i in record.get(field, [])]
            if len(ids) != len(set(ids)):
                raise ValueError('Duplicate local ID: ' + field)
        for topic in record['topic_coverage']:
            if not set(topic['locations']) <= set(source):
                raise ValueError('Unknown topic window')
    return checked


def validate_spoken_forms(record, source):
    """Raw caption forms must not silently become normalized catalog names.

    Whole-episode presence is a minimum literal check, not identity proof.
    A span may continue beyond its quoted anchor; semantic source mapping
    still needs separate review.
    """
    text = '\n'.join(source.values()).casefold()
    checked = 0
    for game in record['games']:
        forms = game.get('spoken_forms')
        if not isinstance(forms, list) or not forms:
            raise ValueError('Need literal spoken forms: ' + game['id'])
        for form in forms:
            if not isinstance(form, str) or not form.strip() or form.casefold() not in text:
                raise ValueError('Nonliteral spoken form: ' + game['id'] + ': ' + str(form))
            checked += 1
    return checked


def validate_record_schema(record):
    """Validate retrieval-critical fields before merging/building artifacts."""
    for game in record['games']:
        for group in game['occurrence_groups']:
            if group.get('type') not in DEPTH:
                raise ValueError('Invalid occurrence role: ' + game['id'])
            if not isinstance(group.get('speaker'), dict) or 'candidate' not in group['speaker']:
                raise ValueError('Game occurrence needs explicit speaker uncertainty: ' + game['id'])
    for field in ('lore', 'corrections'):
        for item in record.get(field, []):
            if not isinstance(item.get('speaker'), dict) or 'candidate' not in item['speaker']:
                raise ValueError('Record needs explicit speaker uncertainty: ' + item['id'])


def answers(base, collection):
    results = []
    expected_episodes = {e['episode_number'] for e in read(base / 'manifest.json')['episodes']}
    store = LoreStore(collection=collection)
    try:
        for path in sorted((base / 'reviews').glob('*-annotations.json')):
            for case in read(path).get('task_cases', []):
                if not case.get('answer') or not case.get('forbidden'):
                    raise ValueError('Need actual composed answer and forbidden inferences')
                bundle = store.answer_evidence(case['query'], case['episode'])
                found = {r['title'] for r in bundle['context']}
                missing = sorted(set(case['evidence_locations']) - found)
                results.append({**case, 'missing_windows': missing,
                                'retrieval_status': 'failed' if missing else 'passed',
                                'source_warnings': bundle['source_warnings'],
                                'retrieved_context': bundle['context']})
    finally:
        store.close()
    if any(sum(r['episode'] == ep for r in results) < 3 for ep in expected_episodes):
        raise ValueError('Every episode needs at least three composed-answer cases')
    if len({r['id'] for r in results}) != len(results):
        raise ValueError('Duplicate answer case IDs')
    return dict(evaluation='Development context coverage; manual semantic adjudication required separately',
                passed=sum(not r['missing_windows'] for r in results), total=len(results), cases=results)


def check_fragment_evidence(base):
    entries = read(base / 'manifest.json')['episodes']
    by_number = {e['episode_number']:e['key'] for e in entries}
    passages = {e['key']:windows(ROOT, e) for e in entries}
    checked = 0
    def inspect(value, key=None):
        nonlocal checked
        if isinstance(value, list):
            for child in value:
                inspect(child, key)
        elif isinstance(value, dict):
            key = value.get('source_key', by_number.get(value.get('episode'), key))
            if 'quote' in value and 'location' in value:
                checked += 1
                if not value['quote'] or value['quote'] not in passages.get(key, {}).get(value['location'], ''):
                    raise ValueError('Unsupported fragment excerpt: ' + str(key) + '/' + value['location'])
            for child in value.values():
                inspect(child, key)
    for path in sorted((base / 'reviews').glob('*-annotations.json')):
        part = read(path)
        default = part['episodes'][0]['source_key'] if len(part['episodes']) == 1 else None
        inspect(part, default)
    return checked


def validate_section_accounting(annotation, headings):
    """Require an explicit, non-overlapping disposition for every source window.

    This checks accounting completeness, not the semantic quality of the map.
    Both per-window and contiguous section-range review formats are supported.
    """
    if annotation.get('mapping_status') != 'complete':
        raise ValueError('Episode mapping remains incomplete')
    sections = annotation.get('section_accounting', annotation.get('section_map', []))
    coverage = [0] * len(headings)
    spans = {s['id']: s for s in annotation['spans']}
    for section in sections:
        if not any(section.get(k) for k in ('summary', 'disposition', 'section')):
            raise ValueError('Source section needs a written disposition')
        if 'location' in section:
            a = headings.index(section['location'])
            b = a + 1
            if 'next_location' in section:
                expected = headings[b] if b < len(headings) else 'END'
                if section['next_location'] != expected:
                    raise ValueError('Source accounting next location is incorrect')
        else:
            a = headings.index(section['start'])
            b = len(headings) if section['end_exclusive'] == 'END' else headings.index(section['end_exclusive'])
        if a >= b:
            raise ValueError('Empty or reversed source accounting section')
        for i in range(a, b):
            coverage[i] += 1
        for ref in section.get('span_refs', []):
            if ref not in spans:
                raise ValueError('Unknown accounting span reference')
            span = spans[ref]
            sa = headings.index(span['start'])
            sb = len(headings) if span['end_exclusive'] == 'END' else headings.index(span['end_exclusive'])
            if not max(a, sa) < min(b, sb):
                raise ValueError('Accounting span does not overlap its source section')
    if not coverage or any(c != 1 for c in coverage):
        raise ValueError('Every source window must be accounted for exactly once')
    return len(coverage)


def check_accounting(base):
    entries = {e['key']: e for e in read(base / 'manifest.json')['episodes']}
    annotations = merged(base)
    total = 0
    for annotation in annotations['episodes']:
        headings = list(windows(ROOT, entries[annotation['source_key']]))
        total += validate_section_accounting(annotation, headings)
        record = read(base / entries[annotation['source_key']]['record_path'])
        record['games'].extend(a['game'] for a in annotations['new_games']
                               if a['source_key'] == annotation['source_key'])
        validate_reference_mapping(record, annotation, headings)
        validate_span_identity_kinds(annotation)
    return total


def validate_span_identity_kinds(annotation):
    """New batch maps cannot silently default every product to a video game."""
    by_entity = {}
    for span in annotation['spans']:
        kind = span.get('entity_kind')
        if not isinstance(kind, str) or not kind.strip():
            raise ValueError('Every batch span needs an explicit entity kind: ' + span['id'])
        previous = by_entity.setdefault(span['entity_id'], kind)
        if previous != kind:
            raise ValueError('One ranking identity cannot mix entity kinds: ' + span['entity_id'])
    return len(annotation['spans'])


def validate_reference_mapping(record, annotation, headings):
    """Every recorded reference's evidence window must have a mapped role.

    Passing and uncertain references still need maps; they do not gain meaningful
    duration merely by satisfying this structural reconciliation.
    """
    by_game = {}
    for span in annotation['spans']:
        a = headings.index(span['start'])
        b = len(headings) if span['end_exclusive'] == 'END' else headings.index(span['end_exclusive'])
        for ref in span['game_refs']:
            by_game.setdefault(ref, set()).update(headings[a:b])
    checked = 0
    for game in record['games']:
        if game['id'] not in by_game:
            raise ValueError('Unmapped game reference: ' + game['id'])
        for group in game['occurrence_groups']:
            for proof in group['evidence']:
                checked += 1
                if proof['location'] not in by_game[game['id']]:
                    raise ValueError('Reference evidence lacks mapped role: ' + game['id'] + '/' + proof['location'])
    return checked


def check_manual_answers(answer_result, semantic):
    """A prior pass cannot silently approve a changed answer or test scope."""
    expected = {c['id']: c for c in answer_result['cases']}
    reviewed = {c['id']: c for c in semantic}
    if len(reviewed) != len(semantic) or set(reviewed) != set(expected):
        raise ValueError('Every answer needs exactly one manual adjudication')
    for case_id, case in expected.items():
        review = reviewed[case_id]
        if review['status'] != 'passed' or not review.get('reason'):
            raise ValueError('Manual answer review has unresolved failures')
        for field in ('episode', 'answer', 'evidence_locations', 'forbidden'):
            if review.get(field) != case.get(field):
                raise ValueError('Manual answer review is stale: ' + case_id + '/' + field)
    return len(reviewed)


def sample_check(base, collection):
    sample = read(base / 'reviews/source-first-sample.json')
    entries = {e['key']:e for e in read(base / 'manifest.json')['episodes']}
    store = LoreStore(collection=collection)
    result = []
    try:
        spans = store._items('spans')
        for window in sample['windows']:
            source_windows = windows(ROOT, entries[window['source_key']])
            if source_windows[window['location']].strip() != window['text'].strip():
                raise ValueError('Frozen source window changed')
            headings = list(source_windows)
            index = headings.index(window['location'])
            for reference in window['references']:
                if reference['quote'] not in window['text']:
                    raise ValueError('Frozen reference quote invalid')
                if not reference['reviewed_game_ids'] and reference.get('comparison_status') != 'missing':
                    raise ValueError('Reference identity comparison pending: ' + reference['id'])
                matched = [s['id'] for s in spans if s['source_key'] == window['source_key']
                           and set(s['game_refs']).intersection(reference['reviewed_game_ids'])
                           and headings.index(s['start']) <= index <
                           (len(headings) if s['end_exclusive'] == 'END' else headings.index(s['end_exclusive']))]
                result.append(dict(id=reference['id'], episode=window['episode'],
                                   location=window['location'], title=reference['title'], spans=matched))
    finally:
        store.close()
    return dict(windows=len(sample['windows']), total=len(result), passed=sum(bool(r['spans']) for r in result),
                no_title_windows=sum(not w['references'] for w in sample['windows']), results=result)


def gate(base, collection):
    ledger = read(base / 'episode-review-ledger.json')
    from lore_review_binding import verify_review_binding
    verify_review_binding(ROOT, collection, ledger)
    expected = {e['episode_number'] for e in read(base / 'manifest.json')['episodes']}
    if len(ledger['episodes']) != len(expected) or {e['episode'] for e in ledger['episodes']} != expected:
        raise ValueError('Every batch episode needs one ledger')
    for episode in ledger['episodes']:
        if set(episode['checks']) != {f'A{i}' for i in range(1, 9)}:
            raise ValueError('Missing mandatory check')
        for check in episode['checks'].values():
            if check['status'] != 'passed' or not check.get('reason') or not check.get('evidence'):
                raise ValueError('Required episode work remains incomplete')
            for path in check['evidence']:
                target = (ROOT / path).resolve()
                if not target.is_relative_to(ROOT) or not target.is_file():
                    raise ValueError('Missing review evidence')
    answer_result = answers(base, collection)
    sample_result = sample_check(base, collection)
    semantic = read(base / 'reviews/answer-review.json')['cases']
    check_manual_answers(answer_result, semantic)
    accounted = check_accounting(base)
    if answer_result['passed'] != answer_result['total'] or sample_result['passed'] != sample_result['total']:
        raise ValueError('Context or sampled omission regressions failed')
    return dict(episodes=len(expected), mandatory_checks=len(expected)*8,
                integrated_answers=answer_result['total'], manual_answer_reviews=len(semantic),
                source_windows_accounted=accounted,
                sample_references=sample_result['total'], sample_covered=sample_result['passed'],
                limits='Captured-text development review, not audio/independent archive-wide/live certification')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['build', 'check', 'answers', 'sample', 'gate'])
    parser.add_argument('--collection', default='batches/002')
    args = parser.parse_args()
    base = collection_path(ROOT, args.collection)
    if args.collection == 'pilot':
        parser.error('Use the fixed pilot tools for the pilot')
    annotations = merged(base)
    count = check_records(base)
    fragment_count = check_fragment_evidence(base)
    if args.operation == 'build':
        (base / 'annotations.json').write_text(json.dumps(annotations, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        result = {**build(collection=args.collection), 'record_excerpts_checked': count, 'fragment_excerpts_checked': fragment_count}
    else:
        if annotations != read(base / 'annotations.json'):
            raise ValueError('Review inputs changed; rebuild the collection')
        if args.operation == 'gate':
            print(json.dumps(gate(base, args.collection), indent=2))
            return 0
        if args.operation == 'sample':
            result = sample_check(base, args.collection)
            print(json.dumps(result, indent=2))
            return int(result['passed'] != result['total'])
        if args.operation == 'answers':
            report = answers(base, args.collection)
            (base / 'generated/answer-evidence.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            result = {k:report[k] for k in ('passed','total')}
            result['failures'] = [{k:r[k] for k in ('id','missing_windows')} for r in report['cases'] if r['missing_windows']]
            print(json.dumps(result, indent=2))
            return int(report['passed'] != report['total'])
        store = LoreStore(collection=args.collection)
        store.close()
        result = dict(record_excerpts_checked=count, fragment_excerpts_checked=fragment_count, fragments_match=True, database_fresh=True)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
