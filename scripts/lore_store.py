"""Persistent, reproducible CQ lore queries. Standard library; no network/model calls."""

import argparse
from collections import defaultdict
from contextlib import closing
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import tempfile
import os

from search_lore_pilot import ROOT, STOP, DEPTH, load_records, searchable_rows, collection_path

VERSION = 'cq-lore-store-1'
DEFAULT_DB = ROOT / 'pilot/generated/lore.sqlite3'


def query_terms(query):
    """Expose the lexical budget instead of silently discarding later terms."""
    terms = list(dict.fromkeys(t for t in re.findall(r'\w+', query.lower()) if t not in STOP))
    return dict(effective_terms=terms[:16], omitted_terms=terms[16:],
                truncated=len(terms) > 16, term_limit=16)


def mixed_action_states(query):
    """Evidence for explicit multi-state history questions, never inferred actions."""
    q = query.casefold()
    if (not re.search(r'\b(?:what|which)\b', q)
            or not re.search(r'\b(?:and|or|versus|vs|but)\b', q)
            or re.search(r'\b(?:should|could|would|best|recommend|recommended|wishlist)\b', q)
            or re.search(r'\b(?:want(?:ed|s)?|plan(?:ned|s)?)\s+to\b|\bfinish(?:ed)?\s+collecting\b', q)):
        return set()
    groups = []
    if re.search(r'\b(?:buy|bought|purchases?|purchased|acquired|ordered|received)\b', q):
        groups.append({'purchased', 'ordered', 'received'})
    if re.search(r'\b(?:wants?|wanted|missing|unbought|pending)\b', q):
        groups.append({'wanted'})
    if re.search(r'\b(?:play|played|finish|finished|beat|completed)\b', q):
        groups.append({'played'})
    # "Wanted to buy" is one intention, not two completed/pending states.
    # Explicit nonplay and denied purchases are represented as mentioned,
    # with their actual polarity/qualification retained in the source claim.
    return set().union(*groups, {'mentioned'}) if len(groups) >= 2 else set()


def question_route(query, participants=()):
    """Generic intents only: no episode IDs, answer keys or source locations."""
    q = query.casefold()
    if mixed_action_states(query):
        return 'action_states', None
    # A contrast explicitly excludes the trailing alternative from the main
    # question: discussion "rather than recommendations" is still prominence.
    main_question = re.split(r'\brather than\b|\binstead of\b', q, maxsplit=1)[0]
    constrained = bool(re.search(r'\b(?:wanted|want|buy|bought|purchased|owned|own|played|completed|favorite|favourite|best|recommend|recommended|guest|his|her)\b', main_question))
    named_actor = any(re.search(r'\b' + re.escape(name.casefold()) + r'\b', main_question) for name in participants if name)
    discussion = (re.search(r'\bgames?\b', q) and
                  (re.search(r'\bmost\s+(?:(?:meaningful|real|substantial)\s+)?(?:discussion|discussed|talked)', q)
                   or re.search(r'\b(?:talked about|discussed)\s+(?:the\s+)?most\b', q)
                   or re.search(r'\bgames?\b.*\bdominated\b.*\b(?:interview|discussion|conversation|episode)\b', q)
                   or re.search(r'\b(?:biggest|largest)\s+(?:game\s+)?discussions?\b', q)
                   or (re.search(r'\b(?:rank|ranked|ranking)\b', q) and re.search(r'\b(?:discussions?|coverage)\b', q))))
    bare_top = re.fullmatch(r'(?:what (?:are|were) (?:the )?)?top\s+(?:\d+|three|five)\s+games(?:\s+(?:in|from|for)\s+(?:episode|cq)\s*#?\s*\d+)?[?.! ]*', q)
    if (discussion or bare_top) and not constrained and not named_actor:
        return 'game_prominence', None
    if (re.search(r'\b(?:lists?|picks|selections)\b', q)
            and re.search(r'\b(?:starter|starting|recommended|recommendation|ten.game|both|hot|aspirational|strive|secondary|launch)\b', q)):
        return 'selection_lists', None
    if re.search(r'\bfollow[- ]?ups?\b|\bopen loops?\b|\bunanswered\b|\bstill hunting for\b|\bwaiting\b|\bplans?\b.*\bstill\b', q):
        return 'open_loops', None
    if re.search(r'\b(?:ports?|ported|remasters?)\b', q):
        return 'port_classification', 'ports sequels remasters transition releases hypothetical predictions'
    if (re.search(r'\b(?:want|wanted|wish|wished|hope|hoped)\b.*\b(?:see|release|released|arrive)\b', q)
            or re.search(r'\b(?:hypothetical|invented|inventions)\b.*\b(?:games|ideas|releases)\b', q)):
        return 'release_ideas', 'desired future release hypothetical invented sequel predictions'
    if (re.search(r'\bcollecting\b', q) and re.search(r'\b(?:end|done|stop|finish|finished)\b', q)):
        return 'collecting_end', 'collecting end goals enjoyment purpose motivation'
    if (re.search(r'\b(?:old|older|historical)\b.*\bgames?\b', q)
            and re.search(r'\b(?:good|time|context|evaluate|evaluation)\b', q)):
        return 'historical_evaluation', 'historical context old games good time evaluation enjoyment'
    if (re.search(r'\b(?:practical changes|takeaways|alternatives)\b', q)
            and re.search(r'\b(?:buying|collecting|purchases)\b', q)):
        return 'collecting_alternatives', 'practical collecting changes activities heirs burden'
    if re.search(r'\b(?:process|workflow)\b.*\b(?:collect|collecting|buying|games)\b|\b(?:collecting|collection)\b.*\b(?:process|workflow)\b', q):
        return 'collecting_process', 'goals review documentation inventory insurance shelving organization storage'
    if re.search(r'\bmismatched?\b.*\b(?:parts|contents|discs?|cases?)\b|\bmatched[- ]print\b', q):
        return 'edition_integrity', 'reprints mixed discs cases paperwork print runs contents sealed documentation'
    if (re.search(r'\b(?:master|mastery|skill ceiling)\b', q)
            and re.search(r'\b(?:hardest|difficult|compare|comparing|disagree|debate)\b', q)):
        return 'skill_comparison', 'skill ceiling mastery hidden information randomness execution reflex practice criteria'
    if (re.search(r'\b(?:set|checklist)\b', q)
            and re.search(r'\b(?:counts?|included|include|optional|required|complete|completing|completeness)\b', q)):
        return 'set_scope', 'set checklist standalone separate release duplicate bundle optional required utility completeness'
    if (re.search(r'\b(?:complete|comprehensive|exhaustive)\s+(?:guide|overview|catalog|coverage)\b', q)
            or re.search(r'\b(?:episode|show|conversation)\b.*\b(?:scope|exhaustive)\b', q)):
        return 'episode_scope', 'scope format coverage'
    if (re.search(r'\b(?:cheap|inexpensive|expensive|prices?|value|cost)\b', q)
            and re.search(r'\b(?:assumptions?|challenged?|disagreed?|contradict(?:ed|ion)?|corrected?)\b', q)):
        return 'price_assumptions', 'price value dollar cheap sales correction'
    if (re.search(r'\b(?:expensive|costly|prices?|value)\b', q)
            and re.search(r'\b(?:games?|items?|buys|worth|rarity|scarcity)\b', q)):
        return 'price_evaluation', 'expensive costly price value rarity scarcity sales asking utility exceptions'
    if re.search(r'\b(?:disappointed|disappointing|disappointment|disliked|complaints?|criticize|criticized|criticism)\b', q):
        return 'criticism', 'disliked disappointed complaint criticism frustrating controls weak'
    if (re.search(r'\b(?:what|which)\b.*\b(?:add|added|pickups)\b', q)
            and re.search(r'\b(?:actually|collection|collections|pickups)\b', q)
            and not re.search(r'\b(?:want|wanted|wish|wishlist|should|would|could|planned|hypothetical)\b', q)):
        return 'acquisitions', None
    if (re.search(r'\b(?:which|what)\b.*\b(?:buy|bought|purchase|purchased|acquire|acquired)\b', q)
            and not re.search(r'\b(?:which|what)\s+(?:collector|host|person|speaker|guest)\b', q)
            and not re.search(r'\b(?:want|wanted|should|recommend|recommended|would|could|best|favorite|favourite|hypothetical|planned)\b', q)):
        return 'acquisitions', None
    if (re.search(r'\b(?:what|which)\b.*\bpre[- ]?order(?:ed)?\b', q)
            and not re.search(r'\b(?:want|wanted|should|recommend|recommended|would|could)\b', q)):
        return 'acquisitions', None
    if (re.search(r'\b(?:what|which)\b.*\b(?:new\s+)?purchases\b', q)
            and not re.search(r'\b(?:want|wanted|should|recommend|recommended|would|could|planned|hypothetical)\b', q)):
        return 'acquisitions', None
    if re.search(r'\b(?:correct|corrected|corrections?|clarify|clarified|clarifications?|retract|retracted)\b', q):
        return 'corrections', None
    if (re.search(r'\b(?:store|shop|business|collector|collecting)\b', q)
            and re.search(r'\b(?:start|started|become|became|origin|history|begin|began)\b', q)):
        return 'collecting_history', 'childhood started collecting opened store business laid off job sweepstakes inventory booth'
    if (re.search(r'\b(?:convention|festival|expo|event)\b', q)
            and re.search(r'\b(?:organize|organizing|organizer|organisation|organization|work|build|building|makes|possible|logistics)\b', q)):
        return 'event_organization', 'organizing event rental equipment tables chairs electricity fire approvals volunteers community'
    return 'lexical', None


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def source_inputs(root, collection='pilot'):
    base = collection_path(root, collection)
    paths = [base / 'manifest.json', base / 'relationships.json',
             base / 'annotations.json', Path(__file__).resolve(),
             root / 'scripts/search_lore_pilot.py', Path(__file__).with_name('lore_selections.py')]
    paths.extend(sorted((base / 'reviews').glob('*-annotations.json')))
    manifest = read(paths[0])
    for entry in manifest['episodes'] + manifest['duplicate_controls']:
        source = (root / 'library' / entry['path']).resolve()
        if not source.is_relative_to((root / 'library').resolve()):
            raise ValueError('Source outside library')
        paths.append(source)
        if entry.get('record_path'):
            record = (base / entry['record_path']).resolve()
            if not record.is_relative_to(base):
                raise ValueError('Record outside pilot')
            paths.append(record)
    return paths


def fingerprint(root, collection='pilot'):
    digest = hashlib.sha256(VERSION.encode())
    for path in source_inputs(root, collection):
        digest.update(str(path.resolve()).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def windows(root, source):
    parts = re.split(r'^### (.+)\n', (root / 'library' / source['path']).read_text(encoding='utf-8'), flags=re.M)
    return dict(zip(parts[1::2], parts[2::2]))


def seconds(location):
    if not re.fullmatch(r'\d\d:\d\d:\d\d', location):
        return None
    h, m, s = map(int, location.split(':'))
    return h * 3600 + m * 60 + s


def union_length(intervals):
    end = None
    total = 0
    for a, b in sorted(intervals):
        total += max(0, b - max(a, end if end is not None else a))
        end = max(b, end if end is not None else b)
    return total


def annotate_reference_kinds(rows, spans, passages):
    """Classify each reference row's evidenced windows, not every use of a title.

    Legacy spans without a kind remain unknown; mixed game/hardware references
    cannot pass an exclusive video-game filter merely by sharing an ID.
    """
    indexed = defaultdict(set)
    for span in spans:
        key = span['source_key']
        headings = list(passages[key])
        start = headings.index(span['start'])
        end = len(headings) if span['end_exclusive'] == 'END' else headings.index(span['end_exclusive'])
        for ref in span['game_refs']:
            for location in headings[start:end]:
                indexed[key, ref, location].add(span.get('entity_kind') or 'unknown')
    for row in rows:
        if row['kind'] != 'game':
            continue
        ref = row['local_id'].rsplit(':', 1)[0]
        per_window = [indexed.get((row['source_key'], ref, e['location']), {'unknown'}) for e in row['evidence']]
        kinds = set().union(*per_window) if per_window else {'unknown'}
        row['entity_kinds'] = sorted(kinds - {'unknown'})
        row['entity_kind_status'] = ('incomplete' if 'unknown' in kinds else 'mixed' if len(kinds) != 1 else 'typed')
        row['kind_note'] = "Legacy kind='game' means reference bucket; entity_kinds describe these evidence windows."


def build(root=ROOT, database=None, collection='pilot'):
    root = Path(root).resolve()
    base = collection_path(root, collection)
    database = Path(database or base / 'generated/lore.sqlite3').resolve()
    if not database.is_relative_to(base / 'generated') or database.suffix != '.sqlite3':
        raise ValueError('Generated database must be a .sqlite3 file under ' + str(collection) + '/generated')
    stamp = fingerprint(root, collection)
    records = load_records(root, collection)
    manifest_entries = {e['key']: e for e in read(base / 'manifest.json')['episodes']}
    for record in records:
        source = record['source']
        expected = manifest_entries.get(source['key'])
        if expected is None or any(source[field] != expected[field] for field in ('path', 'episode_number', 'sha256')):
            raise ValueError('Record source disagrees with canonical manifest')
        from lore_selections import validate_selection_lists
        validate_selection_lists(record, windows(root, source))
    sources = {r['source']['key']: r for r in records}
    passages = {key: windows(root, r['source']) for key, r in sources.items()}
    annotations = read(base / 'annotations.json')
    if annotations.get('schema_version') != '1':
        raise ValueError('Unsupported annotation schema')
    if collection == 'pilot' and (base / 'reviews/early-annotations.json').exists():
        from merge_lore_reviews import merge
        if annotations != merge(root):
            raise ValueError('Review fragments changed; run merge_lore_reviews.py before build')
    elif collection != 'pilot' and any((base / 'reviews').glob('*-annotations.json')):
        from process_lore_batch import merged
        if annotations != merged(base):
            raise ValueError('Review fragments changed; run process_lore_batch.py build before retrieval')
    for addition in annotations.get('new_games', []):
        record = sources[addition['source_key']]
        if addition['source_sha256'] != record['source']['sha256']:
            raise ValueError('Stale game addition')
        game = addition['game']
        if not addition.get('reason') or any(g['id'] == game['id'] for g in record['games']):
            raise ValueError('Game addition needs reason and unused ID')
        record['games'].append(game)
    applied = []
    for override in annotations['overrides']:
        record = sources[override['source_key']]
        if override['source_sha256'] != record['source']['sha256']:
            raise ValueError('Stale override source')
        if not override.get('reason'):
            raise ValueError('Override requires a reason')
        if override['collection'] not in ('games', 'lore'):
            raise ValueError('Unsupported override collection')
        item = next(x for x in record[override['collection']] if x['id'] == override['item_id'])
        # Only explicit field replacements with a checked base value; no silent drift.
        for field, change in override['fields'].items():
            if field in ('id', 'evidence') or field not in item:
                raise ValueError('Unsupported override field')
            if item[field] != change['expected']:
                raise ValueError('Override base changed: ' + override['item_id'])
            item[field] = change['value']
        applied.append(override)
    rows = searchable_rows(records)
    for row in rows:
        row['local_id'] = row['id']
        row['id'] = row['source_key'] + '/' + row['id']
    row_ids = {r['id']: r for r in rows}
    if len(row_ids) != len(rows):
        raise ValueError('Duplicate retrieval IDs')

    def evidence_valid(key, evidence):
        if not evidence:
            raise ValueError('Missing evidence')
        for e in evidence:
            if not e.get('quote') or e['quote'] not in passages[key].get(e['location'], ''):
                raise ValueError('Unsupported evidence: ' + key)

    for row in rows:
        evidence_valid(row['source_key'], row['evidence'])
    spans = []
    mapping = {}
    span_ids = set()
    for annotation in annotations['episodes']:
        key = annotation['source_key']
        if key in mapping or annotation['source_sha256'] != sources[key]['source']['sha256']:
            raise ValueError('Duplicate/stale episode annotation')
        if annotation['mapping_status'] not in ('partial', 'complete'):
            raise ValueError('Invalid mapping status')
        if annotation['mapping_status'] == 'complete' and not annotation.get('review_note'):
            raise ValueError('Complete mapping needs review note')
        mapping[key] = annotation['mapping_status']
        headings = list(passages[key])
        game_ids = {g['id'] for g in sources[key]['games']}
        for span in annotation['spans']:
            if span['id'] in span_ids or span['role'] not in DEPTH:
                raise ValueError('Duplicate span ID or invalid role')
            span_ids.add(span['id'])
            if not span.get('reason') or not span.get('game_refs') or not set(span['game_refs']) <= game_ids:
                raise ValueError('Span needs reason and valid game references')
            a = headings.index(span['start'])
            b = len(headings) if span['end_exclusive'] == 'END' else headings.index(span['end_exclusive'])
            if a >= b:
                raise ValueError('Empty/reversed span')
            evidence_valid(key, span['evidence'])
            if any(not a <= headings.index(e['location']) < b for e in span['evidence']):
                raise ValueError('Evidence outside span')
            start_time = seconds(headings[a])
            if start_time is None:
                interval, unit = [a, b], 'paragraphs'
            elif b == len(headings):
                # No fabricated endpoint for the final caption window.
                interval, unit = None, 'seconds'
            else:
                interval, unit = [start_time, seconds(headings[b])], 'seconds'
            spans.append({**span, 'source_key': key, 'episode': sources[key]['source']['episode_number'],
                          'interval': interval, 'unit': unit})
    annotate_reference_kinds(rows, spans, passages)
    claims = []
    for claim in annotations['claims']:
        record = sources[claim['source_key']]
        if claim['source_sha256'] != record['source']['sha256']:
            raise ValueError('Stale action claim')
        if claim['action_state'] not in ('mentioned', 'wanted', 'purchased', 'ordered', 'received', 'returned', 'owned', 'played', 'sold', 'hypothetical'):
            raise ValueError('Invalid action state')
        evidence_valid(claim['source_key'], claim['evidence'])
        claims.append({**claim, 'episode': record['source']['episode_number']})
    if len({c['id'] for c in claims}) != len(claims):
        raise ValueError('Duplicate claim ID')
    relationships = read(base / 'relationships.json')['relationships']
    for relationship in relationships:
        for e in relationship['evidence']:
            evidence_valid(e['source_key'], [e])
    # Refuse to overwrite an unrelated database, even in the generated directory.
    if database.exists():
        with closing(sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)) as old:
            if old.execute("SELECT value FROM metadata WHERE key='version'").fetchone() != (VERSION,):
                raise ValueError('Existing database is not this lore index')
    database.parent.mkdir(parents=True, exist_ok=True)
    handle, temp = tempfile.mkstemp(prefix='lore-', suffix='.sqlite3', dir=database.parent)
    os.close(handle)
    try:
        with closing(sqlite3.connect(temp)) as db, db:
            db.executescript('''
                CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE episodes(source_key TEXT PRIMARY KEY, number INTEGER UNIQUE, payload TEXT, mapping_status TEXT);
                CREATE TABLE records(id TEXT PRIMARY KEY, source_key TEXT, kind TEXT, payload TEXT);
                CREATE VIRTUAL TABLE lookup USING fts5(id UNINDEXED, title, summary, evidence);
                CREATE TABLE spans(id TEXT PRIMARY KEY, source_key TEXT, entity_id TEXT, payload TEXT);
                CREATE TABLE claims(id TEXT PRIMARY KEY, payload TEXT);
                CREATE TABLE relationships(id TEXT PRIMARY KEY, payload TEXT);
                CREATE TABLE overrides(id TEXT PRIMARY KEY, payload TEXT);
            ''')
            db.executemany('INSERT INTO metadata VALUES(?,?)', [('version', VERSION), ('fingerprint', stamp)])
            for r in records:
                s = r['source']
                db.execute('INSERT INTO episodes VALUES(?,?,?,?)', (s['key'], s['episode_number'], json.dumps(r), mapping.get(s['key'], 'not_mapped')))
            for r in rows:
                db.execute('INSERT INTO records VALUES(?,?,?,?)', (r['id'], r['source_key'], r['kind'], json.dumps(r)))
                db.execute('INSERT INTO lookup VALUES(?,?,?,?)', (r['id'], r['title'] + ' ' + r['aliases'], r['summary'], ' '.join(e['quote'] for e in r['evidence'])))
            # Keep complete source windows searchable for checking a composed
            # answer, including qualifications omitted from short extracts.
            for key, source_windows in passages.items():
                source = sources[key]['source']
                for location, passage in source_windows.items():
                    local_id = 'passage:' + location
                    item = dict(id=key + '/' + local_id, local_id=local_id,
                                source_key=key, episode=source['episode_number'], kind='passage',
                                title=location, aliases='', summary='',
                                transcript_path='library/' + source['path'],
                                speaker=dict(candidate=None, confidence='unknown', basis='Undiarized source window'),
                                evidence=[dict(location=location, quote=passage)], depth=None)
                    db.execute('INSERT INTO records VALUES(?,?,?,?)', (item['id'], key, 'passage', json.dumps(item)))
                    db.execute('INSERT INTO lookup VALUES(?,?,?,?)', (item['id'], location, '', passage))
            for s in spans:
                db.execute('INSERT INTO spans VALUES(?,?,?,?)', (s['id'], s['source_key'], s['entity_id'], json.dumps(s)))
            for table, items in [('claims', claims), ('relationships', relationships), ('overrides', applied)]:
                for item in items:
                    db.execute(f'INSERT INTO {table} VALUES(?,?)', (item['id'], json.dumps(item)))
        if fingerprint(root, collection) != stamp:
            raise ValueError('Inputs changed during build')
        os.replace(temp, database)
    finally:
        if Path(temp).exists():
            Path(temp).unlink()
    return {'database': str(database), 'episodes': len(records), 'search_rows': len(rows),
            'spans': len(spans), 'action_claims': len(claims), 'overrides': len(applied)}


class LoreStore:
    def __init__(self, root=ROOT, database=None, collection='pilot'):
        self.root = Path(root).resolve()
        self.collection = collection
        base = collection_path(self.root, collection)
        path = Path(database or base / 'generated/lore.sqlite3').resolve()
        self.db = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
        try:
            meta = dict(self.db.execute('SELECT key,value FROM metadata'))
            if meta.get('version') != VERSION or meta.get('fingerprint') != fingerprint(self.root, collection):
                raise ValueError('Lore index is stale; rebuild before retrieval')
        except Exception:
            self.db.close()
            raise

    def close(self):
        self.db.close()

    def _items(self, table):
        return [json.loads(x[0]) for x in self.db.execute(f'SELECT payload FROM {table}')]

    def search(self, query, speaker=None, kind=None, limit=10, episode=None, required_phrases=None, entity_kind=None):
        if any(not re.findall(r'\w+', p) for p in required_phrases or []):
            raise ValueError('Required phrases must contain words')
        diagnostics = query_terms(query)
        terms = diagnostics['effective_terms']
        if not terms:
            raise ValueError('Supply meaningful query terms')
        expression = ' OR '.join('"' + t + '"' for t in terms)
        hits = []
        for payload, score in self.db.execute('SELECT records.payload,bm25(lookup,0,5,2,1) FROM lookup JOIN records ON records.id=lookup.id WHERE lookup MATCH ?', (expression,)):
            hit = json.loads(payload)
            if not kind and hit['kind'] == 'passage':
                continue
            if (kind and hit['kind'] != kind) or (episode is not None and hit['episode'] != episode):
                continue
            if entity_kind and (hit.get('entity_kind_status') != 'typed' or hit.get('entity_kinds') != [entity_kind]):
                continue
            full = ' '.join([hit['title'], hit['aliases'], hit['summary']] + [e['quote'] for e in hit['evidence']]).lower()
            if any(not re.search(r'\b' + r'\W+'.join(re.escape(t) for t in re.findall(r'\w+', p.lower())) + r'\b', full)
                   for p in required_phrases or []):
                continue
            matches = sum(bool(re.search(r'\b' + re.escape(t) + r'\b', full)) for t in terms)
            title_matches = sum(bool(re.search(r'\b' + re.escape(t) + r'\b', (hit['title'] + ' ' + hit['aliases']).lower())) for t in terms)
            candidate = hit['speaker'].get('candidate')
            hit['speaker_match'] = 'not_requested' if not speaker else ('contextual_match' if (candidate or '').casefold() == speaker.casefold() else 'uncertain_or_other_speaker')
            # Keep useful partial evidence when no speaker matches. Never label
            # caption continuity as verified diarization.
            hit['evidence'] = [{**e, 'transcript_url': 'https://github.com/johnnyiucci-eng/collectors-quest-jen/blob/main/'
                               + hit['transcript_path'] + '#' + e['location'].lower().replace(' ', '-').replace(':', '')}
                              for e in hit['evidence']]
            hits.append((-matches, -title_matches, 0 if hit['speaker_match'] == 'contextual_match' else 1, DEPTH.get(hit.get('depth'), 1), score, hit))
        hits.sort(key=lambda x: (*x[:-1], x[-1]['id']))
        return {'scope': 'processed collection only: ' + self.collection, 'results': [h[-1] for h in hits[:max(1, min(limit, 50))]],
                'query_diagnostics': diagnostics,
                'entity_kind_filter': entity_kind,
                'entity_kind_note': 'Exclusive typed evidence-window filter; mixed and untyped legacy references are excluded when requested. Coarse game kind is a legacy reference bucket.',
                'warning': 'Lexical candidates require claim-level checking; no hit is not archive absence.'}

    def top_games(self, episode, limit=3):
        row = self.db.execute('SELECT source_key,mapping_status FROM episodes WHERE number=?', (episode,)).fetchone()
        if not row:
            return {'episode': episode, 'status': 'not_processed', 'results': []}
        grouped = defaultdict(list)
        series = defaultdict(list)
        for span in self._items('spans'):
            if span['source_key'] != row[0] or span['role'] not in ('SUBSTANTIAL_COVERAGE', 'SUPPORTING_EXAMPLE'):
                continue
            kind = span.get('entity_kind', 'video_game')
            if kind == 'video_game':
                grouped[span['entity_id']].append(span)
            elif kind == 'game_series':
                series[span['entity_id']].append(span)

        def rank(groups):
            results = []
            for entity, spans in groups.items():
                intervals = [s['interval'] for s in spans if s['interval'] is not None]
                substantial = [s['interval'] for s in spans if s['role'] == 'SUBSTANTIAL_COVERAGE' and s['interval'] is not None]
                results.append({'entity_id': entity, 'title': spans[0]['title'], 'coverage': union_length(intervals),
                                'substantial_coverage': union_length(substantial), 'unit': spans[0]['unit'],
                                'unknown_endpoint': any(s['interval'] is None for s in spans), 'spans': spans})
            results.sort(key=lambda r: (-r['coverage'], -r['substantial_coverage'], r['title']))
            previous = None
            for i, result in enumerate(results):
                value = (result['coverage'], result['substantial_coverage'])
                result['rank'] = previous[1] if previous and previous[0] == value else i + 1
                previous = (value, result['rank'])
            return results

        results = rank(grouped)
        series_results = rank(series)
        complete = row[1] == 'complete'
        timing_complete = not any(r['unknown_endpoint'] for r in results)
        return {'episode': episode, 'status': 'mapped_estimate' if complete else 'incomplete_mapping',
                'mapping_complete': complete, 'timing_complete': timing_complete,
                'results': results[:max(1, min(limit, 50))],
                'series_results': series_results[:max(1, min(limit, 50))],
                'identity_warning': 'Series coverage is separate; do not assign it to every installment.',
                'warning': 'Caption-window estimates, not exact speech time. Overlap is unioned per game. '
                           + ('Unknown final-window duration remains uncounted. ' if not timing_complete else '')
                           + 'Near ties within a caption window are not decisive rankings. '
                           + ('' if complete else 'These are provisional leaders among mapped spans, not a certified episode top three.')}

    def answer_evidence(self, query, episode, limit=12):
        """Retrieve full windows and adjacent qualifications from the database.

        This is an evidence bundle, not an automatically certified answer.
        """
        raw = self.search(query, kind='passage', episode=episode, limit=limit)
        hits = raw['results']
        rows = [r for r in self._items('records') if r['kind'] == 'passage' and r['episode'] == episode]
        selected = {r['id'] for r in hits}
        indices = {i for i, r in enumerate(rows) if r['id'] in selected}
        # Title aliases and reviewed return spans bridge words omitted or
        # misspelled in raw captions. Never rely on a single lexical excerpt.
        structured = self.search(query, episode=episode, limit=5)['results']
        # Repeated occurrence rows for one title must not crowd out a reviewed
        # multi-game explanation. Reserve a small separate lore channel.
        structured += self.search(query, kind='lore', episode=episode, limit=3)['results']
        # Explicit four-digit topic anchors (often years) should not be lost to
        # incidental words inside long quotations. Require a whole-token match
        # in the reviewed topic/summary, not merely an evidence quote. Keep this
        # separate, bounded and disclosed; never infer dates or list membership.
        numeric_terms = set(re.findall(r'\b\d{4}\b', query))
        numeric_lore = []
        if numeric_terms:
            candidates = self.search(' '.join(sorted(numeric_terms)), kind='lore', episode=episode, limit=50)['results']
            numeric_lore = [r for r in candidates if numeric_terms.intersection(
                re.findall(r'\b\d{4}\b', r['title'] + ' ' + r['summary']))][:3]
            structured += numeric_lore
        episode_record = next((r for r in self._items('episodes') if r['source']['episode_number'] == episode), {})
        participants = [p.get('name') for p in episode_record.get('participants', [])]
        route, expansion = question_route(query, participants)
        routed_locations = set()
        ranking = None
        selection_lists = []
        selection_scope = None
        route_candidates = []
        if expansion:
            # Preserve original query hits; expansion is a separate, disclosed pass.
            if route == 'episode_scope':
                # Use explicitly typed episode-format/scope notes. A generic
                # question is not permission to assume the opening is evidence
                # or to collect every note containing "complete".
                route_candidates = [r for r in self.search(
                    expansion, kind='lore', episode=episode, limit=50)['results']
                    if str(r.get('lore_kind', '')).casefold() in ('format', 'scope', 'episode_scope')][:3]
            elif route in ('collecting_end', 'historical_evaluation', 'collecting_alternatives'):
                # Conceptual questions need multiple reviewed perspectives,
                # not a wider raw-caption sweep. Keep this channel bounded.
                route_candidates = self.search(expansion, kind='lore', episode=episode, limit=4)['results']
            elif route in ('criticism', 'price_assumptions'):
                # One reviewed explanation is enough to bridge a missing
                # qualification; avoid expanding unrelated passage channels.
                route_candidates = self.search(expansion, kind='lore', episode=episode, limit=1)['results']
            else:
                route_candidates = (self.search(expansion, kind='passage', episode=episode, limit=6)['results']
                                    + self.search(expansion, episode=episode, limit=5)['results'])
            if route in ('skill_comparison', 'set_scope', 'price_evaluation'):
                # A bounded reviewed-summary channel bridges conceptual wording
                # without promoting a generated answer or hard-coded episode key.
                route_candidates += self.search(expansion, kind='lore', episode=episode, limit=3)['results']
            if route == 'collecting_history':
                route_candidates += [r for r in self._items('records') if r['episode'] == episode
                                     and r.get('lore_kind') in ('history', 'collecting')
                                     and re.search(r'\b(?:origin|childhood|started|began|reacquisition|tipping point)\b',
                                                   r['title'] + ' ' + r['summary'], re.IGNORECASE)]
            elif route in ('port_classification', 'release_ideas', 'collecting_process'):
                # Reviewed lore connects dispersed topic passages. These are
                # context candidates, never a classification of every claim.
                topic_pattern = {
                    'port_classification': r'\b(?:ports?|sequels?|transition releases|collection contents)\b',
                    'release_ideas': r'\b(?:future|hypothetical|prediction|predictions|conditional want)\b',
                    'collecting_process': r'\b(?:goals?|documentation|catalog|insurance|storage|organization|organizing)\b',
                }[route]
                route_candidates += [r for r in self._items('records') if r['episode'] == episode
                                     and r['kind'] == 'lore'
                                     and re.search(topic_pattern, r['title'] + ' ' + r['summary'], re.IGNORECASE)]
        elif route == 'corrections':
            route_candidates = self.search(query, kind='correction', episode=episode, limit=6)['results']
        elif route == 'acquisitions':
            route_candidates = [c for c in self._items('claims') if c['episode'] == episode
                                and c['action_state'] in ('purchased', 'ordered', 'received')]
        elif route == 'action_states':
            states = mixed_action_states(query)
            route_candidates = [c for c in self._items('claims') if c['episode'] == episode
                                and c['action_state'] in states]
        elif route == 'open_loops':
            route_candidates = [r for r in self._items('records') if r['episode'] == episode
                                and str(r.get('lore_kind', '')).casefold() in ('open_loop', 'lead')]
            route_candidates += [c for c in self._items('claims') if c['episode'] == episode
                                 and c['action_state'] in ('wanted', 'ordered')]
        elif route == 'selection_lists':
            from lore_selections import selection_query
            selection_result = selection_query(episode_record, query)
            selection_lists = selection_result.pop('lists')
            selection_scope = selection_result
            for selection in selection_lists:
                routed_locations.update(e['location'] for e in selection['evidence'])
                for entry in selection['entries']:
                    routed_locations.update(e['location'] for e in entry['evidence'])
        for candidate in route_candidates:
            routed_locations.update(e['location'] for e in candidate['evidence'])
        locations = {e['location'] for r in structured for e in r['evidence']}
        indices.update(i for i, r in enumerate(rows) if r['title'] in locations)
        terms = set(re.findall(r'\w+', query.casefold())) - STOP
        game_ids = {r['local_id'].rsplit(':', 1)[0] for r in structured if r['kind'] == 'game'
                    and terms.intersection(re.findall(r'\w+', (r['title'] + ' ' + r['aliases']).casefold()))}
        # Explicit multiword titles must survive occurrence-row crowding. Match
        # whole source/canonical phrases, not a lone shared franchise word.
        explicit_refs = set()
        for game in episode_record.get('games', []):
            for name in [game.get('canonical_title'), *game.get('spoken_forms', [])]:
                words = re.findall(r'\w+', (name or '').casefold())
                if len(set(words) - STOP) < 2:
                    continue
                if re.search(r'\b' + r'\W+'.join(map(re.escape, words)) + r'\b', query.casefold()):
                    explicit_refs.add(game['id'])
                    break
        game_ids.update(explicit_refs)
        headings = [r['title'] for r in rows]
        if route == 'game_prominence':
            # Five leaders allow the brief to explain close runners-up; ties at
            # the cutoff stay visible instead of silently selecting one title.
            ranking = self.top_games(episode, limit=50)
            leaders = ranking['results']
            if len(leaders) > 5:
                cutoff = leaders[4]['coverage']
                ranking['results'] = [r for r in leaders if r['coverage'] >= cutoff]
            for leader in ranking['results']:
                for span in leader['spans']:
                    a = headings.index(span['start'])
                    b = len(headings) if span['end_exclusive'] == 'END' else headings.index(span['end_exclusive'])
                    routed_locations.update(headings[a:b])
        indices.update(i for i, r in enumerate(rows) if r['title'] in routed_locations)
        source_warnings = [q for q in episode_record.get('review_queue', []) if q.get('kind') == 'source_quality']
        warning_locations = {e['location'] for q in source_warnings for e in q.get('evidence', [])}
        indices.update(i for i, r in enumerate(rows) if r['title'] in warning_locations)
        for span in self._items('spans'):
            if span['episode'] == episode and game_ids.intersection(span['game_refs']):
                a = headings.index(span['start'])
                b = len(headings) if span['end_exclusive'] == 'END' else headings.index(span['end_exclusive'])
                indices.update(range(a, b))
        expanded = {j for i in indices for j in (i - 1, i, i + 1) if 0 <= j < len(rows)}
        return dict(query=query, episode=episode, matched_windows=[r['evidence'][0]['location'] for r in hits],
                    scope='processed collection only: ' + self.collection,
                    query_diagnostics=raw['query_diagnostics'],
                    route=dict(intent=route, expansion_query=expansion,
                               action_states=sorted(mixed_action_states(query)) if route == 'action_states' else [],
                               added_seed_windows=[h for h in headings if h in routed_locations],
                               explicit_reference_ids=sorted(explicit_refs),
                               numeric_topic_lore_ids=[r['id'] for r in numeric_lore],
                               scope_note='Named-actor/action/preference questions do not use whole-episode prominence.',
                               status='Heuristic evidence routing, not a certified answer'),
                    ranking=ranking,
                    selection_lists=selection_lists,
                    selection_scope=selection_scope,
                    context=[rows[i] for i in sorted(expanded)],
                    context_coverage=dict(returned_windows=len(expanded), episode_windows=len(rows)),
                    source_warnings=source_warnings,
                    warning='Read all supporting qualifications; no result does not establish absence.')

    def actions(self, speaker=None, state=None):
        # A reporting speaker is not necessarily the person who acted.
        return [c for c in self._items('claims')
                if (not speaker or speaker.casefold() in {
                    name.casefold() for name in [c.get('subject', c['speaker']['candidate']), *c.get('co_subjects', [])]
                    if isinstance(name, str)})
                and (not state or c['action_state'] == state)]

    def topics(self):
        groups = defaultdict(dict)
        for record in self._items('episodes'):
            for topic in record['topic_coverage']:
                key = topic['topic'].casefold().strip()
                old = groups[key].get(record['source']['key'])
                if old is None or DEPTH[topic['depth']] < DEPTH[old['depth']]:
                    groups[key][record['source']['key']] = {'episode': record['source']['episode_number'],
                        'date': record['source']['date'], 'depth': topic['depth'], 'locations': topic['locations']}
        return [{'topic': topic, 'substantial_episodes': sum(v['depth'] == 'SUBSTANTIAL_COVERAGE' for v in entries.values()),
                 'supporting_episodes': sum(v['depth'] == 'SUPPORTING_EXAMPLE' for v in entries.values()),
                 'first_in_processed_corpus': min(v['date'] for v in entries.values()),
                 'last_in_processed_corpus': max(v['date'] for v in entries.values()),
                 'episodes': list(entries.values()), 'saturation': 'not_adjudicated'} for topic, entries in sorted(groups.items())]

    def brief(self, query):
        hits = self.search(query, limit=30)['results']
        return {'topic': query, 'documented_history': hits,
                'corrections': [h for h in hits if h['kind'] == 'correction'],
                'jokes': [h for h in hits if h.get('lore_kind') in ('joke', 'running_joke_candidate')],
                'open_loops': [h for h in hits if str(h.get('lore_kind', '')).casefold() in ('open_loop', 'lead', 'uncertain_claim')],
                'editorial_suggestions': [], 'freshness': 'Requires editorial review; limited pilot cannot establish saturation.',
                'delivery_status': 'Evidence packet only; not a rehearsed on-air response.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['build', 'search', 'top', 'actions', 'topics', 'timeline', 'brief', 'answer-evidence'])
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--episode', type=int)
    parser.add_argument('--collection', default='pilot', help='Repository-local corpus directory, e.g. batches/002; pilot remains the default')
    parser.add_argument('--speaker')
    parser.add_argument('--entity-kind', help='Exclusive explicit span type, e.g. video_game, hardware, game_series')
    parser.add_argument('--state')
    parser.add_argument('--require-phrase', action='append', default=[])
    args = parser.parse_args()
    if args.operation in ('top', 'answer-evidence') and args.episode is None:
        parser.error('--episode is required for this operation')
    if args.operation == 'build':
        result = build(collection=args.collection)
    else:
        store = LoreStore(collection=args.collection)
        try:
            if args.operation == 'search': result = store.search(args.query, speaker=args.speaker, episode=args.episode, required_phrases=args.require_phrase, entity_kind=args.entity_kind)
            elif args.operation == 'top': result = store.top_games(args.episode)
            elif args.operation == 'actions': result = store.actions(args.speaker, args.state)
            elif args.operation == 'topics': result = store.topics()
            elif args.operation == 'timeline': result = store._items('relationships')
            elif args.operation == 'answer-evidence': result = store.answer_evidence(args.query, args.episode)
            else: result = store.brief(args.query)
        finally:
            store.close()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
