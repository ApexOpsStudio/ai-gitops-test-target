"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import mark_done, validate_task_id
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


def test_json_output(tmp_path, monkeypatch, capsys):
    """Test --json output for add/list/done."""
    monkeypatch.setattr(
        "utils.paths.Path.home", lambda: tmp_path
    )

    add_task("json task", as_json=True)
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "added"
    assert out["id"] == 1
    assert out["description"] == "json task"
    assert out["done"] is False

    list_tasks(as_json=True)
    out = json.loads(capsys.readouterr().out)
    assert out["tasks"][0]["description"] == "json task"

    mark_done(1, as_json=True)
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "done"
    assert out["done"] is True

    list_tasks(as_json=True)
    out = json.loads(capsys.readouterr().out)
    assert out["tasks"][0]["done"] is True
