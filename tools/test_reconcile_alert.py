#!/usr/bin/env python3
"""Unit tests for reconcile-alert.py (pure; no network, no Discord)."""
import importlib.util
import os
import unittest

_spec = importlib.util.spec_from_file_location(
    "ra", os.path.join(os.path.dirname(__file__), "reconcile-alert.py"))
ra = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ra)


def report(clean=False, needs_upload=None, missing_card=None, drift=None, dead=None,
           fully=10, expected=12):
    return {"clean": clean, "needs_upload": needs_upload or {}, "missing_card": missing_card or [],
            "wiring_drift": drift or [], "wired_404": dead or [],
            "summary": {"fully_on_r2": fully, "expected_episodes": expected}}


class TestHeartbeat(unittest.TestCase):
    def test_clean_and_due_emits_heartbeat(self):
        o = ra.build(report(clean=True, fully=12, expected=12), 0, True)
        self.assertIsNone(o["admin_alert"])
        self.assertIsNotNone(o["heartbeat"])
        self.assertIn("12/12", o["heartbeat"])
        self.assertFalse(o["escalate"])

    def test_clean_not_due_is_silent(self):
        o = ra.build(report(clean=True), 0, False)
        self.assertIsNone(o["admin_alert"])
        self.assertIsNone(o["heartbeat"])

    def test_heartbeat_only_when_clean(self):
        o = ra.build(report(clean=False, needs_upload={"17": ["916"]}), 1, True)
        self.assertIsNone(o["heartbeat"])           # gap present -> no green heartbeat
        self.assertIsNotNone(o["admin_alert"])


class TestAlert(unittest.TestCase):
    def test_upload_ready_gives_r2_sync_line(self):
        o = ra.build(report(needs_upload={"17": ["916"]}), 1, False)
        a = o["admin_alert"]
        self.assertIn("UPLOAD", a)
        self.assertIn("ep17", a)
        self.assertIn("r2-sync.sh 17", a)
        self.assertIn("⚠️", a)
        self.assertFalse(o["escalate"])

    def test_uncarded_is_render_first_not_upload(self):
        o = ra.build(report(needs_upload={"18": ["45", "916"]}, missing_card=["18"]), 1, False)
        a = o["admin_alert"]
        self.assertIn("RENDER+UPLOAD", a)
        self.assertIn("ep18", a)
        self.assertNotIn("r2-sync.sh 18", a)        # no card -> must build first, not just upload

    def test_escalation_at_three_consecutive(self):
        o = ra.build(report(needs_upload={"17": ["916"]}), 3, False)
        self.assertTrue(o["escalate"])
        self.assertIn("URGENT", o["admin_alert"])
        self.assertIn("3×", o["admin_alert"])

    def test_self_healed_drift_is_context_only(self):
        o = ra.build(report(clean=False, needs_upload={"17": ["916"]}, drift=["5"], dead=["9"]), 1, False)
        self.assertIn("self-healed wiring: 1 set, 1 stripped", o["admin_alert"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
