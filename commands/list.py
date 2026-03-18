"""List tasks command."""

import json

from commands.utils import get_tasks_file


def list_tasks():
    """List all tasks."""
    tasks_file = get_tasks_file()

    if not tasks_file.exists():
        print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        print("No tasks yet!")
        return

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")
