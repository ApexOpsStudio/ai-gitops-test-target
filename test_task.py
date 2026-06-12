"""Basic tests for task CLI."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
from io import StringIO

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


def test_add_task_json_output(capsys):
    """Test add task with --json flag outputs valid JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = Path(tmpdir) / "tasks.json"
        with patch("commands.add.get_tasks_file", return_value=tasks_file):
            add_task("Test task", json_output=True)
            captured = capsys.readouterr()
            output = json.loads(captured.out)
            assert output["status"] == "created"
            assert output["task"]["description"] == "Test task"
            assert output["task"]["id"] == 1
            assert output["task"]["done"] is False


def test_list_tasks_json_output_empty(capsys):
    """Test list tasks with --json flag when no tasks exist."""
    with patch("commands.list.validate_task_file", return_value=[]):
        list_tasks(json_output=True)
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["tasks"] == []


def test_list_tasks_json_output_with_tasks(capsys):
    """Test list tasks with --json flag when tasks exist."""
    tasks = [
        {"id": 1, "description": "Task 1", "done": False},
        {"id": 2, "description": "Task 2", "done": True},
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = Path(tmpdir) / "tasks.json"
        tasks_file.write_text(json.dumps(tasks))
        with patch("commands.list.validate_task_file", return_value=tasks_file):
            list_tasks(json_output=True)
            captured = capsys.readouterr()
            output = json.loads(captured.out)
            assert len(output["tasks"]) == 2
            assert output["tasks"][0]["description"] == "Task 1"
            assert output["tasks"][1]["done"] is True


def test_mark_done_json_output(capsys):
    """Test mark done with --json flag outputs valid JSON."""
    tasks = [{"id": 1, "description": "Test task", "done": False}]
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = Path(tmpdir) / "tasks.json"
        tasks_file.write_text(json.dumps(tasks))
        with patch("commands.done.get_tasks_file", return_value=tasks_file):
            mark_done(1, json_output=True)
            captured = capsys.readouterr()
            output = json.loads(captured.out)
            assert output["status"] == "completed"
            assert output["task"]["done"] is True
            assert output["task"]["id"] == 1


def test_mark_done_json_output_no_tasks(capsys):
    """Test mark done with --json flag when no tasks file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = Path(tmpdir) / "tasks.json"
        with patch("commands.done.get_tasks_file", return_value=tasks_file):
            mark_done(1, json_output=True)
            captured = capsys.readouterr()
            output = json.loads(captured.out)
            assert output["status"] == "error"
            assert "No tasks found" in output["message"]


def test_add_task_human_output(capsys):
    """Test add task without --json flag outputs human-readable text."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = Path(tmpdir) / "tasks.json"
        with patch("commands.add.get_tasks_file", return_value=tasks_file):
            add_task("Test task", json_output=False)
            captured = capsys.readouterr()
            assert "Added task 1: Test task" in captured.out


def test_list_tasks_human_output(capsys):
    """Test list tasks without --json flag outputs human-readable text."""
    tasks = [{"id": 1, "description": "Task 1", "done": False}]
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = Path(tmpdir) / "tasks.json"
        tasks_file.write_text(json.dumps(tasks))
        with patch("commands.list.validate_task_file", return_value=tasks_file):
            list_tasks(json_output=False)
            captured = capsys.readouterr()
            assert "[ ] 1. Task 1" in captured.out


def test_mark_done_human_output(capsys):
    """Test mark done without --json flag outputs human-readable text."""
    tasks = [{"id": 1, "description": "Test task", "done": False}]
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = Path(tmpdir) / "tasks.json"
        tasks_file.write_text(json.dumps(tasks))
        with patch("commands.done.get_tasks_file", return_value=tasks_file):
            mark_done(1, json_output=False)
            captured = capsys.readouterr()
            assert "Marked task 1 as done: Test task" in captured.out
