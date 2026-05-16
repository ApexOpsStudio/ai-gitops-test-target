"""Tests for task CLI configuration loading."""

import pytest
from pathlib import Path

from task import load_config


def test_load_config_reads_user_config(monkeypatch, tmp_path):
    """load_config reads the YAML file from the expected config directory."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    config_dir = tmp_path / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text("storage: local\n")

    assert load_config() == "storage: local\n"


def test_load_config_raises_when_config_missing(monkeypatch, tmp_path):
    """load_config surfaces the current missing-file behavior."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    with pytest.raises(FileNotFoundError):
        load_config()
