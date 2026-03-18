"""Tests for task CLI."""

import json
import pytest
from pathlib import Path

from commands.utils import validate_description, validate_task_id, get_tasks_file


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


def test_get_tasks_file():
    """Test tasks file path."""
    path = get_tasks_file()
    assert path.name == "tasks.json"
    assert "task-cli" in str(path)
