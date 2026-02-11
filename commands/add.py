"""Add task command."""

import json

from .utils import load_tasks, save_tasks, validate_description


def add_task(description, json_output=False):
    """Add a new task."""
    description = validate_description(description)

    tasks = load_tasks()

    task_id = len(tasks) + 1
    task = {"id": task_id, "description": description, "done": False}
    tasks.append(task)

    save_tasks(tasks)

    if json_output:
        print(json.dumps(task))
    else:
        print(f"Added task {task_id}: {description}")
