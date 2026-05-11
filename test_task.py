"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import DEFAULT_CONFIG, get_config_path, load_config


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
    """Missing config should not crash and should create a default config."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_path = get_config_path()
    assert not config_path.exists()

    config = load_config()

    assert config == DEFAULT_CONFIG
    assert config_path.exists()
    assert config_path.read_text() == DEFAULT_CONFIG
