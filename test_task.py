"""Basic tests for task CLI."""

import json
import pytest
import subprocess
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import load_config, get_config_path, DEFAULT_CONFIG


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


# ── Config file tests ────────────────────────────────────────────────────


def test_load_config_creates_default_when_missing(tmp_path, monkeypatch):
    """Test that load_config creates a default config when file is missing."""
    config_path = tmp_path / "config" / "task-cli" / "config.yaml"
    monkeypatch.setattr("task.get_config_path", lambda: config_path)

    result = load_config()

    assert config_path.exists(), "Config file should be created"
    assert result == DEFAULT_CONFIG
    assert "storage:" in result
    assert "display:" in result


def test_load_config_reads_existing(tmp_path, monkeypatch):
    """Test that load_config reads an existing config without overwriting."""
    config_path = tmp_path / "config.yaml"
    custom_config = "custom: true\n"
    config_path.write_text(custom_config)
    monkeypatch.setattr("task.get_config_path", lambda: config_path)

    result = load_config()

    assert result == custom_config


def test_load_config_creates_parent_dirs(tmp_path, monkeypatch):
    """Test that load_config creates parent directories if needed."""
    config_path = tmp_path / "deep" / "nested" / "dir" / "config.yaml"
    monkeypatch.setattr("task.get_config_path", lambda: config_path)

    load_config()

    assert config_path.exists()
    assert config_path.parent.is_dir()


def test_cli_no_crash_without_config():
    """Test that CLI doesn't crash when config file is missing."""
    result = subprocess.run(
        ["python3", "task.py", "list"],
        capture_output=True, text=True, cwd=str(Path(__file__).parent),
    )
    # Should not crash with FileNotFoundError
    assert result.returncode == 0
    assert "FileNotFoundError" not in result.stderr
