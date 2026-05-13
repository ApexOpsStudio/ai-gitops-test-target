"""List tasks command."""
import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def list_tasks(json_output=False):
    """List all tasks."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        if json_output:
            print(json.dumps({"tasks": []}))
        else:
            print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())
    if json_output:
        print(json.dumps({"tasks": tasks}))
        return

    if not tasks:
        print("No tasks yet!")
        return

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")
