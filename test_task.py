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


def test_load_config_creates_default_when_missing(tmp_path, monkeypatch):
    """Test that load_config() creates a default config when the file is missing."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: fake_home))

    config_dir = fake_home / ".config" / "task-cli"
    config_path = config_dir / "config.yaml"

    # Ensure config does not exist
    assert not config_path.exists()

    # load_config should NOT crash and should return default content
    result = load_config()
    assert result is not None
    assert "storage:" in result
    assert "display:" in result

    # It should have created the file on disk
    assert config_path.exists()
    assert config_path.read_text() == result


def test_load_config_reads_existing_file(tmp_path, monkeypatch):
    """Test that load_config() reads an existing config file."""
    fake_home = tmp_path / "home"
    config_dir = fake_home / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    config_path = config_dir / "config.yaml"
    config_path.write_text("custom: value\n")

    monkeypatch.setattr(Path, "home", staticmethod(lambda: fake_home))

    result = load_config()
    assert "custom: value" in result
