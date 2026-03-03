"""Tests for task CLI."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from commands.utils import validate_description, validate_task_id, get_tasks_file
from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


# ---- Validation tests (utils) ----

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


def test_get_tasks_file():
    """get_tasks_file returns a Path under home."""
    p = get_tasks_file()
    assert isinstance(p, Path)
    assert "task-cli" in str(p)


# ---- JSON output tests ----

def test_add_json_output(tmp_path, capsys, monkeypatch):
    """add_task with json_output=True prints valid JSON."""
    monkeypatch.setattr("commands.utils.get_tasks_file", lambda: tmp_path / "tasks.json")
    monkeypatch.setattr("commands.add.get_tasks_file", lambda: tmp_path / "tasks.json")
    add_task("Buy groceries", json_output=True)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["status"] == "added"
    assert data["task"]["description"] == "Buy groceries"
    assert data["task"]["id"] == 1
    assert data["task"]["done"] is False


def test_list_json_output(tmp_path, capsys, monkeypatch):
    """list_tasks with json_output=True prints valid JSON."""
    tasks = [{"id": 1, "description": "Test", "done": False}]
    (tmp_path / "tasks.json").write_text(json.dumps(tasks))
    monkeypatch.setattr("commands.utils.get_tasks_file", lambda: tmp_path / "tasks.json")
    monkeypatch.setattr("commands.list.get_tasks_file", lambda: tmp_path / "tasks.json")
    list_tasks(json_output=True)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["count"] == 1
    assert data["tasks"][0]["description"] == "Test"


def test_list_json_empty(tmp_path, capsys, monkeypatch):
    """list_tasks JSON output handles empty task list."""
    monkeypatch.setattr("commands.utils.get_tasks_file", lambda: tmp_path / "tasks.json")
    monkeypatch.setattr("commands.list.get_tasks_file", lambda: tmp_path / "tasks.json")
    list_tasks(json_output=True)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["tasks"] == []
    assert data["count"] == 0


def test_done_json_output(tmp_path, capsys, monkeypatch):
    """mark_done with json_output=True prints valid JSON."""
    tasks = [{"id": 1, "description": "Test", "done": False}]
    (tmp_path / "tasks.json").write_text(json.dumps(tasks))
    monkeypatch.setattr("commands.utils.get_tasks_file", lambda: tmp_path / "tasks.json")
    monkeypatch.setattr("commands.done.get_tasks_file", lambda: tmp_path / "tasks.json")
    mark_done(1, json_output=True)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["status"] == "done"
    assert data["task"]["done"] is True


# ---- Config graceful handling tests ----

def test_load_config_creates_default(tmp_path, monkeypatch):
    """load_config creates a default config when missing."""
    from task import load_config, DEFAULT_CONFIG
    config_dir = tmp_path / ".config" / "task-cli"
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    result = load_config()
    assert "storage_path" in result
    assert (config_dir / "config.yaml").exists()


def test_load_config_reads_existing(tmp_path, monkeypatch):
    """load_config reads existing config file without overwriting."""
    from task import load_config
    config_dir = tmp_path / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    (config_dir / "config.yaml").write_text("custom: true\n")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    result = load_config()
    assert "custom: true" in result
