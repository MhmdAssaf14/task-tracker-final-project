import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import reset_tasks


@pytest.fixture()
def client():
    reset_tasks()
    with TestClient(app) as test_client:
        yield test_client
    reset_tasks()
