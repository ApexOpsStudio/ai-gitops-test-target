"""Shared path helpers."""

from pathlib import Path


def get_config_file():
    """Get path to config file."""
    return Path.home() / ".config" / "task-cli" / "config.yaml"


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"
