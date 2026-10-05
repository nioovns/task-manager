from datetime import datetime

class TaskValidator:
    VALID_PRIORITIES = ["low", "medium", "high"]

    @staticmethod
    def get_valid_title(
        user_input,
        current_value=None,
        min_length=3
    ):
        if not user_input:
            if current_value is not None:
                return current_value, True

            return "Task title cannot be empty", False

        user_input = user_input.strip()

        if not user_input:
            return "Task title cannot be empty", False

        if len(user_input) < min_length:
            return (
                f"Task title must be at least {min_length} characters",
                False
            )

        return user_input, True

    @staticmethod
    def get_valid_due_date(
        user_input,
        current_value=None
    ):
        if not user_input:
            if current_value is not None:
                return current_value, True

            return None, True

        try:
            validated_date = datetime.strptime(
                user_input,
                "%Y-%m-%d"
            ).strftime("%Y-%m-%d")

            return validated_date, True

        except ValueError:
            return (
                "Date format is invalid. Please use YYYY-MM-DD.",
                False
            )

    @staticmethod
    def get_valid_priority(priority):
        if priority not in TaskValidator.VALID_PRIORITIES:
            return (
                "Priority must be low, medium, or high.",
                False
            )

        return priority, True