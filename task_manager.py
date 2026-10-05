#task_manager.py
import os
import json
from datetime import datetime
from repository import DataRepository
from task_validation import TaskValidator
from models import Task
DATA_FILE = 'data.json'

class TaskManager:
    def __init__(self, data_file=DATA_FILE):
        self.data_repo = DataRepository()
        self.data_file = data_file
    
    def add_task(self, title, description, priority, due_date, tag, tasks):
        new_id = max((task.id for task in tasks), default=0) + 1
        new_task = Task(id = new_id, 
                        title = title, 
                        description = description,
                        priority=priority, 
                        due_date = due_date, 
                        tag = tag,
                        created_at = str(datetime.now().strftime("%Y-%m-%d")))

        tasks.append(new_task)
        self.data_repo.save_to_json(tasks)    
    
    def edit_task(self, id, title, description, priority, due_date, tag,  tasks):
        task = self.find_task(tasks, id)
        if not task:
            return("task not found"), False
        valid_title , check = TaskValidator.get_valid_title(user_input=title)   
        if not check:
            return valid_title , check

        valid_due_date, check = TaskValidator.get_valid_due_date(due_date)
        if not check:
            return valid_due_date , check
        
        task.title = valid_title
        task.description = description
        task.priority = priority
        task.tag = tag
        task.due_date = valid_due_date
        self.data_repo.save_to_json(tasks)
        return "" , True

    def delete_task(self, task_to_delete, tasks):      
        tasks.remove(task_to_delete)
        # self.reindexing_id(tasks)
        # Save the updated list of tasks back to the JSON file
        self.data_repo.save_to_json(tasks = tasks)

    # Imports tasks from a user-specified JSON file into the main data file.
    def import_tasks(self, json_file_path="import.json"):
            # Check if the specified file exists.
            if not os.path.isfile(json_file_path):
                return (f"Error: File '{json_file_path}' not found."), False
            try:
                new_tasks_data = self.data_repo.load_from_json(file_path = json_file_path)
                valid_new_tasks = []
                for item in new_tasks_data:
                    # Check if the item is a Task model
                    if isinstance(item, Task):
                        valid_new_tasks.append(item)
                    else:
                        # Print a warning for invalid items.
                        return(f"Warning: Skipping invalid item in '{json_file_path}': {item}. Must be an object with a 'title'."), False
                # If no valid tasks were found, inform the user and stop the import process.
                if not valid_new_tasks:
                    return(f"No valid tasks found in '{json_file_path}' to import."), False
                    

                # Load the tasks that are already in the main data file.
                current_tasks = self.data_repo.load_from_json(DATA_FILE)
                # Determine the next ID based on the current maximum ID in DATA_FILE
                if current_tasks:
                    last_id = max(task.id for task in current_tasks if task.id is not None)
                else:
                    last_id = 0

                # Append new tasks with updated IDs
                for task in valid_new_tasks:
                    last_id += 1
                    task.id = last_id
                    current_tasks.append(task)

                # Save the updated list of tasks back to the main data file.
                self.data_repo.save_to_json(current_tasks, DATA_FILE)
                return "", True
            except FileNotFoundError:
                return(f"Error: File '{json_file_path}' not found during read attempt."), False
            except json.JSONDecodeError:
                return(f"Error: Could not decode JSON from '{json_file_path}'. Please ensure it's valid JSON."), False
            except Exception as e:
                return(f"An unexpected error occurred during import: {e}"), False

    # Exports all current tasks to a specified JSON file.
    def export_tasks(self, export_file_name="export.json"):
        current_tasks = self.data_repo.load_from_json(DATA_FILE)
        if not current_tasks:
            return("No tasks found to export."), False

        try:
            # Ensure the export file name ends with .json
            if not export_file_name.lower().endswith(".json"):
                export_file_name += ".json"

            self.data_repo.save_to_json(current_tasks, export_file_name)
            return(f" Successfully exported {len(current_tasks)} tasks to '{export_file_name}'."), True
        except Exception as e:
            return(f"An error occurred during export to '{export_file_name}': {e}"), False

    # def reindexing_id(self, tasks):
    #     for i, task in enumerate(tasks, start=1):
    #         task.id = i

    def find_task(self, tasks, task_id):
        for task in tasks:
            if task.id == task_id: 
                return task
        return None
                
    def sort_tasks(self, sort_key, tasks):
        if sort_key == "status":
            tasks.sort(key=lambda x: (not x.active, x.id))
        elif sort_key == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            tasks.sort(key=lambda x: priority_order.get(x.priority, 3)) 
        return tasks

    def search_task(self, tasks, search_text):
        filtered_tasks = []
        for task in tasks:
            title_matches = task.title is not None and search_text in task.title
            tag_matches = task.tag is not None and search_text in task.tag
            if title_matches or tag_matches:
                filtered_tasks.append(task)   
        return filtered_tasks                 