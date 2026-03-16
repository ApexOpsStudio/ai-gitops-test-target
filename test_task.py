"""Basic tests for task CLI."""

import json
import pytest
import subprocess
from pathlib import Path
from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done
from utils.validation import validate_description, validate_task_id, validate_task_file
from utils.paths import get_tasks_file


def _patch_tasks_file(monkeypatch, tmp_path):
    """Patch get_tasks_file in all modules that import it."""
    target = tmp_path / "tasks.json"
    monkeypatch.setattr("commands.add.get_tasks_file", lambda: target)
    monkeypatch.setattr("commands.list.get_tasks_file", lambda: target)
    monkeypatch.setattr("commands.done.get_tasks_file", lambda: target)
    return target


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


def test_validate_task_file(tmp_path):
    """Test task file validation."""
    # Non-existent file returns empty list
    missing = tmp_path / "nonexistent.json"
    assert validate_task_file(missing) == []

    # Existing file returns the path
    existing = tmp_path / "tasks.json"
    existing.write_text("[]")
    assert validate_task_file(existing) == existing


def test_get_tasks_file():
    """Test shared path helper returns expected path."""
    result = get_tasks_file()
    assert result == Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def test_add_task(capsys, tmp_path, monkeypatch):
    """Test add command produces correct output."""
    _patch_tasks_file(monkeypatch, tmp_path)
    add_task("Test task")
    output = capsys.readouterr().out.strip()
    assert "Added task 1: Test task" == output


def test_list_empty(capsys, tmp_path, monkeypatch):
    """Test list command with no tasks."""
    _patch_tasks_file(monkeypatch, tmp_path)
    list_tasks()
    output = capsys.readouterr().out.strip()
    assert "No tasks yet!" == output


def test_list_tasks(capsys, tmp_path, monkeypatch):
    """Test list command shows tasks."""
    _patch_tasks_file(monkeypatch, tmp_path)
    add_task("First task")
    add_task("Second task")
    list_tasks()
    output = capsys.readouterr().out.strip()
    assert "1. First task" in output
    assert "2. Second task" in output


def test_mark_done(capsys, tmp_path, monkeypatch):
    """Test done command marks task complete."""
    _patch_tasks_file(monkeypatch, tmp_path)
    add_task("Task to complete")
    mark_done(1)
    lines = capsys.readouterr().out.strip().split("\n")
    assert "Marked task 1 as done: Task to complete" == lines[-1]

    # Verify the file was updated
    tasks = json.loads((tmp_path / "tasks.json").read_text())
    assert tasks[0]["done"] is True
