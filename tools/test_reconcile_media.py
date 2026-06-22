#!/usr/bin/env python3
"""Unit tests for reconcile-media.py — all four drift classes, no files/network.

Run: python3 tools/test_reconcile_media.py
"""
import importlib.util, os, unittest

_spec = importlib.util.spec_from_file_location(
    "reconcile_media", os.path.join(os.path.dirname(__file__), "reconcile-media.py"))
rm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rm)

BASE = "https://r2.example"


def cat(*eps):
    return {"claude_code": {"title": "claude code", "meta": "", "episodes": list(eps)}, "extras": []}


def ep(n, v916=None):
    e = {"ep": f"Ep {n}", "title": f"t{n}", "desc": "d",
         "poster": f"videos/claude-ep{n}-poster.jpg", "file": f"videos/claude-ep{n}-45.mp4"}
    e["v916"] = v916
    return e


def r2(*keys):
    return {k: {"key": k, "size": 1, "etag": "x"} for k in keys}


class ReconcileTests(unittest.TestCase):
    def test_clean(self):
        c = cat(ep(1, f"{BASE}/claude-ep1-916.mp4"))
        rep, upd, changed = rm.reconcile(c, r2("claude-ep1-45.mp4", "claude-ep1-916.mp4"),
                                         {"1": True}, BASE)
        self.assertTrue(rep["clean"])
        self.assertFalse(changed)
        self.assertEqual(rep["wiring_drift"], [])
        self.assertEqual(rep["needs_upload"], {})

    def test_wiring_drift_selfheal(self):
        # 916 landed on R2 (e.g. after a backfill) but catalog v916 is still null
        c = cat(ep(17, None))
        rep, upd, changed = rm.reconcile(c, r2("claude-ep17-45.mp4", "claude-ep17-916.mp4"),
                                         {"17": True}, BASE)
        self.assertEqual(rep["wiring_drift"], ["17"])
        self.assertTrue(changed)
        self.assertEqual(upd["claude_code"]["episodes"][0]["v916"], f"{BASE}/claude-ep17-916.mp4")
        self.assertEqual(rep["needs_upload"], {})  # both formats present

    def test_wired_but_404_strip(self):
        # catalog points to a 916 that is no longer on R2 -> strip, never leave a broken link
        c = cat(ep(5, f"{BASE}/claude-ep5-916.mp4"))
        rep, upd, changed = rm.reconcile(c, r2("claude-ep5-45.mp4"), {"5": True}, BASE)
        self.assertEqual(rep["wired_404"], ["5"])
        self.assertIsNone(upd["claude_code"]["episodes"][0]["v916"])
        self.assertIn("5", rep["needs_upload"])
        self.assertEqual(rep["needs_upload"]["5"], ["916"])
        self.assertTrue(changed)

    def test_needs_upload_and_missing_card(self):
        # expected ep18 has no card and no bytes -> both flags
        c = cat(ep(1, f"{BASE}/claude-ep1-916.mp4"))
        rep, upd, changed = rm.reconcile(
            c, r2("claude-ep1-45.mp4", "claude-ep1-916.mp4"),
            {"1": True, "18": True}, BASE)
        self.assertEqual(rep["needs_upload"], {"18": ["45", "916"]})
        self.assertEqual(rep["missing_card"], ["18"])
        self.assertFalse(rep["clean"])
        self.assertFalse(changed)  # no v916 mutation, only flags

    def test_published_false_skipped(self):
        c = cat(ep(1, f"{BASE}/claude-ep1-916.mp4"))
        rep, _, _ = rm.reconcile(c, r2("claude-ep1-45.mp4", "claude-ep1-916.mp4"),
                                 {"1": True, "99": False}, BASE)
        self.assertNotIn("99", rep["needs_upload"])
        self.assertNotIn("99", rep["missing_card"])
        self.assertTrue(rep["clean"])

    def test_upload_ready_vs_render_first(self):
        # ep17 is carded but its bytes are absent (just upload); fable5 has no card and is
        # non-numeric (render first). The report must split the two and render both hints.
        c = cat(ep(17, None))  # carded, v916 null
        rep, _, _ = rm.reconcile(c, r2(), {"17": True, "fable5": True}, BASE)
        self.assertIn("17", rep["needs_upload"])
        self.assertIn("fable5", rep["needs_upload"])
        self.assertEqual(rep["missing_card"], ["fable5"])  # ep17 is carded; fable5 is not
        line = rm.human(rep)
        self.assertIn("r2-sync.sh 17", line)        # carded -> upload command
        self.assertIn("build-ep.sh first", line)    # uncarded -> render-first guidance
        self.assertIn("epfable5", line)


if __name__ == "__main__":
    unittest.main(verbosity=2)
