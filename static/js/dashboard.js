 // fetches the data for the next 30 days from the get endpoint
 const getData = async () => {
    const response = await fetch(`${api_base_url}/tasks/`, {
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        }
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error("Error fetching tasks:", errorText);
        throw new Error("Failed to fetch tasks");
    }
    const taskData = await response.json();
    return taskData;
}

getData().then(taskData => {

    // generates the tasks due date data for the line graph
    const tasksDueDates = taskData.reduce((acc, task) => {
        const dueDate = new Date(task.due_by).toISOString().split('T')[0];
        if (!acc[dueDate]) {
            acc[dueDate] = { date: dueDate, count: 0 };
        }
        acc[dueDate].count += 1;
        return acc;
    }, {});

    const tasksDueDatesArray = Object.values(tasksDueDates).sort((a, b) => new Date(a.date) - new Date(b.date));
    const dateLabels = tasksDueDatesArray.map(item => item.date);
    const dateData = tasksDueDatesArray.map(item => item.count);

    // generates the tasks by priority
    const tasksPriority = taskData.reduce((acc, task) => {
        const priority = task.priority;
        if (!acc[priority]) {
            acc[priority] = { priority: priority, count: 0 };
        }
        acc[priority].count += 1;
        return acc;
    }, {});

    const priorityArray = Object.values(tasksPriority);
    const priorityLabels = priorityArray.map(item => item.priority);
    const priorityData = priorityArray.map(item => item.count);

    // return the number of urgent tasks
    const urgentTasksCount = taskData.filter(task => task.is_urgent).length; 
    document.querySelector(".urgent-tasks p").textContent = urgentTasksCount;

    // Line Chart: Tasks Due in the Next 30 Days
    var ctxLine = document.getElementById('tasksDueLineChart').getContext('2d');
    var tasksDueLineChart = new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: dateLabels,
            datasets: [{
                label: 'Tasks Due',
                data: dateData,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });



    // Pie Chart: Tasks by Priority
    var ctxPie = document.getElementById('tasksPriorityPieChart').getContext('2d');
    var tasksPriorityPieChart = new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: priorityLabels,
            datasets: [{
                data: priorityData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            },
            // Reduce the size of the pie
            layout: {
                padding: {
                    top: 20,
                    bottom: 20,
                    left: 20,
                    right: 20
                }
            },
        }
    });
});