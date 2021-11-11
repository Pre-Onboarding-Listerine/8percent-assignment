import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import dependencies
from src.configs.database import Base
from src.main import app
from tests.conftest import TEST_SQLITE_URL


engine = create_engine(
    TEST_SQLITE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_session_factory():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_client():
    app.dependency_overrides[dependencies.get_session_factory] = test_session_factory
    return TestClient(app)
