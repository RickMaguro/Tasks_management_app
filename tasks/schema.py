from ninja import Schema, ModelSchema
from .models import Task
from datetime import datetime

class TaskSchema(ModelSchema):
    class Meta:
        model = Task
        fields = ["user_email", "task", "due_by", "priority", "is_urgent"]

class TaskNotFoundSchema(Schema):
    message: str