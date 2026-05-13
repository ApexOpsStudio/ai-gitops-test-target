"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
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


def test_list_tasks_json_output(tmp_path, monkeypatch, capsys):
    """Test JSON list output."""
    tasks_file = tmp_path / ".local" / "share" / "task-cli" / "tasks.json"
    tasks_file.parent.mkdir(parents=True)
    tasks_file.write_text(json.dumps([{"id": 1, "description": "test", "done": False}]))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    list_tasks(json_output=True)

    output = capsys.readouterr().out
    assert json.loads(output) == [{"id": 1, "description": "test", "done": False}]
