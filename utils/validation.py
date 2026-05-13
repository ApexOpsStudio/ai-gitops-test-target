"""Shared validation helpers for task CLI commands."""

from .paths import get_tasks_file


def validate_description(description):
    """Validate and normalize a task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_file():
    """Return the tasks file path if it exists, otherwise an empty list sentinel."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return tasks_file


def validate_task_id(tasks, task_id):
    """Validate task ID exists."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
