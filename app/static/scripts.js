document.addEventListener("DOMContentLoaded", function () {
    loadTasks();

    document.getElementById("taskForm").addEventListener("submit", function (event) {
        event.preventDefault();
        addTask();
    });

    document.getElementById("searchInput").addEventListener("input", function () {
        if (this.value.trim() === "") {
            loadTasks();  // Загружаем все задачи при очистке строки поиска
        } else {
            searchTasks();
        }
    });
});


function loadTasks() {
    fetch("/tasks")
        .then(response => response.json())
        .then(tasks => {
            renderTasks(tasks);
        })
        .catch(error => console.error("Error loading tasks:", error));
}


function renderTasks(tasks) {
    const taskTableBody = document.getElementById("taskTableBody");
    taskTableBody.innerHTML = "";
    tasks.forEach(task => {
        taskTableBody.innerHTML += createTaskRow(task);
    });
}


function createTaskRow(task) {
    return `<tr>
        <td>${task.id}</td>
        <td>${task.title}</td>
        <td>${task.description || "No description"}</td>
        <td>${task.completed ? "Completed" : "Active"}</td>
        <td>
            <button class="btn btn-warning btn-sm" onclick="editTask(${task.id}, '${task.title}', '${task.description || ""}', ${task.completed})">Edit</button>
            <button class="btn btn-success btn-sm" onclick="toggleTask(${task.id})">${task.completed ? "Activate" : "Complete"}</button>
            <button class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})">Delete</button>
        </td>
    </tr>`;
}


function addTask() {
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();

    if (!title) {
        alert("Title is required!");
        return;
    }

    fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description, completed: false })
    })
    .then(response => response.json())
    .then(() => {
        document.getElementById("taskForm").reset();
        loadTasks();
    })
    .catch(error => console.error("Error adding task:", error));
}


function editTask(id, currentTitle, currentDesc, completed) {
    const newTitle = prompt("Edit Task Title:", currentTitle);
    if (newTitle === null || newTitle.trim() === "") return;

    const newDesc = prompt("Edit Task Description:", currentDesc);
    fetch(`/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle, description: newDesc, completed })
    })
    .then(() => loadTasks())
    .catch(error => console.error("Error updating task:", error));
}


function toggleTask(id) {
    fetch(`/tasks/${id}`)
        .then(response => response.json())
        .then(task => {
            fetch(`/tasks/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: task.title,
                    description: task.description,
                    completed: !task.completed
                })
            })
            .then(() => loadTasks());
        })
        .catch(error => console.error("Error toggling task:", error));
}


function deleteTask(id) {
    if (confirm("Are you sure you want to delete this task?")) {
        fetch(`/tasks/${id}`, { method: "DELETE" })
            .then(() => loadTasks())
            .catch(error => console.error("Error deleting task:", error));
    }
}


function searchTasks() {
    const query = document.getElementById("searchInput").value.trim();

    if (query === "") {
        loadTasks();
        return;
    }

    fetch(`/extra-tasks/search-by-title?title=${query}`)
        .then(response => response.json())
        .then(tasks => {
            renderTasks(tasks);
        })
        .catch(error => console.error("Error searching tasks:", error));
}
