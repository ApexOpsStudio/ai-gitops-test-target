"""Shared storage helpers for task commands."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def read_tasks():
    """Read tasks from disk, returning an empty list when no task file exists."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return json.loads(tasks_file.read_text())


def write_tasks(tasks):
    """Write tasks to disk."""
    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    tasks_file.write_text(json.dumps(tasks, indent=2))


def emit_json(payload):
    """Print a JSON payload."""
    print(json.dumps(payload, indent=2))
