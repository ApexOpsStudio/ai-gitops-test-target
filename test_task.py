"""Basic tests for task CLI."""

import json
import pytest
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from commands.done import mark_done
from commands.list import list_tasks
from task import get_config_path, load_config


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
    """Test JSON output for add, list, and done commands."""
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    added = add_task("Buy groceries", json_output=True)
    add_output = json.loads(capsys.readouterr().out)
    assert add_output == {"task": added}
    assert add_output["task"]["description"] == "Buy groceries"
    assert add_output["task"]["done"] is False

    listed = list_tasks(json_output=True)
    list_output = json.loads(capsys.readouterr().out)
    assert list_output == {"tasks": listed}
    assert list_output["tasks"][0]["description"] == "Buy groceries"

    completed = mark_done(1, json_output=True)
    done_output = json.loads(capsys.readouterr().out)
    assert done_output == {"task": completed}
    assert done_output["task"]["done"] is True


def test_missing_config_file_is_created(tmp_path, monkeypatch):
    """Test missing config file is created instead of crashing."""
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    config_path = get_config_path()
    assert not config_path.exists()

    config = load_config()

    assert config_path.exists()
    assert "storage:" in config
    assert "display:" in config
