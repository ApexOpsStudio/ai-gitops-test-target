"""List tasks command."""

import json

from utils.paths import get_tasks_file


def list_tasks(json_output: bool = False) -> None:
    """List all tasks."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        if json_output:
            print(json.dumps([]))
        else:
            print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

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
