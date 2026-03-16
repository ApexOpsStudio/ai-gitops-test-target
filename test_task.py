"""Tests for task CLI."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from commands.utils import validate_description, validate_task_id, get_tasks_file, load_tasks, save_tasks
from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done
from task import load_config


# --- Validation tests (Issue #3: utils module) ---

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


# --- Config crash fix tests (Issue #2) ---

def test_load_config_creates_default(tmp_path):
    """Test that load_config creates default config when missing."""
    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    with patch.object(Path, 'home', return_value=tmp_path):
        config = load_config()
        assert config_path.exists()
        assert "storage:" in config
        assert "display:" in config


def test_load_config_reads_existing(tmp_path):
    """Test that load_config reads existing config."""
    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("custom: true\n")
    with patch.object(Path, 'home', return_value=tmp_path):
        config = load_config()
        assert "custom: true" in config


# --- JSON output tests (Issue #1) ---

def test_list_tasks_json(tmp_path, capsys):
    """Test JSON output for list command."""
    tasks_file = tmp_path / ".local" / "share" / "task-cli" / "tasks.json"
    tasks_file.parent.mkdir(parents=True)
    tasks_file.write_text(json.dumps([
        {"id": 1, "description": "Test task", "done": False},
        {"id": 2, "description": "Done task", "done": True},
    ]))
    with patch('commands.utils.get_tasks_file', return_value=tasks_file):
        list_tasks(as_json=True)
    output = capsys.readouterr().out
    data = json.loads(output)
    assert len(data) == 2
    assert data[0]["description"] == "Test task"
    assert data[1]["done"] is True


def test_list_tasks_json_empty(tmp_path, capsys):
    """Test JSON output for empty task list."""
    tasks_file = tmp_path / "nonexistent" / "tasks.json"
    with patch('commands.utils.get_tasks_file', return_value=tasks_file):
        list_tasks(as_json=True)
    output = capsys.readouterr().out
    assert json.loads(output) == []


def test_list_tasks_human(tmp_path, capsys):
    """Test human-readable output still works."""
    tasks_file = tmp_path / ".local" / "share" / "task-cli" / "tasks.json"
    tasks_file.parent.mkdir(parents=True)
    tasks_file.write_text(json.dumps([
        {"id": 1, "description": "Buy groceries", "done": False},
    ]))
    with patch('commands.utils.get_tasks_file', return_value=tasks_file):
        list_tasks(as_json=False)
    output = capsys.readouterr().out
    assert "[ ] 1. Buy groceries" in output


# --- Integration tests (utils shared across commands) ---

def test_save_and_load_tasks(tmp_path):
    """Test save/load round-trip through shared utils."""
    tasks_file = tmp_path / "tasks.json"
    with patch('commands.utils.get_tasks_file', return_value=tasks_file):
        save_tasks([{"id": 1, "description": "Test", "done": False}])
        loaded = load_tasks()
        assert len(loaded) == 1
        assert loaded[0]["description"] == "Test"
