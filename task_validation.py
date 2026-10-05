#task_validation.py
from datetime import datetime

class TaskValidator:
    VALID_PRIORITIES = ["low", "medium", "high"]
    VALID_STATUS = ["todo", "done"]
    
    @staticmethod
    def get_valid_due_date(user_input, current_value=None):
        if user_input:    
            try:
                validated_date = datetime.strptime(user_input, '%Y-%m-%d').strftime('%Y-%m-%d')
                return validated_date, True
            except ValueError:
                return("Date format is invalid. Please use YYYY-MM-DD."), False
        else:
            return None, True
        
    @staticmethod
    def get_valid_title(user_input, current_value=None, min_length=3):
        if not user_input:
            if current_value is not None:
                return current_value
            else:
                return ("Task title cannot be empty"), False
            
        if len(user_input) < min_length:
            return (f"Task title must be at least {min_length} characters"), False
        return user_input, True             


        while True:
            try:
                user_input = input(f"{prompt_message}: ").strip()
                if not user_input: 
                    print("Operation cancelled.")
                    return
                task_id = int(user_input) 
                return task_id
            except ValueError:
                print("Task ID must be a number.")

    @staticmethod
    def get_valid_priority(priority):
        if priority not in TaskValidator.VALID_PRIORITIES:
            return "Invalid priority.", False
        return priority, True
    
    @staticmethod
    def get_valid_status(status):
        if status not in TaskValidator.VALID_STATUS:
            return "Invalid status.", False
        return status, True