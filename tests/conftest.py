import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities as _activities


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities to their original state after each test."""
    original = copy.deepcopy(_activities)
    yield
    _activities.clear()
    _activities.update(copy.deepcopy(original))
