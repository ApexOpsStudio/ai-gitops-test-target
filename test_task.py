"""Basic tests for task CLI."""

import json
import os
import subprocess
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.list import list_tasks
from commands.done import validate_task_id, mark_done


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


def _clean_tasks():
    """Remove tasks file for clean test state."""
    tasks_file = Path.home() / ".local" / "share" / "task-cli" / "tasks.json"
    if tasks_file.exists():
        tasks_file.unlink()


def test_add_json_output(capsys):
    """Test add command with --json flag outputs valid JSON."""
    _clean_tasks()
    add_task("json test task", as_json=True)
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["description"] == "json test task"
    assert result["done"] is False
    assert "id" in result


def test_list_json_output(capsys):
    """Test list command with --json flag outputs valid JSON array."""
    _clean_tasks()
    add_task("task one", as_json=True)
    add_task("task two", as_json=True)
    capsys.readouterr()  # clear add output
    list_tasks(as_json=True)
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["description"] == "task one"
    assert result[1]["description"] == "task two"


def test_list_json_empty(capsys):
    """Test list --json with no tasks returns empty array."""
    _clean_tasks()
    list_tasks(as_json=True)
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result == []


def test_done_json_output(capsys):
    """Test done command with --json flag outputs valid JSON."""
    _clean_tasks()
    add_task("mark me done", as_json=True)
    capsys.readouterr()  # clear add output
    mark_done(1, as_json=True)
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["id"] == 1
    assert result["done"] is True


def test_cli_json_flag():
    """Test --json flag works via CLI subprocess."""
    _clean_tasks()
    result = subprocess.run(
        ["python3", "task.py", "--json", "add", "cli json test"],
        capture_output=True, text=True, cwd="/tmp/ai-gitops-test-target"
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["description"] == "cli json test"
