"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.list import list_tasks
from commands.done import validate_task_id
from commands.done import mark_done


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


def test_commands_support_json_output(tmp_path, monkeypatch, capsys):
    """Test JSON output for add, list, and done commands."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("Buy groceries", json_output=True)
    created = json.loads(capsys.readouterr().out)
    assert created == {"id": 1, "description": "Buy groceries", "done": False}

    list_tasks(json_output=True)
    listed = json.loads(capsys.readouterr().out)
    assert listed == [created]

    mark_done(1, json_output=True)
    updated = json.loads(capsys.readouterr().out)
    assert updated == {"id": 1, "description": "Buy groceries", "done": True}


def test_empty_json_outputs(tmp_path, monkeypatch, capsys):
    """Test JSON output when no tasks exist."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    list_tasks(json_output=True)
    assert json.loads(capsys.readouterr().out) == []

    mark_done(1, json_output=True)
    assert json.loads(capsys.readouterr().out) == {
        "error": "no_tasks",
        "message": "No tasks found!",
    }
