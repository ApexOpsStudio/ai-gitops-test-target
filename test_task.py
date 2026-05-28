"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.list import list_tasks
from commands.done import mark_done
from commands.done import validate_task_id


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


def test_json_output_for_task_commands(tmp_path, monkeypatch, capsys):
    """All task commands should emit parseable JSON when requested."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    add_task("Write tests", json_output=True)
    added = json.loads(capsys.readouterr().out)
    assert added["task"] == {"id": 1, "description": "Write tests", "done": False}

    list_tasks(json_output=True)
    listed = json.loads(capsys.readouterr().out)
    assert listed["tasks"] == [added["task"]]

    mark_done(1, json_output=True)
    done = json.loads(capsys.readouterr().out)
    assert done["task"] == {"id": 1, "description": "Write tests", "done": True}
