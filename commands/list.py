"""List tasks command."""

import json

from .utils import load_tasks


def list_tasks(json_output=False):
    """List all tasks."""
    tasks = load_tasks()

    if not tasks:
        if json_output:
            print(json.dumps([]))
        else:
            print("No tasks yet!")
        return

    if json_output:
        print(json.dumps(tasks))
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")
