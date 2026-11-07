import json
from storage import load_tasks, save_tasks
from utils import parse_task_id


def run(args, json_output=False):
    if not args:
        print("Error: task ID required")
        return
    try:
        task_id = parse_task_id(args[0])
    except ValueError:
        print(f"Error: invalid ID '{args[0]}'")
        return
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            if json_output:
                print(json.dumps(t))
            else:
                print(f"Marked task #{task_id} as done.")
            return
    print(f"Error: task #{task_id} not found")
