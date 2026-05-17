"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, get_tasks_file, validate_description
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
    """Test JSON output for add command."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("  Buy milk  ", json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == {
        "message": "Added task 1",
        "task": {"id": 1, "description": "Buy milk", "done": False},
    }

    tasks_file = get_tasks_file()
    assert json.loads(tasks_file.read_text()) == [
        {"id": 1, "description": "Buy milk", "done": False}
    ]


def test_list_tasks_json_output(tmp_path, monkeypatch, capsys):
    """Test JSON output for list command."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    tasks_file.write_text(
        json.dumps(
            [
                {"id": 1, "description": "Buy milk", "done": False},
                {"id": 2, "description": "Write tests", "done": True},
            ]
        )
    )

    list_tasks(json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == {
        "tasks": [
            {"id": 1, "description": "Buy milk", "done": False},
            {"id": 2, "description": "Write tests", "done": True},
        ]
    }


def test_mark_done_json_output(tmp_path, monkeypatch, capsys):
    """Test JSON output for done command."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    tasks_file.write_text(
        json.dumps(
            [
                {"id": 1, "description": "Buy milk", "done": False},
                {"id": 2, "description": "Write tests", "done": False},
            ]
        )
    )

    mark_done(2, json_output=True)

    output = json.loads(capsys.readouterr().out)
    assert output == {
        "message": "Marked task 2 as done",
        "task": {"id": 2, "description": "Write tests", "done": True},
    }
    assert json.loads(tasks_file.read_text()) == [
        {"id": 1, "description": "Buy milk", "done": False},
        {"id": 2, "description": "Write tests", "done": True},
    ]
