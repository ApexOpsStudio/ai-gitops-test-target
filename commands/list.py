"""List tasks command."""

import json
from .validation import get_tasks_file, read_tasks


def list_tasks(json_output=False):
    """List all tasks."""
    tasks_file = get_tasks_file()
    tasks = read_tasks(tasks_file)

    if not tasks:
        if json_output:
            print(json.dumps([]))
        else:
            print("No tasks yet!")
        return

    if json_output:
        print(json.dumps(tasks))
        return

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")
