"""Basic tests for task CLI."""

import json
import pytest
import subprocess
import sys
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


def test_add_task_json_output(monkeypatch, tmp_path, capsys):
    """Test JSON output when adding a task."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("Buy milk", json_output=True)
    output = json.loads(capsys.readouterr().out)

    assert output == {
        "status": "added",
        "task": {"id": 1, "description": "Buy milk", "done": False},
    }


def test_list_tasks_json_output(monkeypatch, tmp_path, capsys):
    """Test JSON output when listing tasks."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    add_task("Buy milk")
    capsys.readouterr()

    list_tasks(json_output=True)
    output = json.loads(capsys.readouterr().out)

    assert output == {
        "tasks": [{"id": 1, "description": "Buy milk", "done": False}],
    }


def test_list_tasks_json_output_when_empty(monkeypatch, tmp_path, capsys):
    """Test JSON output when no tasks exist."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    list_tasks(json_output=True)
    output = json.loads(capsys.readouterr().out)

    assert output == {"tasks": []}


def test_mark_done_json_output(monkeypatch, tmp_path, capsys):
    """Test JSON output when marking a task done."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    add_task("Buy milk")
    capsys.readouterr()

    mark_done(1, json_output=True)
    output = json.loads(capsys.readouterr().out)

    assert output == {
        "status": "done",
        "task": {"id": 1, "description": "Buy milk", "done": True},
    }


def test_cli_json_flag_for_all_commands(tmp_path):
    """Test --json support through the CLI entry point."""
    env = {"HOME": str(tmp_path)}

    add_result = subprocess.run(
        [sys.executable, "task.py", "add", "Buy milk", "--json"],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )
    assert json.loads(add_result.stdout)["status"] == "added"

    list_result = subprocess.run(
        [sys.executable, "task.py", "list", "--json"],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )
    assert json.loads(list_result.stdout) == {
        "tasks": [{"id": 1, "description": "Buy milk", "done": False}],
    }

    done_result = subprocess.run(
        [sys.executable, "task.py", "done", "1", "--json"],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )
    assert json.loads(done_result.stdout) == {
        "status": "done",
        "task": {"id": 1, "description": "Buy milk", "done": True},
    }
