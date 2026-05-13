"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from utils.paths import get_tasks_file
from utils.validation import validate_task_file


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


def test_shared_task_file_path(monkeypatch, tmp_path):
    """Test shared task file helpers preserve the existing path contract."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    tasks_file = get_tasks_file()
    assert tasks_file == tmp_path / ".local" / "share" / "task-cli" / "tasks.json"
    assert validate_task_file() == []
    tasks_file.parent.mkdir(parents=True)
    tasks_file.write_text("[]")
    assert validate_task_file() == tasks_file
