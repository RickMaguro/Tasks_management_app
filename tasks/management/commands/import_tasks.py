# import the data from Excel.csv
import pandas as pd
from django.core.management.base import BaseCommand
from tasks.models import Task

class Command(BaseCommand):
    help = 'Import tasks from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Read the CSV file
        data = pd.read_csv(file_path)

        # Loop through the rows in the CSV file and create Task objects
        for index, row in data.iterrows():
            task = Task(
                user_email=row['user_email'],
                task=row['task'],
                due_by=row['due_by'],
                priority=row['priority'],
                is_urgent=row['is_urgent']
            )
            task.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully imported task {task.task}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported all tasks'))
