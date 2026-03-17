"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from commands.validation import validate_description as validation_validate_description
from task import load_config


def test_validate_description():
    """Test description validation."""
    assert validate_description("  test  ") == "test"

    with pytest.raises(ValueError):
        validate_description("")

    with pytest.raises(ValueError):
        validate_description("x" * 201)


def test_validate_description_reuses_shared_validation(monkeypatch):
    """Ensure command validation and shared validation stay aligned."""
    assert validate_description("  shared validation  ") == validation_validate_description(
        "  shared validation  "
    )


def test_validate_task_id():
    """Test task ID validation."""
    tasks = [{"id": 1}, {"id": 2}]
    assert validate_task_id(tasks, 1) == 1

    with pytest.raises(ValueError):
        validate_task_id(tasks, 0)

    with pytest.raises(ValueError):
        validate_task_id(tasks, 99)


def test_load_config_missing_is_safe(monkeypatch, tmp_path):
    """Load config should not crash if config file is missing."""
    monkeypatch.setenv("HOME", str(tmp_path))
    assert load_config() == ""


def test_list_tasks_outputs_json(monkeypatch, tmp_path):
    """list command should emit valid JSON."""
    monkeypatch.setenv("HOME", str(tmp_path))

    with StringIO() as buffer, redirect_stdout(buffer):
        from commands import list as list_cmd

        list_cmd.list_tasks(json_output=True)
        payload = json.loads(buffer.getvalue())

    assert payload == []


def test_add_and_done_json_output(monkeypatch, tmp_path):
    """add and done should return valid JSON."""
    monkeypatch.setenv("HOME", str(tmp_path))
    from commands import add as add_cmd
    from commands import done as done_cmd

    with StringIO() as buffer, redirect_stdout(buffer):
        add_cmd.add_task("test task", json_output=True)
        added = json.loads(buffer.getvalue())

    assert added["status"] == "ok"
    assert added["task"]["description"] == "test task"

    with StringIO() as buffer, redirect_stdout(buffer):
        done_cmd.mark_done(1, json_output=True)
        done_payload = json.loads(buffer.getvalue())

    assert done_payload["status"] == "ok"
    assert done_payload["task"]["id"] == 1
