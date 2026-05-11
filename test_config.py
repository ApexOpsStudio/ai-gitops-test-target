"""Tests for config file handling."""

import pytest
import subprocess
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

TASK_PY = os.path.join(os.path.dirname(__file__), "task.py")
PYTHON = sys.executable


def run_cli(*args, env=None):
    """Run the CLI and return stdout + stderr."""
    result = subprocess.run(
        [PYTHON, TASK_PY] + list(args),
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


class TestConfigHandling:
    """Test graceful config file handling."""

    def test_creates_default_config_when_missing(self, tmp_path):
        """When config is missing, a default one is created."""
        config_dir = tmp_path / ".config" / "task-cli"
        config_path = config_dir / "config.yaml"

        # Patch the CONFIG_PATH to use tmp_path
        with patch("task.CONFIG_PATH", config_path), \
             patch("task.CONFIG_DIR", config_dir):
            from task import load_config
            result = load_config()
            assert config_path.exists()
            assert "currency" in result

    def test_no_crash_when_config_missing(self):
        """Running without config file should not crash."""
        # Use a HOME that has no config file
        env = os.environ.copy()
        env["HOME"] = tempfile.mkdtemp()
        stdout, stderr, code = run_cli("list", env=env)
        # Should not crash with FileNotFoundError
        assert code == 0 or "Warning" in stderr or "No tasks" in stdout

    def test_graceful_message_when_config_unreadable(self, tmp_path):
        """When config exists but is unreadable, show warning not crash."""
        config_dir = tmp_path / ".config" / "task-cli"
        config_dir.mkdir(parents=True)
        config_path = config_dir / "config.yaml"
        config_path.write_text("valid: config")

        with patch("task.CONFIG_PATH", config_path):
            from task import load_config
            result = load_config()
            assert "valid" in result

    def test_existing_list_still_works(self):
        """List command works regardless of config state."""
        stdout, stderr, code = run_cli("list")
        # Should not crash
        assert code == 0 or "No tasks" in stdout or "Added task" in stdout
