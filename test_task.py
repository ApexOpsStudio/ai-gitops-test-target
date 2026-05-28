"""Basic tests for task CLI."""

import json
from pathlib import Path

import pytest

from commands.add import add_task
from utils.paths import get_tasks_file
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


def test_validate_task_file_missing(monkeypatch, tmp_path):
    """Test missing task file validation returns an empty list."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    assert validate_task_file() == []


def test_validate_task_file_existing(monkeypatch, tmp_path):
    """Test existing task file validation returns the task file path."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True)
    tasks_file.write_text(json.dumps([]))

    assert validate_task_file() == tasks_file


def test_get_tasks_file(monkeypatch, tmp_path):
    """Test shared tasks file path helper."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    assert get_tasks_file() == tmp_path / ".local" / "share" / "task-cli" / "tasks.json"
