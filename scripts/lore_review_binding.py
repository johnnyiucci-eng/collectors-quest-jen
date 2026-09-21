"""Bind human review to exact local evidence inputs, independently of database builds."""
import hashlib
import json
from pathlib import Path

from lore_store import ROOT, read
from search_lore_pilot import collection_path

VERSION = 'cq-review-binding-1'


def review_fingerprint(root, collection, ledger):
    root = Path(root).resolve()
    base = collection_path(root, collection)
    manifest_path = base / 'manifest.json'
    manifest = read(manifest_path)
    paths = {manifest_path, base / 'relationships.json', base / 'annotations.json'}
    paths.update((base / 'reviews').glob('*.json'))
    if (base / 'answer-cases.json').is_file():
        paths.add(base / 'answer-cases.json')
    for entry in manifest['episodes'] + manifest.get('duplicate_controls', []):
        source = (root / 'library' / entry['path']).resolve()
        if not source.is_relative_to((root / 'library').resolve()):
            raise ValueError('Review source outside library')
        paths.add(source)
        if entry.get('record_path'):
            record = (base / entry['record_path']).resolve()
            if not record.is_relative_to(base):
                raise ValueError('Review record outside collection')
            paths.add(record)
    for episode in ledger['episodes']:
        for check in episode['checks'].values():
            paths.update(root / p for p in check.get('evidence', []))
    # The binding itself is excluded to avoid a self-referential hash. Review
    # decisions/reasons are included; a changed approval is also a new review.
    decision = {k: v for k, v in ledger.items() if k != 'review_binding'}
    digest = hashlib.sha256(VERSION.encode())
    digest.update(json.dumps(decision, sort_keys=True, ensure_ascii=False).encode('utf-8'))
    resolved = sorted({p.resolve() for p in paths}, key=lambda p: str(p))
    for path in resolved:
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Review input missing or outside repository')
        digest.update(path.relative_to(root).as_posix().encode('utf-8'))
        digest.update(b'\0')
        digest.update(path.read_bytes())
        digest.update(b'\0')
    return digest.hexdigest()


def make_review_binding(root, collection, ledger, reviewed_utc):
    """Prepare an explicit review attestation; never write or auto-approve it."""
    return dict(version=VERSION, sha256=review_fingerprint(root, collection, ledger),
                reviewed_utc=reviewed_utc,
                meaning='Exact reviewed local inputs; not independent semantic, audio or live certification')


def verify_review_binding(root, collection, ledger):
    binding = ledger.get('review_binding')
    if not binding or binding.get('version') != VERSION or not binding.get('reviewed_utc'):
        raise ValueError('Review binding missing; explicit input review required')
    if binding.get('sha256') != review_fingerprint(root, collection, ledger):
        raise ValueError('Review binding stale; changed inputs need review, not just a database rebuild')
    return True
