"""Basic tests for task CLI."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from utils.validation import validate_description, validate_task_id
from task import load_config
from commands.add import add_task
from commands.list import list_tasks
from commands.done import mark_done


def test_validate_description():
    assert validate_description("  test  ") == "test"
    with pytest.raises(ValueError):
        validate_description("")
    with pytest.raises(ValueError):
        validate_description("x" * 201)


def test_validate_task_id():
    tasks = [{"id": 1}, {"id": 2}]
    assert validate_task_id(tasks, 1) == 1
    with pytest.raises(ValueError):
        validate_task_id(tasks, 0)
    with pytest.raises(ValueError):
        validate_task_id(tasks, 99)


def test_load_config_missing_file(tmp_path):
    with patch("task.Path.home", return_value=tmp_path):
        result = load_config()
    assert "version: 1" in result
    assert (tmp_path / ".config" / "task-cli" / "config.yaml").exists()


def test_load_config_existing_file(tmp_path):
    config_dir = tmp_path / ".config" / "task-cli"
    config_dir.mkdir(parents=True)
    (config_dir / "config.yaml").write_text("version: 2\n")
    with patch("task.Path.home", return_value=tmp_path):
        result = load_config()
    assert "version: 2" in result


def test_add_task_json_output(tmp_path, capsys):
    with patch("utils.paths.Path.home", return_value=tmp_path):
        add_task("test task", output_json=True)
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["description"] == "test task"
    assert data["done"] == False
    assert "id" in data


def test_list_tasks_json_output(tmp_path, capsys):
    with patch("utils.paths.Path.home", return_value=tmp_path):
        add_task("task one")
        add_task("task two")
        list_tasks(output_json=True)
    captured = capsys.readouterr()
    # last line is the JSON from list_tasks
    lines = [l for l in captured.out.strip().split("\n") if l.startswith("[")]
    data = json.loads(lines[-1])
    assert len(data) == 2
    assert data[0]["description"] == "task one"


def test_list_tasks_empty_json(tmp_path, capsys):
    with patch("utils.paths.Path.home", return_value=tmp_path):
        list_tasks(output_json=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == "[]"
