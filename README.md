# Task CLI

A simple command-line task manager.

## Usage

```bash
# Add a task
python task.py add "Buy groceries"

# List all tasks
python task.py list

# Mark a task as done
python task.py done 1
```

## JSON Output

Add `--json` flag to any command for machine-readable JSON output:

```bash
# Add task with JSON output
python task.py --json add "Buy groceries"
# {"status": "added", "task": {"id": 1, "description": "Buy groceries", "done": false}}

# List tasks as JSON
python task.py --json list
# {"tasks": [...], "count": 3}

# Mark done with JSON output
python task.py --json done 1
# {"status": "done", "task": {"id": 1, "description": "Buy groceries", "done": true}}
```

## Configuration

Config is stored at `~/.config/task-cli/config.yaml`. A default config is created automatically on first run if the file doesn't exist.

## Running Tests

```bash
pytest test_task.py -v
```
