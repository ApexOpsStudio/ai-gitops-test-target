"""Basic tests for task CLI."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

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


def test_load_config_creates_default_when_missing():
    """Test that load_config creates a default config when file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_home = Path(tmpdir)
        with patch("task.Path") as mock_path:
            mock_path.home.return_value = fake_home
            config = load_config()
            assert "storage:" in config
            assert "display:" in config
            # Verify file was created
            config_path = fake_home / ".config" / "task-cli" / "config.yaml"
            assert config_path.exists()
            assert config_path.read_text() == DEFAULT_CONFIG


def test_load_config_reads_existing_config():
    """Test that load_config reads an existing config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_home = Path(tmpdir)
        config_dir = fake_home / ".config" / "task-cli"
        config_dir.mkdir(parents=True)
        config_path = config_dir / "config.yaml"
        custom_config = "storage:\n  format: yaml\n"
        config_path.write_text(custom_config)

        with patch("task.Path") as mock_path:
            mock_path.home.return_value = fake_home
            config = load_config()
            assert config == custom_config
