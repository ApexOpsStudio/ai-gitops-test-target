"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from commands.add import add_task, validate_description
from commands.list import list_tasks
from commands.done import mark_done, validate_task_id


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


def test_add_task_json_output(tmp_path, capsys):
    """Test add_task with JSON output."""
    with patch("commands.add.get_tasks_file", return_value=tmp_path / "tasks.json"):
        add_task("test task", json_output=True)
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "added"
    assert output["task"]["description"] == "test task"
    assert output["task"]["id"] == 1


def test_list_tasks_json_output_empty(capsys):
    """Test list_tasks JSON output when no tasks."""
    with patch("commands.list.validate_task_file", return_value=[]):
        list_tasks(json_output=True)
    output = json.loads(capsys.readouterr().out)
    assert output == {"tasks": []}


def test_list_tasks_json_output(tmp_path, capsys):
    """Test list_tasks JSON output with tasks."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps([{"id": 1, "description": "hello", "done": False}]))
    with patch("commands.list.validate_task_file", return_value=tasks_file):
        list_tasks(json_output=True)
    output = json.loads(capsys.readouterr().out)
    assert len(output["tasks"]) == 1
    assert output["tasks"][0]["description"] == "hello"


def test_mark_done_json_output(tmp_path, capsys):
    """Test mark_done with JSON output."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps([{"id": 1, "description": "hello", "done": False}]))
    with patch("commands.done.get_tasks_file", return_value=tasks_file):
        mark_done(1, json_output=True)
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "done"
    assert output["task"]["done"] is True
