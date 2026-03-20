"""Validation utilities for task CLI."""

from .paths import get_tasks_file


def validate_description(description):
    """Validate task description.
    
    Args:
        description: Task description string.
        
    Returns:
        Stripped description string.
        
    Raises:
        ValueError: If description is empty or too long.
    """
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_file():
    """Validate tasks file exists.
    
    Returns:
        Path to tasks file if it exists, empty list otherwise.
    """
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return tasks_file


def validate_task_id(tasks, task_id):
    """Validate task ID exists.
    
    Args:
        tasks: List of task dictionaries.
        task_id: Task ID to validate.
        
    Returns:
        Validated task ID.
        
    Raises:
        ValueError: If task ID is invalid.
    """
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
