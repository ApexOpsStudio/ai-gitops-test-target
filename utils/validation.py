"""Shared validation functions for task-cli."""


def validate_description(description: str) -> str:
    """Validate task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_id(tasks: list, task_id: int) -> int:
    """Validate task ID exists."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
