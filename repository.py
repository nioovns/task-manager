#repository.py
import json
import os
from typing import List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict 
from models import Task 

DATA_FILE = 'data.json'

class DataRepository:
    def __init__(self):
        pass

    # Loads tasks from the JSON file 
    def load_from_json(self, file_path: str = DATA_FILE) -> List[Task]:
        try:
            # Open and read the JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validate that the loaded data is a list.
                if not isinstance(data, list):
                    print(f"Warning: '{file_path}' did not contain a valid list. Returning empty list.")
                    return [] 
                # Use Task.from_dict to convert each item to a Task object
                return [Task.from_dict(item) for item in data]
        # Handle file not found specifically, though os.path.isfile should catch it.
        except FileNotFoundError:
            print(f"Info: Data file '{file_path}' not found. Starting with an empty list.")
            return [] 
        # Handle errors during JSON decoding
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{file_path}'. File might be corrupted. Returning empty list.")
            return []
        # Catch any other unexpected exceptions during file loading.
        except Exception as e:
            print(f"An error occurred while loading tasks from '{file_path}': {e}. Returning empty list.")
            return []

    # Saves tasks to a JSON file
    def save_to_json(self, tasks: List[Task], file_path: str = DATA_FILE):
        # Convert list of Task objects to a list of dictionaries using task.to_dict()
        data_to_save = [task.to_dict() for task in tasks]
        try:
            # Open the file in write mode
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        # Catch file I/O errors
        except IOError as e:
            print(f"Error: Could not write to file '{file_path}'. Reason: {e}")
        # Catch any other unexpected exceptions during the saving process.
        except Exception as e:
            print(f"An unexpected error occurred while saving tasks to '{file_path}': {e}")
