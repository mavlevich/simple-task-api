import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def create_test_tasks():
    tasks = [
        {"title": "Test Task 1", "description": "Test Description 1", "completed": False},
        {"title": "Another Task", "description": "This is another test", "completed": False},
        {"title": "Test Task 2", "description": "Another test description", "completed": True},
    ]
    created_tasks = []
    for task in tasks:
        response = client.post("/tasks", json=task)
        assert response.status_code == 200
        created_tasks.append(response.json())
    return created_tasks


def test_search_task_by_title(create_test_tasks):
    response = client.get("/extra-tasks/search-by-title?title=Test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    for task in data:
        assert "test" in task["title"].lower()


def test_search_task_by_description(create_test_tasks):
    response = client.get("/extra-tasks/search-by-description?description=another")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    for task in data:
        assert "another" in task["description"].lower()


def test_search_task_by_title_no_results():
    response = client.get("/extra-tasks/search-by-title?title=NonExistentTask")
    assert response.status_code == 200
    assert response.json() == []


def test_search_task_by_description_no_results():
    response = client.get("/extra-tasks/search-by-description?description=NonExistentDesc")
    assert response.status_code == 200
    assert response.json() == []
