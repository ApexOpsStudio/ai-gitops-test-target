"""Mark task done command."""

import json
from utils.paths import get_tasks_file
from utils.validation import validate_task_id


def mark_done(task_id, json_output=False):
    """Mark a task as complete."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        if not json_output:
            print("No tasks found!")
        return None

    tasks = json.loads(tasks_file.read_text())
    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            tasks_file.write_text(json.dumps(tasks, indent=2))
            if not json_output:
                print(f"Marked task {task_id} as done: {task['description']}")
            return task

    if not json_output:
        print(f"Task {task_id} not found")
    return None
