import json
import os
import shutil
import tempfile
import unittest

from models import Task
from repository import DataRepository
from task_manager import TaskManager


DATA_FILE = "tasks.json"


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        self.data_file_path = os.path.join(
            self.test_dir,
            DATA_FILE
        )

        self.initial_tasks_data = [
            {
                "id": 1,
                "title": "shop",
                "description": "go to mall",
                "due_date": "2024-12-31",
                "priority": "high",
                "created_at": "2024-01-01",
                "tag": "personal",
                "active": True
            },
            {
                "id": 2,
                "title": "project",
                "description": "working on project",
                "due_date": "2024-07-15",
                "priority": "high",
                "created_at": "2024-01-01",
                "tag": "work",
                "active": True
            },
            {
                "id": 3,
                "title": "python",
                "description": "learning python",
                "due_date": "2024-08-01",
                "priority": "low",
                "created_at": "2024-01-01",
                "tag": "study",
                "active": True
            }
        ]

        with open(
            self.data_file_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.initial_tasks_data,
                file,
                ensure_ascii=False,
                indent=4
            )

        self.task_manager = TaskManager(
            data_file=self.data_file_path
        )

        self.repository = DataRepository()

        self.all_tasks = self.repository.load_from_json(
            self.data_file_path
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_task(self):
        initial_count = len(self.all_tasks)

        message, success = self.task_manager.add_task(
            title="reading",
            description=None,
            priority="low",
            due_date=None,
            tag=None,
            tasks=self.all_tasks
        )

        self.assertTrue(success)
        self.assertEqual(message, "")
        self.assertEqual(
            len(self.all_tasks),
            initial_count + 1
        )

        added_task = self.task_manager.find_task(
            self.all_tasks,
            4
        )

        self.assertIsNotNone(added_task)
        self.assertEqual(
            added_task.title,
            "reading"
        )

        saved_tasks = self.repository.load_from_json(
            self.data_file_path
        )

        self.assertEqual(len(saved_tasks), 4)

    def test_add_task_with_invalid_title(self):
        message, success = self.task_manager.add_task(
            title="hi",
            description=None,
            priority="low",
            due_date=None,
            tag=None,
            tasks=self.all_tasks
        )

        self.assertFalse(success)

        self.assertEqual(
            message,
            "Task title must be at least 3 characters"
        )

    def test_add_task_with_invalid_priority(self):
        message, success = self.task_manager.add_task(
            title="reading",
            description=None,
            priority="invalid",
            due_date=None,
            tag=None,
            tasks=self.all_tasks
        )

        self.assertFalse(success)

    def test_edit_task(self):
        message, success = self.task_manager.edit_task(
            task_id=1,
            title="driving",
            description=None,
            priority="low",
            due_date=None,
            tag=None,
            tasks=self.all_tasks
        )

        self.assertTrue(success)
        self.assertEqual(message, "")

        task = self.task_manager.find_task(
            self.all_tasks,
            1
        )

        self.assertIsNotNone(task)
        self.assertEqual(task.title, "driving")
        self.assertEqual(task.description, None)
        self.assertEqual(task.priority, "low")

    def test_edit_task_with_short_title(self):
        message, success = self.task_manager.edit_task(
            task_id=1,
            title="hi",
            description=None,
            priority="low",
            due_date=None,
            tag=None,
            tasks=self.all_tasks
        )

        self.assertFalse(success)

        self.assertEqual(
            message,
            "Task title must be at least 3 characters"
        )

    def test_edit_task_with_empty_title(self):
        message, success = self.task_manager.edit_task(
            task_id=1,
            title="",
            description=None,
            priority="low",
            due_date=None,
            tag=None,
            tasks=self.all_tasks
        )

        self.assertFalse(success)

        self.assertEqual(
            message,
            "Task title cannot be empty"
        )

    def test_edit_task_with_invalid_date(self):
        message, success = self.task_manager.edit_task(
            task_id=1,
            title="driving",
            description=None,
            priority="low",
            due_date="2024-04-99",
            tag=None,
            tasks=self.all_tasks
        )

        self.assertFalse(success)

        self.assertEqual(
            message,
            "Date format is invalid. Please use YYYY-MM-DD."
        )

    def test_edit_task_not_found(self):
        message, success = self.task_manager.edit_task(
            task_id=99,
            title="driving",
            description=None,
            priority="low",
            due_date=None,
            tag=None,
            tasks=self.all_tasks
        )

        self.assertFalse(success)
        self.assertEqual(message, "Task not found")

    def test_delete_task(self):
        task = self.task_manager.find_task(
            self.all_tasks,
            1
        )

        initial_count = len(self.all_tasks)

        result = self.task_manager.delete_task(
            task,
            self.all_tasks
        )

        self.assertTrue(result)
        self.assertEqual(
            len(self.all_tasks),
            initial_count - 1
        )

        remaining_ids = [
            task.id
            for task in self.all_tasks
        ]

        self.assertEqual(
            remaining_ids,
            [2, 3]
        )

        saved_tasks = self.repository.load_from_json(
            self.data_file_path
        )

        self.assertEqual(len(saved_tasks), 2)

    def test_find_task(self):
        found_task = self.task_manager.find_task(
            self.all_tasks,
            1
        )

        self.assertIsNotNone(found_task)
        self.assertEqual(
            found_task.title,
            "shop"
        )

        not_found_task = self.task_manager.find_task(
            self.all_tasks,
            99
        )

        self.assertIsNone(not_found_task)

    def test_sort_tasks_by_priority(self):
        sorted_tasks = self.task_manager.sort_tasks(
            sort_key="priority",
            tasks=self.all_tasks
        )

        self.assertEqual(
            sorted_tasks[0].priority,
            "high"
        )

        self.assertEqual(
            sorted_tasks[1].priority,
            "high"
        )

        self.assertEqual(
            sorted_tasks[2].priority,
            "low"
        )

    def test_sort_tasks_by_status(self):
        self.all_tasks[0].active = False

        sorted_tasks = self.task_manager.sort_tasks(
            sort_key="status",
            tasks=self.all_tasks
        )

        self.assertTrue(sorted_tasks[0].active)
        self.assertFalse(sorted_tasks[-1].active)

    def test_search_task_by_title(self):
        results = self.task_manager.search_task(
            self.all_tasks,
            "py"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 3)
        self.assertEqual(results[0].title, "python")

    def test_search_task_case_insensitive(self):
        results = self.task_manager.search_task(
            self.all_tasks,
            "PYTHON"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "python")

    def test_search_task_by_tag(self):
        results = self.task_manager.search_task(
            self.all_tasks,
            "work"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 2)

    def test_search_task_with_no_results(self):
        results = self.task_manager.search_task(
            self.all_tasks,
            "nnnn"
        )

        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()