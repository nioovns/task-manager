#models.py
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict

@dataclass
class Task:
    id: int
    title: str
    priority: str
    created_at: str
    description: str | None = None
    due_date: str | None = None
    tag: str | None = None
    active: bool = True
    
    def to_dict(self) -> dict:
        data = asdict(self)
        return data

    @staticmethod
    def from_dict(data: dict) -> 'Task':
        return Task(
            id=data['id'],
            title=data['title'],
            priority=data['priority'],
            created_at=data.get('created_at', None), 
            description=data.get('description', None),
            due_date=data.get('due_date', None),
            tag=data.get('tag', None),
            active=data.get('active', True)
        )

    def display_info(self) -> str:
        task_dict = self.to_dict()
        task_dict['status'] = "todo" if self.active else "done"
        return json.dumps(task_dict, indent=4, ensure_ascii=False)
