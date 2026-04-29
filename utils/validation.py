"""Shared validation helpers for task CLI commands."""

from utils.paths import get_tasks_file


def validate_description(description):
    """Validate task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_file():
    """Validate tasks file exists."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return tasks_file


def validate_task_id(tasks, task_id):
    """Validate task ID exists."""
    if task_id < 1:
        raise ValueError("Task ID must be positive")

    task_ids = [task["id"] for task in tasks]
    if task_id not in task_ids:
        raise ValueError(f"Task {task_id} not found")

    return task_id
