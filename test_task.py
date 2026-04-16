"""Basic tests for task CLI."""

import json
import os
import shutil
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import load_config


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


def test_load_config_missing_creates_default():
    """Test that load_config creates default config when file is missing."""
    config_dir = Path.home() / ".config" / "task-cli"
    config_path = config_dir / "config.yaml"
    backup = None

    try:
        # Back up existing config if present
        if config_path.exists():
            backup = config_path.read_text()
            config_path.unlink()

        # load_config should create default config, not crash
        result = load_config()
        assert config_path.exists()
        assert "storage:" in result
        assert "format: json" in result
        assert "display:" in result
    finally:
        # Restore original config
        if backup is not None:
            config_path.write_text(backup)
        elif config_path.exists():
            config_path.unlink()
