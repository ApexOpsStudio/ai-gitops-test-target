# Task CLI - Test Target for ai-gitops

A minimal Python CLI task manager used to test the [ai-gitops](https://github.com/scooke11/ai-gitops) workflow.

## What is this?

This is a **test target repository** - not a real project. It exists solely to validate that our AI-assisted bounty hunting workflow looks professional before we use it on real open-source projects.

## Installation

```bash
python task.py --help
```

## Usage

```bash
# Add a task
python task.py add "Buy groceries"

# List tasks
python task.py list

# Complete a task
python task.py done 1
```

### JSON Output

All commands support a `--json` flag for machine-readable output:

```bash
# Add a task with JSON output
python task.py add --json "Buy groceries"
# {"success": true, "message": "Added task 1", "task": {"id": 1, "description": "Buy groceries", "done": false}}

# List tasks in JSON format
python task.py list --json
# {"success": true, "tasks": [{"id": 1, "description": "Buy groceries", "done": false}]}

# Mark done with JSON output
python task.py done --json 1
# {"success": true, "message": "Marked task 1 as done", "task": {"id": 1, "description": "Buy groceries", "done": true}}
```

## Testing

```bash
python -m pytest test_task.py
```

## Configuration

Copy `config.yaml.example` to `~/.config/task-cli/config.yaml` and customize.
