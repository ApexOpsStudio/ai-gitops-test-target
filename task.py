#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


def load_config():
    """Load configuration from file. Creates default if missing."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        default_config = (
            "# Task CLI configuration\n"
            "storage:\n"
            "  format: json\n"
            "  max_tasks: 1000\n"
            "\n"
            "display:\n"
            "  color: true\n"
            "  unicode: true\n"
        )
        config_path.write_text(default_config)
        print(f"Created default config at {config_path}")
    with open(config_path) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Simple task manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Shared --json flag on each subcommand
    json_arg = {"flags": ["--json"], "action": "store_true", "help": "Output in JSON format"}

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument(*json_arg["flags"], action=json_arg["action"], help=json_arg["help"])

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(*json_arg["flags"], action=json_arg["action"], help=json_arg["help"])

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")
    done_parser.add_argument(*json_arg["flags"], action=json_arg["action"], help=json_arg["help"])

    args = parser.parse_args()
    use_json = args.json

    if args.command == "add":
        add_task(args.description)
        if use_json:
            import json
            print(json.dumps({"status": "added", "description": args.description}))
    elif args.command == "list":
        list_tasks(as_json=use_json)
    elif args.command == "done":
        mark_done(args.task_id)
        if use_json:
            import json
            print(json.dumps({"status": "done", "task_id": args.task_id}))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
