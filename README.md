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

### JSON output

All commands support `--json` for scripting and automation:

```bash
python task.py add "Buy groceries" --json
python task.py list --json
python task.py done 1 --json
```

## Testing

```bash
python -m pytest test_task.py
```

## Configuration

On first run, the CLI creates a default config file at
`~/.config/task-cli/config.yaml` if it does not already exist. You can also copy
`config.yaml.example` to that path and customize it manually.
