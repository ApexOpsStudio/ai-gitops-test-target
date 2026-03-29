"""Basic tests for task CLI."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
from utils.validation import validate_description, validate_task_id


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


def test_load_config_creates_default_on_missing():
    """Test that load_config creates a default config when file is missing."""
    import importlib
    import sys

    # We need to reimport task to get fresh module state
    # Create a temp home dir for this test
    with tempfile.TemporaryDirectory() as tmp_home:
        mock_home = Path(tmp_home)
        config_path = mock_home / ".config" / "task-cli" / "config.yaml"

        # Verify config doesn't exist
        assert not config_path.exists()

        # Patch Path.home to return our temp dir
        with patch("pathlib.Path.home", return_value=mock_home):
            # Reimport to pick up patched Path
            import task as task_module
            importlib.reload(task_module)

            # Patch open to intercept file operations
            original_open = open

            created_files = []
            def mock_open(path, *args, **kwargs):
                path = Path(path)
                if str(path) == str(config_path):
                    created_files.append(path)
                    # Simulate file creation then read
                    if 'r' in args or 'rb' in args:
                        if not path.exists():
                            raise FileNotFoundError()
                        return original_open(path, *args, **kwargs)
                return original_open(path, *args, **kwargs)

            with patch("builtins.open", side_effect=mock_open):
                try:
                    result = task_module.load_config()
                except Exception:
                    pass

        # Verify config was created
        assert config_path.exists(), "Config file should be created when missing"
        content = config_path.read_text()
        assert "storage:" in content
        assert "display:" in content


def test_load_config_reads_existing():
    """Test that load_config reads existing config without modification."""
    with tempfile.TemporaryDirectory() as tmp_home:
        mock_home = Path(tmp_home)
        config_path = mock_home / ".config" / "task-cli" / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("# Custom config\nkey: value\n")

        with patch("pathlib.Path.home", return_value=mock_home):
            import task as task_module
            import importlib
            importlib.reload(task_module)

            result = task_module.load_config()
            assert result == "# Custom config\nkey: value\n"


