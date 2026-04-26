#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done
from utils.paths import get_config_file


def load_config():
    """Load configuration from file."""
    config_path = get_config_file()
    if not config_path.exists():
        # Return empty config instead of crashing
        return ""
    return config_path.read_text()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output results as JSON"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output results as JSON"
    )

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")
    done_parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output results as JSON"
    )

    args = parser.parse_args()
    json_output = getattr(args, "json_output", False)

    if args.command == "add":
        add_task(args.description, json_output=json_output)
    elif args.command == "list":
        list_tasks(json_output=json_output)
    elif args.command == "done":
        mark_done(args.task_id, json_output=json_output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
