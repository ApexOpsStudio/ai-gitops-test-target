#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from utils.paths import get_config_path
from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done

DEFAULT_CONFIG = """# Task CLI Configuration
# Edit this file to customize behavior
tasks_path: ~/.local/share/task-cli/tasks.json
"""


def load_config():
    """Load configuration from file. Creates default config if missing."""
    config_path = get_config_path()
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(DEFAULT_CONFIG)
        print(f"Created default config at {config_path}")
    return config_path.read_text()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    list_parser = subparsers.add_parser("list", help="List all tasks")

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
