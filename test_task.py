"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from utils.validation import validate_description, validate_task_id, validate_task_file
from utils.paths import get_tasks_file


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


def test_validate_task_file_missing(tmp_path):
    """Test validate_task_file with missing file."""
    missing = tmp_path / "nonexistent.json"
    assert validate_task_file(missing) == []


def test_validate_task_file_exists(tmp_path):
    """Test validate_task_file with existing file."""
    existing = tmp_path / "tasks.json"
    existing.write_text("[]")
    assert validate_task_file(existing) == existing


def test_get_tasks_file():
    """Test get_tasks_file returns expected path."""
    result = get_tasks_file()
    assert result.name == "tasks.json"
    assert "task-cli" in str(result)
