"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import load_config, get_config_path, DEFAULT_CONFIG


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


def test_creates_default_config_when_missing(tmp_path):
    """Config file is auto-created with defaults when it doesn't exist."""
    config_path = tmp_path / "config.yaml"
    with patch("task.get_config_path", return_value=config_path):
        result = load_config()

    assert config_path.exists()
    assert result == DEFAULT_CONFIG
    assert "max_tasks: 1000" in config_path.read_text()


def test_reads_existing_config(tmp_path):
    """Existing config file is read without modification."""
    config_path = tmp_path / "config.yaml"
    custom = "storage:\n  format: csv\n"
    config_path.write_text(custom)

    with patch("task.get_config_path", return_value=config_path):
        result = load_config()

    assert result == custom


def test_creates_parent_directories(tmp_path):
    """Parent directories are created if they don't exist."""
    config_path = tmp_path / "deep" / "nested" / "config.yaml"
    with patch("task.get_config_path", return_value=config_path):
        load_config()

    assert config_path.exists()


def test_no_crash_on_missing_config(tmp_path):
    """load_config never raises FileNotFoundError."""
    config_path = tmp_path / "nonexistent" / "config.yaml"
    with patch("task.get_config_path", return_value=config_path):
        result = load_config()

    assert isinstance(result, str)
