"""Source-bound regressions for batches following the fixed pilot."""
from pathlib import Path
import sys
import unittest
import copy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from lore_store import ROOT, LoreStore, build
from process_lore_batch import check_accounting, sample_check, answers
from lore_store import read
from evaluate_lore_continuity import evaluate, review_digest


class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.cases = read(ROOT / 'batches/reviews/continuity-cases.json')['cases']

    def test_all_nine_paired_source_answers_retrieve_context(self):
        result = evaluate(self.cases)
        self.assertEqual((result['passed'], result['total'], result['source_checks']), (9, 9, 24))

    def test_changed_answer_cannot_inherit_manual_pass(self):
        cases = copy.deepcopy(self.cases)
        cases[0]['answer'] = 'Johnny never finished it.'
        with self.assertRaisesRegex(ValueError, 'manual review is stale'):
            evaluate(cases)

    def test_reversed_report_order_is_rejected(self):
        cases = copy.deepcopy(self.cases[:1])
        cases[0]['sources'].reverse()
        cases[0]['review']['snapshot_sha256'] = review_digest(cases[0])
        with self.assertRaisesRegex(ValueError, 'chronologically ordered'):
            evaluate(cases)

    def test_changed_source_hash_is_rejected(self):
        cases = copy.deepcopy(self.cases[:1])
        cases[0]['sources'][0]['source_sha256'] = '0' * 64
        cases[0]['review']['snapshot_sha256'] = review_digest(cases[0])
        with self.assertRaisesRegex(ValueError, 'source changed'):
            evaluate(cases)


class Batch003Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ROOT / 'batches/003'
        build(collection='batches/003')
        cls.store = LoreStore(collection='batches/003')

    @classmethod
    def tearDownClass(cls):
        cls.store.close()

    def test_all_source_sections_accounted(self):
        self.assertEqual(check_accounting(self.base), 183)

    def test_all_frozen_references_repaired(self):
        result = sample_check(self.base, 'batches/003')
        self.assertEqual((result['passed'], result['total']), (24, 24))

    def test_turok_series_is_not_first_game(self):
        episode = next(e for e in self.store._items('episodes') if e['source']['episode_number'] == 202)
        series = next(g for g in episode['games'] if g['id'] == 'cq202-g130')
        first = next(g for g in episode['games'] if g['id'] == 'cq202-g018')
        self.assertEqual(series['entity_granularity'], 'series')
        self.assertNotEqual(first['entity_granularity'], 'series')

    def test_kat_identity_is_consistent(self):
        episode = next(e for e in self.store._items('episodes') if e['source']['episode_number'] == 76)
        self.assertEqual({p['name'] for p in episode['participants']}, {'Johnny', 'Kat', 'Tyler'})
        self.assertTrue(any(c['episode'] == 76 and 'Skylar' in c['title'] for c in self.store.actions('Kat', 'played')))

    def test_remake_plan_is_not_completed_play(self):
        played = [c for c in self.store.actions('Johnny', 'played') if c['episode'] == 9]
        self.assertFalse(any(c['title'] == 'Final Fantasy VII Remake' for c in played))
        self.assertTrue(any('handheld remakes' in c['title'] for c in played))

    def test_original_vii_and_remake_rank_separately(self):
        games = {r['title']: r for r in self.store.top_games(9, limit=10)['results']}
        self.assertEqual(games['Final Fantasy VII Remake']['substantial_coverage'], 12)
        self.assertEqual(games['Final Fantasy VII']['substantial_coverage'], 0)

    def test_actual_answers_have_all_required_context(self):
        result = answers(self.base, 'batches/003')
        self.assertEqual((result['passed'], result['total']), (22, 22))


class Batch004005Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stores = {}
        for batch in ('004', '005'):
            build(collection='batches/' + batch)
            cls.stores[batch] = LoreStore(collection='batches/' + batch)

    @classmethod
    def tearDownClass(cls):
        for store in cls.stores.values():
            store.close()

    def test_both_complete_source_maps(self):
        self.assertEqual(check_accounting(ROOT / 'batches/004'), 218)
        self.assertEqual(check_accounting(ROOT / 'batches/005'), 186)

    def test_both_frozen_samples(self):
        for batch, count in [('004', 14), ('005', 21)]:
            result = sample_check(ROOT / ('batches/' + batch), 'batches/' + batch)
            self.assertEqual((result['passed'], result['total']), (count, count))

    def test_all_actual_answer_contexts(self):
        for batch, count in [('004', 25), ('005', 27)]:
            result = answers(ROOT / ('batches/' + batch), 'batches/' + batch)
            self.assertEqual((result['passed'], result['total']), (count, count))

    def test_maze_inclination_is_not_purchase(self):
        claims = self.stores['004']._items('claims')
        maze = [c for c in claims if c['id'] == 'cq077-action-008']
        self.assertEqual([c['action_state'] for c in maze], ['wanted'])

    def test_xbox_manual_actor_remains_unknown(self):
        claim = next(c for c in self.stores['004']._items('claims') if c['id'] == 'cq077-action-010')
        self.assertIsNone(claim['subject'])
        self.assertEqual(claim['action_state'], 'received')

    def test_scooby_variants_union_and_series_is_separate(self):
        result = self.stores['004'].top_games(77, limit=20)
        spooky = [r for r in result['results'] if 'Spooky Swamp' in r['title']]
        self.assertEqual(len(spooky), 1)
        self.assertEqual(spooky[0]['coverage'], 2)
        self.assertEqual(result['series_results'][0]['coverage'], 5)

    def test_re4_controller_is_not_game_duration(self):
        result = self.stores['005'].top_games(78, limit=100)
        re4 = next(r for r in result['results'] if r['title'] == 'Resident Evil 4')
        self.assertEqual(re4['coverage'], 3)
        self.assertFalse(any('Hobbit' in r['title'] or 'Metallica' in r['title'] for r in result['results']))

    def test_absent_gamegear_empire_is_not_released_game(self):
        spans = self.stores['005']._items('spans')
        negative = next(s for s in spans if 'cq011-g043' in s['game_refs'])
        self.assertEqual(negative['entity_kind'], 'hypothetical_game')
        self.assertEqual(negative['role'], 'PASSING_MENTION')

    def test_rendering_reissue_purchase_overrides_misunderstanding(self):
        claims = {c['id']: c for c in self.stores['005']._items('claims')}
        self.assertEqual(claims['cq204-action-020']['action_state'], 'purchased')
        self.assertEqual(claims['cq204-action-020']['subject'], 'Johnny')
        self.assertNotEqual(claims['cq204-action-019']['action_state'], 'received')


class Batch006Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ROOT / 'batches/006'
        build(collection='batches/006')
        cls.store = LoreStore(collection='batches/006')

    @classmethod
    def tearDownClass(cls):
        cls.store.close()

    def test_complete_sections_and_frozen_references(self):
        self.assertEqual(check_accounting(self.base), 246)
        result = sample_check(self.base, 'batches/006')
        self.assertEqual((result['passed'], result['total']), (22, 22))

    def test_all_actual_answer_contexts(self):
        result = answers(self.base, 'batches/006')
        self.assertEqual((result['passed'], result['total']), (28, 28))

    def test_joint_actors_are_queryable_not_only_reporter(self):
        for actor, state, claim_id in [
            ('Stefan', 'played', 'cq205-action-015'),
            ('April', 'played', 'cq205-action-015'),
            ('Johnny', 'owned', 'cq205-action-032'),
            ('Carly', 'owned', 'cq205-action-032'),
        ]:
            self.assertIn(claim_id, {c['id'] for c in self.store.actions(actor, state)})

    def test_missing_play_reports_keep_unknown_actor(self):
        claims = {c['id']: c for c in self.store._items('claims')}
        for claim_id in ('cq205-action-073', 'cq205-action-074'):
            self.assertEqual(claims[claim_id]['action_state'], 'played')
            self.assertIsNone(claims[claim_id]['subject'])
            self.assertEqual(claims[claim_id]['speaker']['confidence'], 'unknown')

    def test_movie_window_does_not_inflate_game(self):
        span = next(s for s in self.store._items('spans') if s['id'] == 'cq205-span-125-2')
        self.assertEqual(span['role'], 'PASSING_MENTION')

    def test_shallow_ties_and_compilation_stay_honest(self):
        result = self.store.top_games(12, limit=100)
        self.assertEqual(sum(r['coverage'] == 2 for r in result['results']), 9)
        result = self.store.top_games(79, limit=100)
        self.assertEqual(result['results'][0]['title'], 'Super Mario Odyssey')
        self.assertFalse(any('Duck Hunt' in r['title'] for r in result['results']))


class Batch007Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ROOT / 'batches/007'
        build(collection='batches/007')
        cls.store = LoreStore(collection='batches/007')

    @classmethod
    def tearDownClass(cls):
        cls.store.close()

    def test_complete_sections_and_repaired_frozen_references(self):
        self.assertEqual(check_accounting(self.base), 129)
        result = sample_check(self.base, 'batches/007')
        self.assertEqual((result['passed'], result['total']), (26, 26))

    def test_all_actual_answer_contexts(self):
        result = answers(self.base, 'batches/007')
        self.assertEqual((result['passed'], result['total']), (25, 25))

    def test_returned_copy_does_not_erase_replacement_history(self):
        returned = {c['id'] for c in self.store.actions('Johnny', 'returned')}
        self.assertIn('cq013-action-71', returned)
        self.assertIn('cq206-action-006', returned)
        owned = {c['id'] for c in self.store.actions('Johnny', 'owned')}
        self.assertIn('cq013-action-31', owned)
        self.assertNotIn('cq206-action-006', owned)

    def test_kat_purchase_not_played_and_husband_not_johnny(self):
        bought = {c['id'] for c in self.store.actions('Kat', 'purchased')}
        self.assertIn('cq080-action-039', bought)
        self.assertFalse(any('Call of Duty' in c['title'] for c in self.store.actions('Kat', 'played')))
        self.assertIn('cq080-action-041', {c['id'] for c in self.store.actions('John', 'played')})
        self.assertNotIn('cq080-action-041', {c['id'] for c in self.store.actions('Johnny', 'played')})

    def test_series_and_prospective_sequel_do_not_merge(self):
        record = next(r for r in self.store._items('episodes') if r['source']['episode_number'] == 206)
        games = {g['id']: g for g in record['games']}
        self.assertEqual(games['cq206-g024']['entity_granularity'], 'series')
        self.assertIsNone(games['cq206-g048']['canonical_title'])
        self.assertNotEqual(games['cq206-g048']['entity_granularity'], 'series')
        spans = [s for s in self.store._items('spans') if 'cq206-g048' in s['game_refs']]
        self.assertTrue(spans)
        self.assertTrue(all(s['role'] == 'PASSING_MENTION' for s in spans))

    def test_normalized_titles_are_not_fabricated_spoken_forms(self):
        record = next(r for r in self.store._items('episodes') if r['source']['episode_number'] == 80)
        for game in record['games']:
            source = ' '.join(e['quote'] for g in game['occurrence_groups'] for e in g['evidence']).casefold()
            for alias in game['spoken_forms']:
                self.assertIn(alias.casefold(), source, game['id'])


class Batch008Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ROOT / 'batches/008'
        build(collection='batches/008')
        cls.store = LoreStore(collection='batches/008')

    @classmethod
    def tearDownClass(cls):
        cls.store.close()

    def test_complete_sections_and_frozen_references(self):
        self.assertEqual(check_accounting(self.base), 226)
        result = sample_check(self.base, 'batches/008')
        self.assertEqual((result['passed'], result['total']), (8, 8))

    def test_all_actual_answer_contexts(self):
        result = answers(self.base, 'batches/008')
        self.assertEqual((result['passed'], result['total']), (31, 31))

    def test_unknown_return_actor_not_assigned_to_tyler(self):
        claim = next(c for c in self.store._items('claims') if c['id'] == 'cq081-action-051')
        self.assertEqual(claim['action_state'], 'returned')
        self.assertIsNone(claim['subject'])
        self.assertNotIn(claim['id'], {c['id'] for c in self.store.actions('Tyler', 'returned')})

    def test_peer_found_owned_states_are_queryable(self):
        self.assertIn('cq081-action-069', {c['id'] for c in self.store.actions('Johnny', 'owned')})
        self.assertTrue({'cq081-action-070', 'cq081-action-071', 'cq081-action-072'} <=
                        {c['id'] for c in self.store.actions('Kat', 'owned')})

    def test_unknown_double_pack_is_not_individual_video_game(self):
        spans = [s for s in self.store._items('spans') if 'cq081-g050' in s['game_refs']]
        self.assertTrue(spans)
        self.assertTrue(all(s['entity_kind'] != 'video_game' for s in spans))

    def test_two_atlantis_receipts_are_retained(self):
        receipts = {c['id'] for c in self.store.actions('Tyler', 'received')}
        self.assertTrue({'cq081-action-062', 'cq081-action-064'} <= receipts)
        self.assertFalse(any('Atlantis' in c['title'] for c in self.store.actions('Tyler', 'returned')))

    def test_guest_steven_is_not_later_cohost_stefan(self):
        episode = next(r for r in self.store._items('episodes') if r['source']['episode_number'] == 14)
        names = {p['name'] for p in episode['participants']}
        self.assertIn('Steven', names)
        self.assertNotIn('Stefan', names)
        self.assertNotIn('Tyler', names)


class Batch009Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ROOT / 'batches/009'
        build(collection='batches/009')
        cls.store = LoreStore(collection='batches/009')

    @classmethod
    def tearDownClass(cls):
        cls.store.close()

    def test_complete_sections_and_frozen_product_references(self):
        self.assertEqual(check_accounting(self.base), 194)
        result = sample_check(self.base, 'batches/009')
        self.assertEqual((result['passed'], result['total'], result['no_title_windows']), (6, 6, 6))

    def test_all_actual_answer_contexts(self):
        result = answers(self.base, 'batches/009')
        self.assertEqual((result['passed'], result['total']), (31, 31))

    def test_incoming_parts_are_not_received(self):
        self.assertIn('cq015-action-018', {c['id'] for c in self.store.actions('Johnny', 'ordered')})
        self.assertFalse(any('Happily Ever After' in c['title'] for c in self.store.actions('Johnny', 'received')))

    def test_guest_interview_does_not_inherit_tyler(self):
        episode = next(r for r in self.store._items('episodes') if r['source']['episode_number'] == 82)
        names = {p['name'] for p in episode['participants']}
        self.assertIn('Steve Torres', names)
        self.assertNotIn('Tyler', names)

    def test_owned_switch_and_wanted_pc_are_distinct(self):
        self.assertIn('cq208-action-028', {c['id'] for c in self.store.actions('Tyler', 'owned')})
        self.assertIn('cq208-action-030', {c['id'] for c in self.store.actions('Tyler', 'wanted')})
        self.assertNotIn('cq208-action-030', {c['id'] for c in self.store.actions('Tyler', 'purchased')})
        self.assertIn('cq208-action-029', {c['id'] for c in self.store.actions('Tyler', 'played')})

    def test_soundtracks_and_pinball_do_not_rank_as_individual_games(self):
        for ep in (82, 208):
            result = self.store.top_games(ep, limit=100)
            self.assertFalse(any('soundtrack' in r['title'].lower() or 'pinball' in r['title'].lower()
                                 for r in result['results']))

    def test_real_outro_recommendation_survives_noise_filter(self):
        claim = next(c for c in self.store._items('claims') if c['id'] == 'cq208-action-077')
        self.assertEqual(claim['action_state'], 'mentioned')
        self.assertIsNone(claim['subject'])
        bundle = self.store.answer_evidence('Evil Twin Cyprian creepy Tim Burton', 208)
        self.assertTrue({'02:11:54', '02:12:56'} <= {r['title'] for r in bundle['context']})


if __name__ == '__main__':
    unittest.main()
