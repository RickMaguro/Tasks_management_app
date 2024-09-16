from ninja import Schema, ModelSchema
from .models import Task
from datetime import date

class TaskSchema(ModelSchema):
    class Meta:
        model = Task
        fields = ["user_email", "task", "due_by", "priority", "is_urgent"]

class TasksByDateSchema(Schema):
    date: date
    count: int

class TasksByPrioritySchema(Schema):
    priority: int
    count: int

class UrgentTasksSchema(Schema):
    count: int

class TaskNotFoundSchema(Schema):
    message: str