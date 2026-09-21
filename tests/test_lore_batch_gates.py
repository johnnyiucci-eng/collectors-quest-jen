"""Synthetic acceptance-gate regressions; not source-accuracy measurements."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from process_lore_batch import validate_section_accounting, validate_reference_mapping, check_manual_answers, validate_record_schema, validate_span_identity_kinds
from lore_store import LoreStore
from process_lore_batch import validate_spoken_forms


class SpokenFormTests(unittest.TestCase):
    def test_catalog_normalization_is_separate_from_literal_alias(self):
        record = dict(games=[dict(id='game', canonical_title='Virtua Fighter Remix',
                                 spoken_forms=['Virtual Fighter Remix'])])
        source = {'Paragraph 1': 'I just got in Virtual Fighter Remix.'}
        self.assertEqual(validate_spoken_forms(record, source), 1)
        record['games'][0]['spoken_forms'] = ['Virtua Fighter Remix']
        with self.assertRaisesRegex(ValueError, 'Nonliteral spoken form'):
            validate_spoken_forms(record, source)

    def test_empty_aliases_are_not_a_validation_escape(self):
        for forms in ([], [''], None):
            with self.subTest(forms=forms), self.assertRaises(ValueError):
                validate_spoken_forms(dict(games=[dict(id='game', spoken_forms=forms)]), {})

    def test_casefold_does_not_require_capitalization_identity(self):
        record = dict(games=[dict(id='game', spoken_forms=['SONIC'])])
        self.assertEqual(validate_spoken_forms(record, {'Paragraph 1': 'Sonic'}), 1)


class IdentityKindTests(unittest.TestCase):
    def test_missing_kind_rejected(self):
        with self.assertRaisesRegex(ValueError, 'explicit entity kind'):
            validate_span_identity_kinds({'spans': [dict(id='s1', entity_id='franchise')]})

    def test_conflicting_kinds_for_same_identity_rejected(self):
        spans = [dict(id='s1', entity_id='same', entity_kind='video_game'),
                 dict(id='s2', entity_id='same', entity_kind='game_series')]
        with self.assertRaisesRegex(ValueError, 'mix entity kinds'):
            validate_span_identity_kinds({'spans': spans})

    def test_explicit_non_game_kind_retained(self):
        self.assertEqual(validate_span_identity_kinds({'spans': [dict(id='s1', entity_id='pin', entity_kind='physical_pinball')]}), 1)


class ActionSubjectTests(unittest.TestCase):
    def setUp(self):
        self.store = object.__new__(LoreStore)
        self.claims = [dict(id='joint', subject='Kat', co_subjects=['John'],
                            speaker=dict(candidate='Johnny'), action_state='owned'),
                       dict(id='reported', subject='Tyler', speaker=dict(candidate='Johnny'), action_state='purchased')]
        self.store._items = lambda table: self.claims

    def test_joint_owner_is_queryable_without_duplicate_claim(self):
        self.assertEqual([c['id'] for c in self.store.actions('John', 'owned')], ['joint'])
        self.assertEqual([c['id'] for c in self.store.actions('Kat', 'owned')], ['joint'])
        self.assertEqual(len(self.store.actions()), 2)

    def test_case_insensitive_subject_filter(self):
        self.assertEqual([c['id'] for c in self.store.actions('kat', 'owned')], ['joint'])

    def test_reporter_is_not_action_subject(self):
        self.assertEqual(self.store.actions('Johnny'), [])


class AccountingTests(unittest.TestCase):
    def setUp(self):
        self.headings = ['Paragraph 1', 'Paragraph 2', 'Paragraph 3']
        self.annotation = dict(mapping_status='complete', spans=[], section_accounting=[
            dict(location=p, summary='Reviewed source disposition') for p in self.headings])

    def test_all_windows_accounted(self):
        self.assertEqual(validate_section_accounting(self.annotation, self.headings), 3)

    def test_missing_window_rejected(self):
        self.annotation['section_accounting'].pop()
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            validate_section_accounting(self.annotation, self.headings)

    def test_duplicate_window_rejected(self):
        self.annotation['section_accounting'].append(self.annotation['section_accounting'][0])
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            validate_section_accounting(self.annotation, self.headings)

    def test_ranges_supported(self):
        del self.annotation['section_accounting']
        self.annotation['section_map'] = [dict(start='Paragraph 1', end_exclusive='END', summary='Full section')]
        self.assertEqual(validate_section_accounting(self.annotation, self.headings), 3)

    def test_reference_must_resolve_and_overlap(self):
        self.annotation['section_accounting'][0]['span_refs'] = ['wrong']
        with self.assertRaisesRegex(ValueError, 'Unknown accounting'):
            validate_section_accounting(self.annotation, self.headings)
        self.annotation['spans'] = [dict(id='wrong', start='Paragraph 2', end_exclusive='END')]
        with self.assertRaisesRegex(ValueError, 'does not overlap'):
            validate_section_accounting(self.annotation, self.headings)

    def test_partial_map_cannot_pass(self):
        self.annotation['mapping_status'] = 'partial'
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            validate_section_accounting(self.annotation, self.headings)


class ManualReviewTests(unittest.TestCase):
    def setUp(self):
        self.case = dict(id='test', episode=1, answer='Reported wanting Alpha, not buying it.',
                         evidence_locations=['Paragraph 1'], forbidden=['Claiming a purchase'])
        self.result = dict(cases=[self.case])
        self.review = [{**copy.deepcopy(self.case), 'status':'passed', 'reason':'Source supports qualified intent.'}]

    def test_matching_review_passes(self):
        self.assertEqual(check_manual_answers(self.result, self.review), 1)

    def test_stale_answer_cannot_reuse_old_pass(self):
        self.case['answer'] = 'Bought Alpha.'
        with self.assertRaisesRegex(ValueError, 'stale'):
            check_manual_answers(self.result, self.review)

    def test_changed_evidence_and_forbidden_require_rereview(self):
        for field in ('episode', 'evidence_locations', 'forbidden'):
            with self.subTest(field=field):
                modified = copy.deepcopy(self.result)
                modified['cases'][0][field] = None
                with self.assertRaisesRegex(ValueError, 'stale'):
                    check_manual_answers(modified, self.review)

    def test_duplicate_review_does_not_inflate_pass_count(self):
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            check_manual_answers(self.result, self.review * 2)

    def test_failed_review_blocks_gate(self):
        self.review[0]['status'] = 'failed'
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            check_manual_answers(self.result, self.review)


class ReferenceMappingTests(unittest.TestCase):
    def setUp(self):
        self.headings = ['Paragraph 1', 'Paragraph 2']
        self.record = dict(games=[dict(id='alpha', occurrence_groups=[dict(
            evidence=[dict(location='Paragraph 1', quote='Alpha')])])])
        self.annotation = dict(spans=[dict(game_refs=['alpha'], start='Paragraph 1',
                                          end_exclusive='Paragraph 2', role='PASSING_MENTION')])

    def test_passing_reference_counts_as_accounted_not_meaningful(self):
        self.assertEqual(validate_reference_mapping(self.record, self.annotation, self.headings), 1)

    def test_unmapped_identity_rejected(self):
        self.annotation['spans'][0]['game_refs'] = ['beta']
        with self.assertRaisesRegex(ValueError, 'Unmapped game'):
            validate_reference_mapping(self.record, self.annotation, self.headings)

    def test_wrong_window_rejected(self):
        self.record['games'][0]['occurrence_groups'][0]['evidence'][0]['location'] = 'Paragraph 2'
        with self.assertRaisesRegex(ValueError, 'lacks mapped role'):
            validate_reference_mapping(self.record, self.annotation, self.headings)


class RecordSchemaTests(unittest.TestCase):
    def test_correction_requires_speaker_including_unknown(self):
        record = dict(games=[], lore=[], corrections=[dict(id='correction')])
        with self.assertRaisesRegex(ValueError, 'explicit speaker'):
            validate_record_schema(record)
        record['corrections'][0]['speaker'] = dict(candidate=None, confidence='unknown')
        validate_record_schema(record)

    def test_unknown_role_is_rejected_before_indexing(self):
        group = dict(type='JOKE_REFERENCE', speaker=dict(candidate=None))
        record = dict(games=[dict(id='game', occurrence_groups=[group])])
        with self.assertRaisesRegex(ValueError, 'Invalid occurrence role'):
            validate_record_schema(record)
        group['type'] = 'JOKE_ASIDE'
        validate_record_schema(record)


if __name__ == '__main__':
    unittest.main()
