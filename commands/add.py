"""Add task command."""

import json
from .validation import get_tasks_file, validate_description, read_tasks, write_tasks


def add_task(description, json_output=False):
    """Add a new task."""
    description = validate_description(description)

    tasks_file = get_tasks_file()
    tasks = read_tasks(tasks_file)

    task_id = len(tasks) + 1
    task = {"id": task_id, "description": description, "done": False}
    tasks.append(task)

    write_tasks(tasks, tasks_file)

    response = {"status": "ok", "task": task}
    if json_output:
        print(json.dumps(response))
    else:
        print(f"Added task {task_id}: {description}")
