"""Behavior checks for local pilot retrieval; not semantic acceptance tests."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from search_lore_pilot import load_records, search, searchable_rows


class LorePilotSearchTests(unittest.TestCase):
    def test_topic_strings_cannot_silently_become_character_spaced_titles(self):
        record = {'source': {'episode_number': 1, 'key': 'x', 'source_url': 'local', 'path': 'x'},
                  'review': {'status': 'draft', 'timing': 'none'}, 'games': [],
                  'lore': [{'id': 'bad', 'topics': 'collection origin'}]}
        with self.assertRaisesRegex(ValueError, 'topics must be'):
            searchable_rows([record])

    @classmethod
    def setUpClass(cls):
        cls.records = load_records()

    def test_unresolved_title_stays_unresolved(self):
        result = search(self.records, 'outback joy', episode=6, kind='game', limit=1)['results'][0]
        self.assertEqual(result['title'], 'outback joy')
        self.assertEqual(result['identification_confidence'], 'low')
        self.assertEqual(result['review_status'], 'extracted_draft')
        self.assertEqual(result['evidence'][0]['location'], 'Paragraph 8')

    def test_specific_game_matches_beat_unrelated_substantial_coverage(self):
        result = search(self.records, 'Fallout 4', kind='game', limit=1)['results'][0]
        self.assertEqual(result['title'], 'Fallout 4')
        self.assertEqual(result['depth'], 'PASSING_MENTION')

    def test_supporting_examples_do_not_become_substantial(self):
        # Freeze this assertion's reviewed fixtures; new episodes may mention
        # the same game with a legitimately different discussion depth.
        fixtures = [r for r in self.records if r['source']['episode_number'] in (6, 248)]
        result = search(fixtures, 'Little Samson', kind='game', limit=10)['results']
        self.assertTrue(result)
        self.assertTrue(all(r['evidence'] for r in result))
        # Neither record actually studies the whole game; a search must not
        # convert a supporting example into substantial coverage.
        samson = [r for r in result if r['title'] == 'Little Samson']
        self.assertEqual(len(samson), 2)
        self.assertTrue(all(r['depth'] == 'SUPPORTING_EXAMPLE' for r in samson))

    def test_correction_preserves_qualified_claim(self):
        result = search(self.records, 'Canadian Zelda cutout', kind='correction', limit=1)['results'][0]
        self.assertEqual(result['id'], 'cq248-c-canadian-zelda')
        self.assertIn('needs checking', result['summary'])
        self.assertEqual(len(result['evidence']), 2)

    def test_empty_result_does_not_claim_archive_absence(self):
        result = search(self.records, 'zzzzneverindexedtoken')
        self.assertEqual(result['results'], [])
        self.assertIn('does not establish absence', result['scope_note'])

    def test_speaker_uncertainty_survives_search(self):
        result = search(self.records, 'Alice Madness Returns', episode=6, kind='game', limit=1)['results'][0]
        self.assertEqual(result['speaker']['candidate'], 'Kat')
        self.assertEqual(result['speaker']['confidence'], 'medium')

    def test_punctuation_is_not_fts_query_syntax(self):
        result = search(self.records, '"Mega Man" OR refund:*', kind='game', limit=2)
        self.assertTrue(result['results'])

    def test_inline_correction_is_searchable_without_becoming_fact(self):
        results = search(self.records, 'Terror Jack Ripper floppy', episode=300,
                         kind='correction', limit=5)['results']
        result = next(r for r in results if 'reverse' in r['summary'])
        self.assertEqual(result['lore_kind'], 'correction')
        self.assertIn('mistaken', result['summary'])
        self.assertEqual(result['review_status'], 'extracted_draft')

    def test_break_search_preserves_no_timetable(self):
        results = search(self.records, 'agreed return timetable', episode=300,
                         kind='lore', limit=5)['results']
        self.assertTrue(any('no agreed return timetable' in r['summary'] for r in results))

    def test_duplicate_upload_not_loaded(self):
        episodes = [r['source']['episode_number'] for r in self.records]
        self.assertEqual(episodes.count(263), 1)
        self.assertEqual(len(episodes), 10)

    def test_required_platform_phrase_rejects_partial_word_matches(self):
        result = search(self.records, 'Virtual Boy Halloween Johnny',
                        required_phrases=['Virtual Boy'])
        for hit in result['results']:
            text = ' '.join([hit['title'], hit['aliases'], hit['summary']]
                            + [e['quote'] for e in hit['evidence']]).lower()
            self.assertIn('virtual boy', text)

    def test_speaker_filter_does_not_upgrade_confidence(self):
        result = search(self.records, 'Jagged Alliance', episode=300, speaker='tyler')
        self.assertTrue(result['results'])
        self.assertTrue(all(r['speaker']['candidate'] == 'Tyler' for r in result['results']))
        self.assertTrue(all(r['speaker']['confidence'] == 'medium' for r in result['results']))


if __name__ == '__main__':
    unittest.main()
