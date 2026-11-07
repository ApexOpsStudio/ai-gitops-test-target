import json
from storage import load_tasks
from utils import format_task_line


def run(args, json_output=False):
    tasks = load_tasks()
    if json_output:
        print(json.dumps(tasks))
        return
    if not tasks:
        print("No tasks yet.")
        return
    for t in tasks:
        print(format_task_line(t))
