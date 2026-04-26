"""Shared path helpers for task-cli."""

from pathlib import Path


def get_tasks_file() -> Path:
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def get_config_file() -> Path:
    """Get path to config file."""
    return Path.home() / ".config" / "task-cli" / "config.yaml"
