"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from commands.list import list_tasks
from task import load_config


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


def test_load_config_creates_default(monkeypatch, tmp_path):
    """Missing config files are created with defaults."""
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))

    config = load_config()

    assert 'storage = "local"' in config
    assert (tmp_path / ".config" / "task-cli" / "config.yaml").exists()


def test_add_and_list_json_output(monkeypatch, tmp_path, capsys):
    """Add and list commands can emit parseable JSON."""
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))

    add_task("Write tests", json_output=True)
    added = json.loads(capsys.readouterr().out)
    assert added["task"]["description"] == "Write tests"
    assert added["task"]["done"] is False

    list_tasks(json_output=True)
    listed = json.loads(capsys.readouterr().out)
    assert listed["tasks"] == [added["task"]]
