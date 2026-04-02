"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from io import StringIO
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


def test_add_task_json_output(tmp_path, monkeypatch):
    """Test add command JSON output."""
    tasks_file = tmp_path / "tasks.json"
    monkeypatch.setattr("commands.add.get_tasks_file", lambda: tasks_file)

    with patch("sys.stdout", new_callable=StringIO) as mock_out:
        add_task("test task", json_output=True)
        output = json.loads(mock_out.getvalue().strip())

    assert output["success"] is True
    assert output["data"]["id"] == 1
    assert output["data"]["description"] == "test task"
    assert output["data"]["done"] is False


def test_list_tasks_json_output(tmp_path, monkeypatch):
    """Test list command JSON output."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps([
        {"id": 1, "description": "task 1", "done": False},
        {"id": 2, "description": "task 2", "done": True},
    ]))
    monkeypatch.setattr("commands.list.get_tasks_file", lambda: tasks_file)
    monkeypatch.setattr("commands.list.validate_task_file", lambda: tasks_file)

    with patch("sys.stdout", new_callable=StringIO) as mock_out:
        list_tasks(json_output=True)
        output = json.loads(mock_out.getvalue().strip())

    assert output["success"] is True
    assert len(output["data"]) == 2
    assert output["data"][0]["description"] == "task 1"


def test_mark_done_json_output(tmp_path, monkeypatch):
    """Test done command JSON output."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps([
        {"id": 1, "description": "task 1", "done": False},
    ]))
    monkeypatch.setattr("commands.done.get_tasks_file", lambda: tasks_file)

    with patch("sys.stdout", new_callable=StringIO) as mock_out:
        from commands.done import mark_done
        mark_done(1, json_output=True)
        output = json.loads(mock_out.getvalue().strip())

    assert output["success"] is True
    assert output["data"]["done"] is True


def test_list_empty_json_output(tmp_path, monkeypatch):
    """Test list command JSON output with no tasks."""
    monkeypatch.setattr("commands.list.validate_task_file", lambda: None)

    with patch("sys.stdout", new_callable=StringIO) as mock_out:
        list_tasks(json_output=True)
        output = json.loads(mock_out.getvalue().strip())

    assert output["success"] is True
    assert output["data"] == []
