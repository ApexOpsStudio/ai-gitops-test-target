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


def test_load_config_missing_file(tmp_path, monkeypatch):
    """Test that load_config handles missing config file gracefully."""
    # Redirect HOME to a temp directory
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    # Ensure config doesn't exist
    config_dir = tmp_path / ".config" / "task-cli"
    if config_dir.exists():
        shutil.rmtree(config_dir)

    # Should not crash, should create default config
    config_content = load_config()
    assert "storage:" in config_content
    assert "display:" in config_content

    # Config file should now exist
    config_path = config_dir / "config.yaml"
    assert config_path.exists()

    # Loading again should return the same content
    config_content2 = load_config()
    assert config_content2 == config_content
