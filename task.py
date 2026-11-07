#!/usr/bin/env python3
"""Simple CLI task manager.

Usage:
    python task.py [--json] add <title>
    python task.py [--json] list
    python task.py [--json] done <id>
"""
import sys
from commands import add, list as list_cmd, done
from utils import validate_command

COMMANDS = {
    "add": add,
    "list": list_cmd,
    "done": done,
}


def main():
    raw_args = sys.argv[1:]
    json_output = "--json" in raw_args
    args = [a for a in raw_args if a != "--json"]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    cmd_args = args[1:]

    if not validate_command(cmd, COMMANDS):
        print(f"Unknown command: {cmd}")
        sys.exit(1)

    COMMANDS[cmd].run(cmd_args, json_output=json_output)


if __name__ == "__main__":
    main()
