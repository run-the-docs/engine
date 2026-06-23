#!/usr/bin/env python3
"""Unit tests for r2-probe.py expected_keys (pure; no network)."""
import importlib.util
import json
import os
import tempfile
import unittest

_spec = importlib.util.spec_from_file_location(
    "rp", os.path.join(os.path.dirname(__file__), "r2-probe.py"))
rp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rp)


class TestExpectedKeys(unittest.TestCase):
    def _dir(self, files):
        d = tempfile.mkdtemp()
        for name, obj in files.items():
            json.dump(obj, open(os.path.join(d, name), "w"))
        return d

    def test_published_and_fable5_and_formats(self):
        d = self._dir({
            "ep17.lines.json": {"title": "x"},          # published implicit -> included
            "ep18.lines.json": {"published": False},     # hole -> excluded
            "epfable5.lines.json": {"title": "f"},        # non-numeric id
        })
        self.assertEqual(set(rp.expected_keys(d)), {
            "claude-ep17-45.mp4", "claude-ep17-916.mp4",
            "claude-epfable5-45.mp4", "claude-epfable5-916.mp4",
        })

    def test_published_false_excluded(self):
        d = self._dir({"ep25.lines.json": {"published": False},
                       "ep5.lines.json": {"published": True}})
        keys = rp.expected_keys(d)
        self.assertNotIn("claude-ep25-45.mp4", keys)
        self.assertIn("claude-ep5-916.mp4", keys)

    def test_non_lines_files_ignored(self):
        d = self._dir({"ep5.lines.json": {}})
        open(os.path.join(d, "notes.md"), "w").write("x")
        open(os.path.join(d, "ep5.timing.json"), "w").write("{}")
        self.assertEqual(set(rp.expected_keys(d)),
                         {"claude-ep5-45.mp4", "claude-ep5-916.mp4"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
