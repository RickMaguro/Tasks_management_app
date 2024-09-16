from typing import List
from ninja import NinjaAPI
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Task
from .schema import TaskSchema, TasksByDateSchema, TasksByPrioritySchema, UrgentTasksSchema

api = NinjaAPI()

@api.post("/tasks/", response={201: TaskSchema})
def add_task(request, data: TaskSchema):
    task = Task.objects.create(**data.dict())
    return task

@api.get("/tasks/due_dates/", response=List[TasksByDateSchema])
def get_tasks_due_date(request):
    now = datetime.now()
    tasks_due_dates = Task.objects.filter(due_by__gte=now, due_by__lte=now + timedelta(days=30)) \
                                  .annotate(date=TruncDate('due_by')) \
                                  .values('date') \
                                  .annotate(count=Count('id')) \
                                  .order_by('date')
    return tasks_due_dates

@api.get("/tasks/priority/", response=List[TasksByPrioritySchema])
def get_tasks_priority(request):
    now = datetime.now()
    task_count_by_priority = Task.objects.filter(due_by__gte=now, due_by__lte=now + timedelta(days=30)) \
                                         .values('priority') \
                                         .annotate(count=Count('id'))
    return task_count_by_priority

@api.get("/tasks/urgent/", response=UrgentTasksSchema)
def get_urgent_tasks(request):
    now = datetime.now()
    count = Task.objects.filter(is_urgent=True, due_by__gte=now, due_by__lte=now + timedelta(days=30)).count()
    return {"count": count}