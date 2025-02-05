import pytest
import json
import os
from unittest.mock import mock_open, patch
from task_cli import Task, TaskManager


@pytest.fixture
def sample_task():
    """Fixture that returns a sample task instance."""
    return Task(1, "Test Task", "todo", "01/02/2025 10:00:00", "01/02/2025 10:00:00")


@pytest.fixture
def sample_task_data():
    """Fixture that returns a sample task as a dictionary."""
    return {
        "id": 1,
        "description": "Test Task",
        "status": "todo",
        "createdAt": "01/02/2025 10:00:00",
        "updatedAt": "01/02/2025 10:00:00",
    }


def test_task_to_dict(sample_task, sample_task_data):
    """Test conversion of a Task instance to a dictionary."""
    assert sample_task.to_dict() == sample_task_data


def test_task_from_dict(sample_task_data):
    """Test conversion from dictionary to Task instance."""
    task = Task.from_dict(sample_task_data)
    assert isinstance(task, Task)
    assert task.id == 1
    assert task.description == "Test Task"
    assert task.status == "todo"


@patch("builtins.open", new_callable=mock_open, read_data="[]")
@patch("os.path.exists", return_value=True)
def test_task_manager_load_tasks(mock_exists, mock_file):
    """Test that TaskManager loads tasks correctly when file exists."""
    manager = TaskManager("test_path")
    assert manager.tasks == []  # Should be empty as mock file contains "[]"


@patch("builtins.open", new_callable=mock_open)
def test_task_manager_save_tasks(mock_file, sample_task):
    """Test saving tasks to a file."""
    manager = TaskManager("test_path")
    manager.tasks = [sample_task]
    manager.save_tasks()

    # Verify that the file was opened in write mode
    mock_file.assert_called_with(os.path.join("test_path", "tasks.json"), "w")

    # Retrieve all `write()` calls and join their arguments into a single string
    written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)

    # Expected JSON data (without formatting, as `json.dump` may not always produce identical formatting)
    expected_data = json.dumps([sample_task.to_dict()], indent=2)

    # Verify that the entire written content matches the expected JSON data
    assert written_data == expected_data


@patch("builtins.open", new_callable=mock_open, read_data="[]")
@patch("os.path.exists", return_value=True)
def test_task_manager_add_task(mock_exists, mock_file):
    """Test adding a new task."""
    manager = TaskManager("test_path")
    task_id = manager.add_task("New Task")

    assert task_id == 1
    assert len(manager.tasks) == 1
    assert manager.tasks[0].description == "New Task"
    assert manager.tasks[0].status == "todo"


@patch("builtins.open", new_callable=mock_open, read_data="[]")
@patch("os.path.exists", return_value=True)
def test_task_manager_get_next_id(mock_exists, mock_file):
    """Test ID generation for new tasks."""
    manager = TaskManager("test_path")

    assert manager.get_next_id() == 1  # No tasks exist yet, should return 1

    # Add a task and check ID generation again
    manager.add_task("Sample Task")
    assert manager.get_next_id() == 2


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "description": "Old Task", "status": "todo", "createdAt": "01/02/2025 10:00:00", "updatedAt": "01/02/2025 10:00:00"}]')
@patch("os.path.exists", return_value=True)
def test_task_manager_update_task(mock_exists, mock_file):
    """Test updating an existing task."""
    manager = TaskManager("test_path")
    assert manager.update_task(1, "Updated Task") is True
    assert manager.get_task_by_id(1).description == "Updated Task"


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "description": "Task to Delete", "status": "todo", "createdAt": "01/02/2025 10:00:00", "updatedAt": "01/02/2025 10:00:00"}]')
@patch("os.path.exists", return_value=True)
def test_task_manager_delete_task(mock_exists, mock_file):
    """Test deleting a task."""
    manager = TaskManager("test_path")
    assert manager.delete_task(1) is True
    assert manager.get_task_by_id(1) is None


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "description": "Sample Task", "status": "todo", "createdAt": "01/02/2025 10:00:00", "updatedAt": "01/02/2025 10:00:00"}]')
@patch("os.path.exists", return_value=True)
def test_task_manager_list_tasks(mock_exists, mock_file):
    """Test listing tasks with and without filtering."""
    manager = TaskManager("test_path")

    # Check that list_tasks returns all tasks
    all_tasks = manager.list_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0].description == "Sample Task"

    # Check that filtering works correctly
    filtered_tasks = manager.list_tasks("todo")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0].status == "todo"

    filtered_tasks = manager.list_tasks("done")
    assert len(filtered_tasks) == 0  # No tasks marked as "done"
