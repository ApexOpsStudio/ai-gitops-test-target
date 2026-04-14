"""List tasks command."""

import json
from utils import get_tasks_file, validate_task_file


def list_tasks(json_output=False):
    """List all tasks."""
    tasks_file = get_tasks_file()
    tasks_file = validate_task_file(tasks_file)
    
    if not tasks_file:
        if json_output:
            print(json.dumps({"success": True, "tasks": []}))
        else:
            print("No tasks yet!")
        return

    tasks = json.loads(tasks_file.read_text())

    if not tasks:
        if json_output:
            print(json.dumps({"success": True, "tasks": []}))
        else:
            print("No tasks yet!")
        return

    if json_output:
        result = {"success": True, "tasks": tasks}
        print(json.dumps(result))
    else:
        for task in tasks:
            status = "[x]" if task["done"] else "[ ]"
            print(f"{status} {task['id']}. {task['description']}")
