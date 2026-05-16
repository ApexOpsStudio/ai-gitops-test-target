"""Shared path utilities for task CLI."""

from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def get_config_path():
    """Get path to config file."""
    return Path.home() / ".config" / "task-cli" / "config.yaml"
