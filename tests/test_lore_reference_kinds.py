"""Strict evidence-window entity scope, independent of legacy reference labels."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_store import annotate_reference_kinds, build, LoreStore


class ReferenceKindTests(unittest.TestCase):
    def row(self, locations=('P1',)):
        return dict(kind='game', local_id='g1:0', source_key='s',
                    evidence=[dict(location=p, quote='x') for p in locations])

    def span(self, kind=None, start='P1', end='P2'):
        result = dict(source_key='s', game_refs=['g1'], start=start, end_exclusive=end)
        if kind is not None:
            result['entity_kind'] = kind
        return result

    def annotate(self, row, spans):
        annotate_reference_kinds([row], spans, {'s': {'P1': 'x', 'P2': 'y'}})
        return row

    def test_hardware_does_not_become_a_game_from_legacy_label(self):
        row = self.annotate(self.row(), [self.span('hardware')])
        self.assertEqual((row['entity_kind_status'], row['entity_kinds']), ('typed', ['hardware']))
        self.assertEqual(row['kind'], 'game')  # Compatibility label is disclosed.

    def test_other_occurrence_of_same_reference_does_not_leak_kind(self):
        row = self.annotate(self.row(), [self.span('hardware'), self.span('video_game', 'P2', 'END')])
        self.assertEqual(row['entity_kinds'], ['hardware'])

    def test_mixed_evidenced_windows_are_not_exclusive_games(self):
        row = self.annotate(self.row(('P1', 'P2')), [self.span('hardware'), self.span('video_game', 'P2', 'END')])
        self.assertEqual(row['entity_kind_status'], 'mixed')

    def test_legacy_missing_kind_is_not_defaulted_to_game(self):
        row = self.annotate(self.row(), [self.span()])
        self.assertEqual((row['entity_kind_status'], row['entity_kinds']), ('incomplete', []))

    def test_partially_unmapped_evidence_remains_incomplete(self):
        row = self.annotate(self.row(('P1', 'P2')), [self.span('video_game')])
        self.assertEqual(row['entity_kind_status'], 'incomplete')

    def test_real_store_filter_excludes_hardware_and_preserves_game(self):
        build(collection='batches/011')
        store = LoreStore(collection='batches/011')
        try:
            hardware = store.search('Nintendo Wii', episode=210, entity_kind='hardware', limit=50)['results']
            self.assertTrue(hardware)
            self.assertTrue(all(r['entity_kinds'] == ['hardware'] for r in hardware))
            games = store.search('Wii Sports', episode=210, entity_kind='video_game', limit=50)['results']
            self.assertTrue(any(r['title'] == 'Wii Sports' for r in games))
            self.assertTrue(all(r['entity_kinds'] == ['video_game'] for r in games))
            self.assertFalse(store.search('Wii Sports', episode=210, entity_kind='invented_type')['results'])
        finally:
            store.close()


if __name__ == '__main__':
    unittest.main()
