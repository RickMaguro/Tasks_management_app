from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_page, name='task_page'),  
]
