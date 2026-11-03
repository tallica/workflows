"""Tests for tests/workflows.py: python3 -m unittest discover -s tests"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import workflows  # noqa: E402

CALLABLE = "on:\n  workflow_call:\n"


class Workflows(unittest.TestCase):
    def check(self, files):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, ".github", "workflows"))
            for name, text in files.items():
                with open(os.path.join(root, ".github", "workflows", name), "w") as f:
                    f.write(text)
            return "\n".join(workflows.problems(root))

    def test_real_tree_is_clean(self):
        self.assertEqual(list(workflows.problems(os.path.dirname(HERE))), [])

    def test_consistent_set_passes(self):
        self_yml = "jobs:\n  a:\n    uses: ./.github/workflows/a.yml\n"
        self.assertEqual(self.check({"self.yml": self_yml, "a.yml": CALLABLE}), "")

    def test_catches_each_problem(self):
        self_yml = "jobs:\n  a:\n    uses: ./.github/workflows/a.yml\n  b:\n    uses: ./.github/workflows/gone.yml\n"
        found = self.check({"self.yml": self_yml, "a.yml": "on: push\n", "c.yml": CALLABLE})
        self.assertIn("a.yml: not callable", found)
        self.assertIn("c.yml: not called by self.yml", found)
        self.assertIn("calls gone.yml, which doesn't exist", found)
        self.assertEqual(self.check({"a.yml": CALLABLE}), "self.yml is missing")


if __name__ == "__main__":
    unittest.main()
