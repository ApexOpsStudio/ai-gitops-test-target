"""Mark task done command."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_task_id(tasks, task_id):
    """Validate task ID exists."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id


def mark_done(task_id, json_output=False):
    """Mark a task as complete. Returns task dict if json_output, else prints."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        if json_output:
            print(json.dumps({"error": "No tasks found"}))
        else:
            print("No tasks found!")
        return None

    tasks = json.loads(tasks_file.read_text())

    result = None
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            result = task
            break

    if result:
        tasks_file.write_text(json.dumps(tasks, indent=2))
        if json_output:
            print(json.dumps(result, indent=2))
        else:
            print(f"Marked task {task_id} as done: {result['description']}")
    else:
        if json_output:
            print(json.dumps({"error": f"Task {task_id} not found"}))
        else:
            print(f"Task {task_id} not found")

    return result
