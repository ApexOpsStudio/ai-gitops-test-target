"""Basic tests for task CLI."""

import json
import os
import shutil
import tempfile

import pytest
from pathlib import Path
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
    """Test that load_config creates default config when file is missing."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config = load_config()

    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    assert config_path.exists()
    assert "storage:" in config
    assert "display:" in config


def test_load_config_reads_existing(tmp_path, monkeypatch):
    """Test that load_config reads existing config file."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_dir = tmp_path / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    (config_dir / "config.yaml").write_text("custom: true\n")

    config = load_config()
    assert "custom: true" in config


def test_default_config_is_valid_yaml():
    """Test that DEFAULT_CONFIG is valid YAML-like content."""
    assert "storage:" in DEFAULT_CONFIG
    assert "display:" in DEFAULT_CONFIG
    assert "format: json" in DEFAULT_CONFIG
