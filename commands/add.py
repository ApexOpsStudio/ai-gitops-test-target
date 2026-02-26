"""Add task command."""

import json
from utils import get_tasks_file, validate_description


def add_task(description):
    """Add a new task."""
    description = validate_description(description)

    tasks_file = get_tasks_file()
    tasks_file.parent.mkdir(parents=True, exist_ok=True)

    tasks = []
    if tasks_file.exists():
        tasks = json.loads(tasks_file.read_text())

    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "description": description, "done": False})

    tasks_file.write_text(json.dumps(tasks, indent=2))
    print(f"Added task {task_id}: {description}")
