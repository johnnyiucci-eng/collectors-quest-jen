"""Typed list membership and conservative query scope regressions."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_selections import validate_selection_lists, matching_selection_lists
from lore_store import question_route, ROOT, read, windows


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.source = {'P1': 'A was picked. B was a joke.'}
        proof = dict(location='P1', quote='A was picked.')
        self.record = dict(games=[dict(id='a'), dict(id='b')], selection_lists=[dict(
            id='list', label='Starter shelf', subject='Alex', purpose='starter', summary='Representative shelf',
            evidence=[proof], entries=[dict(game_ref='a', status='selected', ordinal=1,
                                           reason='Explicit choice', evidence=[proof])])])

    def test_absent_lists_are_not_invented(self):
        self.assertEqual(validate_selection_lists(dict(games=[]), {}), 0)
        self.assertEqual(matching_selection_lists({}, 'both starter lists'), [])

    def test_known_member_with_exact_evidence(self):
        self.assertEqual(validate_selection_lists(self.record, self.source), 1)

    def test_unknown_identity_rejected(self):
        self.record['selection_lists'][0]['entries'][0]['game_ref'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'Unknown or repeated'):
            validate_selection_lists(self.record, self.source)

    def test_joke_cannot_have_selected_ordinal(self):
        self.record['selection_lists'][0]['entries'][0]['status'] = 'joke'
        with self.assertRaisesRegex(ValueError, 'ordinal'):
            validate_selection_lists(self.record, self.source)

    def test_unsupported_evidence_rejected(self):
        self.record['selection_lists'][0]['entries'][0]['evidence'][0]['quote'] = 'B was purchased'
        with self.assertRaisesRegex(ValueError, 'Unsupported selection evidence'):
            validate_selection_lists(self.record, self.source)

    def test_actual_lists_preserve_purpose_and_joke_boundaries(self):
        record = read(ROOT / 'batches/010/records/sc-1391155801.json')
        self.assertEqual(validate_selection_lists(record, windows(ROOT, record['source'])), 29)
        starter = matching_selection_lists(record, 'What are both starter lists?')
        self.assertEqual(len(starter), 2)
        self.assertEqual([sum(e['status'] == 'selected' for e in g['entries']) for g in starter], [10, 10])
        self.assertEqual(sum(e['status'] == 'joke' for g in starter for e in g['entries']), 3)
        self.assertEqual(len(matching_selection_lists(record, 'Tyler aspirational picks')), 1)

    def test_actual_list_scope_constraints(self):
        record = read(ROOT / 'batches/010/records/sc-1391155801.json')
        cases = [('both ten-game lists', ['cq209-list-1', 'cq209-list-2']),
                 ('Tyler hot picks', []), ('Tyler strive picks', ['cq209-list-3']),
                 ('Johnny starter list, not aspirational', ['cq209-list-2']),
                 ('Stephan starter list', []), ("Stephan's starter list", []),
                 ("What were Tyler's strive picks?", ['cq209-list-3']),
                 ("Show Johnny's starter list, not his aspirational picks", ['cq209-list-2'])]
        for query, expected in cases:
            with self.subTest(query=query):
                self.assertEqual([g['id'] for g in matching_selection_lists(record, query)], expected)


class RouteScopeTests(unittest.TestCase):
    def test_excluded_recommendation_is_not_main_question_constraint(self):
        self.assertEqual(question_route('Which games had the most discussion, rather than which ones did they recommend?')[0], 'game_prominence')
        self.assertEqual(question_route('Which games did Alex discuss most, rather than recommend?', ['Alex'])[0], 'lexical')
        self.assertEqual(question_route('Which games did they recommend instead of discussing the most?')[0], 'lexical')

    def test_release_and_process_context_routes(self):
        self.assertEqual(question_route('Were all those games actually ports?')[0], 'port_classification')
        self.assertEqual(question_route('What did they want to see released?')[0], 'release_ideas')
        self.assertEqual(question_route('What process did they recommend instead of buying more games?')[0], 'collecting_process')
        self.assertEqual(question_route('What exactly did Alex preorder?')[0], 'acquisitions')
        self.assertEqual(question_route('What should Alex preorder?')[0], 'lexical')

    def test_acquisition_and_integrity_routes_preserve_action_limits(self):
        self.assertEqual(question_route('Which new games did Alex buy?')[0], 'acquisitions')
        self.assertEqual(question_route('Why can a complete-looking game have mismatched parts?')[0], 'edition_integrity')
        self.assertEqual(question_route('Which plans were still only plans?')[0], 'open_loops')

    def test_shared_launch_list_and_named_reaction_remain_separate(self):
        record = read(ROOT / 'batches/011/records/sc-1400207374.json')
        groups = matching_selection_lists(record, 'What launch games did they list, and which did Tyler single out?')
        self.assertEqual({g['id'] for g in groups}, {'cq210-list-launch', 'cq210-list-launch-core'})
        self.assertEqual([g['id'] for g in matching_selection_lists(record, 'Tyler launch list')], ['cq210-list-launch-core'])
        self.assertEqual(validate_selection_lists(record, windows(ROOT, record['source'])), 54)

    def test_origin_and_correction_intents(self):
        self.assertEqual(question_route('When did Alex become a collector?')[0], 'collecting_history')
        self.assertEqual(question_route('What did they correct about compilation game lists?')[0], 'corrections')
        self.assertEqual(question_route('Which collector bought this game?')[0], 'lexical')

    def test_user_discussion_wording(self):
        self.assertEqual(question_route('Which games were talked about the most?')[0], 'game_prominence')

    def test_bare_top_with_episode_scope(self):
        self.assertEqual(question_route('What are the top three games in episode 123?')[0], 'game_prominence')

    def test_purchase_preference_and_actor_are_not_episode_popularity(self):
        for query in ['What are the top three games Tyler wanted to buy?',
                      'Which games did Alex discuss the most?',
                      'Which games had the most discussion by Alex?',
                      'What are the top three games he played?',
                      'Which games were talked about the most by the guest?',
                      'What are the top three games Alex owns?']:
            with self.subTest(query=query):
                self.assertEqual(question_route(query, ['Alex', 'Tyler'])[0], 'lexical')

    def test_other_media_are_not_game_popularity(self):
        self.assertEqual(question_route('Which movies got the most discussion?')[0], 'lexical')

    def test_list_membership_not_discussion_prominence(self):
        self.assertEqual(question_route('What are the two ten-game starter lists, and why do they differ?')[0], 'selection_lists')

    def test_hunting_is_open_evidence_not_certified_purchase(self):
        self.assertEqual(question_route('What is he still hunting for after finishing the regular games?')[0], 'open_loops')


if __name__ == '__main__':
    unittest.main()
