"""Mark task done command."""

import json
from .validation import get_tasks_file, read_tasks, validate_task_id, write_tasks


def mark_done(task_id, json_output=False):
    """Mark a task as complete."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        response = {"status": "error", "message": "No tasks found!"}
        if json_output:
            print(json.dumps(response))
        else:
            print(response["message"])
        return

    tasks = read_tasks(tasks_file)
    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            write_tasks(tasks, tasks_file)
            response = {
                "status": "ok",
                "task": {"id": task["id"], "description": task["description"]},
            }
            if json_output:
                print(json.dumps(response))
            else:
                print(f"Marked task {task_id} as done: {task['description']}")
            return

    print(f"Task {task_id} not found")
