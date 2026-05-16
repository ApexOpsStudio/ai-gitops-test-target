"""Mark task done command."""

import json
from utils.paths import get_tasks_file
from utils.validation import validate_task_id


def mark_done(task_id, json_output=False):
    """Mark a task as complete."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        msg = "No tasks found!"
        if json_output:
            print(json.dumps({"error": msg, "task_id": task_id}))
        else:
            print(msg)
        return

    tasks = json.loads(tasks_file.read_text())
    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            tasks_file.write_text(json.dumps(tasks, indent=2))
            if json_output:
                print(json.dumps(task))
            else:
                print(f"Marked task {task_id} as done: {task['description']}")
            return

    if json_output:
        print(json.dumps({"error": f"Task {task_id} not found"}))
    else:
        print(f"Task {task_id} not found")
