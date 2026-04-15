"""Basic tests for task CLI."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from commands.add import validate_description
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
    """Run the CLI with an isolated HOME directory."""
    env = {"HOME": str(tmp_path)}
    result = subprocess.run(
        [sys.executable, "task.py", *args],
        cwd=Path(__file__).parent,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_add_command_supports_json_output(tmp_path):
    """Add command emits valid JSON output."""
    payload = run_cli(tmp_path, "add", "Buy groceries", "--json")
    assert payload["success"] is True
    assert payload["task"] == {
        "id": 1,
        "description": "Buy groceries",
        "done": False,
    }


def test_list_command_supports_json_output(tmp_path):
    """List command emits valid JSON output."""
    run_cli(tmp_path, "add", "Buy groceries", "--json")
    payload = run_cli(tmp_path, "list", "--json")
    assert payload["success"] is True
    assert payload["tasks"] == [
        {"id": 1, "description": "Buy groceries", "done": False}
    ]


def test_done_command_supports_json_output(tmp_path):
    """Done command emits valid JSON output."""
    run_cli(tmp_path, "add", "Buy groceries", "--json")
    payload = run_cli(tmp_path, "done", "1", "--json")
    assert payload["success"] is True
    assert payload["task"] == {
        "id": 1,
        "description": "Buy groceries",
        "done": True,
    }
