from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

@login_required
def task_page(request):
    form = TaskForm()
    tasks = Task.objects.all()
    return render(request, 'tasks/task_page.html', {'form': form, 'tasks': tasks})