"""Shared validation utilities for task-cli commands."""

from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_description(description):
    """Validate task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_file(tasks_file):
    """Validate tasks file exists and return it, or None if missing."""
    if not tasks_file.exists():
        return None
    return tasks_file


def validate_task_id(tasks, task_id):
    """Validate task ID exists in the tasks list."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
