"""Test that load_config handles missing config file gracefully."""

import pytest
from unittest.mock import patch
from pathlib import Path


def test_load_config_missing_file_returns_default():
    """load_config should not crash when config file is missing.
    
    It should return a sensible default config string instead of
    raising FileNotFoundError.
    """
    # Ensure config file does not exist
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    original_exists = config_path.exists()
    
    # Temporarily remove it if it exists
    backup = None
    if original_exists:
        backup = config_path.read_text()
        config_path.unlink()
    
    try:
        from task import load_config
        # This should NOT raise FileNotFoundError
        result = load_config()
        # Should return something (default config or empty string)
        assert result is not None
        assert isinstance(result, str)
    finally:
        # Restore if we backed up
        if backup is not None:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(backup)


def test_load_config_existing_file():
    """load_config should still work when config file exists."""
    import tempfile
    import os
    
    config_content = "storage:\n  format: json\n"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / ".config" / "task-cli"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.yaml"
        config_file.write_text(config_content)
        
        with patch("task.Path.home", return_value=Path(tmpdir)):
            from task import load_config
            result = load_config()
            assert result == config_content
