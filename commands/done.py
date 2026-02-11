"""Mark task done command."""

import json

from .utils import load_tasks, save_tasks, validate_task_id


def mark_done(task_id, json_output=False):
    """Mark a task as complete."""
    tasks = load_tasks()
    if not tasks:
        if json_output:
            print(json.dumps({}))
        else:
            print("No tasks found!")
        return

    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            if json_output:
                print(json.dumps(task))
            else:
                print(f"Marked task {task_id} as done: {task['description']}")
            return

    if json_output:
        print(json.dumps({}))
    else:
        print(f"Task {task_id} not found")
