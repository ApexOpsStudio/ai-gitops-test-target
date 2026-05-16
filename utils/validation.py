"""Shared validation utilities for task CLI."""

import json


def validate_description(description):
    """Validate task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_file(tasks_file):
    """Validate tasks file exists. Returns path if valid, empty list if no file."""
    if not tasks_file.exists():
        return []
    return tasks_file


def validate_task_id(tasks, task_id):
    """Validate task ID exists in task list."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
