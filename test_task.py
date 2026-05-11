"""Basic tests for task CLI."""

import json
import pytest
from commands import add, done, list as list_command
from commands.add import validate_description
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


def test_json_output_for_add_list_and_done(tmp_path, monkeypatch, capsys):
    """Test JSON output is valid and parseable for each command."""
    tasks_file = tmp_path / "tasks.json"

    monkeypatch.setattr(add, "get_tasks_file", lambda: tasks_file)
    monkeypatch.setattr(list_command, "get_tasks_file", lambda: tasks_file)
    monkeypatch.setattr(done, "get_tasks_file", lambda: tasks_file)

    add.add_task("Write docs", json_output=True)
    add_payload = json.loads(capsys.readouterr().out)
    assert add_payload == {
        "task": {"id": 1, "description": "Write docs", "done": False}
    }

    list_command.list_tasks(json_output=True)
    list_payload = json.loads(capsys.readouterr().out)
    assert list_payload == [{"id": 1, "description": "Write docs", "done": False}]

    done.mark_done(1, json_output=True)
    done_payload = json.loads(capsys.readouterr().out)
    assert done_payload == {
        "task": {"id": 1, "description": "Write docs", "done": True}
    }
