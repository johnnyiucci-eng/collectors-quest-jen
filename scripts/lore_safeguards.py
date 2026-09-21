"""Early draft checks, archive preservation and observed workflow metrics."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import uuid

from lore_store import ROOT, LoreStore, read, windows
from search_lore_pilot import collection_path, DEPTH
from process_lore_batch import (validate_record_schema, validate_spoken_forms,
                                validate_section_accounting, validate_reference_mapping,
                                validate_span_identity_kinds)
from lore_selections import validate_selection_lists
from query_lore_archive import catalog


def preflight(collection, episode=None, root=ROOT):
    """Check existing drafts before answer integration; never builds or approves."""
    root = Path(root).resolve()
    base = collection_path(root, collection)
    entries = read(base / 'manifest.json')['episodes']
    selected = [e for e in entries if episode is None or e['episode_number'] == episode]
    if not selected:
        raise ValueError('Episode not selected in this collection')
    maps, question_cases = {}, []
    for path in sorted((base / 'reviews').glob('*-annotations.json')):
        fragment = read(path)
        question_cases.extend((c, 'evidence_locations') for c in fragment.get('task_cases', []))
        for annotation in fragment.get('episodes', []):
            maps.setdefault(annotation['source_key'], []).append(annotation)
    fresh = base / 'reviews/fresh-question-cases.json'
    if fresh.is_file():
        question_cases.extend((c, 'required_windows') for c in read(fresh).get('cases', []))
    results, all_ids = [], set()
    for entry in selected:
        try:
            record_path = (base / entry['record_path']).resolve()
            source_path = (root / 'library' / entry['path']).resolve()
            if not record_path.is_relative_to(base) or not source_path.is_relative_to(root / 'library'):
                raise ValueError('Draft path outside permitted scope')
            record = read(record_path)
            if hashlib.sha256(source_path.read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError('Source hash mismatch')
            if any(entry.get(k) != v for k, v in record['source'].items()):
                raise ValueError('Record source metadata mismatch')
            source = windows(root, entry)
            for case, location_field in question_cases:
                if case.get('episode') != entry['episode_number']:
                    continue
                required = case.get(location_field)
                if (not isinstance(required, list) or not required
                        or any(not isinstance(loc, str) or loc not in source for loc in required)):
                    raise ValueError('Question has missing or unknown source locations: ' + str(case.get('id')))
            validate_record_schema(record)
            validate_spoken_forms(record, source)
            for topic in record['topic_coverage']:
                if not isinstance(topic.get('locations'), list) or not topic['locations']:
                    raise ValueError('Topic requires a nonempty locations array')
                if not set(topic['locations']) <= set(source):
                    raise ValueError('Topic has unknown source locations')
            candidates = maps.get(entry['key'], [])
            if len(candidates) != 1:
                raise ValueError('Need exactly one annotation map for this episode')
            annotation = candidates[0]
            if annotation['source_sha256'] != entry['sha256']:
                raise ValueError('Annotation source hash mismatch')
            if not annotation.get('review_note'):
                raise ValueError('Mapping requires review note')
            for span in annotation['spans']:
                if span['id'] in all_ids or span['role'] not in DEPTH:
                    raise ValueError('Duplicate span ID or invalid role: ' + span['id'])
                all_ids.add(span['id'])
                if not span.get('reason') or not span.get('game_refs'):
                    raise ValueError('Span requires reason and references')
            validate_section_accounting(annotation, list(source))
            validate_reference_mapping(record, annotation, list(source))
            validate_span_identity_kinds(annotation)
            validate_selection_lists(record, source)
            results.append(dict(episode=entry['episode_number'], status='passed',
                                windows=len(source), spans=len(annotation['spans'])))
        except (ValueError, KeyError, OSError, TypeError) as error:
            results.append(dict(episode=entry['episode_number'], status='failed', reason=str(error)))
    return dict(status='passed' if all(r['status'] == 'passed' for r in results) else 'failed',
                episodes=results, limits='Early structural readiness only; full evidence/build and A1-A8 still required')


def archive_comparison(baseline, current):
    fields = ('collection', 'episode', 'source_key', 'source_sha256')
    expected = {tuple(e[k] for k in fields) for e in baseline['episodes']}
    actual = {tuple(e[k] for k in fields) for e in current['episodes']}
    if not expected or len(expected) != len(baseline['episodes']):
        raise ValueError('Archive baseline must contain unique nonempty source identities')
    return dict(status='passed' if expected <= actual else 'failed', expected=len(expected),
                current=len(actual), missing=[dict(zip(fields, e)) for e in sorted(expected - actual)],
                added=len(actual - expected))


def archive_check(baseline, root=ROOT):
    """Never lowers the baseline to hide a loss; also checks readable fresh DBs."""
    current = catalog(root)
    result = archive_comparison(baseline, current)
    failures = []
    for collection in sorted({e['collection'] for e in baseline['episodes']}):
        store = None
        try:
            store = LoreStore(Path(root), collection=collection)
            available = {r['source']['key'] for r in store._items('episodes')}
            required = {e['source_key'] for e in baseline['episodes'] if e['collection'] == collection}
            if not required <= available:
                raise ValueError('Reviewed source missing from database')
            store.search('Nintendo', limit=1)  # Exercise search, without asserting a particular hit.
        except Exception as error:
            failures.append(dict(collection=collection, reason=str(error)))
        finally:
            if store is not None:
                store.close()
    result['database_failures'] = failures
    result['excluded_collections'] = current['excluded_collections']
    if failures:
        result['status'] = 'failed'
    return result


def record_event(collection, operation, result, elapsed, output_characters, reviewer='unspecified', root=ROOT):
    """Telemetry observes displays, not whether anyone read or understood them."""
    base = collection_path(Path(root).resolve(), collection)
    event = dict(utc=datetime.now(timezone.utc).isoformat(), operation=operation,
                 elapsed_seconds=elapsed, output_characters=output_characters,
                 reviewer=reviewer, status=result.get('status', 'displayed'))
    if operation == 'source':
        event.update(episode=result['episode'], source_sha=result['source_sha'],
                     locations=[x['location'] for x in result['items']])
    path = base / 'generated/workbench-metrics' / (uuid.uuid4().hex + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(event, indent=2) + '\n', encoding='utf-8')
    return event


def metrics(collection, root=ROOT):
    base = collection_path(Path(root).resolve(), collection)
    events = [read(p) for p in (base / 'generated/workbench-metrics').glob('*.json')]
    seen, repeated, displayed = set(), 0, 0
    for event in sorted(events, key=lambda e: e['utc']):
        for location in event.get('locations', []):
            identity = (event['reviewer'], event['episode'], event['source_sha'], location)
            repeated += identity in seen
            displayed += 1
            seen.add(identity)
    return dict(events=len(events), measured_operation_seconds=round(sum(e['elapsed_seconds'] for e in events), 3),
                output_characters=sum(e['output_characters'] for e in events),
                source_window_displays=displayed, repeated_window_displays=repeated,
                limits='Workbench CLI observations only, not token billing, active reading time or proof of reading. '
                       'Separate reviewer IDs distinguish independent reads; unspecified IDs can conflate readers.')
