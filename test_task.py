"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task
from commands.list import list_tasks
from utils.validation import validate_description, validate_task_id
from utils.paths import get_tasks_file


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
    assert validate_task_id(tasks, 2) == 2

    with pytest.raises(ValueError):
        validate_task_id(tasks, 0)

    with pytest.raises(ValueError):
        validate_task_id(tasks, 3)


def test_list_tasks_json(capsys):
    """Test JSON output for list command."""
    tasks_file = get_tasks_file()
    if tasks_file.exists():
        tasks_file.unlink()
    
    # Test empty list
    list_tasks(json_output=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == "[]"
    
    # Add a task and test
    add_task("Test task")
    capsys.readouterr() # clear buffer
    
    list_tasks(json_output=True)
    captured = capsys.readouterr()
    tasks = json.loads(captured.out)
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Test task"
    assert tasks[0]["done"] is False
