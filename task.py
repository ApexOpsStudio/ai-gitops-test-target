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
    if not config_path.exists():
        # Create default config with sensible defaults
        config_path.parent.mkdir(parents=True, exist_ok=True)
        default_config = """# Task CLI Configuration
default_sort: recent
json_output: false
"""
        config_path.write_text(default_config)
        return default_config
    with open(config_path) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    parser.add_argument("--json", dest="json_output", action="store_true", help="Output in JSON format")
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
        result = add_task(args.description, json_output=args.json_output)
    elif args.command == "list":
        result = list_tasks(json_output=args.json_output)
    elif args.command == "done":
        result = mark_done(args.task_id, json_output=args.json_output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
