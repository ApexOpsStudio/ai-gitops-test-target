"""Mark task done command."""

from commands.storage import get_tasks_file, load_tasks, print_json, save_tasks


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
            print_json({"status": "not_found", "error": "No tasks found"})
            return
        print("No tasks found!")
        return

    tasks = load_tasks()
    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            if json_output:
                print_json({"status": "done", "task": task})
                return
            print(f"Marked task {task_id} as done: {task['description']}")
            return

    if json_output:
        print_json({"status": "not_found", "error": f"Task {task_id} not found"})
        return

    print(f"Task {task_id} not found")
