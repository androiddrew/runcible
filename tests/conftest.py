import os
import pytest
from molten import testing
from molten.contrib.sqlalchemy import EngineData

from runcible.index import create_app
from runcible.db import Base


@pytest.fixture(autouse=True, scope="module")
def ensure_test_env_settings():
    current_env_setting = os.environ.get("ENVIRONMENT")
    os.environ["ENVIRONMENT"] = "test"
    yield
    os.environ["ENVIRONMENT"] = current_env_setting or ""


# requires function scope so that database is removed on every tests
@pytest.fixture(scope="module")
def app():
    app = create_app()
    yield app


@pytest.fixture(autouse=True)
def create_db(app):
    """Creates a test database with session scope"""

    def _retrieve_engine(engine_data: EngineData):
        return engine_data.engine

    engine = app.injector.get_resolver().resolve(_retrieve_engine)()

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(app):
    """Creates a testing client"""
    return testing.TestClient(app)


@pytest.fixture(scope="function")
def session():
    pass
