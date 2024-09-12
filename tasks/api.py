from ninja import NinjaAPI
from datetime import datetime
from .models import Task
from .schema import TaskSchema, TaskNotFoundSchema

api = NinjaAPI()

@api.post("/tasks/", response={201: TaskSchema})
def add_task(request, data: TaskSchema):
    task = Task.objects.create(**data.dict())
    return task
