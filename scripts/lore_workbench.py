"""Bounded review views and content-addressed machine checks. No model/network calls.

Receipts reuse successful machine execution, never human review or acceptance.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from time import perf_counter

from lore_store import ROOT, LoreStore, read, windows
from search_lore_pilot import collection_path

VERSION = 'cq-workbench-2'


def _page(items, start, budget):
    if start < 0 or start > len(items) or budget < 256:
        raise ValueError('Invalid start or budget (minimum 256 characters)')
    selected = []
    for item in items[start:]:
        candidate = selected + [item]
        size = len(json.dumps(candidate, ensure_ascii=True))
        if size > budget:
            if not selected:
                raise ValueError(f'Item exceeds budget; request at least {size} characters. Nothing was truncated.')
            break
        selected = candidate
    end = start + len(selected)
    return dict(items=selected, start=start, next_start=end if end < len(items) else None,
                total=len(items), item_json_characters=len(json.dumps(selected, ensure_ascii=True)),
                truncated=False)


def source_page(collection, episode, start=0, budget=12000, source_sha=None, root=ROOT):
    """Whole windows only; a resumed read must supply the previous source hash."""
    root = Path(root).resolve()
    base = collection_path(root, collection)
    entries = [e for e in read(base / 'manifest.json')['episodes'] if e['episode_number'] == episode]
    if len(entries) != 1:
        raise ValueError('Select exactly one canonical episode in this collection')
    entry = entries[0]
    path = (root / 'library' / entry['path']).resolve()
    if not path.is_relative_to(root / 'library'):
        raise ValueError('Source outside library')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != entry['sha256'] or (source_sha and source_sha != digest):
        raise ValueError('Source changed: resume requires renewed source review')
    if start and not source_sha:
        raise ValueError('Resume with --source-sha from the previous page')
    items = [dict(location=location, text=text) for location, text in windows(root, entry).items()]
    return dict(collection=collection, episode=episode, source_sha=digest,
                read_status='Displayed only; not proof of human reading or acceptance',
                **_page(items, start, budget))


def review_page(collection, view, episode=None, start=0, budget=12000, root=ROOT):
    """Whitelist fields; never dump recursive evidence packets by accident."""
    base = collection_path(Path(root).resolve(), collection)
    items = []
    if view in ('answers', 'actions'):
        episode_by_source = {e['key']: e['episode_number'] for e in read(base / 'manifest.json')['episodes']}
        for path in sorted((base / 'reviews').glob('*-annotations.json')):
            for case in read(path).get('task_cases' if view == 'answers' else 'claims', []):
                case_episode = case.get('episode', episode_by_source.get(case.get('source_key')))
                if case_episode is None:
                    raise ValueError('Review item has no known episode: ' + str(case.get('id')))
                if episode is None or case_episode == episode:
                    fields = (('id', 'episode', 'question', 'query', 'answer', 'evidence_locations', 'forbidden')
                              if view == 'answers' else
                              ('id', 'episode', 'action_state', 'summary', 'speaker', 'subject', 'co_subjects',
                               'game_refs', 'interpretation_confidence'))
                    item = {k: case.get(k) for k in fields}
                    item['episode'] = case_episode
                    if view == 'actions':
                        item['locations'] = [e['location'] for e in case.get('evidence', [])]
                        item['qualifiers'] = {k: case[k] for k in (
                            'title', 'entity_kind', 'entity_type', 'reporter', 'reported_counterparty',
                            'subject_attribution_confidence', 'attribution_candidates', 'co_actor_uncertainty',
                            'event_confidence', 'event_status', 'modality', 'polarity', 'qualification',
                            'uncertainty', 'ownership_scope', 'ownership_status', 'purchase_status',
                            'acquisition_status', 'play_status', 'nonplay', 'completion', 'custody',
                            'disposition', 'encounter', 'intent', 'preference', 'lender', 'action_detail',
                            'item_identity_qualification', 'factual_verification', 'bid_amount', 'claim_type',
                            'intended_action_state', 'return_context')
                            if k in case}
                    items.append(item)
    elif view == 'failures':
        reports = []
        for wording, filename in [('tuned', 'answer-evidence.json'), ('original', 'workbench-original.json')]:
            path = base / 'generated' / filename
            if path.exists():
                report = read(path)
                cases = report.get('cases', []) if wording == 'tuned' else [
                    c for group in report.get('results', []) for c in group.get('cases', [])]
                reports.append((wording, cases))
        if not reports:
            raise ValueError('No saved question reports; run triage or verify first')
        for wording, cases in reports:
            for case in cases:
                if case.get('missing_windows') and (episode is None or case['episode'] == episode):
                    items.append(dict(wording=wording, **{k: case.get(k) for k in
                                 ('id', 'episode', 'question', 'query', 'missing_windows', 'context_coverage')}))
    elif view == 'spans':
        episode_by_source = {e['key']: e['episode_number'] for e in read(base / 'manifest.json')['episodes']}
        for path in sorted((base / 'reviews').glob('*-annotations.json')):
            for mapping in read(path).get('episodes', []):
                mapped_episode = episode_by_source.get(mapping.get('source_key'))
                if mapped_episode is None:
                    raise ValueError('Span mapping has no known episode')
                if episode is not None and mapped_episode != episode:
                    continue
                fields = ('id', 'entity_id', 'title', 'game_refs', 'entity_kind',
                          'identity_granularity', 'variant_context', 'role', 'start',
                          'end_exclusive', 'reason')
                for span in mapping.get('spans', []):
                    items.append(dict(episode=mapped_episode, source_key=mapping['source_key'],
                                      mapping_status=mapping.get('mapping_status'),
                                      **{k: span.get(k) for k in fields},
                                      locations=[e['location'] for e in span.get('evidence', [])],
                                      additional_fields=sorted(set(span) - set(fields) - {'evidence'})))
    elif view in ('lists', 'references'):
        for entry in read(base / 'manifest.json')['episodes']:
            if episode is not None and entry['episode_number'] != episode:
                continue
            record_path = (base / entry['record_path']).resolve()
            if not record_path.is_relative_to(base):
                raise ValueError('Record outside collection')
            record = read(record_path)
            if view == 'references':
                fields = ('id', 'canonical_title', 'spoken_forms', 'entity_granularity',
                          'platform', 'region_edition', 'identification_confidence',
                          'clarification_needed', 'identity_candidates')
                for game in record.get('games', []):
                    groups = []
                    for group in game.get('occurrence_groups', []):
                        groups.append(dict(type=group.get('type'), context=group.get('context'),
                                           speaker=group.get('speaker'),
                                           locations=[e['location'] for e in group.get('evidence', [])],
                                           additional_fields=sorted(set(group) - {
                                               'type', 'context', 'speaker', 'evidence'})))
                    items.append(dict(episode=entry['episode_number'], source_key=entry['key'],
                                      **{k: game.get(k) for k in fields}, occurrence_groups=groups,
                                      additional_fields=sorted(set(game) - set(fields) - {
                                          'occurrence_groups', 'evidence'})))
                continue
            titles = {g['id']: g.get('canonical_title') for g in record.get('games', [])}
            for group in record.get('selection_lists', []):
                for member in group['entries']:
                    items.append(dict(episode=entry['episode_number'], list_id=group['id'],
                                      label=group['label'], subject=group['subject'], purpose=group['purpose'],
                                      summary=group.get('summary'),
                                      title=titles.get(member.get('game_ref')),
                                      **{k: member.get(k) for k in ('game_ref', 'ordinal', 'status', 'reason')},
                                      locations=[e['location'] for e in member.get('evidence', [])]))
    else:
        raise ValueError('Unknown view')
    return dict(collection=collection, view=view,
                limits='Display only, not source/semantic approval. References/spans read authored drafts, not a fresh database. '
                       'Nested quotes omitted; additional_fields names any unprojected qualifiers to inspect in the artifact. '
                       'Saved failure reports may be stale. Triage executes current questions.',
                **_page(items, start, budget))


def triage(collection, case_ids=None, episode=None, root=ROOT):
    """Execute selected questions against a fresh DB, without rebuilding or approving.

    Missing-window lore candidate ranks distinguish absent evidence from candidate
    crowding. This is a focused repair loop, not a substitute for full verification.
    """
    root = Path(root).resolve()
    base = collection_path(root, collection)
    cases = [c for p in sorted((base / 'reviews').glob('*-annotations.json'))
             for c in read(p).get('task_cases', [])]
    if len({c['id'] for c in cases}) != len(cases):
        raise ValueError('Duplicate question case IDs')
    requested = set(case_ids or [])
    if requested - {c['id'] for c in cases}:
        raise ValueError('Unknown case IDs: ' + ', '.join(sorted(requested - {c['id'] for c in cases})))
    cases = [c for c in cases if (not requested or c['id'] in requested)
             and (episode is None or c['episode'] == episode)]
    if not cases:
        raise ValueError('No matching question cases')
    entries = {e['episode_number']: e for e in read(base / 'manifest.json')['episodes']}
    sources = {}
    for case in cases:
        ep = case['episode']
        if ep not in entries:
            raise ValueError('Question episode is not in the manifest')
        if ep not in sources:
            sources[ep] = windows(root, entries[ep])
        required = case.get('evidence_locations')
        if (not isinstance(required, list) or not required or
                any(not isinstance(loc, str) or loc not in sources[ep] for loc in required)):
            raise ValueError('Question has missing or unknown source locations: ' + case['id'])
    store = LoreStore(root, collection=collection)
    results, excluded = [], []
    try:
        for case in cases:
            for wording, field in [('original', 'question'), ('tuned', 'query')]:
                query = case.get(field)
                if not isinstance(query, str) or not query.strip():
                    excluded.append(dict(id=case['id'], wording=wording, reason='Missing wording'))
                    continue
                bundle = store.answer_evidence(query, case['episode'])
                missing = sorted(set(case['evidence_locations']) - {r['title'] for r in bundle['context']})
                candidates = []
                if missing:
                    for rank, hit in enumerate(store.search(query, kind='lore', episode=case['episode'], limit=50)['results'], 1):
                        covered = sorted(set(missing) & {e['location'] for e in hit['evidence']})
                        if covered:
                            candidates.append(dict(id=hit['id'], rank=rank, missing_windows_covered=covered))
                results.append(dict(id=case['id'], episode=case['episode'], wording=wording, query=query,
                                    missing_windows=missing, context_coverage=bundle['context_coverage'],
                                    route=bundle['route'], query_diagnostics=bundle['query_diagnostics'],
                                    missing_window_lore_candidates=candidates))
    finally:
        store.close()
    passed = sum(not r['missing_windows'] for r in results)
    return dict(collection=collection, status='passed' if passed == len(results) and not excluded else 'failed',
                passed=passed, total=len(results), excluded=excluded, cases=results,
                limits='Current selected-case required-window retrieval only; no semantic approval. '
                       'Candidate diagnostics inspect at most50 lexical lore hits; absent hits do not prove absent evidence.')


def _digest(paths, root):
    digest = hashlib.sha256(VERSION.encode())
    for path in sorted({p.resolve() for p in paths}):
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Check input missing or outside repository')
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b'\0' + path.read_bytes() + b'\0')
    return digest.hexdigest()


def _inputs(root, collection):
    base = collection_path(root, collection)
    # Deliberately broad local hashing is cheap compared with rereading via AI.
    # Unknown new review inputs are included rather than guessed irrelevant.
    paths = [p for p in base.rglob('*') if p.is_file() and
             'generated' not in p.relative_to(base).parts and '__pycache__' not in p.parts
             and p != base / 'annotations.json']
    paths += list((root / 'scripts').glob('*.py')) + list((root / 'tests').glob('*.py'))
    paths += [root / 'pilot/WORKFLOW.md', root / 'pilot/requirements.md']
    for e in read(base / 'manifest.json')['episodes'] + read(base / 'manifest.json').get('duplicate_controls', []):
        p = (root / 'library' / e['path']).resolve()
        if not p.is_relative_to(root / 'library'):
            raise ValueError('Check source outside library')
        paths.append(p)
    ledger_path = base / 'episode-review-ledger.json'
    if ledger_path.exists():
        for episode in read(ledger_path)['episodes']:
            for check in episode['checks'].values():
                paths += [root / p for p in check.get('evidence', [])]
    return _digest(paths, root)


def _outputs(root, collection):
    base = collection_path(root, collection)
    paths = [base / 'generated/lore.sqlite3', base / 'generated/answer-evidence.json',
             base / 'generated/workbench-original.json']
    # Deterministic merged annotations are checked by build/check and protected as
    # an output. Their regeneration is not a concurrent authored-input mutation.
    if (base / 'annotations.json').exists():
        paths.append(base / 'annotations.json')
    return _digest(paths, root) if all(p.is_file() for p in paths) else None


def verify(collection, force=False, root=ROOT):
    """Sequential per-collection checks; reuse only a successful exact receipt.

    No auto-binding. Drafts never acquire an accepted ledger. Full cross-archive
    unittest runs remain required after shared-code changes and at handoff.
    """
    root = Path(root).resolve()
    base = collection_path(root, collection)
    if collection == 'pilot':
        raise ValueError('Use the fixed pilot validation tools for the pilot')
    generated = base / 'generated'
    receipt_path = generated / 'workbench-check.json'
    before = _inputs(root, collection)
    receipt = read(receipt_path) if receipt_path.exists() else {}
    if (not force and receipt.get('version') == VERSION and receipt.get('passed') is True
            and receipt.get('inputs') == before and receipt.get('outputs') == _outputs(root, collection)
            and receipt.get('outputs')):
        return dict(collection=collection, status='reused', acceptance='unchanged; never granted here',
                    checked_utc=receipt['checked_utc'], steps=receipt['steps'])
    generated.mkdir(parents=True, exist_ok=True)
    run_dir = generated / 'workbench-runs' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    run_dir.mkdir(parents=True)
    commands = [('build', ['scripts/process_lore_batch.py', 'build', '--collection', collection]),
                ('check', ['scripts/process_lore_batch.py', 'check', '--collection', collection]),
                ('answers', ['scripts/process_lore_batch.py', 'answers', '--collection', collection]),
                ('original', ['scripts/evaluate_lore_questions.py', '--collection', collection])]
    if (base / 'episode-review-ledger.json').exists():
        commands.append(('gate', ['scripts/process_lore_batch.py', 'gate', '--collection', collection]))
    steps = []
    for name, args in commands:
        step_started = perf_counter()
        run = subprocess.run([sys.executable, *args], cwd=root, capture_output=True, text=True,
                             encoding='utf-8', errors='replace')
        # Full diagnostics stay on disk. A failed first build must not launch
        # downstream queries against missing or old generated outputs.
        log = run_dir / f'{name}.log'
        log.write_text(run.stdout + '\n' + run.stderr, encoding='utf-8')
        item = dict(check=name, success=run.returncode == 0, log=log.relative_to(root).as_posix(),
                    elapsed_seconds=round(perf_counter() - step_started, 4))
        try:
            report = json.loads(run.stdout)
            item.update({k + '_cases': report[k] for k in ('passed', 'total') if k in report})
            if name == 'original':
                (generated / 'workbench-original.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        except ValueError:
            pass
        steps.append(item)
        if run.returncode and name in ('build', 'check'):
            break
    after = _inputs(root, collection)
    passed = all(s['success'] for s in steps) and len(steps) == len(commands) and before == after
    if before != after:
        steps.append(dict(check='stable_inputs', success=False,
                          reason='Inputs changed during checks, including possible annotation merge; rerun on stable inputs'))
    receipt = dict(version=VERSION, inputs=after, outputs=_outputs(root, collection),
                   passed=passed, checked_utc=datetime.now(timezone.utc).isoformat(), steps=steps)
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return dict(collection=collection, status='passed' if passed else 'failed', steps=steps,
                acceptance='Existing gate checked if present; no review approval issued')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['source', 'answers', 'actions', 'lists', 'references', 'spans', 'failures', 'triage', 'verify',
                                             'preflight', 'archive-baseline', 'archive-check', 'metrics'])
    parser.add_argument('--collection', required=True)
    parser.add_argument('--episode', type=int)
    parser.add_argument('--case', action='append', help='Exact case ID for triage; repeat to select multiple cases')
    parser.add_argument('--start', type=int, default=0, help='Zero-based item cursor')
    parser.add_argument('--budget', type=int, default=12000, help='Maximum serialized item characters; never cuts an item')
    parser.add_argument('--source-sha')
    parser.add_argument('--reviewer', default='unspecified', help='Reader ID for measured repeat displays, not an approval')
    parser.add_argument('--force', action='store_true', help='Rerun successful checks even if exact inputs match')
    args = parser.parse_args()
    started = perf_counter()
    try:
        from lore_safeguards import preflight, archive_check, record_event, metrics
        baseline_path = ROOT / 'batches/generated/archive-baseline.json'
        if args.operation == 'archive-baseline':
            if baseline_path.exists():
                parser.error('Baseline already exists; never overwrite it to hide a regression')
            from query_lore_archive import catalog
            baseline = catalog()
            result = archive_check(baseline)
            if result['status'] == 'passed':
                baseline_path.parent.mkdir(parents=True, exist_ok=True)
                baseline_path.write_text(json.dumps(baseline, indent=2) + '\n', encoding='utf-8')
        elif args.operation == 'archive-check':
            result = archive_check(read(baseline_path))
        elif args.operation == 'metrics':
            result = metrics(args.collection)
        elif args.operation == 'preflight':
            result = preflight(args.collection, args.episode)
        elif args.operation == 'verify':
            result = preflight(args.collection)
            if result['status'] == 'passed':
                guard = archive_check(read(baseline_path))
                if guard['status'] != 'passed':
                    result = dict(status='failed', archive_preservation=guard)
                else:
                    result = verify(args.collection, args.force)
                    result['archive_preservation'] = archive_check(read(baseline_path))
                    if result['archive_preservation']['status'] != 'passed':
                        result['status'] = 'failed'
        elif args.operation == 'source':
            if args.episode is None:
                parser.error('source requires --episode')
            result = source_page(args.collection, args.episode, args.start, args.budget, args.source_sha)
        elif args.operation == 'triage':
            report = triage(args.collection, args.case, args.episode)
            log = collection_path(ROOT, args.collection) / 'generated/workbench-triage' / (
                datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
            log.parent.mkdir(parents=True, exist_ok=True)
            log.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            result = {k: v for k, v in report.items() if k != 'cases'}
            result.update(log=log.relative_to(ROOT).as_posix(), **_page(report['cases'], args.start, args.budget))
        else:
            result = review_page(args.collection, args.operation, args.episode, args.start, args.budget)
        # Dense inventory views remain within their item budget without adding
        # thousands of whitespace-only lines after pagination.
        output = json.dumps(result, ensure_ascii=True,
                            indent=None if args.operation in ('references', 'spans') else 2)
        if args.operation != 'metrics':
            record_event(args.collection, args.operation, result, perf_counter() - started, len(output), args.reviewer)
        print(output)
        return int(result.get('status') == 'failed')
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
