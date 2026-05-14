"""Add task command."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_description(description):
    """Validate task description."""
    # NOTE: Validation logic scattered here - should be in utils (refactor bounty)
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


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
    return tasks[-1]
