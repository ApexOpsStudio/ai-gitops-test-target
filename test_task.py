"""Basic tests for task CLI."""

import json
import os
import pytest
import subprocess
import sys
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id


ROOT = Path(__file__).resolve().parent


def run_cli(tmp_path, *args):
    """Run the task CLI with an isolated HOME."""
    env = {**os.environ, "HOME": str(tmp_path)}
    result = subprocess.run(
        [sys.executable, str(ROOT / "task.py"), *args],
        text=True,
        capture_output=True,
        env=env,
        check=True,
    )
    return result.stdout.strip()


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


def test_add_outputs_json_when_requested(tmp_path):
    """The add command should support machine-readable JSON output."""
    output = run_cli(tmp_path, "add", "--json", "Buy groceries")

    payload = json.loads(output)
    assert payload["task"] == {"id": 1, "description": "Buy groceries", "done": False}
    assert payload["message"] == "Added task 1"


def test_list_outputs_json_when_requested(tmp_path):
    """The list command should emit a JSON task array."""
    run_cli(tmp_path, "add", "Buy groceries")

    output = run_cli(tmp_path, "list", "--json")

    payload = json.loads(output)
    assert payload == {
        "tasks": [{"id": 1, "description": "Buy groceries", "done": False}]
    }


def test_done_outputs_json_when_requested(tmp_path):
    """The done command should emit the updated task as JSON."""
    run_cli(tmp_path, "add", "Buy groceries")

    output = run_cli(tmp_path, "done", "--json", "1")

    payload = json.loads(output)
    assert payload["task"] == {"id": 1, "description": "Buy groceries", "done": True}
    assert payload["message"] == "Marked task 1 as done"
