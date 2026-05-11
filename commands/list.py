"""List tasks command."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_task_file():
    """Validate tasks file exists."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return tasks_file


def list_tasks(json_output=False):
    """List all tasks. Returns result dict for JSON output."""
    tasks_file = validate_task_file()
    if not tasks_file:
        if not json_output:
            print("No tasks yet!")
        return {"success": True, "tasks": [], "count": 0}

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if not json_output:
            print("No tasks yet!")
        return {"success": True, "tasks": [], "count": 0}

    if not json_output:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")

    return {"success": True, "tasks": tasks, "count": len(tasks)}
