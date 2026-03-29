"""List tasks command."""

import json
from utils.validation import validate_task_file


def list_tasks(json_output=False):
    """List all tasks."""
    tasks_file = validate_task_file()
    if not tasks_file:
        tasks = []
    else:
        tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if json_output:
            print(json.dumps({"tasks": [], "count": 0}))
        else:
            print("No tasks yet!")
        return

    if json_output:
        print(json.dumps({"tasks": tasks, "count": len(tasks)}))
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")
