"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task
from commands.done import mark_done
from commands.list import list_tasks
from utils.paths import get_tasks_file
from utils.validation import validate_description, validate_task_id, validate_task_file


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


def test_validate_task_file():
    """Test task file validation."""
    nonexistent = Path("/nonexistent/tasks.json")
    assert validate_task_file(nonexistent) == []

    tasks_file = Path("/tmp/test-tasks.json")
    tasks_file.write_text("[]")
    result = validate_task_file(tasks_file)
    assert result == tasks_file
    tasks_file.unlink()


def test_get_tasks_file():
    """Test shared path function."""
    path = get_tasks_file()
    assert path.name == "tasks.json"
    assert "task-cli" in str(path)


def test_add_task(tmp_path, monkeypatch):
    """Test add task uses shared utils."""
    from utils import paths
    import commands.add as add_mod
    task_file = tmp_path / "tasks.json"
    monkeypatch.setattr(paths, "get_tasks_file", lambda: task_file)
    monkeypatch.setattr(add_mod, "get_tasks_file", lambda: task_file)

    add_task("test task")
    assert task_file.exists()
    tasks = json.loads(task_file.read_text())
    assert len(tasks) == 1
    assert tasks[0]["description"] == "test task"


def test_mark_done(tmp_path, monkeypatch):
    """Test mark done uses shared utils."""
    import commands.done as done_mod
    task_file = tmp_path / "tasks.json"
    monkeypatch.setattr(done_mod, "get_tasks_file", lambda: task_file)

    task_file.write_text(json.dumps([{"id": 1, "description": "x", "done": False}]))
    mark_done(1)
    tasks = json.loads(task_file.read_text())
    assert tasks[0]["done"] is True


def test_load_config_creates_default(tmp_path, monkeypatch):
    """Test config creation when file is missing."""
    from utils import paths
    import task as task_mod

    fake_config = tmp_path / "config.yaml"
    monkeypatch.setattr(paths, "get_config_path", lambda: fake_config)
    monkeypatch.setattr(task_mod, "get_config_path", lambda: fake_config)

    result = task_mod.load_config()
    assert fake_config.exists()
    assert "task-cli" in result


def test_load_config_reads_existing(tmp_path, monkeypatch):
    """Test config is read when file exists."""
    from utils import paths
    import task as task_mod

    fake_config = tmp_path / "config.yaml"
    fake_config.write_text("custom: true")
    monkeypatch.setattr(paths, "get_config_path", lambda: fake_config)
    monkeypatch.setattr(task_mod, "get_config_path", lambda: fake_config)

    result = task_mod.load_config()
    assert result == "custom: true"

import io


def test_add_task_json_output(tmp_path, monkeypatch):
    """Test add task with --json flag."""
    import commands.add as add_mod
    task_file = tmp_path / "tasks.json"
    monkeypatch.setattr(add_mod, "get_tasks_file", lambda: task_file)

    buf = io.StringIO()
    monkeypatch.setattr("sys.stdout", buf)
    add_task("json task", json_output=True)
    output = buf.getvalue().strip()
    data = json.loads(output)
    assert data["description"] == "json task"
    assert data["done"] is False
    assert "id" in data


def test_list_tasks_json_output(tmp_path, monkeypatch):
    """Test list tasks with --json flag."""
    import commands.list as list_mod
    task_file = tmp_path / "tasks.json"
    task_file.write_text(json.dumps([{"id": 1, "description": "x", "done": False}]))
    monkeypatch.setattr(list_mod, "get_tasks_file", lambda: task_file)

    buf = io.StringIO()
    monkeypatch.setattr("sys.stdout", buf)
    list_mod.list_tasks(json_output=True)
    output = buf.getvalue().strip()
    data = json.loads(output)
    assert "tasks" in data
    assert len(data["tasks"]) == 1


def test_mark_done_json_output(tmp_path, monkeypatch):
    """Test mark done with --json flag."""
    import commands.done as done_mod
    task_file = tmp_path / "tasks.json"
    task_file.write_text(json.dumps([{"id": 1, "description": "x", "done": False}]))
    monkeypatch.setattr(done_mod, "get_tasks_file", lambda: task_file)

    buf = io.StringIO()
    monkeypatch.setattr("sys.stdout", buf)
    done_mod.mark_done(1, json_output=True)
    output = buf.getvalue().strip()
    data = json.loads(output)
    assert data["done"] is True
