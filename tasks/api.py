from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from datetime import timedelta
from django.utils import timezone
from .models import Task
from .schemas import TaskSchema, UpdateTaskSchema
from asgiref.sync import sync_to_async
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

api = NinjaAPI()

# funciton that allows authentication in an async setting
async def async_auth(request):
    session_key = request.COOKIES.get("sessionid")

    if session_key:
        session = await sync_to_async(Session.objects.get)(session_key=session_key)
        user_id = session.get_decoded().get("_auth_user_id")
        if user_id:
            user = await sync_to_async(User.objects.get)(id=user_id)
            return user
    
    return None

# POST creates a new task
@api.post("/tasks/", response={201: TaskSchema}, auth=async_auth)
async def add_task(request, data: TaskSchema):
    task = Task.objects.acreate(**data.dict())
    return task

# GET returns the tasks due in the next 30 days
@api.get("/tasks/", response=List[TaskSchema], auth=async_auth)
async def get_tasks(request):
    now = timezone.now()
    tasks = Task.objects.filter(due_by__gte=now,
        due_by__lte=now + timedelta(days=30)).all()
    return tasks

# PUT updates a task by id
@api.put("/tasks/{task_id}/", response=TaskSchema, auth=async_auth)
async def update_task(request, task_id: int, data: UpdateTaskSchema):
    task = get_object_or_404(Task, id=task_id)
    for attr, value in data.dict().items():
        if value is not None:
            setattr(task, attr, value)
    task.save()
    return task

# DELETE deletes a task by id
@api.delete("/tasks/{task_id}/", response={204: None}, auth=async_auth)
async def delete_task(request, task_id: int):
    try:
        task = await Task.objects.aget(id=task_id)
        await task.adelete()
    except Task.DoesNotExist:
        return 404, {"error": "Task not found"}