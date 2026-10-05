# Task Manager

A desktop task management application built with **Python and PyQt6**.

The application allows users to create, edit, delete, search, sort, and manage tasks while keeping data persistent through JSON files. It also supports task import/export and includes automated unit tests for the core application logic.

## Features

* Create, edit, and delete tasks
* Set task priority: `low`, `medium`, or `high`
* Add descriptions, tags, and due dates
* Mark tasks as active or completed
* Search tasks by title or tag
* Case-insensitive search
* Sort tasks by priority or status
* Validate task titles, priorities, and due dates
* Persist tasks using JSON
* Import tasks from JSON files
* Export tasks to JSON files
* Light and dark themes
* Automated unit testing

## Architecture

The project follows a simple **layered architecture** that separates presentation, business logic, validation, data access, and the domain model.

```text
┌──────────────────────┐
│      PyQt6 GUI       │
│   Presentation Layer │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     TaskManager      │
│   Business Logic     │
└───────┬────────┬─────┘
        │        │
        ▼        ▼
┌────────────┐  ┌────────────────┐
│   Task     │  │ TaskValidator  │
│   Model    │  │   Validation   │
└────────────┘  └────────────────┘
        │
        ▼
┌──────────────────────┐
│   DataRepository     │
│   Data Access Layer  │
└──────────┬───────────┘
           │
           ▼
      ┌──────────┐
      │ JSON     │
      │ Storage  │
      └──────────┘
```

### Main Components

| Component            | Responsibility                          |
| -------------------- | --------------------------------------- |
| `main_gui.py`        | Application entry point and GUI         |
| `task_manager.py`    | Core business logic and task operations |
| `task_validation.py` | Input validation                        |
| `repository.py`      | JSON data persistence                   |
| `models.py`          | `Task` domain model                     |
| `tests.py`           | Automated unit tests                    |

This separation improves **readability, maintainability, and testability** while keeping the core logic independent from the GUI and storage implementation.

## Project Structure

```text
task-manager/
│
├── main_gui.py
├── models.py
├── repository.py
├── task_manager.py
├── task_validation.py
├── tests.py
│
├── data.json
├── import.json
├── theme.txt
├── requirements.txt
├── .gitignore
└── README.md
```

## Task Model

Each task is represented by the `Task` dataclass.

| Field         | Type          | Description                |
| ------------- | ------------- | -------------------------- |
| `id`          | `int`         | Unique task identifier     |
| `title`       | `str`         | Task title                 |
| `description` | `str \| None` | Optional description       |
| `priority`    | `str`         | `low`, `medium`, or `high` |
| `due_date`    | `str \| None` | Optional due date          |
| `tag`         | `str \| None` | Optional task tag          |
| `created_at`  | `str`         | Task creation date         |
| `active`      | `bool`        | Task completion status     |

Tasks are converted to dictionaries for JSON persistence and reconstructed as `Task` objects when loaded.

## Data Validation

User input is validated before tasks are created or updated.

Current validation includes:

* Task titles cannot be empty.
* Task titles must meet a minimum length.
* Priority must be one of:

  * `low`
  * `medium`
  * `high`
* Due dates must follow the `YYYY-MM-DD` format.

## Data Persistence

Task data is stored in JSON format.

The `DataRepository` is responsible for:

* Loading tasks from JSON files
* Converting JSON data into `Task` objects
* Saving tasks to JSON
* Handling missing data files
* Handling invalid JSON data

If the main data file does not exist, the application starts with an empty task list.

## Import and Export

The application supports transferring tasks between JSON files.

### Import

Tasks can be imported from another JSON file.

Imported tasks receive new IDs to prevent conflicts with existing tasks.

### Export

The current task list can be exported to a JSON file for backup or transfer.

## Testing

The project includes automated unit tests covering the main business logic.

Test coverage includes:

* Task creation
* Invalid titles
* Invalid priorities
* Invalid due dates
* Task editing
* Task deletion
* Task lookup
* Sorting
* Searching
* Case-insensitive search
* JSON persistence

Run the test suite with:

```bash
python -m unittest tests.py -v
```

The current test suite contains **16 tests**.

## Technologies

* **Python 3.10+**
* **PyQt6**
* **JSON**
* **unittest**
* **Object-Oriented Programming**
* **Dataclasses**

## Installation

Clone the repository:

```bash
git clone https://github.com/nioovns/task-manager.git
cd task-manager
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Run the application:

```powershell
python main_gui.py
```

## Requirements

* Python 3.10 or higher
* PyQt6

## Future Improvements

Possible future improvements include:

* Database-backed persistence
* Task categories
* Recurring tasks
* Notifications and reminders
* Advanced filtering
* Additional automated tests
* More modular GUI components
* Improved logging and error handling

## What I Learned

This project provided practical experience with:

* Object-oriented programming in Python
* Dataclasses
* Layered application architecture
* Separation of concerns
* Input validation
* JSON-based data persistence
* CRUD operations
* Import/export workflows
* GUI development with PyQt6
* Automated unit testing
* Writing maintainable and testable application logic


## Contributors

- **Newsha Varnaseri** — Co-developer
- **Bahar Taheripour** — Co-developer