"""Storage/query regressions. Synthetic fixtures are not archive accuracy evidence."""

import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_store import ROOT, LoreStore, build, union_length


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ('pilot/records', 'library', 'scripts'):
            (self.root / directory).mkdir(parents=True)
        (self.root / 'scripts/search_lore_pilot.py').write_bytes((ROOT / 'scripts/search_lore_pilot.py').read_bytes())
        transcript = '### 00:00:00\nAlpha wanted. Beta mentioned.\n### 00:01:00\nAlpha discussed.\n### 00:02:00\nUnrelated.\n### 00:03:00\nAlpha returned.\n### 00:04:00\nEnd.\n'
        (self.root / 'library/source.md').write_text(transcript, encoding='utf-8')
        self.sha = hashlib.sha256((self.root / 'library/source.md').read_bytes()).hexdigest()
        self.source = dict(key='source', episode_number=1, path='source.md', sha256=self.sha,
                           title='Fixture', date='2020-01-01', source_url='https://example.invalid')
        self.record = dict(source=self.source, review=dict(status='extracted_draft', timing='coarse'),
                           games=[], lore=[], corrections=[], topic_coverage=[dict(topic='collecting', depth='SUPPORTING_EXAMPLE', locations=['00:00:00'])])
        for title, depth in [('Alpha', 'SUBSTANTIAL_COVERAGE'), ('Beta', 'PASSING_MENTION')]:
            self.record['games'].append(dict(id=title, canonical_title=title, spoken_forms=[title],
                entity_granularity='release', identification_confidence='high',
                occurrence_groups=[dict(type=depth, context=title, speaker=dict(candidate=None, confidence='unknown'),
                    evidence=[dict(location='00:00:00', quote=title)])]))
        self.annotation = dict(schema_version='1', overrides=[], claims=[dict(id='wanted', source_key='source', source_sha256=self.sha,
            action_state='wanted', speaker=dict(candidate='Johnny', confidence='medium'), evidence=[dict(location='00:00:00', quote='Alpha wanted.')])],
            episodes=[dict(source_key='source', source_sha256=self.sha, mapping_status='partial', spans=[])])
        self.span('first', 'Alpha', '00:00:00', '00:02:00')
        self.span('overlap', 'Alpha', '00:01:00', '00:02:00')
        self.span('return', 'Alpha', '00:03:00', '00:04:00')
        self.span('incidental', 'Beta', '00:00:00', '00:04:00', 'PASSING_MENTION')
        self.manifest = dict(episodes=[dict(self.source, record_path='records/source.json')], duplicate_controls=[])
        self.save()

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value), encoding='utf-8')

    def save(self):
        self.write('pilot/manifest.json', self.manifest)
        self.write('pilot/records/source.json', self.record)
        self.write('pilot/annotations.json', self.annotation)
        self.write('pilot/relationships.json', dict(relationships=[]))

    def span(self, name, title, start, end, role='SUBSTANTIAL_COVERAGE'):
        self.annotation['episodes'][0]['spans'].append(dict(id=name, entity_id=title, title=title,
            game_refs=[title], role=role, start=start, end_exclusive=end, reason='Synthetic test range',
            evidence=[dict(location=start, quote=title)]))

    def test_workbench_triage_uses_both_wordings_and_never_approves(self):
        from lore_workbench import triage
        (self.root / 'pilot/reviews').mkdir()
        self.write('pilot/reviews/001-annotations.json', dict(task_cases=[dict(
            id='case', episode=1, question='unknownfoobar', query='Alpha',
            answer='Not an automatic approval', evidence_locations=['00:04:00'])]))
        build(self.root)
        result = triage('pilot', case_ids=['case'], root=self.root)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['passed'], 1)
        self.assertEqual(result['total'], 2)
        original, tuned = result['cases']
        self.assertEqual(original['missing_windows'], ['00:04:00'])
        self.assertEqual(tuned['missing_windows'], [])
        self.assertNotIn('context', original)
        self.assertFalse((self.root / 'pilot/episode-review-ledger.json').exists())
        with self.assertRaisesRegex(ValueError, 'Unknown case'):
            triage('pilot', case_ids=['typo'], root=self.root)
        self.record['main_topic'] = 'changed'
        self.save()
        with self.assertRaisesRegex(ValueError, 'stale'):
            triage('pilot', case_ids=['case'], root=self.root)

    def test_open_loop_labels_are_case_insensitive_in_evidence_and_brief(self):
        for kind in ('OPEN_LOOP', 'Open_Loop', 'LEAD', 'lead'):
            with self.subTest(kind=kind):
                self.record['lore'] = [dict(id='pending', kind=kind, topics=['mystery'],
                    summary='Mystery remains unresolved.', speaker=dict(candidate=None, confidence='unknown'),
                    evidence=[dict(location='00:04:00', quote='End.')])]
                self.save()
                store = self.open_store()
                try:
                    result = store.answer_evidence('What follow-ups are unanswered?', 1)
                    self.assertEqual(result['route']['intent'], 'open_loops')
                    self.assertIn('00:04:00', result['route']['added_seed_windows'])
                    self.assertEqual(len(store.brief('mystery')['open_loops']), 1)
                finally:
                    store.close()

    def test_mixed_action_questions_retrieve_both_states_and_denials(self):
        self.annotation['claims'] = []
        for state, location, quote in (
                ('wanted', '00:00:00', 'Alpha wanted.'),
                ('purchased', '00:02:00', 'Unrelated.'),
                ('played', '00:04:00', 'End.'),
                ('mentioned', '00:03:00', 'Alpha returned.')):
            self.annotation['claims'].append(dict(
                id=state, source_key='source', source_sha256=self.sha,
                action_state=state, speaker=dict(candidate=None, confidence='unknown'),
                summary='Unresolved or qualified source report.',
                evidence=[dict(location=location, quote=quote)]))
        self.save()
        store = self.open_store()
        for question, required, excluded in (
                ('Which purchases were actual and which games were expensive wants?',
                 {'00:00:00', '00:02:00', '00:03:00'}, {'00:04:00'}),
                ('What did hosts finish or play, and buy?',
                 {'00:02:00', '00:03:00', '00:04:00'}, {'00:00:00'})):
            with self.subTest(question=question):
                result = store.answer_evidence(question, 1)
                seeds = set(result['route']['added_seed_windows'])
                self.assertLessEqual(required, seeds)
                self.assertFalse(excluded & seeds)
                self.assertEqual(result['route']['intent'], 'action_states')
                self.assertIsNone(result['ranking'])

    def test_mixed_action_route_does_not_turn_advice_into_history(self):
        from lore_store import question_route
        for question in ('Which games should I buy and play?',
                         'What would he buy or want?',
                         'Which games are best to buy and play?',
                         'What are the top three games Tyler wanted to buy?',
                         'What did she want to buy and play?',
                         'What did he finish collecting and buy?',
                         'What did he add to his wishlist of games to buy and play?'):
            with self.subTest(question=question):
                self.assertNotEqual(question_route(question)[0], 'action_states')

    def test_conceptual_routes_use_bounded_reviewed_lore(self):
        from lore_store import question_route
        cases = [('When should collecting stop?', 'collecting_end'),
                 ('Are older games good only in historical context?', 'historical_evaluation'),
                 ('What alternatives to buying did they suggest?', 'collecting_alternatives')]
        self.record['lore'] = [dict(id=f'concept-{i}', kind='opinion',
            topics=['collecting historical context practical changes'],
            summary='Goals enjoyment purpose motivation old games evaluation heirs burden.',
            speaker=dict(candidate=None, confidence='unknown'),
            evidence=[dict(location='00:04:00', quote='End.')]) for i in range(8)]
        self.save()
        store = self.open_store()
        for question, intent in cases:
            with self.subTest(intent=intent):
                self.assertEqual(question_route(question)[0], intent)
                result = store.answer_evidence(question, 1)
                self.assertEqual(result['route']['intent'], intent)
                self.assertEqual(result['route']['added_seed_windows'], ['00:04:00'])
        self.assertEqual(question_route('When did he finish collecting the set?')[0], 'collecting_end')
        self.assertEqual(question_route('Did he buy an old game?')[0], 'lexical')

    def test_episode_scope_recovers_typed_format_without_opening_guess(self):
        self.record['lore'] = [dict(id='scope', kind='FORMAT', topics=['scope'],
            summary='Selected examples only; exhaustive coverage is not claimed.',
            speaker=dict(candidate=None, confidence='unknown'),
            evidence=[dict(location='00:04:00', quote='End.')])]
        self.save()
        store = self.open_store()
        result = store.answer_evidence('Was this a complete guide to arcade games?', 1)
        self.assertEqual(result['route']['intent'], 'episode_scope')
        self.assertEqual(result['route']['added_seed_windows'], ['00:04:00'])
        self.assertIn('00:04:00', {r['title'] for r in result['context']})

    def test_price_assumption_recovers_one_reviewed_qualification(self):
        self.record['lore'] = [dict(id='price', kind='opinion', topics=['price correction'],
            summary='A dollar-bin valuation was rejected after a sales comparison.',
            speaker=dict(candidate=None, confidence='unknown'),
            evidence=[dict(location='00:04:00', quote='End.')])]
        self.save()
        store = self.open_store()
        for adjective in ('cheap', 'inexpensive'):
            with self.subTest(adjective=adjective):
                result = store.answer_evidence(f'Which {adjective}-game assumptions did they challenge?', 1)
                self.assertEqual(result['route']['intent'], 'price_assumptions')
                self.assertEqual(result['route']['added_seed_windows'], ['00:04:00'])
                self.assertIn('00:04:00', {r['title'] for r in result['context']})

    def test_scope_route_does_not_treat_guidebook_set_as_episode_coverage(self):
        store = self.open_store()
        self.assertNotEqual(store.answer_evidence('Did he complete the guidebook set?', 1)['route']['intent'], 'episode_scope')
        result = store.answer_evidence('Was this a comprehensive overview of arcade games?', 1)
        self.assertEqual(result['route']['intent'], 'episode_scope')
        self.assertEqual(result['route']['added_seed_windows'], [])
        self.assertEqual(result['context'], [])

    def test_criticism_question_recovers_control_qualification(self):
        self.record['lore'] = [dict(id='controls', kind='opinion', topics=['controls'],
            summary='Weak controls prompted a complaint after playing.',
            speaker=dict(candidate=None, confidence='unknown'),
            evidence=[dict(location='00:04:00', quote='End.')])]
        self.save()
        build(self.root)
        s = LoreStore(self.root)
        try:
            b = s.answer_evidence('Why was the new download disappointing?', 1)
            self.assertIn('00:04:00', {r['title'] for r in b['context']})
            self.assertEqual(b['route']['intent'], 'criticism')
            self.assertEqual(s.answer_evidence('Which game was discussed most?', 1)['route']['intent'], 'game_prominence')
        finally:
            s.close()

    def test_numeric_topic_survives_quote_crowding_with_exact_bounded_match(self):
        self.record['lore'] = [dict(id='distractor' + str(i), kind='history', topics=['recap'],
            summary='Strong yield zero choices.', speaker=dict(candidate=None, confidence='unknown'),
            evidence=[dict(location='00:00:00', quote='Alpha')]) for i in range(7)]
        self.record['lore'].append(dict(id='year', kind='history', topics=['1985'],
            summary='The later decision stayed unchanged.', speaker=dict(candidate=None, confidence='unknown'),
            evidence=[dict(location='00:04:00', quote='End.')]))
        self.save()
        build(self.root)
        s = LoreStore(self.root)
        try:
            b = s.answer_evidence('How did a strong 1985 yield zero choices?', 1)
            self.assertIn('00:04:00', {r['title'] for r in b['context']})
            self.assertEqual(b['route']['numeric_topic_lore_ids'], ['source/year'])
            for q in ['How did 19850 yield zero choices?', 'How did 1986 yield zero choices?']:
                other = s.answer_evidence(q, 1)
                self.assertEqual(other['route']['numeric_topic_lore_ids'], [])
                self.assertNotIn('00:04:00', {r['title'] for r in other['context']})
        finally:
            s.close()

    def test_workbench_triage_exposes_crowded_out_evidence_without_injecting_it(self):
        from lore_workbench import triage
        for i in range(7):
            self.record['lore'].append(dict(id='l' + str(i), kind='history', topics=['topic'],
                summary='uniqueaa uniquebb uniquecc' if i < 6 else 'uniqueaa',
                speaker=dict(candidate=None, confidence='unknown'),
                evidence=[dict(location='00:00:00' if i < 6 else '00:04:00', quote='Alpha' if i < 6 else 'End.')]))
        self.save()
        (self.root / 'pilot/reviews').mkdir()
        self.write('pilot/reviews/001-annotations.json', dict(task_cases=[dict(id='case', episode=1,
            question='uniqueaa uniquebb uniquecc', query='uniqueaa uniquebb uniquecc',
            evidence_locations=['00:04:00'])]))
        build(self.root)
        result = triage('pilot', case_ids=['case'], root=self.root)
        self.assertEqual(result['passed'], 0)
        for case in result['cases']:
            self.assertEqual(case['missing_windows'], ['00:04:00'])
            self.assertEqual(case['missing_window_lore_candidates'], [dict(
                id='source/l6', rank=7, missing_windows_covered=['00:04:00'])])

    def test_series_prominence_is_separate_from_game_ranking(self):
        for span in self.annotation['episodes'][0]['spans']:
            if span['title'] == 'Alpha':
                span['entity_kind'] = 'game_series'
        self.save()
        build(self.root)
        store = LoreStore(self.root)
        try:
            result = store.top_games(1)
            self.assertEqual(result['results'], [])
            self.assertEqual(result['series_results'][0]['title'], 'Alpha')
            self.assertEqual(result['series_results'][0]['coverage'], 180)
        finally:
            store.close()

    def open_store(self):
        build(self.root)
        store = LoreStore(self.root)
        self.addCleanup(store.close)
        return store

    def test_query_truncation_is_visible_without_changing_budget(self):
        query = ' '.join(['Alpha'] + ['word' + str(i) for i in range(20)])
        result = self.open_store().search(query)
        diag = result['query_diagnostics']
        self.assertTrue(diag['truncated'])
        self.assertEqual(len(diag['effective_terms']), 16)
        self.assertEqual(diag['omitted_terms'], ['word' + str(i) for i in range(15, 20)])

    def test_short_query_reports_no_omission(self):
        diag = self.open_store().search('Alpha Alpha')['query_diagnostics']
        self.assertEqual(diag['effective_terms'], ['alpha'])
        self.assertFalse(diag['truncated'])
        self.assertEqual(diag['omitted_terms'], [])

    def test_ranking_question_routes_to_typed_prominence(self):
        result = self.open_store().answer_evidence('Which games had the most discussion?', 1)
        self.assertEqual(result['route']['intent'], 'game_prominence')
        self.assertEqual(result['ranking']['results'][0]['title'], 'Alpha')
        self.assertEqual(result['ranking']['results'][0]['coverage'], 180)
        self.assertEqual(result['ranking']['status'], 'incomplete_mapping')
        self.assertFalse(any(r['title'] == 'Beta' for r in result['ranking']['results']))

    def test_natural_discussion_and_purchase_phrasings_use_shared_interface(self):
        store = self.open_store()
        for query in ('Which games received the most real discussion?',
                      'Which games dominated the interview?'):
            with self.subTest(query=query):
                result = store.answer_evidence(query, 1)
                self.assertEqual(result['route']['intent'], 'game_prominence')
                self.assertEqual(result['ranking']['results'][0]['title'], 'Alpha')
        result = store.answer_evidence('Which new purchases were theirs?', 1)
        self.assertEqual(result['route']['intent'], 'acquisitions')
        result = store.answer_evidence('Which things did they actually buy?', 1)
        self.assertEqual(result['route']['intent'], 'acquisitions')
        for query in ('Which games dominated the market?',
                      'Which purchases should they make?',
                      'Which hypothetical purchases were discussed?',
                      'Which games did he want with the most real discussion?'):
            with self.subTest(query=query):
                result = store.answer_evidence(query, 1)
                self.assertNotIn(result['route']['intent'], ('game_prominence', 'acquisitions'))

    def test_ordinary_title_question_does_not_invent_intent(self):
        result = self.open_store().answer_evidence('Why did Alpha appeal?', 1)
        self.assertEqual(result['route']['intent'], 'lexical')
        self.assertIsNone(result['ranking'])
        self.assertIn('pilot', result['scope'])
        self.assertEqual(result['context_coverage']['episode_windows'], 5)

    def test_concept_questions_retrieve_reviewed_context_through_shared_interface(self):
        self.record['lore'] = [dict(id='concept', kind='debate',
            topics=['skill ceiling mastery set checklist expensive price utility'],
            summary='Criteria for comparing mastery; optional standalone releases and costly utility exceptions.',
            speaker=dict(candidate=None, confidence='unknown'),
            evidence=[dict(location='00:04:00', quote='End.')])]
        self.save()
        store = self.open_store()
        for query, intent in [
            ('Why disagree about the hardest game to master?', 'skill_comparison'),
            ('What counts toward the set and what is optional?', 'set_scope'),
            ('What did completing the set actually mean?', 'set_scope'),
            ('Which costly items are worth collecting?', 'price_evaluation')]:
            with self.subTest(query=query):
                result = store.answer_evidence(query, 1)
                self.assertEqual(result['route']['intent'], intent)
                self.assertIn('00:04:00', result['route']['added_seed_windows'])
                self.assertIn('00:04:00', [r['title'] for r in result['context']])
                self.assertIsNone(result['ranking'])

    def test_actual_additions_are_acquisitions_not_wishlist_changes(self):
        self.annotation['claims'][0]['action_state'] = 'received'
        self.save()
        store = self.open_store()
        result = store.answer_evidence('What variants did the guest actually add?', 1)
        self.assertEqual(result['route']['intent'], 'acquisitions')
        self.assertIn('00:00:00', result['route']['added_seed_windows'])
        for query in ('What should she add to her collection?',
                      'What did they add to the wishlist?',
                      'What is the hardest boss?', 'What was the value of the friendship?'):
            with self.subTest(query=query):
                self.assertEqual(store.answer_evidence(query, 1)['route']['intent'], 'lexical')

    def test_explicit_multiword_reference_survives_occurrence_crowding(self):
        self.record['games'][1]['canonical_title'] = 'Beta Quest'
        self.record['games'][1]['spoken_forms'] = ['Beta']
        self.save()
        store = self.open_store()
        result = store.answer_evidence('Tell me about Beta Quest', 1, limit=1)
        self.assertEqual(result['route']['explicit_reference_ids'], ['Beta'])
        self.assertIn('00:03:00', [r['title'] for r in result['context']])
        self.assertEqual(store.answer_evidence('Tell me about Quest', 1)['route']['explicit_reference_ids'], [])

    def test_person_name_substring_is_not_ranking_intent(self):
        result = self.open_store().answer_evidence('Which games did Frank like?', 1)
        self.assertEqual(result['route']['intent'], 'lexical')

    def test_missing_episode_keeps_empty_context_for_route(self):
        result = self.open_store().answer_evidence('Which games had the most discussion?', 99)
        self.assertEqual(result['ranking']['status'], 'not_processed')
        self.assertEqual(result['context'], [])

    def test_open_loop_route_uses_states_without_certifying_ownership(self):
        result = self.open_store().answer_evidence('What follow-ups are unanswered?', 1)
        self.assertEqual(result['route']['intent'], 'open_loops')
        self.assertIn('00:00:00', result['route']['added_seed_windows'])
        self.assertIn('not a certified answer', result['route']['status'])

    def test_union_preserves_returns_without_counting_gap_or_overlap(self):
        result = self.open_store().top_games(1)
        self.assertEqual(result['results'][0]['coverage'], 180)
        self.assertEqual(len(result['results']), 1)  # Beta never inherits whole span.
        self.assertEqual(result['status'], 'incomplete_mapping')

    def test_union_handles_nested_intervals(self):
        self.assertEqual(union_length([(1, 10), (2, 3), (9, 12), (15, 17)]), 13)

    def test_unknown_end_is_not_fabricated(self):
        self.annotation['episodes'][0]['spans'][2]['end_exclusive'] = 'END'
        self.save()
        result = self.open_store().top_games(1)
        self.assertTrue(result['results'][0]['unknown_endpoint'])
        self.assertEqual(result['status'], 'incomplete_mapping')

    def test_complete_mapping_requires_review_note(self):
        self.annotation['episodes'][0]['mapping_status'] = 'complete'
        self.save()
        with self.assertRaisesRegex(ValueError, 'review note'):
            build(self.root)

    def test_missing_episode_is_not_absence_claim(self):
        self.assertEqual(self.open_store().top_games(99)['status'], 'not_processed')

    def test_unknown_speaker_is_retained_with_qualification(self):
        hit = self.open_store().search('Alpha', speaker='Tyler')['results'][0]
        self.assertEqual(hit['speaker_match'], 'uncertain_or_other_speaker')
        self.assertEqual(hit['speaker']['confidence'], 'unknown')

    def test_wanted_is_not_owned(self):
        store = self.open_store()
        self.assertEqual(len(store.actions('Johnny', 'wanted')), 1)
        self.assertEqual(store.actions('Johnny', 'owned'), [])

    def test_reporter_is_not_action_subject(self):
        self.annotation['claims'][0]['subject'] = "John (Kat's spouse)"
        self.annotation['claims'][0]['speaker']['candidate'] = 'Kat'
        self.annotation['claims'][0]['action_state'] = 'purchased'
        self.save()
        store = self.open_store()
        self.assertEqual(store.actions('Kat', 'purchased'), [])
        self.assertEqual(len(store.actions("John (Kat's spouse)", 'purchased')), 1)

    def test_returned_purchase_is_queryable_without_current_ownership(self):
        claim = self.annotation['claims'][0]
        claim['action_state'] = 'returned'
        claim['subject'] = 'Johnny'
        claim['evidence'] = [dict(location='00:03:00', quote='Alpha returned.')]
        self.save()
        store = self.open_store()
        self.assertEqual(len(store.actions('Johnny', 'returned')), 1)
        self.assertEqual(store.actions('Johnny', 'owned'), [])

    def test_non_video_subjects_do_not_rank_as_games(self):
        for span in self.annotation['episodes'][0]['spans']:
            span['entity_kind'] = 'tabletop'
        self.save()
        self.assertEqual(self.open_store().top_games(1)['results'], [])

    def test_durable_new_game_is_searchable_and_rebuildable(self):
        game = copy.deepcopy(self.record['games'][0])
        game['id'] = 'new-ref'
        self.annotation['new_games'] = [dict(source_key='source', source_sha256=self.sha,
            reason='Missed reference', game=game)]
        self.save()
        store = self.open_store()
        self.assertEqual(len(store.search('Alpha', kind='game')['results']), 2)

    def test_exact_phrase_filter(self):
        store = self.open_store()
        self.assertEqual(store.search('Alpha', required_phrases=['Alpha received'])['results'], [])

    def test_stale_inputs_block_retrieval(self):
        build(self.root)
        self.annotation['claims'][0]['action_state'] = 'owned'
        self.save()
        with self.assertRaisesRegex(ValueError, 'stale'):
            LoreStore(self.root)

    def test_source_change_blocks_build(self):
        with (self.root / 'library/source.md').open('a', encoding='utf-8') as stream:
            stream.write(' changed')
        with self.assertRaisesRegex(ValueError, 'Stale source'):
            build(self.root)

    def test_bad_quote_blocks_build(self):
        self.annotation['claims'][0]['evidence'][0]['quote'] = 'made up'
        self.save()
        with self.assertRaisesRegex(ValueError, 'Unsupported evidence'):
            build(self.root)

    def test_override_survives_two_rebuilds_and_rejects_drift(self):
        previous = copy.deepcopy(self.record['games'][0]['occurrence_groups'])
        replacement = copy.deepcopy(previous)
        replacement[0]['type'] = 'SUPPORTING_EXAMPLE'
        self.annotation['overrides'] = [dict(id='fix', source_key='source', source_sha256=self.sha,
            collection='games', item_id='Alpha', reason='Fixture correction',
            fields=dict(occurrence_groups=dict(expected=previous, value=replacement)))]
        self.save()
        for _ in range(2):
            build(self.root)
            store = LoreStore(self.root)
            try:
                self.assertEqual(store.search('Alpha', kind='game')['results'][0]['depth'], 'SUPPORTING_EXAMPLE')
            finally:
                store.close()
        self.record['games'][0]['occurrence_groups'][0]['context'] = 'base drift'
        self.save()
        with self.assertRaisesRegex(ValueError, 'Override base changed'):
            build(self.root)

    def test_unsafe_database_target_rejected(self):
        with self.assertRaisesRegex(ValueError, 'under pilot/generated'):
            build(self.root, self.root / 'unrelated.sqlite3')

    def test_unrelated_database_preserved(self):
        path = self.root / 'pilot/generated/other.sqlite3'
        path.parent.mkdir()
        db = sqlite3.connect(path)
        db.execute('CREATE TABLE preserve(value)')
        db.close()
        before = path.read_bytes()
        with self.assertRaises((ValueError, sqlite3.DatabaseError)):
            build(self.root, path)
        self.assertEqual(path.read_bytes(), before)

    def test_canonical_episode_counts_ignore_duplicate_upload(self):
        self.manifest['duplicate_controls'] = [dict(self.source, key='old-upload')]
        self.save()
        store = self.open_store()
        self.assertEqual(len(store.topics()[0]['episodes']), 1)

    def test_episode_local_ids_are_namespaced(self):
        second = copy.deepcopy(self.record)
        second['source']['key'] = 'second'
        second['source']['episode_number'] = 2
        self.write('pilot/records/second.json', second)
        self.manifest['episodes'].append(dict(second['source'], record_path='records/second.json'))
        self.save()
        result = self.open_store().search('Alpha', kind='game')['results']
        self.assertEqual(len(result), 2)
        self.assertEqual(len({r['id'] for r in result}), 2)

    def test_separate_collection_does_not_expand_pilot(self):
        batch = self.root / 'batches/002'
        shutil.copytree(self.root / 'pilot', batch)
        build(self.root, collection='batches/002')
        with self.assertRaises(FileNotFoundError):
            (self.root / 'pilot/generated/lore.sqlite3').read_bytes()
        store = LoreStore(self.root, collection='batches/002')
        self.addCleanup(store.close)
        self.assertIn('batches/002', store.search('Alpha')['scope'])

    def test_collection_cannot_escape_repository(self):
        with self.assertRaisesRegex(ValueError, 'within the repository'):
            build(self.root, collection='../outside')

    def test_batch_build_cannot_overwrite_pilot_database(self):
        with self.assertRaisesRegex(ValueError, 'under batches/002/generated'):
            build(self.root, database=self.root / 'pilot/generated/lore.sqlite3', collection='batches/002')

    def test_changed_batch_fragment_requires_merge(self):
        batch = self.root / 'batches/002'
        shutil.copytree(self.root / 'pilot', batch)
        (batch / 'reviews').mkdir()
        annotation = {**self.annotation, 'new_games': []}
        self.write('batches/002/annotations.json', annotation)
        self.write('batches/002/reviews/001-annotations.json', annotation)
        build(self.root, collection='batches/002')
        before = (batch / 'generated/lore.sqlite3').read_bytes()
        annotation['episodes'][0]['spans'][0]['reason'] = 'Reviewed reason changed'
        self.write('batches/002/reviews/001-annotations.json', annotation)
        with self.assertRaisesRegex(ValueError, 'Review fragments changed'):
            build(self.root, collection='batches/002')
        self.assertEqual(before, (batch / 'generated/lore.sqlite3').read_bytes())


class PilotFunctionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build()
        cls.store = LoreStore()

    @classmethod
    def tearDownClass(cls):
        cls.store.close()

    def test_specific_title_does_not_lose_to_shared_context(self):
        self.assertEqual(self.store.search('Fallout 4', kind='game', limit=1)['results'][0]['title'], 'Fallout 4')

    def test_frozen_retrieval_cases_cover_each_pilot_episode(self):
        cases = json.loads((ROOT / 'pilot/functional-cases.json').read_text(encoding='utf-8'))['cases']
        self.assertEqual({c['episode'] for c in cases}, {6, 7, 146, 200, 222, 248, 259, 263, 299, 300})
        for case in cases:
            with self.subTest(episode=case['episode']):
                results = self.store.search(case['query'], episode=case['episode'], limit=5)['results']
                hit = next(r for r in results if r['local_id'] == case['expected_local_id'])
                self.assertIn(case['expected_location'], [e['location'] for e in hit['evidence']])
                self.assertEqual(case['answer_quality_status'], 'not_scored')

    def test_coarse_untimed_sources_never_gain_seconds(self):
        for ep in (6, 7):
            result = self.store.top_games(ep)
            self.assertEqual(result['status'], 'mapped_estimate')
            self.assertTrue(all(r['unit'] == 'paragraphs' for r in result['results']))

    def test_purchase_pending_arrival_not_reported_as_received(self):
        ordered = {c['title'] for c in self.store.actions('Johnny', 'ordered')}
        self.assertTrue({'Rusty', 'Witchaven prize-copy variant'} <= ordered)
        self.assertFalse({'Rusty', 'Witchaven prize-copy variant'} & {c['title'] for c in self.store.actions('Johnny', 'received')})

    def test_corrected_incidental_depths(self):
        expected = {'cq300-g006:0': 'JOKE_ASIDE', 'cq300-g092:0': 'SUPPORTING_EXAMPLE',
                    'cq300-g095:0': 'PASSING_MENTION', 'cq300-g292:0': 'SUPPORTING_EXAMPLE'}
        actual = {r['local_id']: r['depth'] for r in self.store._items('records') if r['local_id'] in expected}
        self.assertEqual(actual, expected)

    def test_return_does_not_count_the_hour_between_blasty_mentions(self):
        result = self.store.top_games(300, limit=50)
        blasty = next(r for r in result['results'] if r['title'] == 'Cruise Chaser Blasty')
        self.assertEqual(blasty['coverage'], 122)
        jack = next(r for r in result['results'] if r['title'] == 'Jack the Ripper')
        self.assertEqual(jack['substantial_coverage'], 0)

    def test_timeline_preserves_changed_opinion_and_milestone_distinction(self):
        kinds = {r['kind'] for r in self.store._items('relationships')}
        self.assertTrue({'changed_opinion', 'collection_milestone', 'promised_followup_delivered'} <= kinds)

    def test_brief_is_evidence_packet_not_approved_performance(self):
        packet = self.store.brief('inserts')
        self.assertTrue(packet['documented_history'])
        self.assertEqual(packet['editorial_suggestions'], [])
        self.assertIn('not a rehearsed', packet['delivery_status'])
        self.assertTrue(all(h['evidence'] for h in packet['documented_history']))

    def test_full_review_and_unknown_timing_are_separate(self):
        result = self.store.top_games(263)
        self.assertTrue(result['mapping_complete'])
        self.assertFalse(result['timing_complete'])
        self.assertEqual(result['status'], 'mapped_estimate')

    def test_physical_pinball_is_not_a_video_game_leader(self):
        self.assertFalse(any('pinball' in r['title'] for r in self.store.top_games(6, 50)['results']))

    def test_answer_context_includes_return_and_caption_alias(self):
        for episode, query, location in [(6, 'Speed Racer Mountain Bike Rally', 'Paragraph 11'),
                                         (300, 'Witchaven inconclusive', '03:44:06')]:
            bundle = self.store.answer_evidence(query, episode)
            self.assertIn(location, [r['evidence'][0]['location'] for r in bundle['context']])

    def test_omission_repair_stays_passing_and_boundary_stays_narrow(self):
        spans = {s['id']:s for s in self.store._items('spans')}
        self.assertEqual(spans['cq300-audit-span-389']['role'], 'PASSING_MENTION')
        self.assertEqual(spans['cq300-audit-span-389']['start'], '01:34:38')
        self.assertEqual(spans['cq222-audit-span-053']['end_exclusive'], '01:29:43')


if __name__ == '__main__':
    unittest.main()
