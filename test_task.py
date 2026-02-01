"""Basic tests for task CLI."""

import json
import pytest
import tempfile
import os
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
    """Test that load_config creates default config when file is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock Path.home() to return our temp directory
        fake_home = Path(tmpdir)
        config_path = fake_home / ".config" / "task-cli" / "config.yaml"
        
        with patch.object(Path, 'home', return_value=fake_home):
            # Config should not exist initially
            assert not config_path.exists()
            
            # Load config - should create default
            result = load_config()
            
            # Config file should now exist
            assert config_path.exists()
            
            # Content should match default config
            assert result == DEFAULT_CONFIG


def test_load_config_reads_existing_config():
    """Test that load_config reads existing config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_home = Path(tmpdir)
        config_path = fake_home / ".config" / "task-cli" / "config.yaml"
        
        # Create config directory and file
        config_path.parent.mkdir(parents=True, exist_ok=True)
        custom_config = "custom: config\n"
        config_path.write_text(custom_config)
        
        with patch.object(Path, 'home', return_value=fake_home):
            result = load_config()
            assert result == custom_config
