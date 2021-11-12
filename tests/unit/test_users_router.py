import unittest

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status
from starlette.testclient import TestClient

from src import dependencies
from src.configs.database import Base
from src.main import app


class TestUserRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

        def test_session_factory():
            Base.metadata.create_all(bind=self.engine)
            return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        app.dependency_overrides[dependencies.get_session_factory] = test_session_factory
        self.client = TestClient(app)

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=self.engine)
        print("teardown")

    def test_signup_with_valid_info(self):
        data = {
            "name": "asd",
            "password": "123qwe"
        }
        response = self.client.post(
            "/api/users",
            json=data
        )

        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

    def test_signup_with_empty_name(self):
        data = {
            "name": "",
            "password": "123qwe"
        }
        response = self.client.post(
            "/api/users",
            json=data
        )

        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

    def test_signup_with_duplicated_name(self):
        data = {
            "name": "asd",
            "password": "123qwe"
        }
        print("response")
        response = self.client.post(
            "/api/users",
            json=data
        )
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        print("duplicated")
        response_duplicated = self.client.post(
            "/api/users",
            json=data
        )
        assert_that(response_duplicated.status_code).is_equal_to(status.HTTP_409_CONFLICT)
