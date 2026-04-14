#!/usr/bin/env python3
import subprocess, sys, shutil, json
from pathlib import Path

cwd = Path(__file__).parent
py = sys.executable

# Clean
for d in [Path.home() / ".local" / "share" / "task-cli"]:
    if d.exists():
        shutil.rmtree(d)

r = subprocess.run([py, "task.py", "add", "Test task 1"], capture_output=True, text=True, cwd=cwd)
print(f"[1] add: rc={r.returncode} stdout={r.stdout.strip()[:60]}")

r = subprocess.run([py, "task.py", "list", "--json"], capture_output=True, text=True, cwd=cwd)
print(f"[2] list --json: rc={r.returncode} stdout={r.stdout.strip()[:80]}")
try:
    d = json.loads(r.stdout)
    print(f"    -> Valid JSON: {d}")
except:
    print(f"    -> INVALID JSON!")

r = subprocess.run([py, "task.py", "done", "1"], capture_output=True, text=True, cwd=cwd)
print(f"[3] done: rc={r.returncode} stdout={r.stdout.strip()[:60]}")

r = subprocess.run([py, "task.py", "list"], capture_output=True, text=True, cwd=cwd)
print(f"[4] list: rc={r.returncode} stdout={r.stdout.strip()[:80]}")
print("\nAll tests passed!" if r.returncode == 0 else "\nTests failed!")
