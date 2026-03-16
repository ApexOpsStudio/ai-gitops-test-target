"""Mark task done command."""

from .utils import load_tasks, save_tasks, validate_task_id


def mark_done(task_id):
    """Mark a task as complete."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found!")
        return

    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Marked task {task_id} as done: {task['description']}")
            return

    print(f"Task {task_id} not found")
