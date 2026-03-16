"""Basic tests for task CLI."""

import json
import pytest
import subprocess
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


# ── JSON output tests ─────────────────────────────────────────────────────


def test_add_json_output(capsys, tmp_path, monkeypatch):
    """Test add command with --json flag produces valid JSON."""
    monkeypatch.setattr(
        "commands.add.get_tasks_file", lambda: tmp_path / "tasks.json"
    )
    add_task("Test task", json_output=True)
    output = json.loads(capsys.readouterr().out)
    assert output["success"] is True
    assert output["task"]["description"] == "Test task"
    assert output["task"]["id"] == 1
    assert output["task"]["done"] is False


def test_add_text_output(capsys, tmp_path, monkeypatch):
    """Test add command without --json flag produces plain text."""
    monkeypatch.setattr(
        "commands.add.get_tasks_file", lambda: tmp_path / "tasks.json"
    )
    add_task("Test task", json_output=False)
    output = capsys.readouterr().out.strip()
    assert "Added task 1: Test task" == output


def test_list_json_output(capsys, tmp_path, monkeypatch):
    """Test list command with --json flag produces valid JSON."""
    monkeypatch.setattr(
        "commands.add.get_tasks_file", lambda: tmp_path / "tasks.json"
    )
    monkeypatch.setattr(
        "commands.list.get_tasks_file", lambda: tmp_path / "tasks.json"
    )
    add_task("Task one")
    add_task("Task two")
    list_tasks(json_output=True)
    output = json.loads(capsys.readouterr().out.strip().split("\n")[-1])
    assert output["success"] is True
    assert len(output["tasks"]) == 2
    assert output["tasks"][0]["description"] == "Task one"


def test_list_empty_json(capsys, tmp_path, monkeypatch):
    """Test list --json with no tasks returns empty array."""
    monkeypatch.setattr(
        "commands.list.get_tasks_file", lambda: tmp_path / "tasks.json"
    )
    list_tasks(json_output=True)
    output = json.loads(capsys.readouterr().out)
    assert output["success"] is True
    assert output["tasks"] == []


def test_done_json_output(capsys, tmp_path, monkeypatch):
    """Test done command with --json flag produces valid JSON."""
    monkeypatch.setattr(
        "commands.add.get_tasks_file", lambda: tmp_path / "tasks.json"
    )
    monkeypatch.setattr(
        "commands.done.get_tasks_file", lambda: tmp_path / "tasks.json"
    )
    add_task("Task to complete")
    mark_done(1, json_output=True)
    lines = capsys.readouterr().out.strip().split("\n")
    output = json.loads(lines[-1])
    assert output["success"] is True
    assert output["task"]["done"] is True


def test_cli_json_flag():
    """Test --json flag works via CLI invocation."""
    result = subprocess.run(
        ["python3", "task.py", "list", "--json"],
        capture_output=True, text=True, cwd=str(Path(__file__).parent),
    )
    output = json.loads(result.stdout)
    assert "success" in output
    assert "tasks" in output
