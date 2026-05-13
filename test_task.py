"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from task import DEFAULT_CONFIG, load_config
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


def test_load_config_creates_default_when_missing(tmp_path):
    """Missing config file should be created with defaults."""
    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"

    assert load_config(config_path) == DEFAULT_CONFIG
    assert config_path.read_text() == DEFAULT_CONFIG


def test_load_config_reads_existing_file(tmp_path):
    """Existing config file should be returned unchanged."""
    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("display:\n  color: false\n")

    assert load_config(config_path) == "display:\n  color: false\n"
