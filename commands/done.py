"""Mark task done command."""

import json
from utils.validation import validate_task_id, validate_task_file, load_tasks, save_tasks


def mark_done(task_id, json_output=False):
    """Mark a task as complete."""
    tasks_file = validate_task_file()
    if not tasks_file:
        if json_output:
            print(json.dumps({"success": False, "error": "No tasks found"}))
        else:
            print("No tasks found!")
        return

    tasks = load_tasks()
    try:
        validate_task_id(tasks, task_id)
    except ValueError as e:
        if json_output:
            print(json.dumps({"success": False, "error": str(e)}))
        else:
            print(f"Task {task_id} not found")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            if json_output:
                print(json.dumps({"success": True, "task": task}))
            else:
                print(f"Marked task {task_id} as done: {task['description']}")
            return
