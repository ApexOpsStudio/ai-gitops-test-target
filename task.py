#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


DEFAULT_CONFIG = """\
# task-cli configuration
storage_path: ~/.local/share/task-cli/tasks.json
max_description_length: 200
"""


def load_config():
    """Load configuration from file.

    If the config file does not exist, a default one is created automatically.
    """
    config_dir = Path.home() / ".config" / "task-cli"
    config_path = config_dir / "config.yaml"

    if not config_path.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path.write_text(DEFAULT_CONFIG)

    return config_path.read_text()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output results as JSON",
    )
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

    json_mode = getattr(args, "json_output", False)

    if args.command == "add":
        add_task(args.description, json_output=json_mode)
    elif args.command == "list":
        list_tasks(json_output=json_mode)
    elif args.command == "done":
        mark_done(args.task_id, json_output=json_mode)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
