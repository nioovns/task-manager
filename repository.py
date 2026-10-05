import json
from typing import List
from models import Task

DATA_FILE = "data.json"

class DataRepository:

    def load_from_json(self, file_path: str = DATA_FILE) -> List[Task]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                print(
                    f"Warning: '{file_path}' does not contain a valid list."
                )
                return []

            return [
                Task.from_dict(item)
                for item in data
                if isinstance(item, dict)
            ]

        except FileNotFoundError:
            print(
                f"Info: Data file '{file_path}' not found. "
                f"Starting with an empty list."
            )
            return []

        except json.JSONDecodeError:
            print(
                f"Error: Could not decode JSON from '{file_path}'. "
                f"The file may be corrupted."
            )
            return []

    def save_to_json(
        self,
        tasks: List[Task],
        file_path: str = DATA_FILE
    ) -> bool:

        data_to_save = [
            task.to_dict()
            for task in tasks
        ]

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    data_to_save,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except OSError as error:
            print(
                f"Error: Could not write to '{file_path}'. "
                f"Reason: {error}"
            )
            return False