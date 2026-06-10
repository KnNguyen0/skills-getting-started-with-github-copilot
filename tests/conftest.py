import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


# Snapshot the initial activities state so tests run with a clean slate
_initial_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: ensure activities are reset before each test
    app_module.activities = copy.deepcopy(_initial_activities)
    yield
    # Teardown: restore original state after test
    app_module.activities = copy.deepcopy(_initial_activities)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app_module.app) as c:
        yield c
