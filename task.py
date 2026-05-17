#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
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
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON",
    )

    parser = argparse.ArgumentParser(
        description="Simple task manager",
        parents=[common_parser],
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new task",
        parents=[common_parser],
    )
    add_parser.add_argument("description", help="Task description")

    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List all tasks",
        parents=[common_parser],
    )

    # Done command
    done_parser = subparsers.add_parser(
        "done",
        help="Mark task as complete",
        parents=[common_parser],
    )
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description, json_output=args.json)
    elif args.command == "list":
        list_tasks(json_output=args.json)
    elif args.command == "done":
        mark_done(args.task_id, json_output=args.json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
