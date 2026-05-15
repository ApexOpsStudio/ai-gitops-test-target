#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import json
import sys

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done
from utils.paths import get_config_file


def load_config():
    """Load configuration from file."""
    config_path = get_config_file()
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("tasks_file: ~/.local/share/task-cli/tasks.json\n")
    return config_path.read_text()


def print_json(data):
    """Print a JSON response."""
    print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("--json", action="store_true", help="Output JSON")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--json", action="store_true", help="Output JSON")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")
    done_parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()
    load_config()

    if args.command == "add":
        task = add_task(args.description, json_output=args.json)
        if args.json:
            print_json({"task": task})
    elif args.command == "list":
        tasks = list_tasks(json_output=args.json)
        if args.json:
            print_json({"tasks": tasks})
    elif args.command == "done":
        task = mark_done(args.task_id, json_output=args.json)
        if args.json:
            print_json({"task": task})
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
