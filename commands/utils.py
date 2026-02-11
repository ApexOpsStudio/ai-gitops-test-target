"""Shared utilities for task-cli commands.

This module centralizes common file path and validation logic.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List, Dict


def get_tasks_file() -> Path:
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from disk.

    Returns an empty list when the tasks file does not exist yet.
    """
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return json.loads(tasks_file.read_text())


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Persist tasks to disk."""
    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)
    tasks_file.write_text(json.dumps(tasks, indent=2))


def validate_description(description: str) -> str:
    """Validate task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def validate_task_id(tasks: List[Dict[str, Any]], task_id: int) -> int:
    """Validate task ID exists."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
