"""Private local history and explicitly approved notes; no global memory."""

from datetime import datetime, timezone
from pathlib import Path
import sqlite3


def private_directory(root: Path, requested: Path):
    target = requested.expanduser().resolve()
    if target.is_relative_to(root.resolve()):
        raise ValueError('Private agent data must be outside the public repository')
    target.mkdir(parents=True, exist_ok=True)
    return target


class State:
    def __init__(self, path: Path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA secure_delete=ON')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS turns (
                id INTEGER PRIMARY KEY, owner TEXT, session TEXT, user TEXT,
                assistant TEXT, created TEXT, profile_hash TEXT);
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY, owner TEXT, session TEXT, text TEXT,
                created TEXT, source TEXT, status TEXT);
        ''')

    def history(self, owner, session, budget=24000):
        rows = self.db.execute('SELECT user,assistant FROM turns WHERE owner=? AND session=? ORDER BY id DESC LIMIT 20', (owner, session)).fetchall()
        pairs, used = [], 0
        for row in rows:
            size = len(row['user']) + len(row['assistant'])
            if used + size > budget:
                break
            pairs.append([{'role': 'user', 'content': row['user']}, {'role': 'assistant', 'content': row['assistant']}])
            used += size
        return [message for pair in reversed(pairs) for message in pair]

    def append(self, owner, session, user, assistant, profile_hash):
        with self.db:
            self.db.execute('INSERT INTO turns(owner,session,user,assistant,created,profile_hash) VALUES (?,?,?,?,?,?)',
                            (owner, session, user, assistant, datetime.now(timezone.utc).isoformat(), profile_hash))

    def notes(self, owner, session):
        return [dict(r) for r in self.db.execute('SELECT id,text,created,source,status FROM notes WHERE owner=? AND session=? ORDER BY id', (owner, session))]

    def remember(self, owner, session, text):
        if not text.strip() or len(text) > 1200:
            raise ValueError('A note must contain 1–1200 characters')
        if len(self.notes(owner, session)) >= 30:
            raise ValueError('This session has 30 saved notes; remove outdated notes first')
        with self.db:
            row = self.db.execute('INSERT INTO notes(owner,session,text,created,source,status) VALUES (?,?,?,?,?,?)',
                                 (owner, session, text.strip(), datetime.now(timezone.utc).isoformat(), 'explicit local /remember command', 'approved by local user'))
        return row.lastrowid

    def forget(self, owner, session, note_id):
        with self.db:
            return self.db.execute('DELETE FROM notes WHERE owner=? AND session=? AND id=?', (owner, session, note_id)).rowcount == 1

    def clear_history(self, owner, session):
        with self.db:
            self.db.execute('DELETE FROM turns WHERE owner=? AND session=?', (owner, session))
