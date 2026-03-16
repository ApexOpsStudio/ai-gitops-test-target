#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done

DEFAULT_CONFIG = """\
# Task CLI configuration
# See config.yaml.example for all options

# Task storage settings
storage:
  format: json
  max_tasks: 1000

# Display settings
display:
  color: true
  unicode: true
"""


def get_config_path():
    """Get path to config file."""
    return Path.home() / ".config" / "task-cli" / "config.yaml"


def load_config():
    """Load configuration from file.

    If the config file does not exist, creates a default one and returns it.
    If the config directory does not exist, creates it first.

    Returns:
        The configuration file contents as a string.
    """
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

    # Load config gracefully — creates default if missing
    config = load_config()

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
