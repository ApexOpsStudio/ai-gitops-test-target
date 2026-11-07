import json
from storage import load_tasks, save_tasks
from utils import sanitize_title


def run(args, json_output=False):
    if not args:
        print("Error: task title required")
        return
    title = sanitize_title(" ".join(args))
    if not title:
        print("Error: task title required")
        return
    tasks = load_tasks()
    task = {"id": len(tasks) + 1, "title": title, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    if json_output:
        print(json.dumps(task))
    else:
        print(f"Added task #{task['id']}: {title}")
