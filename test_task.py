"""Basic tests for task CLI."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from commands.add import validate_description
from commands.done import validate_task_id


def run_cli(home_dir: Path, *args):
    """Run the task CLI in a sandboxed HOME."""
    env = os.environ.copy()
    env["HOME"] = str(home_dir)

    proc = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "task.py"), *args],
        env=env,
        capture_output=True,
        text=True,
    )
    return proc


class TestValidation(unittest.TestCase):
    def test_validate_description(self):
        self.assertEqual(validate_description("  test  "), "test")

        with self.assertRaises(ValueError):
            validate_description("")

        with self.assertRaises(ValueError):
            validate_description("x" * 201)

    def test_validate_task_id(self):
        tasks = [{"id": 1}, {"id": 2}]
        self.assertEqual(validate_task_id(tasks, 1), 1)

        with self.assertRaises(ValueError):
            validate_task_id(tasks, 0)

        with self.assertRaises(ValueError):
            validate_task_id(tasks, 99)


class TestJsonOutput(unittest.TestCase):
    def test_json_add_list_done_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            proc = run_cli(home, "--json", "add", "Buy groceries")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["success"])
            self.assertEqual(payload["task"]["id"], 1)
            self.assertFalse(payload["task"]["done"])

            proc = run_cli(home, "--json", "list")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["success"])
            self.assertEqual(payload["tasks"][0]["description"], "Buy groceries")

            proc = run_cli(home, "--json", "done", "1")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertTrue(payload["success"])
            self.assertTrue(payload["task"]["done"])

    def test_json_list_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            proc = run_cli(home, "--json", "list")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload, {"success": True, "tasks": []})


if __name__ == "__main__":
    unittest.main()
