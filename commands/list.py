"""List tasks command."""

import json
from utils.paths import get_tasks_file
from utils.validation import validate_task_file


def list_tasks(json_output=False):
    """List all tasks."""
    tasks_file = validate_task_file(get_tasks_file())
    if not tasks_file:
        msg = "No tasks yet!"
        if json_output:
            print(json.dumps({"tasks": [], "message": msg}))
        else:
            print(msg)
        return

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        msg = "No tasks yet!"
        if json_output:
            print(json.dumps({"tasks": [], "message": msg}))
        else:
            print(msg)
        return

    if json_output:
        print(json.dumps({"tasks": tasks}))
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")
