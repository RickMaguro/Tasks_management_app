from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user_email', 'task', 'due_by', 'priority', 'is_urgent']
        error_messages = {
            'user_email': {
                'required': "Please enter your email address.",
                'invalid': "Enter a valid email address.",
            },
            'due_by': {
                'required': "Please specify the due date.",
            },
        }
        widgets = {
            'due_by': forms.DateTimeInput(format='%d-%m-%y %H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['due_by'].input_formats = ['%d-%m-%y %H:%M'] 

