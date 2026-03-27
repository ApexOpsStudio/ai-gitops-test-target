"""List tasks command."""

import json
from utils.paths import get_tasks_file
from utils.validation import validate_task_file


def list_tasks(output_json=False):
    """List all tasks."""
    tasks_file = validate_task_file(get_tasks_file())
    if not tasks_file:
        if output_json:
            print("[]")
        else:
            print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if output_json:
            print("[]")
        else:
            print("No tasks yet!")
        return

    if output_json:
        print(json.dumps(tasks))
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")
