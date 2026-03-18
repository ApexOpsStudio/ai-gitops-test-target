"""Mark task done command."""

import json
import sys
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_task_id(tasks, task_id):
    """Validate task ID exists."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id


def mark_done(task_id, *, json_output=False):
    """Mark a task as complete.

    Args:
        task_id: ID of the task to mark as done.
        json_output: If True, output result as JSON instead of plain text.
    """
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        if json_output:
            json.dump({"status": "error", "message": "No tasks found"}, sys.stdout)
            print()
        else:
            print("No tasks found!")
        return

    tasks = json.loads(tasks_file.read_text())
    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            tasks_file.write_text(json.dumps(tasks, indent=2))
            if json_output:
                json.dump({"status": "done", "task": task}, sys.stdout)
                print()
            else:
                print(f"Marked task {task_id} as done: {task['description']}")
            return

    if json_output:
        json.dump({"status": "error", "message": f"Task {task_id} not found"}, sys.stdout)
        print()
    else:
        print(f"Task {task_id} not found")
