#!/usr/bin/env python3
import subprocess, sys, os
from pathlib import Path

# Clean up any existing data
for d in [Path.home() / ".local" / "share" / "task-cli", Path.home() / ".config" / "task-cli"]:
    import shutil
    if d.exists():
        shutil.rmtree(d)

cwd = Path(__file__).parent
py = sys.executable

print("=== Test add ===")
r = subprocess.run([py, "task.py", "add", "First task"], capture_output=True, text=True, cwd=cwd)
print("stdout:", r.stdout)
print("stderr:", r.stderr[:200] if r.stderr else "")

print("\n=== Test list --json ===")
r = subprocess.run([py, "task.py", "list", "--json"], capture_output=True, text=True, cwd=cwd)
print("stdout:", r.stdout.strip())

print("\n=== Test done 1 --json ===")
r = subprocess.run([py, "task.py", "done", "1", "--json"], capture_output=True, text=True, cwd=cwd)
print("stdout:", r.stdout.strip())

print("\n=== Test list --json after done ===")
r = subprocess.run([py, "task.py", "list", "--json"], capture_output=True, text=True, cwd=cwd)
print("stdout:", r.stdout.strip())

print("\n=== Test list (no flag) ===")
r = subprocess.run([py, "task.py", "list"], capture_output=True, text=True, cwd=cwd)
print("stdout:", r.stdout)

print("\n=== Test config missing (should not crash) ===")
r = subprocess.run([py, "task.py", "list"], capture_output=True, text=True, cwd=cwd)
print("rc:", r.returncode, "| stdout:", r.stdout.strip()[:100])
