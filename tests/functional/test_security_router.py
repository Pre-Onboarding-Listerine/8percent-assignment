import unittest

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from starlette import status

from src import dependencies
from src.configs.database import Base
from src.main import app


class TestSecurityRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

        def test_session_factory():
            Base.metadata.create_all(bind=self.engine)
            return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        app.dependency_overrides[dependencies.get_session_factory] = test_session_factory
        self.client = TestClient(app)
        self.client.post("/api/users", json={"name": "asd", "password": "123qwe"})

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def test_login_with_valid_info(self):
        data = {
            "name": "asd",
            "password": "123qwe"
        }
        response = self.client.post(
            "/api/auth/login",
            json=data
        )

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.json()).contains_key("access_token")
