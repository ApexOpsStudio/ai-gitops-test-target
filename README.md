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

The CLI creates `~/.config/task-cli/config.yaml` from `config.yaml.example` on first use. Edit that generated file to customize settings.
