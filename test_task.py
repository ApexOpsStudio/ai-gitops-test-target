"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import mark_done, validate_task_id
from commands.list import list_tasks


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


def test_add_task_json_output(tmp_path, monkeypatch, capsys):
    """Add command should support parseable JSON output."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("Write tests", json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == {"id": 1, "description": "Write tests", "done": False}


def test_list_tasks_json_output(tmp_path, monkeypatch, capsys):
    """List command should output a JSON array."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("Write tests")
    capsys.readouterr()
    list_tasks(json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == [{"id": 1, "description": "Write tests", "done": False}]


def test_done_task_json_output(tmp_path, monkeypatch, capsys):
    """Done command should output the updated task as JSON."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("Write tests")
    capsys.readouterr()
    mark_done(1, json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == {"id": 1, "description": "Write tests", "done": True}
