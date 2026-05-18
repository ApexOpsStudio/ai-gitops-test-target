"""Shared task storage helpers."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def load_tasks():
    """Load tasks from disk, returning an empty list when no file exists."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return json.loads(tasks_file.read_text())


def save_tasks(tasks):
    """Persist tasks to disk."""
    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    tasks_file.write_text(json.dumps(tasks, indent=2))


def print_json(payload):
    """Print a payload as stable, valid JSON."""
    print(json.dumps(payload, indent=2))
