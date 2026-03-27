"""Basic tests for task CLI."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from utils.validation import validate_description, validate_task_id
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


def test_load_config_missing_file(tmp_path):
    """Test load_config creates default config when file is missing."""
    fake_config = tmp_path / ".config" / "task-cli" / "config.yaml"
    with patch("task.Path.home", return_value=tmp_path):
        result = load_config()
    assert "version: 1" in result
    assert fake_config.exists()


def test_load_config_existing_file(tmp_path):
    """Test load_config reads existing config."""
    config_dir = tmp_path / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text("version: 2\ncustom: true\n")
    with patch("task.Path.home", return_value=tmp_path):
        result = load_config()
    assert "version: 2" in result
