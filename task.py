#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


def load_config():
    """Load configuration from file. Creates default config if missing."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        default_config = "# task-cli configuration\nversion: 1\n"
        config_path.write_text(default_config)
        return default_config
    with open(config_path) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")
    done_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()
    use_json = getattr(args, "json", False)

    if args.command == "add":
        add_task(args.description, output_json=use_json)
    elif args.command == "list":
        list_tasks(output_json=use_json)
    elif args.command == "done":
        mark_done(args.task_id, output_json=use_json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
