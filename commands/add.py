"""Add task command."""

import json
import sys

from utils.paths import get_tasks_file
from utils.validation import validate_description


def add_task(description: str, json_output: bool = False) -> None:
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

    if json_output:
        print(json.dumps({"status": "added", "task": task}))
    else:
        print(f"Added task {task_id}: {description}")
