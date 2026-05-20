"""Basic tests for task CLI."""

import pytest

import task
from commands.add import add_task, validate_description
from commands.done import validate_task_id


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
    """Missing config should be initialized instead of crashing."""
    monkeypatch.setattr(task.Path, "home", staticmethod(lambda: tmp_path))
    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"

    assert not config_path.exists()

    config = task.load_config()

    assert config == task.DEFAULT_CONFIG
    assert config_path.read_text(encoding="utf-8") == task.DEFAULT_CONFIG
