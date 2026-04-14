#!/usr/bin/env python3
"""Test JSON output for all commands."""

import subprocess
import json
import sys
import os
from pathlib import Path

# Ensure we use the local module
sys.path.insert(0, str(Path(__file__).parent))

def run_cmd(args):
    """Run command and return parsed JSON output."""
    result = subprocess.run(
        [sys.executable, "task.py"] + args,
        capture_output=True, text=True, cwd=Path(__file__).parent
    )
    return result.stdout.strip(), result.returncode

def test_list_json():
    """Test list --json outputs valid JSON."""
    out, code = run_cmd(["list", "--json"])
    try:
        data = json.loads(out)
        assert "success" in data, "Missing 'success' key"
        assert "tasks" in data, "Missing 'tasks' key"
        print("PASS: list --json outputs valid JSON")
        return True
    except json.JSONDecodeError:
        print(f"FAIL: list --json not valid JSON: {out}")
        return False

def test_add_json():
    """Test add --json outputs valid JSON."""
    out, code = run_cmd(["add", "Test task for JSON", "--json"])
    try:
        data = json.loads(out)
        assert "success" in data, "Missing 'success' key"
        assert "task_id" in data, "Missing 'task_id' key"
        print("PASS: add --json outputs valid JSON")
        return True
    except json.JSONDecodeError:
        print(f"FAIL: add --json not valid JSON: {out}")
        return False

def test_done_json():
    """Test done --json outputs valid JSON."""
    out, code = run_cmd(["done", "1", "--json"])
    try:
        data = json.loads(out)
        assert "success" in data, "Missing 'success' key"
        print("PASS: done --json outputs valid JSON")
        return True
    except json.JSONDecodeError:
        print(f"FAIL: done --json not valid JSON: {out}")
        return False

if __name__ == "__main__":
    print("Running JSON output tests...")
    results = [test_list_json(), test_add_json(), test_done_json()]
    if all(results):
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")
        sys.exit(1)
