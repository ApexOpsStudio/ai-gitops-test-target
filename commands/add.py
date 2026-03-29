"""Add task command."""

import json
from utils.validation import validate_description, save_tasks
from utils.paths import get_tasks_file


def add_task(description, json_output=False):
    """Add a new task."""
    description = validate_description(description)

    tasks = []
    tasks_file = get_tasks_file()
    if tasks_file.exists():
        tasks = json.loads(tasks_file.read_text())

    task_id = len(tasks) + 1
    new_task = {"id": task_id, "description": description, "done": False}
    tasks.append(new_task)

    save_tasks(tasks)

    if json_output:
        print(json.dumps({"success": True, "task": new_task}))
    else:
        print(f"Added task {task_id}: {description}")
