"""Add task command."""

import json

from utils.paths import get_tasks_file
from utils.validation import validate_description

__all__ = ["add_task", "get_tasks_file", "validate_description"]


def add_task(description, as_json=False):
    """Add a new task."""
    description = validate_description(description)

    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)

    tasks = []
    if tasks_file.exists():
        tasks = json.loads(tasks_file.read_text())

    task_id = len(tasks) + 1
    task = {"id": task_id, "description": description, "done": False}
    tasks.append(task)

    tasks_file.write_text(json.dumps(tasks, indent=2))
    if as_json:
        print(json.dumps({"status": "added", **task}))
    else:
        print(f"Added task {task_id}: {description}")
