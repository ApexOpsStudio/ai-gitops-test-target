#!/usr/bin/env python3
import subprocess, sys, json, shutil
from pathlib import Path

cwd = Path(__file__).parent
py = sys.executable

# Just run list
r = subprocess.run([py, "task.py", "list"], capture_output=True, text=True, cwd=cwd)
print(f"rc={r.returncode}")
print(f"stdout: {repr(r.stdout)}")
print(f"stderr: {repr(r.stderr)}")

tf = Path.home() / ".local" / "share" / "task-cli" / "tasks.json"
print(f"tasks file exists: {tf.exists()}")
if tf.exists():
    print(f"content: {tf.read_text()}")
