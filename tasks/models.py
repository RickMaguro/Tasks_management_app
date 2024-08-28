from django.db import models

class Task(models.Model):
    user_email = models.EmailField()
    task = models.CharField(max_length=75)
    due_by = models.DateTimeField()
    priority = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return self.task
