"""List tasks command."""

import json
from utils import get_tasks_file, validate_task_file


def list_tasks():
    """List all tasks."""
    # NOTE: No --json flag support yet (feature bounty)
    tasks_file = validate_task_file()
    if not tasks_file:
        print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        print("No tasks yet!")
        return

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")
