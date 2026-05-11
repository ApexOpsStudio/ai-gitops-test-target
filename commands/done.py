"""Mark task done command."""

from commands.storage import emit_json, get_tasks_file, read_tasks, write_tasks


def validate_task_id(tasks, task_id):
    """Validate task ID exists."""
    if task_id < 1 or task_id > len(tasks):
        raise ValueError(f"Invalid task ID: {task_id}")
    return task_id


def mark_done(task_id, json_output=False):
    """Mark a task as complete."""
    tasks_file = get_tasks_file()
    if not tasks_file.exists():
        if json_output:
            emit_json({"error": "No tasks found!"})
        else:
            print("No tasks found!")
        return None

    tasks = read_tasks()
    task_id = validate_task_id(tasks, task_id)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            write_tasks(tasks)
            if json_output:
                emit_json({"task": task})
            else:
                print(f"Marked task {task_id} as done: {task['description']}")
            return task

    if json_output:
        emit_json({"error": f"Task {task_id} not found"})
    else:
        print(f"Task {task_id} not found")
    return None
