import pytest
import threading
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.task_model import Task

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Creates a test database before each test and deletes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def create_test_task():
    """Creates a test task before the test"""
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Desc", "completed": False},
    )
    assert response.status_code == 200
    return response.json()


# Testing task creation
def test_create_task():
    response = client.post(
        "/tasks",
        json={"title": "New Task", "description": "Some description", "completed": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "Some description"
    assert data["completed"] is False


# Passing an empty header
def test_create_task_invalid():
    response = client.post(
        "/tasks",
        json={"title": "", "description": "Some description", "completed": False},
    )
    assert response.status_code == 422


# Getting a list of all tasks
def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# Getting a task by ID
def test_get_task_by_id(create_test_task):
    task_id = create_test_task["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == create_test_task["title"]


# Receiving a task with a nonexistent ID
def test_get_task_not_found():
    response = client.get("/tasks/99999")
    assert response.status_code == 404


# Updating a task
def test_update_task(create_test_task):
    task_id = create_test_task["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Task", "description": "Updated Desc", "completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["completed"] is True


# Updating a non-existent task
def test_update_task_not_found():
    response = client.put(
        "/tasks/99999",
        json={"title": "Updated Task", "description": "Updated Desc", "completed": True},
    )
    assert response.status_code == 404


# Deleting a task
def test_delete_task(create_test_task):
    task_id = create_test_task["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}


# Deleting a non-existent task
def test_delete_task_not_found():
    response = client.delete("/tasks/99999")
    assert response.status_code == 404


# Creates 100 tasks and verifies that the API saves them correctly
def test_bulk_create_tasks():
    num_tasks = 100
    for i in range(num_tasks):
        response = client.post(
            "/tasks",
            json={"title": f"Task {i}", "description": f"Desc {i}", "completed": False},
        )
        assert response.status_code == 200  # All must be successfully created

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= num_tasks


def create_task_thread():
    response = client.post(
        "/tasks",
        json={"title": "Thread Task", "description": "Created from thread", "completed": False},
    )
    assert response.status_code == 200


# Creates tasks in 10 threads at the same time
def test_concurrent_task_creation():
    threads = []
    for _ in range(10):
        t = threading.Thread(target=create_task_thread)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    response = client.get("/tasks")
    assert response.status_code == 200
    assert any(task["title"] == "Thread Task" for task in response.json())


# Checks that only one task attribute can be updated
def test_partial_update_task(create_test_task):
    task_id = create_test_task["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Title", "description": create_test_task["description"],
              "completed": create_test_task["completed"]},
    )
    assert response.status_code == 200
    updated_task = response.json()

    assert updated_task["title"] == "Updated Title"
    assert updated_task["description"] == create_test_task["description"]
    assert updated_task["completed"] == create_test_task["completed"]


# Creating a task with Unicode, emoji and special characters
def test_create_task_with_special_characters():
    response = client.post(
        "/tasks",
        json={"title": "🔥 Special!@#💡", "description": "Text with emojis 😊", "completed": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "🔥 Special!@#💡"
    assert data["description"] == "Text with emojis 😊"


# Deletes all tasks and verifies that they are indeed gone
def test_delete_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()

    for task in tasks:
        del_response = client.delete(f"/tasks/{task['id']}")
        assert del_response.status_code == 200

    final_response = client.get("/tasks")
    assert final_response.status_code == 200
    assert final_response.json() == []


def test_create_task_without_description():
    response = client.post(
        "/tasks",
        json={"title": "Task Without Desc", "completed": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Task Without Desc"
    assert data["description"] is None


def test_get_tasks_when_empty(test_db):
    test_db.query(Task).delete()
    test_db.commit()

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_task_with_negative_id():
    response = client.get("/tasks/-1")
    assert response.status_code == 404


def test_partial_task_update(create_test_task):
    task_id = create_test_task["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Partially Updated Title", "description": create_test_task["description"],
              "completed": create_test_task["completed"]},
    )
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Partially Updated Title"
    assert updated_task["description"] == create_test_task["description"]
    assert updated_task["completed"] == create_test_task["completed"]


def test_delete_already_deleted_task(create_test_task):
    task_id = create_test_task["id"]
    response1 = client.delete(f"/tasks/{task_id}")
    response2 = client.delete(f"/tasks/{task_id}")

    assert response1.status_code == 200
    assert response2.status_code == 404
