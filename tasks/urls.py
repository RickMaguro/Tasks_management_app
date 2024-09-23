from django.urls import path
from . import views
from .api import api

urlpatterns = [
    path('', views.task_page, name='task_page'),
    path('api/', api.urls),  
]
