#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


def load_config():
    """Load configuration from file.

    Returns the config contents as a string, or a sensible default config
    if the file does not exist yet.  A default config file is also created
    on disk so future runs pick it up automatically.
    """
    config_dir = Path.home() / ".config" / "task-cli"
    config_path = config_dir / "config.yaml"

    if not config_path.exists():
        # Create a sensible default config
        default_config = (
            "# Task CLI configuration\n"
            "storage:\n"
            "  format: json\n"
            "  max_tasks: 1000\n"
            "display:\n"
            "  color: true\n"
            "  unicode: true\n"
        )
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path.write_text(default_config)
        return default_config

    with open(config_path) as f:
        return f.read()


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
