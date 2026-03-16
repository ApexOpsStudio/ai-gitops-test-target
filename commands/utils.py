"""Shared validation utilities for task CLI."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def load_tasks():
    """Load tasks from file. Returns empty list if file doesn't exist."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return json.loads(tasks_file.read_text())


def save_tasks(tasks):
    """Save tasks to file."""
    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    tasks_file.write_text(json.dumps(tasks, indent=2))


def validate_description(description):
    """Validate task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_id(tasks, task_id):
    """Validate task ID exists."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
