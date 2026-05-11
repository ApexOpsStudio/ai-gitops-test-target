"""Validation utilities for task CLI."""

from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_description(description):
    """Validate task description.

    Args:
        description: The task description to validate

    Returns:
        The trimmed description

    Raises:
        ValueError: If description is empty or too long
    """
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_id(tasks, task_id):
    """Validate task ID exists in the tasks list.

    Args:
        tasks: List of task dictionaries
        task_id: The task ID to validate

    Returns:
        The validated task ID

    Raises:
        ValueError: If task ID is invalid
    """
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id


def validate_task_file():
    """Validate tasks file exists.

    Returns:
        The tasks file path if it exists, None otherwise
    """
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return None
    return tasks_file
