"""Shared validation utilities for task CLI commands."""

from pathlib import Path


def get_tasks_file():
    """Get path to the tasks storage file.

    Returns:
        Path to ~/.local/share/task-cli/tasks.json
    """
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_description(description):
    """Validate a task description.

    Args:
        description: Raw description string.

    Returns:
        Stripped description string.

    Raises:
        ValueError: If description is empty or exceeds 200 characters.
    """
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_id(tasks, task_id):
    """Validate that a task ID exists in the task list.

    Args:
        tasks: List of task dicts.
        task_id: Integer task ID to validate.

    Returns:
        The validated task_id.

    Raises:
        ValueError: If task_id is out of range.
    """
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
