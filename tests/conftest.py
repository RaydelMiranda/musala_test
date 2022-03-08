import os

import pymongo
import pytest


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

