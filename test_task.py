"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import main


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


def test_add_outputs_json(tmp_path, monkeypatch, capsys):
    """Add command should emit parseable JSON when requested."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr("sys.argv", ["task.py", "add", "Buy milk", "--json"])

    main()

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "success": True,
        "task": {"id": 1, "description": "Buy milk", "done": False},
    }


def test_list_outputs_json(tmp_path, monkeypatch, capsys):
    """List command should emit parseable JSON when requested."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    add_task("Buy milk")
    capsys.readouterr()
    monkeypatch.setattr("sys.argv", ["task.py", "--json", "list"])

    main()

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "success": True,
        "tasks": [{"id": 1, "description": "Buy milk", "done": False}],
    }


def test_done_outputs_json(tmp_path, monkeypatch, capsys):
    """Done command should emit parseable JSON when requested."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    add_task("Buy milk")
    capsys.readouterr()
    monkeypatch.setattr("sys.argv", ["task.py", "done", "1", "--json"])

    main()

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "success": True,
        "task": {"id": 1, "description": "Buy milk", "done": True},
    }
