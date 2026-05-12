"""Output helpers for task CLI commands."""

import json
from typing import Any


def emit_json(payload: dict[str, Any]) -> None:
    """Print a stable, machine-readable JSON response."""
    print(json.dumps(payload, ensure_ascii=False))
