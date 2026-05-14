#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import contextlib
import io
import json
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


def print_json(payload):
    """Print a stable JSON payload for automation."""
    print(json.dumps(payload, indent=2))


def run_quietly(action, *args):
    """Run an existing command without its human-readable stdout."""
    with contextlib.redirect_stdout(io.StringIO()):
        return action(*args)


def load_config():
    """Load configuration from file."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    # NOTE: This will crash if config doesn't exist - known bug for bounty testing
    with open(config_path) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Output JSON")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Output JSON")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")
    done_parser.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Output JSON")

    args = parser.parse_args()

    if args.command == "add":
        if args.json:
            task = run_quietly(add_task, args.description)
            print_json({"success": True, "task": task})
        else:
            add_task(args.description)
    elif args.command == "list":
        if args.json:
            tasks = run_quietly(list_tasks)
            print_json({"success": True, "tasks": tasks})
        else:
            list_tasks()
    elif args.command == "done":
        if args.json:
            task = run_quietly(mark_done, args.task_id)
            print_json({"success": task is not None, "task": task})
        else:
            mark_done(args.task_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
