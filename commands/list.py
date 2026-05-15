"""List tasks command."""

import json
from utils.validation import validate_task_file


def list_tasks(json_output=False):
    """List all tasks."""
    # NOTE: No --json flag support yet (feature bounty)
    tasks_file = validate_task_file()
    if not tasks_file:
        if not json_output:
            print("No tasks yet!")
        return []

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if not json_output:
            print("No tasks yet!")
        return []

    if json_output:
        return tasks

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")
    return tasks
