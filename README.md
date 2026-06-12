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

## Testing

```bash
python -m pytest test_task.py
```

## Configuration

The CLI looks for its config at `~/.config/task-cli/config.yaml`.

If the config file doesn't exist, it will be **automatically created** with sensible defaults:

```yaml
# Task CLI configuration
storage:
  format: json
  max_tasks: 1000

display:
  color: true
  unicode: true
```

You can also manually copy `config.yaml.example` to customize your settings.
