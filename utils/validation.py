"""Shared validation helpers for task-cli."""


def validate_description(description: str) -> str:
    """Validate and normalise a task description.

    Raises:
        ValueError: if the description is empty or exceeds 200 characters.
    """
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_file(tasks_file):
    """Check whether the tasks file exists.

    Returns:
        The ``tasks_file`` path if it exists, otherwise an empty list so
        callers can treat a falsy return as "no tasks yet".
    """
    if not tasks_file.exists():
        return []
    return tasks_file


def validate_task_id(tasks, task_id: int) -> int:
    """Validate that *task_id* refers to an existing task.

    Raises:
        ValueError: if *task_id* is out of range.
    """
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
