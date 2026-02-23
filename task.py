#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


DEFAULT_CONFIG = """# Default configuration for task CLI
# Auto-generated on first run

# Task storage settings
storage:
  format: json
  max_tasks: 1000

# Display settings
display:
  color: true
  unicode: true
"""


def ensure_config_exists():
    """Ensure config file exists, create default if missing."""
    config_dir = Path.home() / ".config" / "task-cli"
    config_path = config_dir / "config.yaml"
    
    if not config_path.exists():
        # Create config directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        # Create default config file
        config_path.write_text(DEFAULT_CONFIG)
        print(f"Created default config at {config_path}")
    
    return config_path


def load_config():
    """Load configuration from file."""
    config_path = ensure_config_exists()
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
