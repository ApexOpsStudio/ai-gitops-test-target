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

# JSON output (for scripting and automation)
python task.py --json add "Buy groceries"
python task.py --json list
python task.py --json done 1
```

### JSON Output Format

When using the `--json` flag, all commands return a consistent JSON envelope:

```json
{
  "success": true,
  "message": "Added task 1",
  "data": {"id": 1, "description": "Buy groceries", "done": false}
}
```

## Testing

```bash
python -m pytest test_task.py
```

## Configuration

Copy `config.yaml.example` to `~/.config/task-cli/config.yaml` and customize.
