"""Basic tests for task CLI."""

import json
import os
import subprocess
import sys
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
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


def run_cli(tmp_path, *args):
    env = {**os.environ, "HOME": str(tmp_path)}
    result = subprocess.run(
        [sys.executable, "task.py", *args],
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )
    return result.stdout


def test_add_json_output(tmp_path):
    output = run_cli(tmp_path, "add", "Buy groceries", "--json")
    payload = json.loads(output)
    assert payload["success"] is True
    assert payload["task"] == {"id": 1, "description": "Buy groceries", "done": False}


def test_list_json_output(tmp_path):
    run_cli(tmp_path, "add", "Buy groceries", "--json")
    output = run_cli(tmp_path, "list", "--json")
    payload = json.loads(output)
    assert payload["success"] is True
    assert payload["tasks"][0]["description"] == "Buy groceries"


def test_done_json_output(tmp_path):
    run_cli(tmp_path, "add", "Buy groceries", "--json")
    output = run_cli(tmp_path, "done", "1", "--json")
    payload = json.loads(output)
    assert payload["success"] is True
    assert payload["task"]["done"] is True
