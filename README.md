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

# Machine-readable JSON output for scripting
python task.py add "Buy groceries" --json
python task.py list --json
python task.py done 1 --json
```

JSON responses use a consistent envelope:

```json
{
  "success": true,
  "message": "Added task 1: Buy groceries",
  "data": {
    "task": {
      "id": 1,
      "description": "Buy groceries",
      "done": false
    }
  }
}
```

For commands that return multiple tasks, the payload is available under `data.tasks`:

```bash
python task.py list --json
```

```json
{
  "success": true,
  "message": "Found 1 task",
  "data": {
    "tasks": [
      {
        "id": 1,
        "description": "Buy groceries",
        "done": false
      }
    ]
  }
}
```

## Testing

```bash
python -m pytest test_task.py
```

## Configuration

Copy `config.yaml.example` to `~/.config/task-cli/config.yaml` and customize.
