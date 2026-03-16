"""List tasks command."""

import json

from .utils import load_tasks


def list_tasks(as_json=False):
    """List all tasks. Returns task list if as_json is True."""
    tasks = load_tasks()

    if not tasks:
        if as_json:
            print(json.dumps([]))
        else:
            print("No tasks yet!")
        return tasks

    if as_json:
        print(json.dumps(tasks, indent=2))
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")

    return tasks
