# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app
import backend.storage as st
client = TestClient(app)


# --- TESTS ROOT ---

def test_root_returns_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


# --- TESTS TASKS ---

def test_create_task_and_get_it_back():
    task_data = {"name": "Dormir", "priority": 2}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200

    task = response.json()
    assert task["name"] == "Dormir"
    assert task["priority"] == 2
    assert task["completed"] is False

    task_id = task["id"]
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id


def test_get_all_tasks_returns_dict():
    client.post("/tasks", json={"name": "A"})
    client.post("/tasks", json={"name": "B"})
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(isinstance(v, dict) for v in data.values())


def test_toggle_task_changes_status():
    response = client.post("/tasks", json={"name": "Lire"})
    task_id = response.json()["id"]

    toggle_response = client.patch(f"/tasks/{task_id}")
    assert toggle_response.status_code == 200
    assert toggle_response.json()["completed"] is True


def test_toggle_task_nonexistent_returns_500():
    response = client.patch("/tasks/999")
    # Ton code actuel ne gère pas l'erreur, donc FastAPI renvoie 500
    assert response.status_code == 404


# --- TESTS TASK LISTS ---

def test_create_and_get_task_list():
    response = client.post("/lists", json={"name": "Sport"})
    assert response.status_code == 200
    assert response.json()["name"] == "Sport"

    all_lists = client.get("/lists/")
    assert response.status_code == 200
    assert "Sport" in all_lists.json()


def test_add_task_to_task_list():
    client.post("/lists", json={"name": "Courses"})
    response_task = client.post(
        "/tasks",
        json={"name": "Acheter du lait"},
        params={"list_name": "Courses"},
    )
    assert response_task.status_code == 200

    task_list_response = client.get("/lists/Courses")
    task_list = task_list_response.json()
    assert len(task_list["tasks"]) == 1


def test_get_nonexistent_list_returns_500():
    response = client.get("/lists/Inconnue")
    assert response.status_code == 404


# --- TESTS INTÉGRÉS ---

def test_create_task_directly_in_list():
    """Crée une tâche déjà associée à une liste existante."""
    client.post("/lists", json={"name": "Projets"})
    response = client.post(
        "/tasks",
        json={"name": "Coder"},
        params={"list_name": "Projets"},
    )
    assert response.status_code == 200

    task = response.json()
    assert task["list_name"] == "Projets"

    list_response = client.get("/lists/Projets")
    assert list_response.status_code == 200
    list_data = list_response.json()
    assert task["id"] in list_data["tasks"]
