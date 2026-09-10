"""Local full-text retrieval over the existing, source-linked Markdown library."""

import hashlib
import json
from pathlib import Path
import re
import sqlite3


class Archive:
    def __init__(self, root: Path, database: Path):
        self.root = root
        self.db = sqlite3.connect(database)
        self.db.row_factory = sqlite3.Row
        self.db.execute('CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT)')
        self.db.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS passages USING fts5(
            source_key UNINDEXED, episode UNINDEXED, location UNINDEXED,
            date UNINDEXED, source UNINDEXED, text_url UNINDEXED, title, passage,
            tokenize='porter unicode61')''')

    def build(self):
        manifest = (self.root / 'library/manifest.json').read_bytes()
        entries = json.loads(manifest)['entries']
        digest = hashlib.sha256(manifest)
        pages = []
        for entry in entries:
            path = (self.root / 'library' / entry['path']).resolve()
            if not path.is_relative_to((self.root / 'library').resolve()):
                raise ValueError('Library path leaves the library directory')
            raw = path.read_bytes()
            digest.update(raw)
            pages.append((entry, raw.decode('utf-8')))
        fingerprint = digest.hexdigest()
        previous = self.db.execute("SELECT value FROM metadata WHERE key='fingerprint'").fetchone()
        if previous is None or previous[0] != fingerprint:
            with self.db:
                self.db.execute('DELETE FROM passages')
                for entry, body in pages:
                    for section in re.split(r'\n### ', body)[1:]:
                        location, _, passage = section.partition('\n')
                        source = entry.get('primary_transcript_source') or entry['source_url']
                        if 'youtube.com/watch?' in source and re.fullmatch(r'\d+:\d{2}:\d{2}', location):
                            h, m, s = map(int, location.split(':'))
                            source += f'&t={h * 3600 + m * 60 + s}s'
                        self.db.execute('INSERT INTO passages VALUES (?,?,?,?,?,?,?,?)', (
                            entry['key'], entry['episode_number'], location, entry['date'], source,
                            'https://raw.githubusercontent.com/johnnyiucci-eng/collectors-quest-jen/main/library/' + entry['path'],
                            entry['title'], passage.strip()))
                self.db.execute("INSERT OR REPLACE INTO metadata VALUES ('fingerprint',?)", (fingerprint,))
        return {'entries': len(entries), 'passages': self.db.execute('SELECT count(*) FROM passages').fetchone()[0], 'fingerprint': fingerprint}

    def search(self, query: str, episode=None, limit=5):
        if not isinstance(query, str) or len(query) > 300:
            raise ValueError('Use a query of at most 300 characters')
        if episode is not None and (type(episode) is not int or not 0 <= episode <= 300):
            raise ValueError('Episode must be a number from 0 to 300 or null')
        terms = re.findall(r'\w+', query, flags=re.UNICODE)[:12]
        if not terms:
            raise ValueError('Search needs keywords')
        # Quoted tokens prevent callers from injecting FTS operators or column queries.
        match = ' AND '.join('"' + term + '"' for term in terms)
        sql = 'SELECT rowid AS passage_id, * FROM passages WHERE passages MATCH ?'
        params = [match]
        if episode is not None:
            sql += ' AND episode = ?'
            params.append(episode)
        sql += ' ORDER BY bm25(passages,0,0,0,0,0,0,3,1), rowid LIMIT ?'
        params.append(max(1, min(int(limit), 8)))
        return [dict(row) for row in self.db.execute(sql, params)]

    def read(self, passage_id: int):
        if type(passage_id) is not int:
            raise ValueError('Passage ID must be an integer returned by search')
        center = self.db.execute('SELECT source_key FROM passages WHERE rowid=?', (passage_id,)).fetchone()
        if center is None:
            return []
        return [dict(row) for row in self.db.execute(
            'SELECT rowid AS passage_id,* FROM passages WHERE source_key=? AND rowid BETWEEN ? AND ? ORDER BY rowid',
            (center[0], passage_id - 1, passage_id + 1))]
