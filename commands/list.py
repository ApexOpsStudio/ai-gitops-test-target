"""List tasks command."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_task_file():
    """Validate tasks file exists."""
    # NOTE: Validation logic scattered here - should be in utils (refactor bounty)
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return tasks_file


def list_tasks():
    """List all tasks."""
    # NOTE: No --json flag support yet (feature bounty)
    tasks_file = validate_task_file()
    if not tasks_file:
        print("No tasks yet!")
        return []

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        print("No tasks yet!")
        return []

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")

    return tasks
