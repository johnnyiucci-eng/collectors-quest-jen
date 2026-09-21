"""Archive scope and exact-review binding tests, not semantic accuracy scores."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_review_binding import make_review_binding, verify_review_binding
from query_lore_archive import catalog, LoreArchive


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content) if not isinstance(content, str) else content, encoding='utf-8')

    def collection(self, name='pilot', episode=1, key='one'):
        self.write('library/' + key + '.md', 'Original source')
        self.write(name + '/manifest.json', dict(episodes=[dict(episode_number=episode, key=key,
                   sha256='source-hash', path=key + '.md', record_path='record.json', date='2000-01-01', title='Episode')], duplicate_controls=[]))
        self.write(name + '/record.json', dict(source='reviewed record'))
        self.write(name + '/annotations.json', {})
        self.write(name + '/relationships.json', {})
        self.write(name + '/reviews/proof.md', 'Actual review')
        ledger = dict(episodes=[dict(episode=episode, checks={f'A{i}': dict(status='passed', reason='Reviewed',
                      evidence=[name + '/reviews/proof.md']) for i in range(1, 9)})])
        ledger['review_binding'] = make_review_binding(self.root, name, ledger, '2026-09-13 11:00:00 UTC')
        self.write(name + '/episode-review-ledger.json', ledger)
        return ledger

    def test_only_complete_bound_collections_enter_archive(self):
        self.collection()
        self.write('batches/010/manifest.json', {})
        result = catalog(self.root)
        self.assertEqual(result['reviewed_episode_count'], 1)
        self.assertEqual(result['excluded_collections'][0]['collection'], 'batches/010')

    def test_missing_binding_excluded_not_assumed_accepted(self):
        ledger = self.collection()
        ledger.pop('review_binding')
        self.write('pilot/episode-review-ledger.json', ledger)
        result = catalog(self.root)
        self.assertEqual(result['reviewed_episode_count'], 0)
        self.assertIn('binding missing', result['excluded_collections'][0]['reason'])

    def test_changed_source_and_manifest_do_not_reuse_acceptance(self):
        self.collection()
        self.write('library/one.md', 'Different source')
        path = self.root / 'pilot/manifest.json'
        data = json.loads(path.read_text())
        data['episodes'][0]['sha256'] = 'new-source-hash'
        self.write('pilot/manifest.json', data)
        result = catalog(self.root)
        self.assertEqual(result['reviewed_episode_count'], 0)
        self.assertIn('binding stale', result['excluded_collections'][0]['reason'])

    def test_database_rebuild_cannot_refresh_changed_review(self):
        ledger = self.collection()
        self.write('pilot/record.json', dict(source='Changed interpretation'))
        self.write('pilot/generated/lore.sqlite3', 'Rebuilt database')
        with self.assertRaisesRegex(ValueError, 'binding stale'):
            verify_review_binding(self.root, 'pilot', ledger)

    def test_rebuildable_output_alone_does_not_change_review(self):
        ledger = self.collection()
        self.write('pilot/generated/lore.sqlite3', 'Rebuilt database')
        self.assertTrue(verify_review_binding(self.root, 'pilot', ledger))

    def test_new_review_input_requires_rebinding(self):
        ledger = self.collection()
        self.write('pilot/reviews/new-annotations.json', {})
        with self.assertRaisesRegex(ValueError, 'binding stale'):
            verify_review_binding(self.root, 'pilot', ledger)

    def test_changed_approval_is_bound_too(self):
        ledger = self.collection()
        ledger['episodes'][0]['checks']['A1']['reason'] = 'Different decision'
        with self.assertRaisesRegex(ValueError, 'binding stale'):
            verify_review_binding(self.root, 'pilot', ledger)

    def test_duplicate_source_key_rejected(self):
        self.collection()
        self.collection('batches/002', 2, 'one')
        with self.assertRaisesRegex(ValueError, 'Duplicate source keys'):
            catalog(self.root)

    def test_episode_versions_are_not_double_counted_or_silently_chosen(self):
        self.collection()
        self.collection('batches/002', 1, 'different')
        archive = LoreArchive(self.root)
        self.assertEqual(archive.catalog['reviewed_episode_count'], 1)
        self.assertEqual(archive.catalog['reviewed_source_count'], 2)
        with self.assertRaisesRegex(ValueError, 'multiple reviewed source versions'):
            archive.answer_evidence('game', 1)

    def test_absent_episode_is_not_archive_absence(self):
        self.collection()
        with self.assertRaisesRegex(ValueError, 'does not mean archive absence'):
            LoreArchive(self.root).top_games(2)

    def test_outside_evidence_rejected(self):
        ledger = self.collection()
        ledger['episodes'][0]['checks']['A1']['evidence'] = ['../outside.md']
        self.write('pilot/episode-review-ledger.json', ledger)
        with self.assertRaisesRegex(ValueError, 'Invalid review evidence path'):
            catalog(self.root)

    def test_query_preserves_store_freshness_failure(self):
        self.collection()
        with patch('query_lore_archive.LoreStore', side_effect=ValueError('stale database')):
            with self.assertRaisesRegex(ValueError, 'stale database'):
                LoreArchive(self.root).search('game')

    def test_archive_merge_preserves_title_relevance_across_collections(self):
        self.collection()
        self.collection('batches/002', 2, 'two')
        calls = []
        class Store:
            def __init__(self, root, collection):
                self.collection = collection
            def search(self, query, **kwargs):
                calls.append(kwargs)
                title = 'Wii Sports' if self.collection == 'pilot' else 'Mario Party'
                return {'results': [dict(id=self.collection, title=title, aliases='', summary='',
                                          evidence=[dict(quote='Wii Sports was compared here.')])]}
            def close(self):
                pass
        with patch('query_lore_archive.LoreStore', Store):
            result = LoreArchive(self.root).search('Wii Sports', entity_kind='video_game')
        self.assertEqual(result['results'][0]['title'], 'Wii Sports')
        self.assertTrue(all(c['entity_kind'] == 'video_game' for c in calls))
        self.assertIn('title/alias', result['merge_method'])


if __name__ == '__main__':
    unittest.main()
