#!/usr/bin/env python3
"""Simple task manager CLI."""

import argparse
import sys
from pathlib import Path

from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


DEFAULT_CONFIG_TEXT = """\
# Task CLI configuration
storage_dir: ~/.local/share/task-cli
default_format: text
"""

DEFAULT_CONFIG = {
    "storage_dir": "~/.local/share/task-cli",
    "default_format": "text",
}


def get_config_path():
    """Get path to config file."""
    return Path.home() / ".config" / "task-cli" / "config.yaml"


def _parse_config(text):
    """Parse simple YAML key-value config into a dict."""
    config = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            config[key.strip()] = value.strip()
    return config


def load_config():
    """Load configuration from file.

    If the config file does not exist, creates one with sensible defaults.
    Returns a parsed config dict.
    """
    config_path = get_config_path()

    if not config_path.exists():
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(DEFAULT_CONFIG_TEXT)
        except OSError as e:
            print(f"Warning: Could not write default config: {e}", file=sys.stderr)
        return dict(DEFAULT_CONFIG)

    try:
        with open(config_path) as f:
            return _parse_config(f.read())
    except OSError as e:
        print(f"Warning: Could not read config file: {e}", file=sys.stderr)
        return dict(DEFAULT_CONFIG)


def main():
    config = load_config()

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
