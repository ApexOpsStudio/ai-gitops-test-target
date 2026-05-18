"""List tasks command."""

from commands.storage import get_tasks_file, load_tasks, print_json


def validate_task_file():
    """Validate tasks file exists."""
    # NOTE: Validation logic scattered here - should be in utils (refactor bounty)
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        return []
    return tasks_file


def list_tasks(json_output=False):
    """List all tasks."""
    tasks_file = validate_task_file()
    if not tasks_file:
        if json_output:
            print_json({"tasks": []})
            return
        print("No tasks yet!")
        return

    tasks = load_tasks()

    if not tasks:
        if json_output:
            print_json({"tasks": []})
            return
        print("No tasks yet!")
        return

    if json_output:
        print_json({"tasks": tasks})
        return

    for task in tasks:
        status = "✓" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['description']}")
