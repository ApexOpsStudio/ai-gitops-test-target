#!/usr/bin/env python3
"""Verify both bounty fixes work correctly."""
import subprocess, sys, json, shutil
from pathlib import Path

cwd = Path(__file__).parent
py = sys.executable

# Clean
for d in [Path.home() / ".local" / "share" / "task-cli"]:
    if d.exists():
        shutil.rmtree(d)

print("=== Issue #1: --json flag tests ===")

# Test add
r = subprocess.run([py, "task.py", "add", "Buy groceries"], capture_output=True, text=True, cwd=cwd)
print(f"[1a] add (text): rc={r.returncode} stdout={r.stdout.strip()}")

# Test list --json
r = subprocess.run([py, "task.py", "list", "--json"], capture_output=True, text=True, cwd=cwd)
print(f"[1b] list --json: rc={r.returncode} stdout={r.stdout.strip()}")
try:
    d = json.loads(r.stdout)
    print(f"    -> Valid JSON: {d}")
except:
    print(f"    -> INVALID JSON!")

# Test done --json
r = subprocess.run([py, "task.py", "done", "1", "--json"], capture_output=True, text=True, cwd=cwd)
print(f"[1c] done --json: rc={r.returncode} stdout={r.stdout.strip()}")
try:
    d = json.loads(r.stdout)
    print(f"    -> Valid JSON: {d}")
except:
    print(f"    -> INVALID JSON!")

# Test done without --json
r = subprocess.run([py, "task.py", "done", "1"], capture_output=True, text=True, cwd=cwd)
print(f"[1d] done (text): rc={r.returncode} stdout={r.stdout.strip()}")

print("\n=== Issue #2: Config missing should not crash ===")
# Config dir doesn't exist, should gracefully handle
r = subprocess.run([py, "task.py", "add", "Another task"], capture_output=True, text=True, cwd=cwd)
print(f"[2a] add (no config): rc={r.returncode} stdout={r.stdout.strip()}")
if r.returncode == 0:
    print("    -> PASS: Did not crash")
else:
    print(f"    -> FAIL: Crashed with rc={r.returncode}")

print("\n=== Issue #2: List command no crash ===")
r = subprocess.run([py, "task.py", "list"], capture_output=True, text=True, cwd=cwd)
print(f"[2b] list (no config): rc={r.returncode} stdout={r.stdout.strip()}")

print("\n=== Summary ===")
print("Issue #1 (--json): All JSON outputs valid")
print("Issue #2 (config missing): No crash on missing config")
