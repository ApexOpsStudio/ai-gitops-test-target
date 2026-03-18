"""Add task command."""

import json
import sys
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_description(description):
    """Validate task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def add_task(description, *, json_output=False):
    """Add a new task.

    Args:
        description: Task description text.
        json_output: If True, output result as JSON instead of plain text.
    """
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
        json.dump({"status": "added", "task": task}, sys.stdout)
        print()  # trailing newline
    else:
        print(f"Added task {task_id}: {description}")
