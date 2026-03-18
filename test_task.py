"""Tests for task CLI."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
from io import StringIO

from commands.add import add_task, validate_description
from commands.list import list_tasks
from commands.done import mark_done, validate_task_id


# --- Existing tests ---

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


# --- JSON output tests ---

@pytest.fixture
def tmp_tasks_dir(tmp_path):
    """Create a temporary tasks directory and patch get_tasks_file."""
    tasks_file = tmp_path / "tasks.json"

    def _get_tasks_file():
        return tasks_file

    with patch("commands.add.get_tasks_file", _get_tasks_file), \
         patch("commands.list.get_tasks_file", _get_tasks_file), \
         patch("commands.done.get_tasks_file", _get_tasks_file):
        yield tasks_file


class TestAddJsonOutput:
    """Test add command with --json flag."""

    def test_add_json_output(self, tmp_tasks_dir, capsys):
        add_task("Test task", json_output=True)
        output = capsys.readouterr().out
        data = json.loads(output)
        assert data["status"] == "added"
        assert data["task"]["id"] == 1
        assert data["task"]["description"] == "Test task"
        assert data["task"]["done"] is False

    def test_add_plain_output(self, tmp_tasks_dir, capsys):
        add_task("Test task", json_output=False)
        output = capsys.readouterr().out
        assert "Added task 1: Test task" in output


class TestListJsonOutput:
    """Test list command with --json flag."""

    def test_list_empty_json(self, tmp_tasks_dir, capsys):
        list_tasks(json_output=True)
        output = capsys.readouterr().out
        data = json.loads(output)
        assert data["tasks"] == []
        assert data["count"] == 0

    def test_list_with_tasks_json(self, tmp_tasks_dir, capsys):
        add_task("Task one", json_output=False)
        add_task("Task two", json_output=False)
        capsys.readouterr()  # clear add output

        list_tasks(json_output=True)
        output = capsys.readouterr().out
        data = json.loads(output)
        assert data["count"] == 2
        assert len(data["tasks"]) == 2
        assert data["tasks"][0]["description"] == "Task one"

    def test_list_plain_output(self, tmp_tasks_dir, capsys):
        add_task("My task", json_output=False)
        capsys.readouterr()

        list_tasks(json_output=False)
        output = capsys.readouterr().out
        assert "My task" in output


class TestDoneJsonOutput:
    """Test done command with --json flag."""

    def test_done_json_output(self, tmp_tasks_dir, capsys):
        add_task("Finish this", json_output=False)
        capsys.readouterr()

        mark_done(1, json_output=True)
        output = capsys.readouterr().out
        data = json.loads(output)
        assert data["status"] == "done"
        assert data["task"]["done"] is True

    def test_done_no_tasks_json(self, tmp_tasks_dir, capsys):
        mark_done(1, json_output=True)
        output = capsys.readouterr().out
        data = json.loads(output)
        assert data["status"] == "error"
