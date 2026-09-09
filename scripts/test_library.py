"""Regression checks for episode identity and incomplete caption detection."""

import unittest
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import build_library
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

    def test_airtable_only_entry_reads_its_original_attachment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo, source = root / "repo", root / "raw"
            repo.mkdir()
            source.mkdir()
            (source / "collectors-quest.rss").write_text('<rss><channel><item><title>Episode 5 - New Host</title><guid>tag:soundcloud,2010:tracks/123</guid><pubDate>Tue, 24 Nov 2015 00:00:00 GMT</pubDate><link>https://soundcloud.com/example/episode5</link></item></channel></rss>', encoding="utf-8")
            (source / "original-attachment.txt").write_text("Original source words. " * 100, encoding="utf-8")
            record = {"title": "Episode 2 - Types of Collectors", "episode_number": 2, "source_url": "https://soundcloud.com/example/episode2", "publication_date": "2015-10-01", "path": "original-attachment.txt", "status": "transcript"}
            (source / "airtable-transcripts.json").write_text(json.dumps([record]), encoding="utf-8")
            with patch.object(build_library, "ROOT", repo), patch("sys.argv", ["build_library", "--source-dir", str(source)]), redirect_stdout(io.StringIO()):
                build_library.main()
            result = json.loads((repo / "library/manifest.json").read_text(encoding="utf-8"))
            added = next(e for e in result["entries"] if e["episode_number"] == 2)
            self.assertEqual(added["transcript_words"], 300)
            self.assertEqual(added["date"], "2015-10-01")
            self.assertIn("Original source words.", (repo / "library" / added["path"]).read_text())


if __name__ == "__main__":
    unittest.main()
