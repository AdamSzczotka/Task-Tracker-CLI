# Autor: Adam Szczotka
# Title: Task Tracker CLI

import json
import os


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


def main():
    pass


if __name__ == "__main__":
    main()
