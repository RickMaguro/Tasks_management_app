function parseCustomDate(dateString) {
    const parts = dateString.split(' ');
    const dateParts = parts[0].split('-');
    const timeParts = parts[1].split(':');

    const year = '20' + dateParts[2]; 
    const month = dateParts[1];
    const day = dateParts[0];
    const hour = timeParts[0];
    const minute = timeParts[1];

    const isoDateString = `${year}-${month}-${day}T${hour}:${minute}:00`;

    return isoDateString;
}

document.getElementById("task-form").addEventListener("submit", function(e) {
    e.preventDefault();

    const taskData = {
        user_email: document.getElementById("id_user_email").value,
        task: document.getElementById("id_task").value,
        due_by: parseCustomDate(document.getElementById('id_due_by').value),
        priority: parseInt(document.getElementById("id_priority").value),
        is_urgent: document.getElementById("id_is_urgent").checked,
    }

    console.log(JSON.stringify(taskData));

    fetch("api/tasks/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify(taskData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("task-form").reset();
    })
    .catch(error => {
        console.error("Error: ", error);
    });
});