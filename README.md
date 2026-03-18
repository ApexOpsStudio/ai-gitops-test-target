# Task CLI

A simple task manager for the command line.

## Usage

### Add a task
```bash
python task.py add "Buy groceries"
# Added task 1: Buy groceries
```

### List tasks
```bash
python task.py list
# [ ] 1. Buy groceries
# [✓] 2. Write docs
```

### Mark task as done
```bash
python task.py done 1
# Marked task 1 as done: Buy groceries
```

## JSON Output

All commands support a `--json` flag for scripting and automation:

### Add (JSON)
```bash
python task.py --json add "Deploy v2"
```
```json
{"status": "added", "task": {"id": 1, "description": "Deploy v2", "done": false}}
```

### List (JSON)
```bash
python task.py --json list
```
```json
{"tasks": [{"id": 1, "description": "Deploy v2", "done": false}], "count": 1}
```

### Done (JSON)
```bash
python task.py --json done 1
```
```json
{"status": "done", "task": {"id": 1, "description": "Deploy v2", "done": true}}
```

### Scripting example
```bash
# Add a task and capture the ID
TASK_ID=$(python task.py --json add "Run tests" | python -c "import sys,json; print(json.load(sys.stdin)['task']['id'])")

# Mark it done
python task.py --json done $TASK_ID

# List as JSON and pipe to jq
python task.py --json list | jq '.tasks[] | select(.done == false)'
```

## Configuration

Copy the example config:
```bash
mkdir -p ~/.config/task-cli
cp config.yaml.example ~/.config/task-cli/config.yaml
```

## Tests

```bash
pip install pytest
pytest test_task.py -v
```
