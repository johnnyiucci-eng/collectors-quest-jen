"""Original-wording development regressions; no episode-specific routing code."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_store import ROOT, read, build, LoreStore
from evaluate_lore_questions import evaluate


class QuestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collections = [f'batches/{n:03d}' for n in range(3, 10)]
        for collection in cls.collections:
            build(collection=collection)

    def test_all_original_questions_without_hiding_missing_fields(self):
        result = evaluate(self.collections)
        self.assertEqual((result['passed'], result['total'], result['excluded']), (116, 116, 73))
        for collection in result['results']:
            for case in collection['cases']:
                coverage = case['context_coverage']
                self.assertLessEqual(coverage['returned_windows'], coverage['episode_windows'])

    def test_four_original_failure_windows_recovered_without_rewriting_questions(self):
        baseline = read(ROOT / 'batches/reviews/original-question-diagnostic.json')
        self.assertEqual((baseline['passed'], baseline['total']), (112, 116))
        for collection in baseline['results']:
            store = LoreStore(collection=collection['collection'])
            try:
                for case in collection['failures']:
                    episode = int(case['id'].split('cq')[1].split('-')[0])
                    result = store.answer_evidence(case['question'], episode)
                    self.assertTrue(set(case['missing_windows']) <= {r['title'] for r in result['context']})
                    self.assertNotEqual(result['route']['intent'], 'lexical')
            finally:
                store.close()

    def test_batch010_original_wording_and_retained_initial_misses(self):
        build(collection='batches/010')
        initial = read(ROOT / 'batches/010/reviews/original-wording-initial-results.json')
        self.assertEqual((initial['passed'], initial['total']), (36, 38))
        current = evaluate(['batches/010'])
        self.assertEqual((current['passed'], current['total'], current['excluded']), (38, 38, 0))

    def test_batch012_original_and_lore_channel_keep_initial_failures(self):
        build(collection='batches/012')
        initial = read(ROOT / 'batches/012/reviews/initial-retrieval-results.json')
        self.assertEqual((initial['tuned']['passed'], initial['tuned']['total']), (44, 48))
        self.assertEqual((initial['original']['passed'], initial['original']['total']), (43, 48))
        current = evaluate(['batches/012'])
        self.assertEqual((current['passed'], current['total'], current['excluded']), (48, 48, 0))
        store = LoreStore(collection='batches/012')
        try:
            bundle = store.answer_evidence('MarioMaker Pikmin3 Smash CaptainToad KirbyYarn YoshiWoolly RainbowCurse GameWario ZeldaMaker', 85)
            self.assertTrue({'Paragraph 29', 'Paragraph 34'} <= {r['title'] for r in bundle['context']})
        finally:
            store.close()

    def test_batch013_keeps_initial_misses_and_checks_reviewed_qualifications(self):
        from process_lore_batch import answers, sample_check
        build(collection='batches/013')
        initial = read(ROOT / 'batches/013/reviews/initial-retrieval-results.json')
        self.assertEqual((initial['tuned']['passed'], initial['tuned']['total']), (46, 48))
        sample = read(ROOT / 'batches/013/reviews/initial-sample-results.json')
        self.assertEqual((sample['passed'], sample['total']), (13, 14))
        current = answers(ROOT / 'batches/013', 'batches/013')
        self.assertEqual((current['passed'], current['total']), (48, 48))
        self.assertEqual(sample_check(ROOT / 'batches/013', 'batches/013')['passed'], 14)
        original = evaluate(['batches/013'])
        self.assertEqual((original['passed'], original['total'], original['excluded']), (48, 48, 0))


    def test_batch014_originals_preserve_initial_failures(self):
        from process_lore_batch import answers, sample_check
        build(collection='batches/014')
        initial = read(ROOT / 'batches/014/reviews/initial-retrieval-results.json')
        self.assertEqual((initial['tuned']['passed'], initial['original']['passed']), (51, 48))
        self.assertEqual(evaluate(['batches/014'])['passed'], 52)
        self.assertEqual(answers(ROOT / 'batches/014', 'batches/014')['passed'], 52)
        self.assertEqual(sample_check(ROOT / 'batches/014', 'batches/014')['passed'], 17)

    def test_batch015_originals_preserve_initial_failures(self):
        from process_lore_batch import answers, sample_check
        build(collection='batches/015')
        initial = read(ROOT / 'batches/015/reviews/initial-retrieval-results.json')
        self.assertEqual((initial['tuned']['passed'], initial['original']['passed']), (49, 48))
        self.assertEqual(evaluate(['batches/015'])['passed'], 50)
        self.assertEqual(answers(ROOT / 'batches/015', 'batches/015')['passed'], 50)
        self.assertEqual(sample_check(ROOT / 'batches/015', 'batches/015')['passed'], 20)


if __name__ == '__main__':
    unittest.main()
