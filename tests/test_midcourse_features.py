from datetime import date, timedelta


def _iso(days_from_today: int) -> str:
    return (date.today() + timedelta(days=days_from_today)).isoformat()


def test_create_task_with_valid_due_date(client):
    due_date = _iso(3)

    response = client.post("/tasks", json={"title": "Submit report", "due_date": due_date})

    assert response.status_code == 201
    body = response.json()
    assert body["due_date"] == due_date
    assert body["is_overdue"] is False


def test_invalid_due_date_format_is_rejected(client):
    response = client.post("/tasks", json={"title": "Bad date", "due_date": "26-07-2026"})

    assert response.status_code == 422


def test_overdue_filter_returns_only_open_overdue_tasks(client):
    overdue_open = client.post(
        "/tasks",
        json={"title": "Overdue open", "due_date": _iso(-2), "priority": "high"},
    ).json()
    overdue_done = client.post("/tasks", json={"title": "Overdue done", "due_date": _iso(-1)}).json()
    client.patch(f"/tasks/{overdue_done['id']}", json={"status": "in_progress"})
    client.patch(f"/tasks/{overdue_done['id']}", json={"status": "done"})
    client.post("/tasks", json={"title": "Future open", "due_date": _iso(2)})

    response = client.get("/tasks?overdue=true")

    assert response.status_code == 200
    body = response.json()
    assert [task["id"] for task in body] == [overdue_open["id"]]
    assert body[0]["is_overdue"] is True


def test_update_due_date_changes_overdue_state(client):
    created = client.post("/tasks", json={"title": "Move deadline", "due_date": _iso(2)}).json()

    response = client.patch(f"/tasks/{created['id']}", json={"due_date": _iso(-1)})

    assert response.status_code == 200
    assert response.json()["is_overdue"] is True


def test_create_task_with_tags_normalizes_values(client):
    response = client.post(
        "/tasks",
        json={"title": "Tagged task", "tags": [" api ", "Frontend", "api"]},
    )

    assert response.status_code == 201
    assert response.json()["tags"] == ["api", "Frontend"]


def test_empty_tag_value_is_rejected(client):
    response = client.post("/tasks", json={"title": "Bad tag", "tags": ["valid", " "]})

    assert response.status_code == 422


def test_filter_by_tag_is_case_insensitive(client):
    client.post("/tasks", json={"title": "API task", "tags": ["API"]})
    client.post("/tasks", json={"title": "Design task", "tags": ["design"]})

    response = client.get("/tasks?tag=api")

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["API task"]


def test_update_tags_and_preserve_after_unrelated_update(client):
    created = client.post("/tasks", json={"title": "Keep tags", "tags": ["backend"]}).json()

    update_tags = client.patch(f"/tasks/{created['id']}", json={"tags": ["backend", "testing"]})
    assert update_tags.status_code == 200
    assert update_tags.json()["tags"] == ["backend", "testing"]

    update_title = client.patch(f"/tasks/{created['id']}", json={"title": "Keep tags renamed"})
    assert update_title.status_code == 200
    assert update_title.json()["tags"] == ["backend", "testing"]
