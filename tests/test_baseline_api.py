def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "timestamp" in response.json()


def test_create_and_read_task(client):
    created = client.post("/tasks", json={"title": "Write baseline tests"})

    assert created.status_code == 201
    task_id = created.json()["id"]

    fetched = client.get(f"/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Write baseline tests"
    assert fetched.json()["status"] == "to_do"
    assert fetched.json()["priority"] == "medium"


def test_blank_title_is_rejected(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_filter_by_status_and_priority(client):
    client.post("/tasks", json={"title": "High todo", "priority": "high"})
    task = client.post("/tasks", json={"title": "Medium todo"}).json()
    client.patch(f"/tasks/{task['id']}", json={"status": "in_progress"})

    todo_tasks = client.get("/tasks?status=to_do&priority=high")
    assert todo_tasks.status_code == 200
    assert [task["title"] for task in todo_tasks.json()] == ["High todo"]


def test_invalid_status_transition_is_rejected(client):
    created = client.post("/tasks", json={"title": "Cannot jump"}).json()

    response = client.patch(f"/tasks/{created['id']}", json={"status": "done"})

    assert response.status_code == 422
    assert "not allowed" in response.json()["detail"]


def test_delete_task_then_get_returns_404(client):
    created = client.post("/tasks", json={"title": "Delete me"}).json()

    deleted = client.delete(f"/tasks/{created['id']}")
    assert deleted.status_code == 204

    missing = client.get(f"/tasks/{created['id']}")
    assert missing.status_code == 404
