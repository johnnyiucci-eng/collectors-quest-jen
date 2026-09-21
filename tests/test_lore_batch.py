"""Batch002 regressions; fixed pilot remains a separate collection."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_store import ROOT, LoreStore, build, read
from process_lore_batch import answers, sample_check, check_records, check_fragment_evidence


class Batch002Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ROOT / 'batches/002'
        build(collection='batches/002')
        cls.store = LoreStore(collection='batches/002')

    @classmethod
    def tearDownClass(cls):
        cls.store.close()

    def test_fixed_pilot_and_batch_are_separate(self):
        self.assertEqual(len(read(ROOT / 'pilot/manifest.json')['episodes']), 10)
        episodes = {r['source']['episode_number'] for r in self.store._items('episodes')}
        self.assertEqual(episodes, {8, 75, 201})
        self.assertEqual(self.store.top_games(6)['status'], 'not_processed')

    def test_fallout_loaded_does_not_mean_played(self):
        played = [c for c in self.store.actions('Johnny', 'played') if c['episode'] == 8]
        self.assertFalse(any('fallout' in c.get('title', '').lower() for c in played))
        self.assertTrue(any('tomb raider' in c.get('title', '').lower() for c in played))

    def test_roster_uses_source_not_era_guess(self):
        records = {r['source']['episode_number']:r for r in self.store._items('episodes')}
        self.assertEqual({p['name'] for p in records[8]['participants']}, {'Johnny', 'Kat'})
        self.assertEqual({p['name'] for p in records[75]['participants']}, {'Johnny', 'Tyler'})

    def test_corrupted_tail_does_not_gain_coverage(self):
        for span in self.store._items('spans'):
            if span['episode'] != 75 or span['role'] not in ('SUBSTANTIAL_COVERAGE', 'SUPPORTING_EXAMPLE'):
                continue
            a, b = span['interval']
            self.assertFalse(a <= 56 < b or a <= 57 < b)

    def test_source_warning_is_retrieved_without_inflating_spans(self):
        bundle = self.store.answer_evidence('Rondo inverted castle', 75)
        self.assertTrue(any(q['id'] == 'cq075-source-repetition' for q in bundle['source_warnings']))
        self.assertIn('Paragraph 58', [r['title'] for r in bundle['context']])

    def test_complete_answers_retrieve_required_context(self):
        result = answers(self.base, 'batches/002')
        self.assertGreaterEqual(result['total'], 9)
        self.assertEqual(result['passed'], result['total'])

    def test_fresh_sample_references_remain_mapped(self):
        result = sample_check(self.base, 'batches/002')
        self.assertEqual(result['total'], 27)
        self.assertEqual(result['passed'], 27)

    def test_stadium_passing_mentions_do_not_inflate_prominence(self):
        game = next(r for r in self.store.top_games(201, limit=200)['results']
                    if r['title'] == 'Stadium Events')
        self.assertEqual(game['coverage'], 451)
        self.assertEqual(game['substantial_coverage'], 129)
        spans = [s for s in self.store._items('spans')
                 if s['episode'] == 201 and s['title'] == 'Stadium Events']
        self.assertEqual(len(spans), 9)
        self.assertTrue(any(s['role'] == 'PASSING_MENTION' for s in spans))

    def test_all_source_and_review_quotes_are_exact(self):
        self.assertGreater(check_records(self.base), 0)
        self.assertGreater(check_fragment_evidence(self.base), 0)


if __name__ == '__main__':
    unittest.main()
