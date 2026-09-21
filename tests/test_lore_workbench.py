"""Public workbench interface: bounded reads, conservative reuse, no approval."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_workbench import source_page, review_page, verify


class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.collection = 'batches/001'
        self.base = self.root / self.collection
        for folder in ('library/episodes', 'scripts', 'tests', 'pilot',
                       'batches/001/reviews', 'batches/001/records', 'batches/001/generated'):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        self.source = self.root / 'library/episodes/source.md'
        self.source.write_text('# Source\n### Paragraph 1\n' + 'x' * 600 + '\n### Paragraph 2\nSecond\u00a0window\n', encoding='utf-8')
        self.sha = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.write(self.base / 'manifest.json', dict(episodes=[dict(episode_number=1, key='one',
                   path='episodes/source.md', sha256=self.sha, record_path='records/one.json')]))
        self.write(self.base / 'records/one.json', dict(selection_lists=[dict(id='l1', label='Favorites',
                   subject='Host', purpose='favorites', entries=[dict(game_ref='g1', status='selected',
                   reason='Stated', evidence=[dict(location='Paragraph 2', quote='HUGE' * 10000)])])]))
        self.write(self.base / 'reviews/001-annotations.json', dict(task_cases=[dict(id='case', episode=1,
                   question='Original?', query='terms', answer='Qualified answer', forbidden=['Wrong actor'],
                   evidence_locations=['Paragraph 2'], retrieved_context=['HUGE' * 10000])]))
        for name in ('WORKFLOW.md', 'requirements.md'):
            (self.root / 'pilot' / name).write_text('Required review', encoding='utf-8')
        # Local stand-in executables exercise real subprocess/disk behavior.
        (self.root / 'scripts/process_lore_batch.py').write_text(
            "import sys,json,pathlib\nb=pathlib.Path(sys.argv[-1]); g=b/'generated'\n"
            "op=sys.argv[1]\n"
            "if op=='build': (g/'lore.sqlite3').write_bytes(b'database')\n"
            "if op=='answers': (g/'answer-evidence.json').write_text('{}')\n"
            "print(json.dumps({'passed':1,'total':1}))\n"
            "sys.exit(1 if (b/('fail-'+op)).exists() else 0)\n", encoding='utf-8')
        (self.root / 'scripts/evaluate_lore_questions.py').write_text(
            "print('{\"passed\":1,\"total\":1}')\n", encoding='utf-8')

    def write(self, path, data):
        path.write_text(json.dumps(data), encoding='utf-8')

    def test_source_pages_preserve_whole_windows_and_resume_hash(self):
        first = source_page(self.collection, 1, budget=700, root=self.root)
        self.assertEqual(first['next_start'], 1)
        self.assertEqual(len(first['items'][0]['text'].strip()), 600)
        second = source_page(self.collection, 1, start=1, source_sha=first['source_sha'], root=self.root)
        self.assertIn('\u00a0', second['items'][0]['text'])
        self.assertIsNone(second['next_start'])
        self.assertFalse(first['truncated'])

    def test_no_silent_truncation_or_unbound_resume(self):
        with self.assertRaisesRegex(ValueError, 'Nothing was truncated'):
            source_page(self.collection, 1, budget=256, root=self.root)
        with self.assertRaisesRegex(ValueError, 'Resume with'):
            source_page(self.collection, 1, start=1, root=self.root)
        with self.assertRaises(ValueError):
            source_page(self.collection, 1, start=-1, root=self.root)

    def test_changed_source_invalidates_cursor_even_if_manifest_updated(self):
        self.source.write_text('### New\nChanged', encoding='utf-8')
        manifest = json.loads((self.base / 'manifest.json').read_text())
        manifest['episodes'][0]['sha256'] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.write(self.base / 'manifest.json', manifest)
        with self.assertRaisesRegex(ValueError, 'Source changed'):
            source_page(self.collection, 1, start=1, source_sha=self.sha, root=self.root)

    def test_outside_source_and_collection_rejected(self):
        with self.assertRaises(ValueError):
            source_page('../outside', 1, root=self.root)
        manifest = json.loads((self.base / 'manifest.json').read_text())
        manifest['episodes'][0]['path'] = '../pilot/WORKFLOW.md'
        self.write(self.base / 'manifest.json', manifest)
        with self.assertRaisesRegex(ValueError, 'outside library'):
            source_page(self.collection, 1, root=self.root)

    def test_review_projections_do_not_dump_nested_quotes(self):
        for view in ('answers', 'lists'):
            result = review_page(self.collection, view, root=self.root)
            self.assertNotIn('HUGE', json.dumps(result))
            self.assertEqual(result['total'], 1)
        answer = review_page(self.collection, 'answers', root=self.root)['items'][0]
        self.assertEqual(answer['forbidden'], ['Wrong actor'])
        self.assertEqual(answer['question'], 'Original?')

    def test_failures_only_and_episode_filter(self):
        self.write(self.base / 'generated/answer-evidence.json', dict(cases=[
            dict(id='bad', episode=1, missing_windows=['Paragraph 2'], retrieved_context=['HUGE']),
            dict(id='good', episode=1, missing_windows=[])]))
        result = review_page(self.collection, 'failures', episode=1, root=self.root)
        self.assertEqual([c['id'] for c in result['items']], ['bad'])
        self.assertEqual(review_page(self.collection, 'failures', episode=2, root=self.root)['total'], 0)

    def test_reference_view_keeps_identity_uncertainty_and_whole_occurrences(self):
        self.write(self.base / 'records/one.json', dict(games=[dict(
            id='g1', canonical_title=None, spoken_forms=['raw title'], platform=None,
            identification_confidence='low', clarification_needed=True,
            identity_candidates=['Candidate only'], uncertain_edition='inspect this field',
            occurrence_groups=[dict(type='PASSING_REFERENCE', context='Not played',
                speaker={'candidate': None, 'confidence': 'low'},
                evidence=[dict(location='Paragraph 2', quote='HUGE' * 1000)])])]))
        result = review_page(self.collection, 'references', root=self.root)
        item = result['items'][0]
        self.assertNotIn('HUGE', json.dumps(result))
        self.assertIsNone(item['canonical_title'])
        self.assertEqual(item['spoken_forms'], ['raw title'])
        self.assertEqual(item['identity_candidates'], ['Candidate only'])
        self.assertEqual(item['additional_fields'], ['uncertain_edition'])
        self.assertEqual(item['occurrence_groups'][0]['locations'], ['Paragraph 2'])
        self.assertEqual(item['occurrence_groups'][0]['context'], 'Not played')
        self.assertEqual(review_page(self.collection, 'references', episode=2, root=self.root)['total'], 0)
        with self.assertRaisesRegex(ValueError, 'Nothing was truncated'):
            review_page(self.collection, 'references', budget=256, root=self.root)

    def test_span_view_pages_all_rows_without_losing_roles_or_endpoints(self):
        path = self.base / 'reviews/001-annotations.json'
        self.write(path, dict(episodes=[dict(source_key='one', mapping_status='partial', spans=[
            dict(id=f's{i}', entity_id='one:g1', title='Series', game_refs=['g1'],
                 entity_kind='game_series', role='PASSING_REFERENCE', start='Paragraph 1',
                 end_exclusive='END', reason='Only a passing mention', variant_context='uncertain edition',
                 uncertainty='extra qualification',
                 evidence=[dict(location='Paragraph 1', quote='HUGE' * 1000)])
            for i in range(71)])]))
        rows, cursor = [], 0
        while cursor is not None:
            result = review_page(self.collection, 'spans', start=cursor, budget=1100, root=self.root)
            self.assertFalse(result['truncated'])
            self.assertNotIn('HUGE', json.dumps(result))
            rows.extend(result['items'])
            cursor = result['next_start']
        self.assertEqual([r['id'] for r in rows], [f's{i}' for i in range(71)])
        self.assertEqual(rows[0]['mapping_status'], 'partial')
        self.assertEqual(rows[0]['entity_kind'], 'game_series')
        self.assertEqual(rows[0]['end_exclusive'], 'END')
        self.assertEqual(rows[0]['role'], 'PASSING_REFERENCE')
        self.assertEqual(rows[0]['additional_fields'], ['uncertainty'])
        self.assertEqual(review_page(self.collection, 'spans', episode=2, root=self.root)['total'], 0)
        self.write(path, dict(episodes=[dict(source_key='unknown', spans=[])]))
        with self.assertRaisesRegex(ValueError, 'no known episode'):
            review_page(self.collection, 'spans', root=self.root)

    def test_reference_view_rejects_record_outside_collection(self):
        path = self.base / 'manifest.json'
        manifest = json.loads(path.read_text())
        manifest['episodes'][0]['record_path'] = '../../outside.json'
        self.write(path, manifest)
        with self.assertRaisesRegex(ValueError, 'outside collection'):
            review_page(self.collection, 'references', root=self.root)

    def test_actions_keep_attribution_and_locations_without_recursive_quotes(self):
        path = self.base / 'reviews/001-annotations.json'
        data = json.loads(path.read_text())
        data['claims'] = [dict(id='action', source_key='one', action_state='wanted',
                              summary='Not yet received', speaker={'candidate': None},
                              subject='Household', co_subjects=['Partner'], game_refs=['g1'],
                              polarity='negative', custody='returned', ownership_scope='household',
                              intended_action_state='sold', return_context='recovered_escaped_pet',
                              evidence=[dict(location='Paragraph 2', quote='HUGE' * 1000)])]
        self.write(path, data)
        result = review_page(self.collection, 'actions', root=self.root)
        self.assertNotIn('HUGE', json.dumps(result))
        self.assertEqual(result['items'][0]['subject'], 'Household')
        self.assertEqual(result['items'][0]['episode'], 1)
        self.assertEqual(result['items'][0]['co_subjects'], ['Partner'])
        self.assertEqual(result['items'][0]['locations'], ['Paragraph 2'])
        self.assertEqual(result['items'][0]['qualifiers']['polarity'], 'negative')
        self.assertEqual(result['items'][0]['qualifiers']['custody'], 'returned')
        self.assertEqual(result['items'][0]['qualifiers']['intended_action_state'], 'sold')
        self.assertEqual(result['items'][0]['qualifiers']['return_context'], 'recovered_escaped_pet')
        self.assertEqual(review_page(self.collection, 'actions', episode=2, root=self.root)['total'], 0)

    def test_failures_include_original_wording_without_duplicate_context(self):
        self.write(self.base / 'generated/answer-evidence.json', dict(cases=[
            dict(id='case', episode=1, missing_windows=[])]))
        self.write(self.base / 'generated/workbench-original.json', dict(results=[dict(cases=[
            dict(id='case', episode=1, question='Original?', missing_windows=['Paragraph 2'],
                 context_coverage={'returned_windows': 1}, retrieved_context=['HUGE'])])]))
        result = review_page(self.collection, 'failures', root=self.root)
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['items'][0]['wording'], 'original')
        self.assertNotIn('HUGE', json.dumps(result))

    def test_build_generated_merge_does_not_require_second_verification(self):
        path = self.root / 'scripts/process_lore_batch.py'
        script = path.read_text().replace("if op=='build':", "if op=='build': (b/'annotations.json').write_text('merged')\nif op=='build':")
        path.write_text(script, encoding='utf-8')
        self.assertEqual(verify(self.collection, root=self.root)['status'], 'passed')
        self.assertEqual(verify(self.collection, root=self.root)['status'], 'reused')
        (self.base / 'annotations.json').write_text('tampered', encoding='utf-8')
        self.assertEqual(verify(self.collection, root=self.root)['status'], 'passed')
        self.assertEqual((self.base / 'annotations.json').read_text(), 'merged')

    def test_success_reuses_only_exact_inputs_and_outputs(self):
        first = verify(self.collection, root=self.root)
        self.assertEqual(first['status'], 'passed')
        self.assertTrue(all(s['elapsed_seconds'] >= 0 for s in first['steps']))
        self.assertEqual(verify(self.collection, root=self.root)['status'], 'reused')
        (self.base / 'reviews/note.md').write_text('New review', encoding='utf-8')
        self.assertEqual(verify(self.collection, root=self.root)['status'], 'passed')
        (self.base / 'generated/lore.sqlite3').write_bytes(b'altered')
        self.assertEqual(verify(self.collection, root=self.root)['status'], 'passed')
        self.assertFalse((self.base / 'episode-review-ledger.json').exists())

    def test_shared_code_change_and_force_rerun(self):
        verify(self.collection, root=self.root)
        (self.root / 'scripts/new.py').write_text('# new shared code', encoding='utf-8')
        self.assertEqual(verify(self.collection, root=self.root)['status'], 'passed')
        self.assertEqual(verify(self.collection, force=True, root=self.root)['status'], 'passed')

    def test_failed_build_stops_downstream_and_never_reuses_failure(self):
        (self.base / 'fail-build').touch()
        first = verify(self.collection, root=self.root)
        self.assertEqual(first['status'], 'failed')
        self.assertEqual(len(first['steps']), 1)
        self.assertFalse((self.base / 'generated/workbench-original.json').exists())
        self.assertEqual(verify(self.collection, root=self.root)['status'], 'failed')

    def test_failed_gate_not_approved_or_cached(self):
        ledger = dict(episodes=[], review_binding={'sha256': 'unchanged'})
        self.write(self.base / 'episode-review-ledger.json', ledger)
        (self.base / 'fail-gate').touch()
        result = verify(self.collection, root=self.root)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['steps'][-1]['check'], 'gate')
        self.assertEqual(json.loads((self.base / 'episode-review-ledger.json').read_text()), ledger)

    def test_input_mutation_during_checks_prevents_reuse(self):
        path = self.root / 'scripts/evaluate_lore_questions.py'
        path.write_text("import pathlib,sys\np=pathlib.Path(sys.argv[-1])/'changed'\np.write_text('changed')\nprint('{}')\n", encoding='utf-8')
        result = verify(self.collection, root=self.root)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['steps'][-1]['check'], 'stable_inputs')


if __name__ == '__main__':
    unittest.main()
