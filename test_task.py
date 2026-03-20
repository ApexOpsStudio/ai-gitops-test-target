"""Basic tests for task CLI."""

import pytest
from pathlib import Path
from unittest.mock import patch
from commands.add import add_task, validate_description
from commands.done import validate_task_id
from task import load_config, get_config_path, DEFAULT_CONFIG, DEFAULT_CONFIG_TEXT, _parse_config


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


def test_load_config_missing_creates_default(tmp_path, monkeypatch):
    """Test that missing config file is created with defaults."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config = load_config()

    assert config == DEFAULT_CONFIG
    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    assert config_path.exists()
    assert config_path.read_text() == DEFAULT_CONFIG_TEXT


def test_load_config_existing_file(tmp_path, monkeypatch):
    """Test that existing config file is read correctly."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    custom_config = "storage_dir: /custom/path\n"
    config_path.write_text(custom_config)

    config = load_config()

    assert config == {"storage_dir": "/custom/path"}


def test_load_config_returns_dict_copy(tmp_path, monkeypatch):
    """Test that load_config returns a copy, not the global DEFAULT_CONFIG."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config = load_config()
    config["new_key"] = "new_value"

    assert "new_key" not in DEFAULT_CONFIG


def test_load_config_unwritable_parent(tmp_path, monkeypatch, capsys):
    """Test graceful fallback when config directory cannot be created."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    with patch.object(Path, "exists", return_value=False):
        with patch.object(Path, "mkdir", side_effect=OSError("Permission denied")):
            config = load_config()

    assert config == DEFAULT_CONFIG
    captured = capsys.readouterr()
    assert "Warning" in captured.err


def test_load_config_unreadable_file(tmp_path, monkeypatch, capsys):
    """Test graceful fallback when config file exists but cannot be read."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("storage_dir: /custom/path\n")
    config_path.chmod(0o000)

    config = load_config()

    assert config == DEFAULT_CONFIG
    captured = capsys.readouterr()
    assert "Warning" in captured.err
    # Restore permissions for cleanup
    config_path.chmod(0o644)


def test_load_config_no_crash_without_config(tmp_path, monkeypatch):
    """Test the core issue: CLI does not crash when config file is missing."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    config_path = tmp_path / ".config" / "task-cli" / "config.yaml"
    assert not config_path.exists()

    # Should not raise any exception
    config = load_config()

    assert isinstance(config, dict)
    assert "storage_dir" in config
    assert "default_format" in config


def test_get_config_path(tmp_path, monkeypatch):
    """Test that config path is under .config/task-cli."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    path = get_config_path()

    assert path == tmp_path / ".config" / "task-cli" / "config.yaml"


def test_parse_config_empty():
    """Test parsing empty config text."""
    assert _parse_config("") == {}


def test_parse_config_comments_only():
    """Test parsing config with only comments."""
    assert _parse_config("# comment\n# another") == {}


def test_parse_config_multiple_keys():
    """Test parsing config with multiple keys."""
    text = "storage_dir: /data\ndefault_format: json\n"
    result = _parse_config(text)
    assert result == {"storage_dir": "/data", "default_format": "json"}


def test_parse_config_value_with_colon():
    """Test parsing config where value contains a colon."""
    text = "storage_dir: /path/to:something\n"
    result = _parse_config(text)
    assert result == {"storage_dir": "/path/to:something"}


def test_parse_config_whitespace_handling():
    """Test that keys and values are stripped of whitespace."""
    text = "  storage_dir :  /data  \n"
    result = _parse_config(text)
    assert result == {"storage_dir": "/data"}


def test_parse_config_blank_lines():
    """Test that blank lines are skipped."""
    text = "key1: val1\n\n\nkey2: val2\n"
    result = _parse_config(text)
    assert result == {"key1": "val1", "key2": "val2"}


def test_load_config_creates_parent_dirs(tmp_path, monkeypatch):
    """Test that missing parent directories are created when writing default config."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    parent = tmp_path / ".config" / "task-cli"
    assert not parent.exists()

    load_config()

    assert parent.exists()
    assert parent.is_dir()


def test_default_config_text_matches_default_config():
    """Test that DEFAULT_CONFIG_TEXT parses to DEFAULT_CONFIG."""
    parsed = _parse_config(DEFAULT_CONFIG_TEXT)
    assert parsed == DEFAULT_CONFIG
