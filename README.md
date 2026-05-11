# Task CLI - Test Target for ai-gitops

A minimal Python CLI task manager used to test the [ai-gitops](https://github.com/scooke11/ai-gitops) workflow.

## What is this?

This is a **test target repository** - not a real project. It exists solely to validate that our AI-assisted bounty hunting workflow looks professional before we use it on real open-source projects.

## Installation

```bash
python task.py --help
```

## Usage

### Human-readable output (default)

```bash
# Add a task
python task.py add "Buy groceries"

# List tasks
python task.py list

# Complete a task
python task.py done 1
```

### JSON output (for scripting/automation)

```bash
# Add a task (JSON output)
python task.py --json add "Buy groceries"

# List tasks (JSON output)
python task.py --json list

# Complete a task (JSON output)
python task.py --json done 1
```

**Note:** The `--json` flag must come **before** the subcommand.

### JSON Output Format

All commands with `--json` output valid JSON:

```json
{
  "success": true,
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "done": false
    }
  ],
  "count": 1
}
```

## Testing

```bash
python -m pytest test_task.py
```

## Configuration

Copy `config.yaml.example` to `~/.config/task-cli/config.yaml` and customize.
