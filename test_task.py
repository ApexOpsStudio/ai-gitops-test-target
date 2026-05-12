"""Basic tests for task CLI."""

import json
import os
import subprocess
import sys

import pytest

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
    """Run the CLI with an isolated HOME and return stdout."""
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, "task.py", *args],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return result.stdout.strip()


def test_add_json_output(tmp_path):
    """Add command supports parseable JSON output."""
    output = run_cli(tmp_path, "add", "Buy milk", "--json")

    assert json.loads(output) == {"id": 1, "description": "Buy milk", "done": False}


def test_list_json_output(tmp_path):
    """List command supports parseable JSON output."""
    run_cli(tmp_path, "add", "Buy milk")
    run_cli(tmp_path, "add", "Walk dog")

    output = run_cli(tmp_path, "list", "--json")

    assert json.loads(output) == [
        {"id": 1, "description": "Buy milk", "done": False},
        {"id": 2, "description": "Walk dog", "done": False},
    ]


def test_list_json_output_with_no_tasks(tmp_path):
    """List command returns an empty JSON array when there are no tasks."""
    output = run_cli(tmp_path, "list", "--json")

    assert json.loads(output) == []


def test_done_json_output(tmp_path):
    """Done command supports parseable JSON output."""
    run_cli(tmp_path, "add", "Buy milk")

    output = run_cli(tmp_path, "done", "1", "--json")

    assert json.loads(output) == {"id": 1, "description": "Buy milk", "done": True}

    list_output = run_cli(tmp_path, "list", "--json")
    assert json.loads(list_output) == [
        {"id": 1, "description": "Buy milk", "done": True}
    ]
