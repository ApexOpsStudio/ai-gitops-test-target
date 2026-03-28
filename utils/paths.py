"""Shared path helpers for task CLI."""

from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def get_config_path():
    """Get path to config file."""
    return Path.home() / ".config" / "task-cli" / "config.yaml"


def load_config():
    """Load configuration from file.

    Returns config content as string, or None if config doesn't exist.
    """
    config_path = get_config_path()
    if not config_path.exists():
        return None
    return config_path.read_text()
