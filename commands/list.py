"""List tasks command."""

import json
import sys
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


def list_tasks(*, json_output=False):
    """List all tasks.

    Args:
        json_output: If True, output result as JSON instead of plain text.
    """
    tasks_file = validate_task_file()

    if not tasks_file:
        if json_output:
            json.dump({"tasks": [], "count": 0}, sys.stdout)
            print()
        else:
            print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if json_output:
            json.dump({"tasks": [], "count": 0}, sys.stdout)
            print()
        else:
            print("No tasks yet!")
        return

    if json_output:
        json.dump({"tasks": tasks, "count": len(tasks)}, sys.stdout)
        print()
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")
