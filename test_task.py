"""Basic tests for task CLI."""

import json
import pytest
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import DEFAULT_CONFIG, get_config_path, load_config, main


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


def test_load_config_creates_default_when_missing(monkeypatch, tmp_path):
    """Missing config should be created instead of crashing."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_path = get_config_path()
    assert not config_path.exists()

    assert load_config() == DEFAULT_CONFIG
    assert config_path.exists()
    assert config_path.read_text() == DEFAULT_CONFIG


def test_main_handles_missing_config(monkeypatch, tmp_path, capsys):
    """Running a command with no config should not raise FileNotFoundError."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr("sys.argv", ["task.py", "list"])

    main()

    assert get_config_path().exists()
    assert "No tasks yet!" in capsys.readouterr().out
