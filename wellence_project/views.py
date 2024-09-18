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

    context = {
        'tasks': Task.objects.all(),
        'api_base_url': settings.API_BASE_URL,
    }
    return render(request, 'dashboard_page.html', context)