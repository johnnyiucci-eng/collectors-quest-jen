"""Early draft defects and archive losses fail before expensive integration."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_safeguards import preflight, archive_comparison, record_event, metrics


class SafeguardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / 'batches/001'
        (self.base / 'records').mkdir(parents=True)
        (self.base / 'reviews').mkdir()
        (self.root / 'library').mkdir()
        source = self.root / 'library/source.md'
        source.write_text('### Paragraph 1\nA game\n', encoding='utf-8')
        self.entry = dict(key='one', episode_number=1, path='source.md', record_path='records/one.json',
                          sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        self.record = dict(source=self.entry, games=[], lore=[], corrections=[], topic_coverage=[
            dict(topic='Introduction', locations=['Paragraph 1'])])
        self.annotation = dict(source_key='one', source_sha256=self.entry['sha256'], mapping_status='complete',
                               review_note='Draft full map, not accepted', spans=[],
                               section_accounting=[dict(location='Paragraph 1', summary='Introduction')])
        self.save()

    def save(self):
        for path, data in [(self.base / 'manifest.json', dict(episodes=[self.entry])),
                           (self.base / 'records/one.json', self.record),
                           (self.base / 'reviews/001-annotations.json', dict(episodes=[self.annotation]))]:
            path.write_text(json.dumps(data), encoding='utf-8')

    def check(self):
        return preflight('batches/001', root=self.root)

    def test_clean_preflight_no_database_or_approval(self):
        self.assertEqual(self.check()['status'], 'passed')
        self.assertFalse((self.base / 'generated').exists())
        self.assertFalse((self.base / 'episode-review-ledger.json').exists())

    def test_missing_topic_locations_caught(self):
        del self.record['topic_coverage'][0]['locations']
        self.save()
        self.assertIn('locations array', self.check()['episodes'][0]['reason'])

    def test_missing_review_note_caught(self):
        del self.annotation['review_note']
        self.save()
        self.assertIn('review note', self.check()['episodes'][0]['reason'])

    def test_duplicate_span_caught_before_later_mapping_checks(self):
        span = dict(id='duplicate', role='PASSING_MENTION', reason='Mention', game_refs=['g1'])
        self.annotation['spans'] = [span, span]
        self.save()
        self.assertIn('Duplicate span', self.check()['episodes'][0]['reason'])

    def test_missing_unfinished_draft_is_not_clean(self):
        (self.base / 'records/one.json').unlink()
        self.assertEqual(self.check()['status'], 'failed')

    def test_question_location_typos_fail_before_retrieval(self):
        for filename, field in [('fresh-question-cases.json', 'required_windows'),
                                ('001-annotations.json', 'evidence_locations')]:
            path = self.base / 'reviews' / filename
            original = json.loads(path.read_text()) if path.exists() else {}
            key = 'cases' if field == 'required_windows' else 'task_cases'
            for locations in [[], ['Paragraph 99'], ['Paragraph 1']]:
                with self.subTest(filename=filename, locations=locations):
                    data = {**original, key: [dict(id='question', episode=1, **{field: locations})]}
                    path.write_text(json.dumps(data), encoding='utf-8')
                    self.assertEqual(self.check()['status'], 'passed' if locations == ['Paragraph 1'] else 'failed')
            path.write_text(json.dumps(original), encoding='utf-8')

    def test_archive_same_count_replacement_detected(self):
        row = dict(collection='pilot', episode=1, source_key='one', source_sha256='original')
        baseline = dict(episodes=[row])
        changed = dict(episodes=[dict(row, source_key='replacement')])
        self.assertEqual(archive_comparison(baseline, changed)['status'], 'failed')
        self.assertEqual(archive_comparison(baseline, dict(episodes=[]))['status'], 'failed')
        added = dict(episodes=[row, dict(row, episode=2, source_key='two')])
        self.assertEqual(archive_comparison(baseline, added)['added'], 1)
        self.assertEqual(archive_comparison(baseline, added)['status'], 'passed')

    def test_empty_baseline_rejected(self):
        with self.assertRaises(ValueError):
            archive_comparison(dict(episodes=[]), dict(episodes=[]))

    def test_observed_repeats_separate_reviewers_and_source_versions(self):
        result = dict(episode=1, source_sha='a', items=[dict(location='Paragraph 1')])
        for reviewer in ('root', 'root', 'peer'):
            record_event('batches/001', 'source', result, 0.2, 100, reviewer, self.root)
        record_event('batches/001', 'source', dict(result, source_sha='b'), 0.2, 100, 'root', self.root)
        report = metrics('batches/001', self.root)
        self.assertEqual(report['repeated_window_displays'], 1)
        self.assertEqual(report['source_window_displays'], 4)
        self.assertEqual(report['output_characters'], 400)
        self.assertEqual(report['measured_operation_seconds'], 0.8)


if __name__ == '__main__':
    unittest.main()
