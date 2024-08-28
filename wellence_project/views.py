from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from django.utils.timezone import now, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate

def landing_page(request):
    return render(request, 'landing_page.html')

@login_required
def dashboard_page(request):
    # Group tasks by due date and count them, truncating to the date only
    tasks_due_dates = Task.objects.filter(due_by__gte=now(), due_by__lte=now() + timedelta(days=30)) \
                                  .annotate(date=TruncDate('due_by')) \
                                  .values('date') \
                                  .annotate(count=Count('id')) \
                                  .order_by('date')

    # Count tasks by priority within the next 30 days
    task_count_by_priority = Task.objects.filter(due_by__gte=now(), due_by__lte=now() + timedelta(days=30)) \
                                         .values('priority') \
                                         .annotate(count=Count('id'))

    # Count urgent tasks within the next 30 days
    urgent_tasks = Task.objects.filter(is_urgent=True, due_by__gte=now(), due_by__lte=now() + timedelta(days=30)).count()

    context = {
        'tasks_due_dates': tasks_due_dates,
        'task_count_by_priority': task_count_by_priority,
        'urgent_tasks': urgent_tasks,
        'tasks': Task.objects.all(),  # Include all tasks for the table
    }
    return render(request, 'dashboard_page.html', context)