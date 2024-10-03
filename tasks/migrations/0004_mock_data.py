# Generated by Django 5.1.1 on 2024-09-18 18:26

import csv
from pathlib import Path
from django.utils.timezone import make_aware
from datetime import datetime
from django.db import migrations


def load_csv_data(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")

    path = Path(__file__).resolve().parent.parent / "data" / "mock_data.csv"

    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task = Task (
                user_email = row["user_email"],
                task = row["task"],
                due_by = make_aware(datetime.strptime(row["due_by"], 
                                    '%Y-%m-%d %H:%M:%S')),
                priority = row["priority"],
                is_urgent = row["is_urgent"] == "True"
            )
            task.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_priority'),
    ]

    operations = [
        migrations.RunPython(load_csv_data),
    ]