"""Basic tests for task CLI."""

import json
import os
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
    """Config file missing: auto-create default without crashing."""
    fake_home = tmp_path / "home"
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    config = load_config()
    assert config == {"tasks_file": "tasks.json", "verbose": False}
    config_file = fake_home / ".config" / "task-cli" / "config.yaml"
    assert config_file.exists()


def test_load_config_corrupt_file(tmp_path, monkeypatch):
    """Malformed config file: return defaults without crashing."""
    fake_home = tmp_path / "home"
    config_dir = fake_home / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    (config_dir / "config.yaml").write_text("{{{not valid json")
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    config = load_config()
    assert config == {"tasks_file": "tasks.json", "verbose": False}
