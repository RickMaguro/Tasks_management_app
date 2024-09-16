from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from django.utils.timezone import now, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.conf import settings
import requests

def landing_page(request):
    return render(request, 'landing_page.html')

@login_required
def dashboard_page(request):
    api_base_url = settings.API_BASE_URL

    due_dates_response = requests.get(f"{api_base_url}/tasks/due_dates/")
    priority_response = requests.get(f"{api_base_url}/tasks/priority/")
    urgent_response = requests.get(f"{api_base_url}/tasks/urgent/")

    due_dates_response.raise_for_status()
    priority_response.raise_for_status()
    urgent_response.raise_for_status()

    tasks_due_dates = due_dates_response.json()
    task_count_by_priority = priority_response.json()
    urgent_tasks = urgent_response.json()

    context = {
        'tasks_due_dates': tasks_due_dates,
        'task_count_by_priority': task_count_by_priority,
        'urgent_tasks': urgent_tasks,
        'tasks': Task.objects.all(), 
    }
    return render(request, 'dashboard_page.html', context)