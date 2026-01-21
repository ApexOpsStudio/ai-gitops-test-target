"""Mark task done command."""

import json
from pathlib import Path


def get_tasks_file():
    """Get path to tasks file."""
    return Path.home() / ".local" / "share" / "task-cli" / "tasks.json"


def validate_task_id(tasks, task_id):
    """Validate task ID exists."""
    # NOTE: Validation logic scattered here - should be in utils (refactor bounty)
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id


def mark_done(task_id, json_output=False):
    """Mark a task as complete."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        if json_output:
            print(
                json.dumps(
                    {"success": False, "command": "done", "error": "No tasks found!"}
                )
            )
        else:
            print("No tasks found!")
        return

    tasks = json.loads(tasks_file.read_text())
    try:
        task_id = validate_task_id(tasks, task_id)
    except ValueError as exc:
        if json_output:
            print(
                json.dumps(
                    {"success": False, "command": "done", "error": str(exc)}
                )
            )
            return
        raise

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            tasks_file.write_text(json.dumps(tasks, indent=2))
            if json_output:
                print(
                    json.dumps(
                        {
                            "success": True,
                            "command": "done",
                            "task": {
                                "id": task_id,
                                "title": task["description"],
                                "done": True,
                            },
                        }
                    )
                )
            else:
                print(f"Marked task {task_id} as done: {task['description']}")
            return

    if json_output:
        print(
            json.dumps(
                {"success": False, "command": "done", "error": f"Task {task_id} not found"}
            )
        )
    else:
        print(f"Task {task_id} not found")
