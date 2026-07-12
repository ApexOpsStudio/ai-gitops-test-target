"""List tasks command."""

import json

from utils.validation import validate_task_file


def list_tasks(as_json=False):
    """List all tasks."""
    tasks_file = validate_task_file()
    if not tasks_file:
        if as_json:
            print("[]")
        else:
            print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if as_json:
            print("[]")
        else:
            print("No tasks yet!")
        return

    if as_json:
        print(json.dumps(tasks, indent=2))
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")
