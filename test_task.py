"""Basic tests for task CLI."""

import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import load_config, DEFAULT_CONFIG


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


def test_load_config_creates_default_when_missing(tmp_path):
    """load_config() should create a default config if none exists."""
    fake_config = tmp_path / ".config" / "task-cli" / "config.yaml"
    with patch("task.Path.home", return_value=tmp_path):
        content = load_config()
    assert fake_config.exists(), "Config file should have been created"
    assert "storage" in content


def test_load_config_reads_existing(tmp_path):
    """load_config() should return existing config content without overwriting."""
    config_dir = tmp_path / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text("storage:\n  max_tasks: 42\n")
    with patch("task.Path.home", return_value=tmp_path):
        content = load_config()
    assert "max_tasks: 42" in content


def test_load_config_no_crash_when_missing(tmp_path, capsys):
    """load_config() must not raise FileNotFoundError when config is absent."""
    with patch("task.Path.home", return_value=tmp_path):
        try:
            load_config()
        except FileNotFoundError:
            pytest.fail("load_config() raised FileNotFoundError when config was missing")
    captured = capsys.readouterr()
    assert "Created default config" in captured.err
