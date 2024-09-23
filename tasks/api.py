from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.security import django_auth
from datetime import timedelta
from django.utils import timezone
from .models import Task
from .schemas import TaskSchema, UpdateTaskSchema

api = NinjaAPI(auth=django_auth)

# POST creates a new task
@api.post("/tasks/", response={201: TaskSchema})
def add_task(request, data: TaskSchema):
    task = Task.objects.create(**data.dict())
    return task

# GET returns the tasks due in the next 30 days
@api.get("/tasks/", response=List[TaskSchema])
def get_tasks(request):
    now = timezone.now()
    tasks = Task.objects.filter(due_by__gte=now, due_by__lte=now + timedelta(days=30)).all()
    return tasks

# PUT updates a task by id
@api.put("/tasks/{task_id}/", response=TaskSchema)
def update_task(request, task_id: int, data: UpdateTaskSchema):
    task = get_object_or_404(Task, id=task_id)
    for attr, value in data.dict().items():
        if value is not None:
            setattr(task, attr, value)
    task.save()
    return task

# DELETE deletes a task by id
@api.delete("/tasks/{task_id}/", response={204: None})
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return 204, None