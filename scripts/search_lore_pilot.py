"""Search draft pilot lore locally. Standard library only; no persistent writes."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import time

ROOT = Path(__file__).resolve().parents[1]
STOP = set('a an and are as at be been did do does for from had has have how i in is it its me of on or our that the their them there these they this to was we were what when where which who why with would you your'.split())
DEPTH = {'SUBSTANTIAL_COVERAGE': 0, 'SUPPORTING_EXAMPLE': 1,
         'PASSING_MENTION': 2, 'JOKE_ASIDE': 3}


def collection_path(root, collection='pilot'):
    base = (root / collection).resolve()
    if base == root.resolve() or not base.is_relative_to(root.resolve()):
        raise ValueError('Collection must be a directory within the repository')
    return base


def load_records(root=ROOT, collection='pilot'):
    base = collection_path(root, collection)
    manifest = json.loads((base / 'manifest.json').read_text(encoding='utf-8'))
    records = []
    for entry in manifest['episodes']:
        if not entry.get('record_path'):
            continue
        record_path = (base / entry['record_path']).resolve()
        source_path = (root / 'library' / entry['path']).resolve()
        if not record_path.is_relative_to(base) or not source_path.is_relative_to(root / 'library'):
            raise ValueError('Pilot path leaves its data directory')
        record = json.loads(record_path.read_text(encoding='utf-8'))
        actual = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if actual != entry['sha256'] or record['source']['sha256'] != actual:
            raise ValueError(f"Stale source: {entry['key']}; review before retrieval")
        records.append(record)
    return records


def searchable_rows(records):
    rows = []
    for record in records:
        source = record['source']
        common = {'episode': source['episode_number'], 'source_key': source['key'],
                  'source_url': source['source_url'], 'transcript_path': 'library/' + source['path'],
                  'review_status': record['review']['status'],
                  'timing_note': record['review']['timing']}
        for game in record['games']:
            for group_number, group in enumerate(game['occurrence_groups']):
                title = game['canonical_title'] or ' / '.join(game['spoken_forms'])
                rows.append({**common, 'id': game['id'] + ':' + str(group_number), 'kind': 'game',
                             'title': title, 'aliases': ' '.join(game['spoken_forms']),
                             'summary': group['context'], 'depth': group['type'],
                             'entity_granularity': game['entity_granularity'],
                             'identification_confidence': game['identification_confidence'],
                             'speaker': group['speaker'], 'evidence': group['evidence']})
        for group in record.get('selection_lists', []):
            titles = {g['id']: g['canonical_title'] or ' / '.join(g['spoken_forms']) for g in record['games']}
            membership = '; '.join(e['status'] + ': ' + titles[e['game_ref']] for e in group['entries'])
            rows.append({**common, 'id': group['id'], 'kind': 'lore', 'title': group['label'],
                         'aliases': '', 'summary': group['summary'] + ' Membership: ' + membership,
                         'depth': None, 'lore_kind': 'selection_list',
                         'speaker': {'candidate': group['subject'], 'confidence': 'contextual'},
                         'evidence': group['evidence'] + [p for e in group['entries'] for p in e['evidence']]})
        for item in record['lore']:
            if (not isinstance(item.get('topics'), list) or not item['topics']
                    or any(not isinstance(t, str) or not t.strip() for t in item['topics'])):
                raise ValueError('Lore topics must be a nonempty string array: ' + item['id'])
            # A correction extracted during the same conversation must be
            # discoverable by the correction filter without duplicating it.
            row_kind = 'correction' if item['kind'] == 'correction' else 'lore'
            rows.append({**common, 'id': item['id'], 'kind': row_kind, 'title': ' '.join(item['topics']),
                         'aliases': '', 'summary': item['summary'], 'depth': None,
                         'lore_kind': item['kind'], 'speaker': item['speaker'], 'evidence': item['evidence']})
        for item in record.get('corrections', []):
            rows.append({**common, 'id': item['id'], 'kind': 'correction', 'title': item['category'],
                         'aliases': '', 'summary': item['original'] + ' Clarification: ' + item['current'],
                         'depth': None, 'speaker': item['speaker'], 'evidence': item['evidence']})
    return rows


def search(records, query, episode=None, kind=None, limit=5, required_phrases=None, speaker=None):
    terms = list(dict.fromkeys(t for t in re.findall(r'\w+', query.lower()) if t not in STOP))[:16]
    if not terms:
        raise ValueError('Provide a game, topic, phrase, or other meaningful search terms')
    rows = [r for r in searchable_rows(records)
            if (episode is None or r['episode'] == episode) and (kind is None or r['kind'] == kind)
            and (speaker is None or (r['speaker'].get('candidate') or '').casefold() == speaker.casefold())]
    for phrase in required_phrases or []:
        phrase_terms = re.findall(r'\w+', phrase.casefold())
        if not phrase_terms:
            raise ValueError('Required phrases must contain words')
        pattern = r'\b' + r'\W+'.join(re.escape(t) for t in phrase_terms) + r'\b'
        rows = [r for r in rows if re.search(pattern, ' '.join(
            (r['title'], r['aliases'], r['summary'], ' '.join(e['quote'] for e in r['evidence']))).casefold())]
    # An ephemeral index keeps the existing archive and private databases untouched.
    db = sqlite3.connect(':memory:')
    try:
        db.execute("CREATE VIRTUAL TABLE hits USING fts5(title, aliases, summary, evidence, tokenize='porter unicode61')")
        for index, row in enumerate(rows):
            db.execute('INSERT INTO hits(rowid,title,aliases,summary,evidence) VALUES(?,?,?,?,?)',
                       (index + 1, row['title'], row['aliases'], row['summary'],
                        ' '.join(e['quote'] for e in row['evidence'])))
        expression = ' OR '.join('"' + term + '"' for term in terms)
        candidates = []
        for rowid, score in db.execute('SELECT rowid,bm25(hits,5,4,2,1) FROM hits WHERE hits MATCH ?', (expression,)):
            row = rows[rowid - 1]
            content = ' '.join((row['title'], row['aliases'], row['summary'],
                                ' '.join(e['quote'] for e in row['evidence']))).lower()
            matches = sum(bool(re.search(r'\b' + re.escape(term) + r'\b', content)) for term in terms)
            title_text = (row['title'] + ' ' + row['aliases']).lower()
            title_matches = sum(bool(re.search(r'\b' + re.escape(term) + r'\b', title_text)) for term in terms)
            candidates.append((matches, title_matches, DEPTH.get(row['depth'], 1), score, row))
        # More query terms must match before depth breaks ties. A substantial
        # unrelated discussion must not outrank a specific incidental reference.
        # A title mentioned only as an uncertain candidate in a summary must
        # not outrank a directly identified title solely because its discussion is longer.
        candidates.sort(key=lambda v: (-v[0], -v[1], v[2], v[3], v[4]['source_key'], v[4]['id']))
        results = []
        for matches, _, _, _, row in candidates[:max(1, min(limit, 25))]:
            row = dict(row)
            row['matched_query_terms'] = matches
            row['evidence'] = [{**e, 'transcript_url':
                'https://github.com/johnnyiucci-eng/collectors-quest-jen/blob/main/' + row['transcript_path']
                + '#' + e['location'].lower().replace(' ', '-').replace(':', '')} for e in row['evidence']]
            results.append(row)
        return {'processed_episodes': sorted({r['source']['episode_number'] for r in records}),
                'filters': {'episode': episode, 'kind': kind, 'speaker_candidate': speaker,
                            'required_phrases': required_phrases or []},
                'query': query, 'scope_note': 'Results cover extracted pilot records only, including drafts. '
                "Legacy kind='game' denotes reference buckets, including hardware/media; use the persistent store entity-kind filter for exclusive typed game results. "
                'No hit does not establish absence from CQ. Ranking is lexical, not semantic; confidence labels are retained. '
                'Speaker filtering excludes unknown candidates and does not upgrade attribution confidence.',
                'results': results}
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--episode', type=int)
    parser.add_argument('--kind', choices=['game', 'lore', 'correction'])
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--require-phrase', action='append', default=[])
    parser.add_argument('--speaker', help='Filter contextual speaker candidate; unknown speakers are excluded')
    args = parser.parse_args()
    started = time.perf_counter()
    result = search(load_records(), args.query, args.episode, args.kind, args.limit,
                    args.require_phrase, args.speaker)
    result['local_load_and_search_ms'] = round((time.perf_counter() - started) * 1000, 2)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
