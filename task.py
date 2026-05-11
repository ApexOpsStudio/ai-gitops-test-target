#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
from pathlib import Path

from commands.add import add_task
from commands.done import mark_done
from commands.list import list_tasks


DEFAULT_CONFIG = """storage:
  format: json
  max_tasks: 1000
display:
  color: true
  unicode: true
"""


def get_config_path():
    """Return the task CLI config path."""
    return Path.home() / ".config" / "task-cli" / "config.yaml"


def load_config():
    """Load configuration from file, creating a default config if needed."""
    config_path = get_config_path()
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(DEFAULT_CONFIG)
    return config_path.read_text()


def main():
    json_parent = argparse.ArgumentParser(add_help=False)
    json_parent.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Output JSON",
    )

    parser = argparse.ArgumentParser(description="Simple task manager")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    add_parser = subparsers.add_parser(
        "add", parents=[json_parent], help="Add a new task"
    )
    add_parser.add_argument("description", help="Task description")

    subparsers.add_parser("list", parents=[json_parent], help="List all tasks")

    done_parser = subparsers.add_parser(
        "done", parents=[json_parent], help="Mark task as complete"
    )
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")

    args = parser.parse_args()
    load_config()

    if args.command == "add":
        add_task(args.description, json_output=args.json)
    elif args.command == "list":
        list_tasks(json_output=args.json)
    elif args.command == "done":
        mark_done(args.task_id, json_output=args.json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
