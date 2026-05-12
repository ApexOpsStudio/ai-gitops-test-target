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


def test_add_json_output(monkeypatch, tmp_path, capsys):
    """Test add command JSON output."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("Ship JSON", json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "added"
    assert output["task"] == {"id": 1, "description": "Ship JSON", "done": False}


def test_list_json_output(monkeypatch, tmp_path, capsys):
    """Test list command JSON output."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    add_task("First task")
    capsys.readouterr()

    list_tasks(json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output["tasks"] == [{"id": 1, "description": "First task", "done": False}]


def test_done_json_output(monkeypatch, tmp_path, capsys):
    """Test done command JSON output."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    add_task("Finish me")
    capsys.readouterr()

    mark_done(1, json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "done"
    assert output["task"] == {"id": 1, "description": "Finish me", "done": True}
