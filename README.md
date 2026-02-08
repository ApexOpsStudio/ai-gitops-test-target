# Task CLI

A simple task manager.

## Usage

```bash
./task.py add "Buy groceries"
./task.py list
./task.py done 1
```

## JSON output

All commands support `--json` for scripting and automation.

### Add

```bash
./task.py --json add "Buy groceries"
```

Example output:

```json
{
  "message": "Added task 1: Buy groceries",
  "success": true,
  "task": {
    "description": "Buy groceries",
    "done": false,
    "id": 1
  }
}
```

### List

```bash
./task.py --json list
```

Example output:

```json
{
  "success": true,
  "tasks": [
    {
      "description": "Buy groceries",
      "done": false,
      "id": 1
    }
  ]
}
```

### Done

```bash
./task.py --json done 1
```

Example output:

```json
{
  "message": "Marked task 1 as done: Buy groceries",
  "success": true,
  "task": {
    "description": "Buy groceries",
    "done": true,
    "id": 1
  }
}
```
