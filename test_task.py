"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task
from utils.validation import validate_description, validate_task_file, validate_task_id


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


def test_validate_task_file_returns_empty_list_when_missing(tmp_path, monkeypatch):
    """Test missing task file validation preserves behavior."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    assert validate_task_file() == []
