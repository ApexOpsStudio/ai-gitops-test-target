"""Basic tests for task CLI."""

import json
import os
import subprocess
import sys

import pytest
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import DEFAULT_CONFIG, load_config


def test_validate_description():
    """Test description validation."""
    assert validate_description("  test  ") == "test"

    with pytest.raises(ValueError):
        validate_description("")

    with pytest.raises(ValueError):
        validate_description("x" * 201)


def test_validate_task_id():
    """Test task ID validation."""
    tasks = [{"id": 1}, {"id": 2}]
    assert validate_task_id(tasks, 1) == 1

    with pytest.raises(ValueError):
        validate_task_id(tasks, 0)

    with pytest.raises(ValueError):
        validate_task_id(tasks, 99)


def test_load_config_creates_default_when_missing(tmp_path, monkeypatch):
    """Missing config files are created with sensible defaults instead of crashing."""
    monkeypatch.setenv("HOME", str(tmp_path))

    assert load_config() == DEFAULT_CONFIG
    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    assert config_path.read_text() == DEFAULT_CONFIG


def test_cli_command_creates_default_config_when_missing(tmp_path):
    """CLI commands should run without FileNotFoundError when config is missing."""
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)

    result = subprocess.run(
        [sys.executable, "task.py", "list"],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )

    assert "No tasks yet!" in result.stdout
    assert (tmp_path / ".config" / "task-cli" / "config.yaml").read_text() == DEFAULT_CONFIG
