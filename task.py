#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done
from commands.output import emit_json


def load_config():
    """Load configuration from file."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    # NOTE: This will crash if config doesn't exist - known bug for bounty testing
    with open(config_path) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output machine-readable JSON",
    )
    json_parent = argparse.ArgumentParser(add_help=False)
    json_parent.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        default=argparse.SUPPRESS,
        help="Output machine-readable JSON",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", parents=[json_parent], help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    # List command
    list_parser = subparsers.add_parser("list", parents=[json_parent], help="List all tasks")

    # Done command
    done_parser = subparsers.add_parser("done", parents=[json_parent], help="Mark task as complete")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")

    args = parser.parse_args()
    json_output = bool(getattr(args, "json_output", False))

    try:
        if args.command == "add":
            add_task(args.description, json_output=json_output)
        elif args.command == "list":
            list_tasks(json_output=json_output)
        elif args.command == "done":
            result = mark_done(args.task_id, json_output=json_output)
            if json_output and result is None:
                sys.exit(1)
        else:
            parser.print_help()
    except ValueError as exc:
        if json_output:
            emit_json({"success": False, "message": str(exc), "data": None})
            sys.exit(1)
        raise


if __name__ == "__main__":
    main()
