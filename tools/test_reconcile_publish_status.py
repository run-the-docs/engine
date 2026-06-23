#!/usr/bin/env python3
"""Unit tests for reconcile-publish-status.py (pure core; no network)."""
import importlib.util
import os
import unittest

_spec = importlib.util.spec_from_file_location(
    "rps", os.path.join(os.path.dirname(__file__), "reconcile-publish-status.py"))
rps = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rps)

SAMPLE_RSS = """<?xml version="1.0"?>
<feed>
  <entry><yt:videoId>AAA111</yt:videoId><published>2026-06-23T13:00:05+00:00</published></entry>
  <entry><yt:videoId>BBB222</yt:videoId><published>2026-06-22T19:00:03+00:00</published></entry>
</feed>"""


class TestParseRss(unittest.TestCase):
    def test_extracts_id_and_published(self):
        self.assertEqual(rps.parse_rss(SAMPLE_RSS),
                         {"AAA111": "2026-06-23T13:00:05+00:00",
                          "BBB222": "2026-06-22T19:00:03+00:00"})

    def test_empty_feed(self):
        self.assertEqual(rps.parse_rss("<feed></feed>"), {})


class TestVidOf(unittest.TestCase):
    def test_explicit_youtube_id_wins(self):
        self.assertEqual(rps.vid_of({"youtube_id": "ZZZ", "url": "x?v=YYY"}), "ZZZ")

    def test_parsed_from_url(self):
        self.assertEqual(rps.vid_of({"url": "https://www.youtube.com/watch?v=AAA111"}), "AAA111")

    def test_none_when_unparseable(self):
        self.assertIsNone(rps.vid_of({"url": "https://example.com/nope"}))


class TestRowsFrom(unittest.TestCase):
    def test_flat_list(self):
        self.assertEqual(rps.rows_from([{"video_id": "a"}]), [{"video_id": "a"}])

    def test_raw_mcp_envelope(self):
        env = {"result": [{"results": [{"video_id": "a"}], "success": True}]}
        self.assertEqual(rps.rows_from(env), [{"video_id": "a"}])


class TestReconcile(unittest.TestCase):
    def setUp(self):
        self.rss = rps.parse_rss(SAMPLE_RSS)  # AAA111 + BBB222 public

    def test_published_video_transitions_to_posted_with_real_time(self):
        scheduled = [{"video_id": "cc-ep5", "url": "x?v=AAA111", "publish_at": "2026-06-23T13:00:00Z"}]
        trans, still = rps.reconcile(scheduled, self.rss)
        self.assertEqual(len(trans), 1)
        self.assertEqual(still, [])
        t = trans[0]
        self.assertEqual(t["video_id"], "cc-ep5")
        self.assertEqual(t["new_status"], "posted")
        self.assertEqual(t["new_publish_at"], "2026-06-23T13:00:05+00:00")  # RSS time, not the estimate
        self.assertEqual(t["old_publish_at"], "2026-06-23T13:00:00Z")
        self.assertEqual(t["source"], "rss")

    def test_unpublished_video_stays_scheduled(self):
        scheduled = [{"video_id": "cc-ep9", "url": "x?v=NOTYET", "publish_at": "2026-06-24T16:00:00Z"}]
        trans, still = rps.reconcile(scheduled, self.rss)
        self.assertEqual(trans, [])
        self.assertEqual(len(still), 1)
        self.assertEqual(still[0]["video_id"], "cc-ep9")

    def test_mixed_batch(self):
        scheduled = [
            {"video_id": "cc-ep5", "url": "x?v=AAA111", "publish_at": "p5"},   # public
            {"video_id": "cc-ep9", "url": "x?v=NOTYET", "publish_at": "p9"},   # private
            {"video_id": "cc-ep17", "youtube_id": "BBB222", "publish_at": "p17"},  # public via youtube_id
        ]
        trans, still = rps.reconcile(scheduled, self.rss)
        self.assertEqual({t["video_id"] for t in trans}, {"cc-ep5", "cc-ep17"})
        self.assertEqual({s["video_id"] for s in still}, {"cc-ep9"})

    def test_row_with_no_resolvable_id_stays_scheduled(self):
        scheduled = [{"video_id": "cc-epX", "url": "https://example.com/nope", "publish_at": "pX"}]
        trans, still = rps.reconcile(scheduled, self.rss)
        self.assertEqual(trans, [])
        self.assertEqual(len(still), 1)
        self.assertIsNone(still[0]["youtube_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
