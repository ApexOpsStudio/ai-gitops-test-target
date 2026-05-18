"""Add task command."""

from commands.storage import load_tasks, print_json, save_tasks


def validate_description(description):
    """Validate task description."""
    # NOTE: Validation logic scattered here - should be in utils (refactor bounty)
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 200:
        raise ValueError("Description too long (max 200 chars)")
    return description.strip()


def add_task(description, json_output=False):
    """Add a new task."""
    description = validate_description(description)

    tasks = load_tasks()
    task_id = len(tasks) + 1
    task = {"id": task_id, "description": description, "done": False}
    tasks.append(task)
    save_tasks(tasks)

    if json_output:
        print_json({"status": "added", "task": task})
        return

    print(f"Added task {task_id}: {description}")
