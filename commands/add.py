"""Add task command."""

import json
from .utils import get_tasks_file, validate_description


def add_task(description, *, json_output=False):
    """Add a new task."""
    description = validate_description(description)

    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)

    tasks = []
    if tasks_file.exists():
        tasks = json.loads(tasks_file.read_text())

    task_id = len(tasks) + 1
    new_task = {"id": task_id, "description": description, "done": False}
    tasks.append(new_task)

    tasks_file.write_text(json.dumps(tasks, indent=2))

    if json_output:
        print(json.dumps({"status": "added", "task": new_task}))
    else:
        print(f"Added task {task_id}: {description}")
