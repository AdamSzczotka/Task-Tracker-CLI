# Autor: Adam Szczotka
# Title: Task Tracker CLI

import json
import os
from datetime import datetime
from tabulate import tabulate
import argparse


class Task:
    """
    Represents a single task in the task tracker.

    Attributes:
        id (int): Unique identifier for the task
        description (str): Description of the task
        status (str): Current status ('todo', 'in-progress', 'done')
        createdAt (str): Timestamp when the task was created
        updatedAt (str): Timestamp when the task was last updated
    """
    def __init__(self, id, description, status, createdAt, updatedAt):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def to_dict(self):
        """Convert task object to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary."""
        return cls(
            id=data["id"],
            description=data["description"],
            status=data["status"],
            createdAt=data["createdAt"],
            updatedAt=data["updatedAt"]
        )


class TaskManager:
    """
    Manages task operations and persistence.

    This class handles all operations related to tasks including
    CRUD operations and file storage management.
    """
    def __init__(self, storage_path=None):
        """
        Initialize TaskManager with a storage path.

        Args:
            storage_path (str, optional): Directory path for tasks.json.
                                        Defaults to current directory.
        """
        if storage_path is None:
            storage_path = os.getcwd()

        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)

        self.filepath = os.path.join(storage_path, "tasks.json")
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                return [Task.from_dict(task_data) for task_data in data]
        except json.JSONDecodeError:
            return []
        except IOError as e:
            print(f"Error accessing file: {e}")
            return []

    def save_tasks(self):
        """Save all tasks to the JSON file."""
        try:
            with open(self.filepath, 'w') as file:
                json.dump([task.to_dict() for task in self.tasks], file,
                          indent=2)
        except IOError as e:
            print(f"Error accessing file: {e}")
            return []

    def get_next_id(self):
        """Generate the next available task ID."""
        return max([task.id for task in self.tasks], default=0) + 1

    def add_task(self, description):
        """
        Add a new task.

        Args:
            description (str): Task description

        Returns:
            int: ID of the newly created task
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        task = Task(
            id=self.get_next_id(),
            description=description,
            status="todo",
            createdAt=now,
            updatedAt=now
        )

        self.tasks.append(task)
        self.save_tasks()
        return task.id

    def update_task(self, task_id, description):
        """
        Update an existing task's description.
        
        Args:
            task_id (int): ID of the task to update
            description (str): New task description
            
        Returns:
            bool: True if task was updated, False if not found
        """
        task = self.get_next_id(task_id)

        if task:
            task.description = description
            task.updateAt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id):
        """
        Delete a task by ID.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            bool: True if task was deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False

    def mark_task(self, task_id, status):
        task = self.get_next_id(task_id)

        if task:
            task.status = status
            task.updateAt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.save_tasks()
            return True
        return False

    def get_task_by_id(self, task_id):
        return next((task for task in self.tasks if task.id == task_id), None)

    def list_tasks(self, status=None):
        if status:
            return [task for task in self.tasks if task.status == status]
        return self.tasks


def print_tasks(tasks):
    if not tasks:
        print("No tasks found")
        return

    headers = ["Id", "Description", "Status", "Created At", "Updated At"]
    table_data = [
        [task.id, task.description, task.status, task.createdAt,
         task.updatedAt]
        for task in tasks
    ]

    print(tabulate(table_data, headers=headers, tablefmt="double_grid"))


def setup_parser():
    parser = argparse.ArgumentParser(description='Task Tracker CLI')
    parser.add_argument('--storage-path',
                        help='Path to store the tasks.json file',
                        default=os.getcwd())

    subparsers = parser.add_subparsers(dest='command',
                                       help='Available commands')

    # Add task
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')

    # Update task
    update_parser = subparsers.add_parser('update',
                                          help='Update an existing task')
    update_parser.add_argument('id', type=int, help='Task ID')
    update_parser.add_argument('description', help='New task description')

    # Delete task
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID')

    # Mark in progress
    progress_parser = subparsers.add_parser('mark-in-progress',
                                            help='Mark a task as in progress')
    progress_parser.add_argument('id', type=int, help='Task ID')

    # Mark done
    done_parser = subparsers.add_parser('mark-done',
                                        help='Mark a task as done')
    done_parser.add_argument('id', type=int, help='Task ID')

    # List tasks
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('status', nargs='?',
                             choices=['todo', 'in-progress', 'done'],
                             help='Filter tasks by status')

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = TaskManager(args.storage_path)

    try:
        if args.command == 'add':
            task_id = manager.add_task(args.description)
            print(f"Task added successfully (IDL {task_id})")
            print_tasks([manager.get_task_by_id(task_id)])

        elif args.command == 'update':
            if manager.update_task(args.id, args.description):
                print("Task updated successfully")
                print_tasks([manager.get_task_by_id(args.id)])
            else:
                print("Task not found")

        elif args.command == 'delete':
            if manager.delete_task(args.id):
                print("Task deleted successfully")
            else:
                print("Task not found")

        elif args.command == 'mark-in-progress':
            if manager.mark_task(args.id, "in-progress"):
                print("Task marked as in progress")
                print_tasks([manager.get_task_by_id(args.id)])
            else:
                print("Task not found")

        elif args.command == 'mark-done':
            if manager.mark_task(args.id, "done"):
                print("Task marked as done")
                print_tasks([manager.get_task_by_id(args.id)])
            else:
                print("Task not found")

        elif args.command == 'list':
            tasks = manager.list_tasks(args.status)
            print_tasks(tasks)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    main()
