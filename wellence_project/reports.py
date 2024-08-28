# wellence_project/reports.py

from slick_reporting.views import ReportView
from tasks.models import Task

class TaskReportView(ReportView):
    report_model = Task
    date_field = 'due_by'
    group_by = 'priority'
    columns = ['task', 'user_email', 'is_urgent']
    
    chart_settings = [
        {
            'type': 'line',
            'data_source': 'id__count',
            'title_source': 'due_by',
            'plot_total': True,
            'title': 'Tasks Due in the Next 30 Days',
        },
        {
            'type': 'pie',
            'data_source': 'id__count',
            'title_source': 'priority',
            'title': 'Tasks by Priority in the Next 30 Days',
        },
    ]
    
    # Remove the custom filter for testing
    # time_series_pattern = 'daily'