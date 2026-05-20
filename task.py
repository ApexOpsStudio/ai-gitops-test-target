#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
import json
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done

DEFAULT_CONFIG = {"tasks_file": "tasks.json", "verbose": False}


def load_config():
    """Load configuration from file, creating default if missing."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2))
        print(f"Created default config at {config_path}", file=sys.stderr)
        return DEFAULT_CONFIG
    try:
        with open(config_path) as f:
            return json.load(f) or DEFAULT_CONFIG
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error reading config: {e}. Using defaults.", file=sys.stderr)
        return DEFAULT_CONFIG


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
