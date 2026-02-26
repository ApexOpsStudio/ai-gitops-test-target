"""Path utilities for task-cli."""

from pathlib import Path


def get_tasks_file():
    """Get path to tasks file.
    
    Returns:
        Path to the tasks.json file in user's local data directory.
    """
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"
