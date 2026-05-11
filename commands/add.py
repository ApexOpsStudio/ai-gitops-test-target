"""Add task command."""

from commands.storage import emit_json, read_tasks, write_tasks


def validate_description(description):
    """Validate task description."""
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def add_task(description, json_output=False):
    """Add a new task."""
    description = validate_description(description)

    tasks = read_tasks()
    task_id = len(tasks) + 1
    task = {"id": task_id, "description": description, "done": False}
    tasks.append(task)

    write_tasks(tasks)
    if json_output:
        emit_json({"task": task})
    else:
        print(f"Added task {task_id}: {description}")
    return task
