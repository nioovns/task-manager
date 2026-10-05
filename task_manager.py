import os
from datetime import datetime

from models import Task
from repository import DataRepository, DATA_FILE
from task_validation import TaskValidator


class TaskManager:

    def __init__(self, data_file=DATA_FILE):
        self.data_repo = DataRepository()
        self.data_file = data_file

    def add_task(
        self,
        title,
        description,
        priority,
        due_date,
        tag,
        tasks
    ):
        valid_title, title_is_valid = (
            TaskValidator.get_valid_title(title)
        )

        if not title_is_valid:
            return valid_title, False

        valid_priority, priority_is_valid = (
            TaskValidator.get_valid_priority(priority)
        )

        if not priority_is_valid:
            return valid_priority, False

        valid_due_date, date_is_valid = (
            TaskValidator.get_valid_due_date(due_date)
        )

        if not date_is_valid:
            return valid_due_date, False

        new_id = max(
            (task.id for task in tasks),
            default=0
        ) + 1

        new_task = Task(
            id=new_id,
            title=valid_title,
            description=description,
            priority=valid_priority,
            due_date=valid_due_date,
            tag=tag,
            created_at=datetime.now().strftime("%Y-%m-%d")
        )

        tasks.append(new_task)

        self.data_repo.save_to_json(
            tasks,
            self.data_file
        )

        return "", True

    def edit_task(
        self,
        task_id,
        title,
        description,
        priority,
        due_date,
        tag,
        tasks
    ):
        task = self.find_task(tasks, task_id)

        if not task:
            return "Task not found", False

        valid_title, title_is_valid = (
            TaskValidator.get_valid_title(title)
        )

        if not title_is_valid:
            return valid_title, False

        valid_priority, priority_is_valid = (
            TaskValidator.get_valid_priority(priority)
        )

        if not priority_is_valid:
            return valid_priority, False

        valid_due_date, date_is_valid = (
            TaskValidator.get_valid_due_date(due_date)
        )

        if not date_is_valid:
            return valid_due_date, False

        task.title = valid_title
        task.description = description
        task.priority = valid_priority
        task.tag = tag
        task.due_date = valid_due_date

        self.data_repo.save_to_json(
            tasks,
            self.data_file
        )

        return "", True

    def delete_task(self, task_to_delete, tasks):
        if task_to_delete not in tasks:
            return False

        tasks.remove(task_to_delete)

        self.data_repo.save_to_json(
            tasks,
            self.data_file
        )

        return True

    def find_task(self, tasks, task_id):
        for task in tasks:
            if task.id == task_id:
                return task

        return None

    def sort_tasks(self, sort_key, tasks):
        if sort_key == "status":
            tasks.sort(
                key=lambda task: (
                    not task.active,
                    task.id
                )
            )

        elif sort_key == "priority":
            priority_order = {
                "high": 0,
                "medium": 1,
                "low": 2
            }

            tasks.sort(
                key=lambda task: (
                    priority_order.get(task.priority, 3),
                    task.id
                )
            )

        return tasks

    def search_task(self, tasks, search_text):
        search_text = search_text.strip().lower()

        if not search_text:
            return tasks.copy()

        filtered_tasks = []

        for task in tasks:
            title_matches = (
                task.title is not None
                and search_text in task.title.lower()
            )

            tag_matches = (
                task.tag is not None
                and search_text in task.tag.lower()
            )

            if title_matches or tag_matches:
                filtered_tasks.append(task)

        return filtered_tasks

    def import_tasks(self, json_file_path="import.json"):
        if not os.path.isfile(json_file_path):
            return (
                f"Error: File '{json_file_path}' not found.",
                False
            )

        imported_tasks = self.data_repo.load_from_json(
            json_file_path
        )

        if not imported_tasks:
            return (
                f"No valid tasks found in '{json_file_path}' to import.",
                False
            )

        current_tasks = self.data_repo.load_from_json(
            self.data_file
        )

        last_id = max(
            (task.id for task in current_tasks),
            default=0
        )

        for task in imported_tasks:
            last_id += 1
            task.id = last_id
            current_tasks.append(task)

        success = self.data_repo.save_to_json(
            current_tasks,
            self.data_file
        )

        if not success:
            return (
                "Could not save imported tasks.",
                False
            )

        return "", True

    def export_tasks(self, export_file_name="export.json"):
        current_tasks = self.data_repo.load_from_json(
            self.data_file
        )

        if not current_tasks:
            return (
                "No tasks found to export.",
                False
            )

        if not export_file_name.lower().endswith(".json"):
            export_file_name += ".json"

        success = self.data_repo.save_to_json(
            current_tasks,
            export_file_name
        )

        if not success:
            return (
                f"Could not export tasks to '{export_file_name}'.",
                False
            )

        return (
            f"Successfully exported "
            f"{len(current_tasks)} tasks to "
            f"'{export_file_name}'.",
            True
        )