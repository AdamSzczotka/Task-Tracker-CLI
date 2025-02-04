# Autor: Adam Szczotka
# Title: Task Tracker CLI

import json
import os
from datetime import datetime


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


def main():
    pass


if __name__ == "__main__":
    main()
