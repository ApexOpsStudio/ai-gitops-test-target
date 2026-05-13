"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import DEFAULT_CONFIG, load_config, main


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
    """Missing config should be created instead of crashing."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    assert not config_path.exists()

    assert load_config() == DEFAULT_CONFIG
    assert config_path.read_text() == DEFAULT_CONFIG


def test_load_config_reads_existing_file(tmp_path, monkeypatch):
    """Existing config should be preserved."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("storage:\n  max_tasks: 5\n")

    assert load_config() == "storage:\n  max_tasks: 5\n"


def test_main_creates_missing_config_for_commands(tmp_path, monkeypatch, capsys):
    """Running a command should initialize missing config without crashing."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr("sys.argv", ["task.py", "list"])

    main()

    assert (tmp_path / ".config" / "task-cli" / "config.yaml").read_text() == DEFAULT_CONFIG
    assert "No tasks yet!" in capsys.readouterr().out
