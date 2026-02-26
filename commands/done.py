"""Mark task done command."""

import json
from utils import get_tasks_file, validate_task_id


def mark_done(task_id):
    """Mark a task as complete."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        print("No tasks found!")
        return

    tasks = json.loads(tasks_file.read_text())
    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            tasks_file.write_text(json.dumps(tasks, indent=2))
            print(f"Marked task {task_id} as done: {task['description']}")
            return

    print(f"Task {task_id} not found")
