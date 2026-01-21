"""Basic tests for task CLI."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from commands.add import add_task, validate_description
from commands.done import validate_task_id

REPO_ROOT = Path(__file__).parent


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
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    env["USERPROFILE"] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, "task.py", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env=env,
    )
    return result


def test_add_json_output(tmp_path):
    result = run_cli(tmp_path, "add", "Test add json", "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout.strip())
    assert data["success"] is True
    assert data["command"] == "add"
    assert data["task"]["title"] == "Test add json"
    assert data["task"]["done"] is False
    assert data["task"]["id"] == 1


def test_list_json_output(tmp_path):
    run_cli(tmp_path, "add", "Task one", "--json")
    run_cli(tmp_path, "add", "Task two", "--json")

    result = run_cli(tmp_path, "list", "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout.strip())
    assert data["success"] is True
    assert data["command"] == "list"
    assert data["count"] == 2
    assert len(data["tasks"]) == 2
    assert data["tasks"][0]["title"] == "Task one"
    assert data["tasks"][1]["title"] == "Task two"


def test_done_json_output(tmp_path):
    run_cli(tmp_path, "add", "Finish me", "--json")
    result = run_cli(tmp_path, "done", "1", "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout.strip())
    assert data["success"] is True
    assert data["command"] == "done"
    assert data["task"]["done"] is True
    assert data["task"]["id"] == 1
