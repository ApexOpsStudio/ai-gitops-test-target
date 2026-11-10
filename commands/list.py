"""List tasks command."""

import json

from utils.paths import get_tasks_file
from utils.validation import validate_task_file

__all__ = ["list_tasks", "get_tasks_file", "validate_task_file"]


def list_tasks(as_json=False):
    """List all tasks."""
    tasks_file = validate_task_file()
    if not tasks_file:
        if as_json:
            print(json.dumps({"tasks": []}))
        else:
            print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

    if as_json:
        print(json.dumps({"tasks": tasks}))
        return

    if not tasks:
        print("No tasks yet!")
        return

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")
