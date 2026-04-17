#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


def load_config():
    """Load configuration from file."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    # NOTE: This will crash if config doesn't exist - known bug for bounty testing
    with open(config_path) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")

    args = parser.parse_args()
    as_json = getattr(args, "json", False)

    if args.command == "add":
        add_task(args.description, as_json=as_json)
    elif args.command == "list":
        list_tasks(as_json=as_json)
    elif args.command == "done":
        mark_done(args.task_id, as_json=as_json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
