"""Tests for JSON output mode."""
import json
import subprocess
import sys
from pathlib import Path


def run_cli(home, *args):
    result = subprocess.run(
        [sys.executable, "task.py", *args],
        cwd=Path(__file__).parent,
        env={"HOME": str(home)},
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def test_json_output_for_add_list_and_done(tmp_path):
    added = json.loads(run_cli(tmp_path, "add", "Ship feature", "--json"))
    assert added["status"] == "added"
    assert added["task"] == {"id": 1, "description": "Ship feature", "done": False}

    listed = json.loads(run_cli(tmp_path, "list", "--json"))
    assert listed["tasks"] == [added["task"]]

    done = json.loads(run_cli(tmp_path, "done", "1", "--json"))
    assert done["status"] == "done"
    assert done["task"] == {"id": 1, "description": "Ship feature", "done": True}

    listed_again = json.loads(run_cli(tmp_path, "list", "--json"))
    assert listed_again["tasks"] == [done["task"]]


def test_json_list_empty_state(tmp_path):
    listed = json.loads(run_cli(tmp_path, "list", "--json"))
    assert listed == {"tasks": []}
