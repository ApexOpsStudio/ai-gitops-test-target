"""Tests for --json output format."""

import json
import pytest
import subprocess
import sys
import os
from pathlib import Path

# Use the local task.py
TASK_PY = os.path.join(os.path.dirname(__file__), "task.py")
PYTHON = sys.executable


def run_cli(*args):
    """Run the CLI and return stdout."""
    result = subprocess.run(
        [PYTHON, TASK_PY] + list(args),
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip(), result.returncode


class TestJsonOutput:
    """Test --json flag for all commands."""

    def test_add_json(self):
        """Add command with --json outputs valid JSON."""
        stdout, code = run_cli("--json", "add", "Test task with JSON")
        data = json.loads(stdout)
        assert data["success"] is True
        assert "task_id" in data
        assert data["description"] == "Test task with JSON"

    def test_list_json(self):
        """List command with --json outputs valid JSON."""
        stdout, code = run_cli("--json", "list")
        data = json.loads(stdout)
        assert data["success"] is True
        assert "tasks" in data
        assert "count" in data
        assert isinstance(data["tasks"], list)

    def test_list_json_is_parseable(self):
        """JSON output can be parsed programmatically."""
        stdout, code = run_cli("--json", "list")
        data = json.loads(stdout)
        # Should be able to iterate tasks
        for task in data["tasks"]:
            assert "id" in task
            assert "description" in task
            assert "done" in task

    def test_add_without_json(self):
        """Add command without --json outputs human-readable text."""
        stdout, code = run_cli("add", "Human readable task")
        assert "Added task" in stdout

    def test_list_without_json(self):
        """List command without --json outputs human-readable text."""
        stdout, code = run_cli("list")
        # Should NOT be valid JSON
        with pytest.raises(json.JSONDecodeError):
            json.loads(stdout)

    def test_done_json(self):
        """Done command with --json outputs valid JSON (if task exists)."""
        # First add a task
        stdout, code = run_cli("--json", "add", "Task to complete")
        data = json.loads(stdout)
        task_id = data["task_id"]

        # Mark it done with JSON
        stdout, code = run_cli("--json", "done", str(task_id))
        data = json.loads(stdout)
        assert data["success"] is True
        assert data["done"] is True


class TestValidation:
    """Original validation tests still pass."""

    def test_validate_description(self):
        from commands.add import validate_description
        assert validate_description(" test ") == "test"
        with pytest.raises(ValueError):
            validate_description("")
        with pytest.raises(ValueError):
            validate_description("x" * 201)

    def test_validate_task_id(self):
        from commands.done import validate_task_id
        tasks = [{"id": 1}, {"id": 2}]
        assert validate_task_id(tasks, 1) == 1
        with pytest.raises(ValueError):
            validate_task_id(tasks, 0)
        with pytest.raises(ValueError):
            validate_task_id(tasks, 99)
