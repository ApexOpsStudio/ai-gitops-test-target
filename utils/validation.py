"""Shared validation functions for task CLI."""


def validate_description(description):
    """Validate task description.

    Args:
        description: Raw task description string.

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
    """Validate task ID exists in the task list.

    Args:
        tasks: List of task dicts.
        task_id: Integer task ID to validate.

    Returns:
        Validated task ID.

    Raises:
        ValueError: If task ID is out of range.
    """
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id


def validate_task_file(tasks_file):
    """Validate tasks file exists and return it, or empty list if missing.

    Args:
        tasks_file: Path object to the tasks JSON file.

    Returns:
        The tasks_file Path if it exists, or an empty list if not.
    """
    if not tasks_file.exists():
        return []
    return tasks_file
