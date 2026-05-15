"""Basic tests for task CLI."""

import json
import subprocess
import sys
import pytest
from pathlib import Path
from task import load_config
from utils.validation import validate_description, validate_task_id


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


def test_load_config_creates_default_when_missing(monkeypatch, tmp_path):
    """Missing config should be created instead of crashing."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config = load_config()
    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"

    assert config_path.exists()
    assert "tasks_file" in config


def run_cli_json(tmp_path, *args):
    """Run the CLI with a temporary HOME and parse JSON output."""
    result = subprocess.run(
        [sys.executable, "task.py", *args],
        cwd=Path(__file__).parent,
        env={"HOME": str(tmp_path)},
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_cli_json_output_for_add_list_and_done(tmp_path):
    """All commands should produce parseable JSON with --json."""
    add_result = run_cli_json(tmp_path, "add", "Write tests", "--json")
    assert add_result == {
        "task": {"id": 1, "description": "Write tests", "done": False}
    }

    list_result = run_cli_json(tmp_path, "list", "--json")
    assert list_result == {
        "tasks": [{"id": 1, "description": "Write tests", "done": False}]
    }

    done_result = run_cli_json(tmp_path, "done", "1", "--json")
    assert done_result == {
        "task": {"id": 1, "description": "Write tests", "done": True}
    }
