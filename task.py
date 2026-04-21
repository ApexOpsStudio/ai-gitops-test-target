#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import os
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done

# Module-level config paths (can be overridden for testing)
CONFIG_DIR = Path.home() / ".config" / "task-cli"
CONFIG_PATH = CONFIG_DIR / "config.yaml"

DEFAULT_CONFIG = """# Default configuration for task CLI
# Auto-created if not present

# Task storage settings
storage:
  format: json
  max_tasks: 1000

# Display settings
display:
  color: true
  unicode: true
"""


def load_config():
    """Load configuration from file. Creates default if missing."""
    global CONFIG_PATH, CONFIG_DIR
    
    if not CONFIG_PATH.exists():
        # Create default config directory and file
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CONFIG_PATH.write_text(DEFAULT_CONFIG)
            print(f"Created default config at {CONFIG_PATH}", file=sys.stderr)
        except OSError as e:
            print(f"Error: Could not create config file at {CONFIG_PATH}: {e}", file=sys.stderr)
            sys.exit(1)
    
    with open(CONFIG_PATH) as f:
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
