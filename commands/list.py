"""List tasks command."""

from commands.storage import emit_json, get_tasks_file, read_tasks


def validate_task_file():
    """Validate tasks file exists."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return tasks_file


def list_tasks(json_output=False):
    """List all tasks."""
    tasks_file = validate_task_file()
    if not tasks_file:
        tasks = []
        if json_output:
            emit_json({"tasks": tasks})
        else:
            print("No tasks yet!")
        return tasks

    tasks = read_tasks()
    if not tasks:
        if json_output:
            emit_json({"tasks": tasks})
        else:
            print("No tasks yet!")
        return tasks

    if json_output:
        emit_json({"tasks": tasks})
    else:
        for task in tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] {task['id']}. {task['description']}")
    return tasks
