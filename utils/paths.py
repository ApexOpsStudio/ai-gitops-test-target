"""Shared path helpers for task-cli."""

from pathlib import Path


def get_tasks_file() -> Path:
    """Return the path to the tasks JSON file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"
