"""Basic tests for task CLI."""

import unittest
from pathlib import Path
from unittest.mock import patch
from commands.add import validate_description
from commands.done import validate_task_id
from task import load_config, get_config_path, DEFAULT_CONFIG


class TestValidateDescription(unittest.TestCase):
    def test_strips_whitespace(self):
        self.assertEqual(validate_description("  test  "), "test")

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            validate_description("")

    def test_too_long_raises(self):
        with self.assertRaises(ValueError):
            validate_description("x" * 201)


class TestValidateTaskId(unittest.TestCase):
    def test_valid_id(self):
        tasks = [{"id": 1}, {"id": 2}]
        self.assertEqual(validate_task_id(tasks, 1), 1)

    def test_zero_raises(self):
        tasks = [{"id": 1}, {"id": 2}]
        with self.assertRaises(ValueError):
            validate_task_id(tasks, 0)

    def test_out_of_range_raises(self):
        tasks = [{"id": 1}, {"id": 2}]
        with self.assertRaises(ValueError):
            validate_task_id(tasks, 99)


class TestLoadConfig(unittest.TestCase):
    """Tests for config loading with missing file handling."""

    def test_creates_default_config_when_missing(self):
        """Config file is auto-created with defaults when it doesn't exist."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "config.yaml"
            with patch("task.get_config_path", return_value=config_path):
                result = load_config()

            self.assertTrue(config_path.exists())
            self.assertEqual(result, DEFAULT_CONFIG)
            self.assertIn("max_tasks: 1000", config_path.read_text())

    def test_reads_existing_config(self):
        """Existing config file is read without modification."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "config.yaml"
            custom = "storage:\n  format: csv\n"
            config_path.write_text(custom)

            with patch("task.get_config_path", return_value=config_path):
                result = load_config()

            self.assertEqual(result, custom)

    def test_creates_parent_directories(self):
        """Parent directories are created if they don't exist."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "deep" / "nested" / "config.yaml"
            with patch("task.get_config_path", return_value=config_path):
                load_config()

            self.assertTrue(config_path.exists())

    def test_no_crash_on_missing_config(self):
        """load_config never raises FileNotFoundError."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "nonexistent" / "config.yaml"
            with patch("task.get_config_path", return_value=config_path):
                try:
                    result = load_config()
                except FileNotFoundError:
                    self.fail("load_config raised FileNotFoundError")
            self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
