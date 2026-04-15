"""List tasks command."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_task_file():
    """Validate tasks file exists."""
    tasks_file = get_tasks_file()
    if tasks_file is None or not tasks_file.exists():
        return None
    return tasks_file


def list_tasks(json_output=False):
    """List all tasks. Returns tasks list if json_output, else prints."""
    tasks_file = validate_task_file()
    if not tasks_file:
        if json_output:
            print(json.dumps([]))
        else:
            print("No tasks yet!")
        return []

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if json_output:
            print(json.dumps([]))
        else:
            print("No tasks yet!")
        return tasks

    if json_output:
        print(json.dumps(tasks, indent=2))
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")

    return tasks
