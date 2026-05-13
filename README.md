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

# Add a task and print machine-readable JSON
python task.py add "Buy groceries" --json
# {"task": {"id": 1, "description": "Buy groceries", "done": false}, "message": "Added task 1"}

# List tasks
python task.py list

# List tasks as JSON
python task.py list --json
# {"tasks": [{"id": 1, "description": "Buy groceries", "done": false}], "count": 1}

# Complete a task
python task.py done 1

# Complete a task and print JSON
python task.py done 1 --json
# {"task": {"id": 1, "description": "Buy groceries", "done": true}, "message": "Marked task 1 as done"}
```

## Testing

```bash
python -m pytest test_task.py
```

## Configuration

Copy `config.yaml.example` to `~/.config/task-cli/config.yaml` and customize.
