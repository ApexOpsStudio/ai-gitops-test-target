"""Validation utilities for task CLI."""

import json
from pathlib import Path
from utils.paths import get_tasks_file


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


def validate_task_file():
    """Validate tasks file exists."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return None
    return tasks_file


def load_tasks():
    """Load tasks from the tasks file. Returns empty list if file doesn't exist."""
    tasks_file = validate_task_file()
    if not tasks_file:
        return []
    return json.loads(tasks_file.read_text())


def save_tasks(tasks):
    """Save tasks to the tasks file."""
    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    tasks_file.write_text(json.dumps(tasks, indent=2))
