#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


DEFAULT_CONFIG = """# Task CLI configuration

storage:
  format: json
  max_tasks: 1000

display:
  color: true
  unicode: true
"""


def get_config_path():
    """Return the default task-cli config path."""
    return Path.home() / ".config" / "task-cli" / "config.yaml"


def load_config():
    """Load configuration from file, creating a default one if needed."""
    config_path = get_config_path()

    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(DEFAULT_CONFIG)

    return config_path.read_text()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
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

    load_config()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.task_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
