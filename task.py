#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


def load_config():
    """Load configuration from file. Returns None if config is missing."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    if not config_path.exists():
        return None
    try:
        with open(config_path) as f:
            return f.read()
    except Exception:
        return None


def ensure_config():
    """Ensure config file exists with defaults, otherwise create it."""
    config_path = Path.home() / ".config" / "task-cli" / "config.yaml"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # Copy from example if available
        example = Path(__file__).parent / "config.yaml.example"
        if example.exists():
            import shutil
            shutil.copy(example, config_path)
        else:
            config_path.write_text("# Default config\n# Add your settings here\n")


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
        ensure_config()
        add_task(args.description)
    elif args.command == "list":
        ensure_config()
        list_tasks()
    elif args.command == "done":
        ensure_config()
        mark_done(args.task_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
