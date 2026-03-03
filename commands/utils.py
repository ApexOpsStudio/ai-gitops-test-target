"""Shared validation utilities for the task CLI."""

from pathlib import Path


def get_tasks_file() -> Path:
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_description(description: str) -> str:
    """Validate and sanitize a task description.

    Raises ``ValueError`` if the description is empty or too long.
    """
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_id(tasks: list, task_id: int) -> int:
    """Validate that *task_id* refers to an existing task.

    Raises ``ValueError`` for out-of-range IDs.
    """
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
