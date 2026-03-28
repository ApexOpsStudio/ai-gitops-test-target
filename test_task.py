"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from utils.validation import validate_description, validate_task_id
from utils.paths import get_tasks_file, get_config_path, load_config


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


def test_get_tasks_file():
    """Test tasks file path generation."""
    path = get_tasks_file()
    assert "task-cli" in str(path)
    assert path.name == "tasks.json"


def test_get_config_path():
    """Test config path generation."""
    path = get_config_path()
    assert "task-cli" in str(path)
    assert path.name == "config.yaml"


def test_load_config_missing():
    """Test load_config returns None when config doesn't exist."""
    # Temporarily clear config if it exists
    config_path = get_config_path()
    backup_exists = config_path.exists()
    backup_content = None
    if backup_exists:
        backup_content = config_path.read_text()
        config_path.unlink()

    try:
        result = load_config()
        assert result is None
    finally:
        if backup_exists and backup_content:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(backup_content)
