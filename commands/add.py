"""Add task command."""

from .utils import get_tasks_file, load_tasks, save_tasks, validate_description


def add_task(description):
    """Add a new task."""
    description = validate_description(description)

    tasks = load_tasks()
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "description": description, "done": False})

    save_tasks(tasks)
    print(f"Added task {task_id}: {description}")
