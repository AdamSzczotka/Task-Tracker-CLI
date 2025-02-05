# Task Tracker CLI
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A command-line task management tool built in Python. Efficiently track your todos, work-in-progress items, and completed tasks directly from your terminal.

Project inspired by [Roadmap.sh Task Tracker Project](https://roadmap.sh/projects/task-tracker)

## Features
- ✨ Simple and intuitive CLI interface
- 📝 Create, update, and delete tasks
- 🔄 Track task status (todo/in-progress/done)
- 📊 View tasks in formatted tables
- 💾 Persistent JSON storage
- 🔍 Filter tasks by status
- 📁 Configurable storage location

## Installation

```bash
# Clone the repository
git clone https://github.com/AdamSzczotka/Task-Tracker-CLI.git

# Navigate to directory
cd Task-Tracker-CLI

# Install the package
pip install .
```

## Usage

### Task Management
```bash
# Add a new task
task_cli add "Finish CS50P"

# Update task
task_cli update 2 "Finish CS50P"

# Delete task
task_cli delete 1

# Mark as in-progress
task_cli mark-in-progress 1

# Mark as done
task_cli mark-done 1
```

### Task Listing
```bash
# List all tasks
task_cli list

# Filter by status
task_cli list todo
task_cli list in-progress
task_cli list done
```

### Custom Storage
```bash
task_cli --storage-path /custom/path add "New task"
```

## Development Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest test.py
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Author
Adam Szczotka - [GitHub](https://github.com/AdamSzczotka)

Project Link: [https://github.com/AdamSzczotka/Task-Tracker-CLI](https://github.com/AdamSzczotka/Task-Tracker-CLI)