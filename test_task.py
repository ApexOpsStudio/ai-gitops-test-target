"""Basic tests for task CLI."""

import json
import sys

import pytest

import task
from commands.add import add_task, validate_description
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


def test_add_command_preserves_human_readable_output(monkeypatch, tmp_path, capsys):
    """Existing plain-text add output stays unchanged by default."""
    monkeypatch.setattr(sys, "argv", ["task.py", "add", "Buy groceries"])
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    task.main()

    assert capsys.readouterr().out == "Added task 1: Buy groceries\n"


def test_add_command_outputs_valid_json(monkeypatch, tmp_path, capsys):
    """The add command supports a parseable --json response."""
    monkeypatch.setattr(sys, "argv", ["task.py", "add", "Buy groceries", "--json"])
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    task.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "success": True,
        "message": "Added task 1: Buy groceries",
        "data": {"task": {"id": 1, "description": "Buy groceries", "done": False}},
    }


def test_add_command_accepts_json_before_subcommand(monkeypatch, tmp_path, capsys):
    """The add command accepts --json before the subcommand."""
    monkeypatch.setattr(sys, "argv", ["task.py", "--json", "add", "Buy groceries"])
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    task.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["data"]["task"] == {"id": 1, "description": "Buy groceries", "done": False}


def test_list_command_outputs_valid_json(monkeypatch, tmp_path, capsys):
    """The list command returns tasks as JSON when requested."""
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    add_task("Buy groceries")
    capsys.readouterr()
    monkeypatch.setattr(sys, "argv", ["task.py", "list", "--json"])

    task.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "success": True,
        "message": "Found 1 task",
        "data": {"tasks": [{"id": 1, "description": "Buy groceries", "done": False}]},
    }


def test_done_command_outputs_valid_json(monkeypatch, tmp_path, capsys):
    """The done command returns the updated task as JSON when requested."""
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    add_task("Buy groceries")
    capsys.readouterr()
    monkeypatch.setattr(sys, "argv", ["task.py", "done", "1", "--json"])

    task.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "success": True,
        "message": "Marked task 1 as done: Buy groceries",
        "data": {"task": {"id": 1, "description": "Buy groceries", "done": True}},
    }


def test_done_command_accepts_json_before_subcommand(monkeypatch, tmp_path, capsys):
    """The done command accepts --json before the subcommand."""
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    add_task("Buy groceries")
    capsys.readouterr()
    monkeypatch.setattr(sys, "argv", ["task.py", "--json", "done", "1"])

    task.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["data"]["task"] == {"id": 1, "description": "Buy groceries", "done": True}


def test_json_flag_also_works_before_subcommand(monkeypatch, tmp_path, capsys):
    """Users can place --json before the subcommand for all commands."""
    monkeypatch.setattr(sys, "argv", ["task.py", "--json", "list"])
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    task.main()

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "success": True,
        "message": "No tasks yet!",
        "data": {"tasks": []},
    }


def test_done_command_outputs_json_error_for_invalid_id(monkeypatch, tmp_path, capsys):
    """Validation errors are machine-readable when --json is requested."""
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    add_task("Buy groceries")
    capsys.readouterr()
    monkeypatch.setattr(sys, "argv", ["task.py", "done", "99", "--json"])

    with pytest.raises(SystemExit) as exc_info:
        task.main()

    assert exc_info.value.code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload == {"success": False, "message": "Invalid task ID: 99", "data": None}


def test_done_command_outputs_json_when_no_tasks_exist(monkeypatch, tmp_path, capsys):
    """The done command returns a JSON envelope if the task file is missing."""
    monkeypatch.setattr(sys, "argv", ["task.py", "done", "1", "--json"])
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    with pytest.raises(SystemExit) as exc_info:
        task.main()

    assert exc_info.value.code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload == {"success": False, "message": "No tasks found!", "data": None}
