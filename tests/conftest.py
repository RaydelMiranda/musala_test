import os

import pymongo
import pytest

from app import create_app


@pytest.fixture(autouse=True, scope='function')
def env_setup(monkeypatch):
    """
    Fixture that set ups the test environment.
    """
    monkeypatch.setenv('DB_NAME', 'musala_test')


@pytest.fixture(autouse=True, scope='function')
def db_clean(env_setup):
    """
    Fixture that cleans the test db after each test case.
    """
    yield
    client = pymongo.MongoClient(os.environ.get('MONGO_URL', 'localhost:27017'))
    client.drop_database(os.environ['DB_NAME'])


@pytest.fixture
def drone():
    from model.drone import Drone, DRONE_MODEL_LIGHT, STATE_IDLE, STATE_LOADED
    drone = Drone(DRONE_MODEL_LIGHT, '1234', 500, 50, STATE_IDLE | STATE_LOADED)
    yield drone


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
