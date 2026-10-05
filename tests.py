#tests.py
import unittest
import os
import json
import tempfile
import shutil
from models import Task 
from task_manager import TaskManager
from repository import DataRepository

DATA_FILE = "tasks.json"

class TestTaskManagerRealFile(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.data_file_path = os.path.join(self.test_dir, DATA_FILE)

        self.initial_tasks_data = [
            {"id": 1, "title": "shop", "description": "go to mall", "due_date": "2024-12-31", "priority": "high"},
            {"id": 2, "title": "project", "description": "working on project", "due_date": "2024-07-15", "priority": "high"},
            {"id": 3, "title": "python", "description": "learning python", "due_date": "2024-08-01", "priority": "low"}
        ]

        with open(self.data_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.initial_tasks_data, f, ensure_ascii=False, indent=4)

        self.task_manager = TaskManager(data_file=self.data_file_path)
        self.rep = DataRepository()
        self.all_tasks = self.rep.load_from_json(file_path=self.data_file_path) 

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_task_persistence(self):
        initial_count = len(self.all_tasks)
        tasks = self.all_tasks
        self.task_manager.add_task(title = "reading", description = None, priority= "low", due_date = None, tag=None, tasks = tasks)
        secont_count = len(self.all_tasks)
        
        self.assertIsNotNone(self.all_tasks)
        self.assertEqual(initial_count + 1, secont_count)
        found_added_task = self.task_manager.find_task(tasks, secont_count)
        self.assertIsNotNone(found_added_task)
        self.assertEqual(found_added_task.title, "reading")

    def test_edit_task_persistence(self):
        task_id_to_edit = 1
        tasks = self.all_tasks
        edited_task_instance = self.task_manager.edit_task(task_id_to_edit, title = "driving", description = None, priority= "low", due_date = None, tag=None, tasks = tasks)
        self.assertTrue(edited_task_instance) 

        task_after_edit = self.task_manager.find_task(tasks, task_id_to_edit)
        self.assertIsNotNone(task_after_edit)
        self.assertEqual(task_after_edit.title, "driving")
        self.assertEqual(task_after_edit.description, None)
        
        edited_task_instance, check = self.task_manager.edit_task(task_id_to_edit, title = "hi", description = None, priority= "low", due_date = None, tag=None, tasks = tasks)
        self.assertEqual(check, False)
        self.assertEqual(edited_task_instance, "Task title must be at least 3 characters")
        
        
        edited_task_instance, check = self.task_manager.edit_task(task_id_to_edit, title = "", description = None, priority= "low", due_date = None, tag=None, tasks = tasks)
        self.assertEqual(check, False)
        self.assertEqual(edited_task_instance, "Task title cannot be empty")
        
        edited_task_instance, check = self.task_manager.edit_task(task_id_to_edit, title = "driving", description = None, priority= "low", due_date = "2024-04-09", tag=None, tasks = tasks)
        self.assertEqual(check, True)

        edited_task_instance, check = self.task_manager.edit_task(task_id_to_edit, title = "driving", description = None, priority= "low", due_date = "2024-04-99", tag=None, tasks = tasks)
        self.assertEqual(check, False)
        self.assertEqual(edited_task_instance, "Date format is invalid. Please use YYYY-MM-DD.")

    def test_delete_task_persistence(self):
        task_id_to_delete = 1
        tasks = self.all_tasks
        task_delete = self.task_manager.find_task(tasks, task_id_to_delete)
        title = task_delete.title
        initial_count = len(tasks)

        self.task_manager.delete_task(task_delete, self.all_tasks)
        self.assertEqual(len(self.all_tasks), initial_count - 1)

    def test_find_task(self):
        tasks = self.all_tasks
        found_task = self.task_manager.find_task(tasks, 1)
        self.assertIsNotNone(found_task)
        self.assertEqual(found_task.title, "shop")

        not_found_task = self.task_manager.find_task(tasks, 99)
        self.assertIsNone(not_found_task)

    def test_sort_tasks_by_priority(self):
        tasks = self.all_tasks
        sorted_tasks = self.task_manager.sort_tasks(sort_key='priority', tasks=tasks)

        self.assertEqual(sorted_tasks[0].priority, "high") 
        self.assertEqual(sorted_tasks[1].priority, "high") 
        self.assertEqual(sorted_tasks[2].priority, "low") 


    def test_search_task_by_keyword(self):
        tasks = self.all_tasks

        results = self.task_manager.search_task(tasks, "py")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 3)
        self.assertEqual(results[0].title, "python")

        no_results = self.task_manager.search_task(tasks, "nnnn")
        self.assertEqual(len(no_results), 0)



if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
