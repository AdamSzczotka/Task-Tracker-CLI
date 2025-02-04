# Autor: Adam Szczotka
# Title: Task Tracker CLI

import json
import os
from datetime import datetime
import tabulate
import argparse


class Task:
    def __init__(self, id, description, status, createdAt, updatedAt):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    # Instance method
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            description=data["description"],
            status=data["status"],
            createdAt=data["createdAt"],
            updatedAt=data["updatedAt"]
        )


class TaskManager:
    def __init__(self, storage_path=None):

        if storage_path is None:
            storage_path = os.getcwd()

        os.makedirs(storage_path, exist_ok=True)

        self.filepath = os.path.join(storage_path, "tasks.json")
        self.tasks = self.load_tasks()

    def load_tasks(self):
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
        try:
            with open(self.filepath, 'w') as file:
                json.dump([task.to_dict() for task in self.tasks], file,
                          indent=2)
        except IOError as e:
            print(f"Error accessing file: {e}")
            return []

    def get_next_id(self):
        return max([task.id for task in self.tasks], default=0) + 1

    def add_task(self, description):
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
        task = self.get_next_id(task_id)

        if task:
            task.description = description
            task.updateAt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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

    print(tabulate(table_data, headers=headers, tablemft="double_grid"))


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
    pass


if __name__ == "__main__":
    main()
