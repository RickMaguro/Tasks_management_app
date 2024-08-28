from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

@login_required
def task_page(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('task_page')  
    else:
        form = TaskForm()

    tasks = Task.objects.all()  # All tasks to display
    return render(request, 'tasks/task_page.html', {'form': form, 'tasks': tasks})