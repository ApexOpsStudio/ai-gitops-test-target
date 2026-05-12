"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import load_config


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
    """Test that load_config creates a default config when file is missing."""
    fake_config = tmp_path / ".config" / "task-cli" / "config.yaml"
    with patch("task.Path.home", return_value=tmp_path):
        result = load_config()
    assert fake_config.exists()
    assert "storage:" in result
    assert "display:" in result


def test_load_config_reads_existing(tmp_path):
    """Test that load_config reads an existing config file."""
    fake_config = tmp_path / ".config" / "task-cli" / "config.yaml"
    fake_config.parent.mkdir(parents=True)
    fake_config.write_text("custom: true\n")
    with patch("task.Path.home", return_value=tmp_path):
        result = load_config()
    assert result == "custom: true\n"
