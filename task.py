#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
import shutil
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done
from utils.paths import get_config_path


def load_config():
    """Load configuration from file."""
    config_path = get_config_path()
    config_dir = config_path.parent
    
    if not config_path.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        example_path = Path(__file__).parent / "config.yaml.example"
        if example_path.exists():
            shutil.copy(example_path, config_path)
        else:
            # Fallback if example is missing
            with open(config_path, "w") as f:
                f.write("# Default configuration\nstorage:\n  format: json\n")
                
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
    list_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    # Done command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("task_id", type=int, help="Task ID to mark done")

    args = parser.parse_args()

    # Load config to ensure it exists
    load_config()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks(json_output=args.json)
    elif args.command == "done":
        mark_done(args.task_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
