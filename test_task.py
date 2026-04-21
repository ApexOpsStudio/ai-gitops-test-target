"""Basic tests for task CLI."""

import json
import os
import tempfile
import pytest
from pathlib import Path
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


def test_load_config_creates_default_when_missing():
    """Test that load_config creates default config when missing (BUG FIX)."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    import task
    
    # Use temp directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_config_dir = Path(tmpdir) / ".config" / "task-cli"
        tmp_config_path = tmp_config_dir / "config.yaml"
        
        # Ensure config doesn't exist
        assert not tmp_config_path.exists()
        
        # Temporarily override paths
        original_config_dir = task.config_dir
        original_config_path = task.config_path
        task.config_dir = tmp_config_dir
        task.config_path = tmp_config_path
        
        try:
            # Call load_config which should create the default
            task.load_config()
            
            # Verify config was created
            assert tmp_config_path.exists(), "Config file should be created"
            content = tmp_config_path.read_text()
            assert "storage:" in content, "Default config should have storage section"
            assert "display:" in content, "Default config should have display section"
        finally:
            # Restore original paths
            task.config_dir = original_config_dir
            task.config_path = original_config_path
