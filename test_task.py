"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.list import list_tasks
from commands.done import mark_done
from commands.done import validate_task_id


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


def test_add_task_outputs_json(tmp_path, monkeypatch, capsys):
    """Add command should emit parseable JSON when requested."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("Buy milk", json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == {
        "action": "added",
        "task": {"id": 1, "description": "Buy milk", "done": False},
    }


def test_list_tasks_outputs_json(tmp_path, monkeypatch, capsys):
    """List command should emit parseable JSON when requested."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    add_task("Buy milk")
    capsys.readouterr()

    list_tasks(json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == {
        "tasks": [{"id": 1, "description": "Buy milk", "done": False}]
    }


def test_done_task_outputs_json(tmp_path, monkeypatch, capsys):
    """Done command should emit parseable JSON when requested."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    add_task("Buy milk")
    capsys.readouterr()

    mark_done(1, json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == {
        "action": "completed",
        "task": {"id": 1, "description": "Buy milk", "done": True},
    }
