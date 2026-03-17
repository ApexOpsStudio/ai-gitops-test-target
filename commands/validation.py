import json
from pathlib import Path


def get_tasks_file():
    """Return the default task data file path."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def read_tasks(tasks_file=None):
    """Load tasks from disk and return a list."""
    file_path = tasks_file or get_tasks_file()
    if not file_path.exists():
        return []

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_tasks(tasks, tasks_file=None):
    """Persist all tasks to disk."""
    file_path = tasks_file or get_tasks_file()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def validate_description(description):
    """Validate and normalize task description text."""
    if not description:
        raise ValueError("Description cannot be empty")
    stripped = description.strip()
    if len(stripped) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return stripped


def validate_task_id(tasks, task_id):
    """Validate task ID exists in current tasks list."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id
