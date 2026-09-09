"""Regression checks for episode identity and incomplete caption detection."""

import unittest
from build_library import caption_coverage, episode_number, match_episode


class ArchiveIdentityTests(unittest.TestCase):
    def test_legacy_renumbering_and_publisher_typo(self):
        self.assertEqual(episode_number("Episode 3 (8) - Holiday Memories"), 8)
        self.assertEqual(episode_number("Episide 128 - Rare Games"), 128)

    def test_duplicate_upload_requires_unambiguous_evidence(self):
        entries = [
            {"title": "CQ 263 - Favorite Games", "episode_number": 263, "source_url": "https://soundcloud.com/a/original"},
            {"title": "CQ 263 - Favorite Games", "episode_number": 263, "source_url": "https://soundcloud.com/a/reupload"},
        ]
        self.assertIsNone(match_episode(entries, "CQ 263 - Favorite Games"))
        self.assertIs(match_episode(entries, "CQ 263 - Favorite Games", "https://soundcloud.com/a/reupload"), entries[1])

    def test_same_number_different_subject_does_not_merge(self):
        entries = [{"title": "CQ 219 - What Is Rare?", "episode_number": 219, "source_url": "https://soundcloud.com/a/main"}]
        self.assertIsNone(match_episode(entries, "CQ 219X - An Extended Interview About Neo Geo Collecting"))

    def test_captions_cut_off_halfway_are_flagged(self):
        rows = [{"start": 0, "duration": 2, "text": "Opening"}, {"start": 500, "duration": 2, "text": "Middle"}]
        self.assertEqual(caption_coverage(rows, 3600)[0], "possible partial capture")
        rows.append({"start": 3590, "duration": 3, "text": "Goodbye"})
        self.assertEqual(caption_coverage(rows, 3600)[0], "reaches near video end")


if __name__ == "__main__":
    unittest.main()
