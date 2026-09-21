"""Read-only queries across reviewed local collections; never import private history."""
import argparse
import json
from pathlib import Path
import re

from lore_store import ROOT, LoreStore, read, query_terms
from lore_review_binding import verify_review_binding


def catalog(root=ROOT):
    """Resolve reviewed episodes without changing pilot or batch denominators."""
    root = Path(root).resolve()
    candidates = [root / 'pilot']
    batch_root = root / 'batches'
    if batch_root.is_dir():
        candidates += sorted(p for p in batch_root.iterdir() if p.is_dir() and re.fullmatch(r'\d{3}', p.name))
    episodes, excluded = [], []
    for base in candidates:
        collection = base.relative_to(root).as_posix()
        if not base.resolve().is_relative_to(root):
            raise ValueError('Collection outside repository')
        manifest_path, ledger_path = base / 'manifest.json', base / 'episode-review-ledger.json'
        if not manifest_path.is_file() or not ledger_path.is_file():
            excluded.append(dict(collection=collection, reason='No complete review ledger'))
            continue
        if any(not p.resolve().is_relative_to(root) for p in (manifest_path, ledger_path)):
            raise ValueError('Review metadata outside repository')
        manifest, ledger = read(manifest_path), read(ledger_path)
        selected = manifest['episodes']
        reviewed = ledger['episodes']
        expected = {e['episode_number'] for e in selected}
        if len(selected) != len(expected) or len(reviewed) != len(expected) or {e['episode'] for e in reviewed} != expected:
            excluded.append(dict(collection=collection, reason='Episode review coverage incomplete'))
            continue
        complete = True
        for entry in reviewed:
            checks = entry.get('checks', {})
            if set(checks) != {f'A{i}' for i in range(1, 9)}:
                complete = False
                break
            for check in checks.values():
                if check.get('status') != 'passed' or not check.get('reason') or not check.get('evidence'):
                    complete = False
                    break
                for evidence in check['evidence']:
                    path = (root / evidence).resolve()
                    if not path.is_relative_to(root) or not path.is_file():
                        raise ValueError('Invalid review evidence path in ' + collection)
        if not complete:
            excluded.append(dict(collection=collection, reason='Required review checks not passed'))
            continue
        try:
            verify_review_binding(root, collection, ledger)
        except ValueError as error:
            excluded.append(dict(collection=collection, reason=str(error)))
            continue
        episodes.extend(dict(collection=collection, episode=e['episode_number'], source_key=e['key'],
                             source_sha256=e['sha256'], date=e['date'], title=e['title']) for e in selected)
    if len({e['source_key'] for e in episodes}) != len(episodes):
        raise ValueError('Duplicate source keys across reviewed collections; reconcile before archive query')
    episodes.sort(key=lambda e: (e['episode'], e['collection']))
    return dict(episodes=episodes, reviewed_episode_count=len({e['episode'] for e in episodes}),
                reviewed_source_count=len(episodes), excluded_collections=excluded,
                warning='Reviewed local collections only; not the full archive. Catalog verifies bound review metadata; queries also verify database freshness.')


class LoreArchive:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()
        self.catalog = catalog(self.root)

    def _episode_collection(self, episode):
        matches = [e for e in self.catalog['episodes'] if e['episode'] == episode]
        if not matches:
            raise ValueError(f'Episode {episode} is not in the reviewed local scope; this does not mean archive absence')
        if len(matches) != 1:
            raise ValueError(f'Episode {episode} has multiple reviewed source versions; choose a collection explicitly')
        return matches[0]['collection']

    def answer_evidence(self, query, episode):
        collection = self._episode_collection(episode)
        store = LoreStore(self.root, collection=collection)
        try:
            return store.answer_evidence(query, episode)
        finally:
            store.close()

    def top_games(self, episode):
        collection = self._episode_collection(episode)
        store = LoreStore(self.root, collection=collection)
        try:
            return {**store.top_games(episode), 'collection': collection}
        finally:
            store.close()

    def search(self, query, speaker=None, limit=10, entity_kind=None):
        terms = query_terms(query)['effective_terms']
        hits = []
        for collection in sorted({e['collection'] for e in self.catalog['episodes']}):
            store = LoreStore(self.root, collection=collection)
            try:
                for position, hit in enumerate(store.search(query, speaker=speaker, limit=limit, entity_kind=entity_kind)['results']):
                    text = ' '.join([hit['title'], hit['aliases'], hit['summary']] + [e['quote'] for e in hit['evidence']]).casefold()
                    matches = sum(bool(re.search(r'\b' + re.escape(t) + r'\b', text)) for t in terms)
                    title_text = (hit['title'] + ' ' + hit['aliases']).casefold()
                    title_matches = sum(bool(re.search(r'\b' + re.escape(t) + r'\b', title_text)) for t in terms)
                    hits.append((matches, title_matches, position, collection, hit))
            finally:
                store.close()
        # BM25 values from independent corpora are not comparable. Disclose the
        # deterministic lexical/within-collection merge instead of mixing them.
        hits.sort(key=lambda r: (-r[0], -r[1], r[2], r[3], r[4]['id']))
        return dict(query=query, query_diagnostics=query_terms(query),
                    entity_kind_filter=entity_kind,
                    entity_kind_note='Exclusive typed evidence-window filter; mixed/untyped legacy references excluded. Coarse game kind means a legacy reference bucket.',
                    reviewed_episode_count=self.catalog['reviewed_episode_count'],
                    excluded_collections=self.catalog['excluded_collections'],
                    results=[dict(hit, collection=collection) for _, _, _, collection, hit in hits[:max(1, min(limit, 50))]],
                    merge_method='Matched-term count, title/alias term count, then within-collection rank; not cross-corpus BM25 or semantic confidence.',
                    warning=self.catalog['warning'])

    def actions(self, speaker=None, state=None):
        result = []
        for collection in sorted({e['collection'] for e in self.catalog['episodes']}):
            store = LoreStore(self.root, collection=collection)
            try:
                result.extend(dict(c, collection=collection) for c in store.actions(speaker, state))
            finally:
                store.close()
        return dict(reviewed_episode_count=self.catalog['reviewed_episode_count'], results=result,
                    excluded_collections=self.catalog['excluded_collections'],
                    warning='Historical action claims in reviewed local scope, not a resolved present-day inventory or archive-wide absence finding. Preserve returns and qualifications.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['catalog', 'search', 'answer-evidence', 'top', 'actions'])
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--episode', type=int)
    parser.add_argument('--speaker')
    parser.add_argument('--entity-kind', help='Exclusive explicit span type, e.g. video_game or hardware')
    parser.add_argument('--state')
    args = parser.parse_args()
    archive = LoreArchive()
    if args.operation in ('answer-evidence', 'top') and args.episode is None:
        parser.error('--episode is required')
    if args.operation == 'catalog': result = archive.catalog
    elif args.operation == 'search': result = archive.search(args.query, args.speaker, entity_kind=args.entity_kind)
    elif args.operation == 'answer-evidence': result = archive.answer_evidence(args.query, args.episode)
    elif args.operation == 'top': result = archive.top_games(args.episode)
    else: result = archive.actions(args.speaker, args.state)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
