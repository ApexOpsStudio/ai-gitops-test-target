"""List tasks command."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_task_file():
    """Validate tasks file exists."""
    # NOTE: Validation logic scattered here - should be in utils (refactor bounty)
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return tasks_file


def list_tasks(json_output=False):
    """List all tasks."""
    tasks_file = validate_task_file()
    if not tasks_file:
        if json_output:
            print(json.dumps({"success": True, "message": "No tasks yet", "data": []}))
        else:
            print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if json_output:
            print(json.dumps({"success": True, "message": "No tasks yet", "data": []}))
        else:
            print("No tasks yet!")
        return

    if json_output:
        print(json.dumps({"success": True, "message": f"{len(tasks)} task(s)", "data": tasks}))
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")
