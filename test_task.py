"""Basic tests for task CLI."""

import json
import os
import pytest
from pathlib import Path
from unittest.mock import patch
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import load_config, DEFAULT_CONFIG


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


def test_load_config_creates_default_when_missing(tmp_path, monkeypatch):
    """Test that load_config creates a default config when file is missing."""
    fake_home = tmp_path
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    config_dir = fake_home / ".config" / "task-cli"
    config_path = config_dir / "config.yaml"

    # Ensure it doesn't exist
    assert not config_path.exists()

    result = load_config()

    # Should have created the file
    assert config_path.exists()
    assert "storage:" in result
    assert "format: json" in result


def test_load_config_reads_existing_file(tmp_path, monkeypatch):
    """Test that load_config reads existing config without overwriting."""
    fake_home = tmp_path
    monkeypatch.setattr(Path, "home", lambda: fake_home)

    config_dir = fake_home / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    config_path = config_dir / "config.yaml"
    custom_config = "storage:\n  format: yaml\n"
    config_path.write_text(custom_config)

    result = load_config()

    assert result == custom_config
