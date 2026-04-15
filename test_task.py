"""Basic tests for task CLI."""

import json
import sys
import pytest
from io import StringIO
from pathlib import Path
from commands.add import add_task, validate_description
from commands.done import validate_task_id, mark_done
from commands.list import list_tasks


def test_validate_description():
    """Test description validation."""
    assert validate_description("  test  ") == "test"

    with pytest.raises(ValueError):
        validate_description("")

    with pytest.raises(ValueError):
        validate_description("x" * 201)


def test_validate_task_id():
    """Test task ID validation."""
    tasks = [{"id": 1}, {"id": 2}]
    assert validate_task_id(tasks, 1) == 1

    with pytest.raises(ValueError):
        validate_task_id(tasks, 0)

    with pytest.raises(ValueError):
        validate_task_id(tasks, 99)


class TestJSONOutput:
    """Tests for --json flag output."""

    def test_add_task_json_output(self, tmp_path, monkeypatch):
        """Test add_task outputs valid JSON when json_output=True."""
        tasks_file = tmp_path / "tasks.json"
        monkeypatch.setattr("commands.add.get_tasks_file", lambda: tasks_file)

        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        result = add_task("Test task", json_output=True)
        output = captured.getvalue()

        # Verify valid JSON
        parsed = json.loads(output)
        assert parsed["id"] == 1
        assert parsed["description"] == "Test task"
        assert parsed["done"] is False
        assert result == parsed

    def test_list_tasks_json_output(self, tmp_path, monkeypatch):
        """Test list_tasks outputs valid JSON when json_output=True."""
        tasks_file = tmp_path / "tasks.json"
        tasks_file.write_text(json.dumps([
            {"id": 1, "description": "Task 1", "done": False},
            {"id": 2, "description": "Task 2", "done": True}
        ]))
        monkeypatch.setattr("commands.list.get_tasks_file", lambda: tasks_file)

        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        result = list_tasks(json_output=True)
        output = captured.getvalue()

        parsed = json.loads(output)
        assert len(parsed) == 2
        assert parsed[0]["id"] == 1
        assert parsed[1]["done"] is True
        assert result == parsed

    def test_list_tasks_json_empty(self, tmp_path, monkeypatch):
        """Test list_tasks outputs empty JSON array when no tasks."""
        monkeypatch.setattr("commands.list.get_tasks_file", lambda: None)

        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        result = list_tasks(json_output=True)
        output = captured.getvalue()

        parsed = json.loads(output)
        assert parsed == []
        assert result == []

    def test_mark_done_json_output(self, tmp_path, monkeypatch):
        """Test mark_done outputs valid JSON when json_output=True."""
        tasks_file = tmp_path / "tasks.json"
        tasks = [{"id": 1, "description": "Task 1", "done": False}]
        tasks_file.write_text(json.dumps(tasks))
        monkeypatch.setattr("commands.done.get_tasks_file", lambda: tasks_file)

        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        result = mark_done(1, json_output=True)
        output = captured.getvalue()

        parsed = json.loads(output)
        assert parsed["id"] == 1
        assert parsed["done"] is True
        assert result == parsed

    def test_mark_done_json_not_found(self, tmp_path, monkeypatch):
        """Test mark_done outputs error JSON when task not found."""
        tasks_file = tmp_path / "tasks.json"
        tasks_file.write_text(json.dumps([{"id": 1, "description": "Task 1", "done": False}]))
        monkeypatch.setattr("commands.done.get_tasks_file", lambda: tasks_file)

        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        result = mark_done(99, json_output=True)
        output = captured.getvalue()

        parsed = json.loads(output)
        assert "error" in parsed
        assert result is None


class TestConfigHandling:
    """Tests for config file handling."""

    def test_load_config_creates_default(self, tmp_path, monkeypatch):
        """Test load_config creates default config when missing."""
        config_dir = tmp_path / ".config" / "task-cli"
        config_file = config_dir / "config.yaml"
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

        # Config doesn't exist yet
        assert not config_file.exists()

        from task import load_config
        result = load_config()

        # Config should now exist
        assert config_file.exists()
        assert "Task CLI Configuration" in result

    def test_load_config_returns_existing(self, tmp_path, monkeypatch):
        """Test load_config returns existing config content."""
        config_dir = tmp_path / ".config" / "task-cli"
        config_file = config_dir / "config.yaml"
        config_dir.mkdir(parents=True)
        config_file.write_text("json_output: true\n")
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

        from task import load_config
        result = load_config()

        assert "json_output: true" in result

    def test_no_crash_without_config(self, tmp_path, monkeypatch):
        """Test app doesn't crash when config file is missing."""
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

        from task import load_config
        # Should not raise FileNotFoundError
        result = load_config()
        assert result is not None
        assert len(result) > 0


class TestMarkDoneEdgeCases:
    """Additional mark_done edge case tests."""

    def test_mark_done_json_no_tasks(self, tmp_path, monkeypatch):
        """Test mark_done outputs error JSON when no tasks file."""
        tasks_file = tmp_path / "nonexistent.json"
        monkeypatch.setattr("commands.done.get_tasks_file", lambda: tasks_file)

        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)

        result = mark_done(1, json_output=True)
        output = captured.getvalue()

        parsed = json.loads(output)
        assert "error" in parsed
        assert result is None
