"""Tests for task CLI."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done
from utils.validation import validate_description, validate_task_id
from utils.paths import get_tasks_file, get_config_file
from task import load_config


# --- Validation tests ---

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


# --- Config loading tests ---

def test_load_config_missing_file(tmp_path):
    """Test that load_config returns empty string when config is missing."""
    missing = tmp_path / "nonexistent" / "config.yaml"
    with patch("task.get_config_file", return_value=missing):
        result = load_config()
    assert result == ""


def test_load_config_existing_file(tmp_path):
    """Test that load_config returns file content when config exists."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("key: value\n")
    with patch("task.get_config_file", return_value=config_file):
        result = load_config()
    assert result == "key: value\n"


# --- JSON output tests ---

def test_add_task_json_output(tmp_path, capsys):
    """Test that add_task outputs valid JSON when json_output=True."""
    tasks_file = tmp_path / "tasks.json"
    with patch("commands.add.get_tasks_file", return_value=tasks_file):
        add_task("test task", json_output=True)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["status"] == "added"
    assert data["task"]["description"] == "test task"
    assert data["task"]["done"] is False


def test_add_task_text_output(tmp_path, capsys):
    """Test that add_task outputs human-readable text by default."""
    tasks_file = tmp_path / "tasks.json"
    with patch("commands.add.get_tasks_file", return_value=tasks_file):
        add_task("test task")

    captured = capsys.readouterr()
    assert "Added task" in captured.out
    assert "test task" in captured.out


def test_list_tasks_json_output(tmp_path, capsys):
    """Test that list_tasks outputs valid JSON when json_output=True."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps([{"id": 1, "description": "task one", "done": False}]))
    with patch("commands.list.get_tasks_file", return_value=tasks_file):
        list_tasks(json_output=True)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert isinstance(data, list)
    assert data[0]["description"] == "task one"


def test_list_tasks_empty_json_output(tmp_path, capsys):
    """Test that list_tasks outputs empty JSON array when no tasks."""
    tasks_file = tmp_path / "no_such_file.json"
    with patch("commands.list.get_tasks_file", return_value=tasks_file):
        list_tasks(json_output=True)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data == []


def test_done_task_json_output(tmp_path, capsys):
    """Test that mark_done outputs valid JSON when json_output=True."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps([{"id": 1, "description": "task one", "done": False}]))
    with patch("commands.done.get_tasks_file", return_value=tasks_file):
        mark_done(1, json_output=True)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["status"] == "done"
    assert data["task"]["done"] is True


def test_done_task_no_file_json_output(tmp_path, capsys):
    """Test that mark_done outputs JSON error when tasks file missing."""
    tasks_file = tmp_path / "no_such_file.json"
    with patch("commands.done.get_tasks_file", return_value=tasks_file):
        mark_done(1, json_output=True)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["status"] == "error"
