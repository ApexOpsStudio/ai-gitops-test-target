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
    
    # Check if config file exists
    if not config_path.exists():
        # Create default config directory and file
        config_dir = config_path.parent
        config_dir.mkdir(parents=True, exist_ok=True)
        
        default_config = """# Default configuration for task CLI
# Task storage settings
storage:
  format: json
  max_tasks: 1000

# Display settings
display:
  color: true
  unicode: true
"""
        config_path.write_text(default_config)
        print(f"Created default config at {config_path}")
    
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

    # Load config on startup
    try:
        load_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        return 1

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
