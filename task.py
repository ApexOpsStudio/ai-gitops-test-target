#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task, add_task_json
from commands.list import list_tasks, list_tasks_json
from commands.done import mark_done, mark_done_json


def load_config():
    """Load configuration from file."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    # NOTE: This will crash if config doesn't exist - known bug for bounty testing
    with open(config_path) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    add_parser.add_argument("description", help="Task description")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")

    args = parser.parse_args()

    if args.command == "add":
        if args.json:
            add_task_json(args.description)
        else:
            add_task(args.description)
    elif args.command == "list":
        if args.json:
            list_tasks_json()
        else:
            list_tasks()
    elif args.command == "done":
        if args.json:
            mark_done_json(args.task_id)
        else:
            mark_done(args.task_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
