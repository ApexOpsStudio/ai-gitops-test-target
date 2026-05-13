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


def run_task_cli(tmp_path, *args):
    """Run the task CLI with an isolated HOME directory."""
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, "task.py", *args],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )
    return result.stdout.strip()


def test_add_json_output(tmp_path):
    """Add command prints parseable JSON when --json is present."""
    output = run_task_cli(tmp_path, "add", "Write tests", "--json")
    payload = json.loads(output)

    assert payload["task"] == {"id": 1, "description": "Write tests", "done": False}
    assert payload["message"] == "Added task 1"


def test_list_json_output(tmp_path):
    """List command prints all tasks as parseable JSON."""
    run_task_cli(tmp_path, "add", "First task")
    run_task_cli(tmp_path, "add", "Second task")

    output = run_task_cli(tmp_path, "list", "--json")
    payload = json.loads(output)

    assert payload["count"] == 2
    assert payload["tasks"] == [
        {"id": 1, "description": "First task", "done": False},
        {"id": 2, "description": "Second task", "done": False},
    ]


def test_done_json_output(tmp_path):
    """Done command prints the completed task as parseable JSON."""
    run_task_cli(tmp_path, "add", "Finish bounty")

    output = run_task_cli(tmp_path, "done", "1", "--json")
    payload = json.loads(output)

    assert payload["task"] == {"id": 1, "description": "Finish bounty", "done": True}
    assert payload["message"] == "Marked task 1 as done"


def test_list_json_output_when_empty(tmp_path):
    """List command returns an empty task array as JSON with no task file."""
    output = run_task_cli(tmp_path, "list", "--json")
    assert json.loads(output) == {"tasks": [], "count": 0}
