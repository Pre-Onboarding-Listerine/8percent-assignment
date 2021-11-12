import unittest

from assertpy import assert_that, fail
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status
from starlette.testclient import TestClient

from src import dependencies
from src.configs.database import Base
from src.main import app


class TestAccountsRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

        def test_session_factory():
            Base.metadata.create_all(bind=self.engine)
            return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        app.dependency_overrides[dependencies.get_session_factory] = test_session_factory
        self.client = TestClient(app)
        self.client.post("/api/users", json={"name": "asd", "password": "123qwe"})
        login_response = self.client.post("/api/auth/login", json={"name": "asd", "password": "123qwe"})
        self.access_token = login_response.json()["access_token"]

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def test_retrieve_account_with_valid_password(self):
        data = {"value": "account-password"}
        headers = {"Authorization": self.access_token}
        response = self.client.post(
            "/api/accounts",
            json=data,
            headers=headers
        )
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        response_list = self.client.get(
            "/api/accounts",
            headers=headers
        )
        assert_that(len(response_list.json())).is_equal_to(1)

        account = response_list.json()[0]
        response_retrieve = self.client.get(
            "/api/accounts/" + account['account_number'],
            headers=headers
        )
        assert_that(response_retrieve.status_code).is_equal_to(status.HTTP_200_OK)

    def test_retrieve_with_not_exist_account_number(self):
        account_number = "123-123-123123"
        headers = {"Authorization": self.access_token}
        response = self.client.get(
            "/api/accounts" + account_number,
            headers=headers
        )
        assert_that(response.status_code).is_equal_to(status.HTTP_404_NOT_FOUND)

    def test_get_account_list_without_accounts(self):
        headers = {"Authorization": self.access_token}
        response = self.client.get(
            "/api/accounts",
            headers=headers
        )
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.json()).is_equal_to([])

    def test_withdraw_from_sufficient_balance(self):
        headers = {"authorization": self.access_token}
        data = {"value": "account-password"}
        response = self.client.post(
            "/api/accounts",
            json=data,
            headers=headers
        )
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        response_list = self.client.get(
            "/api/accounts",
            headers=headers
        )
        account_info = response_list.json()[0]

        transaction_data = {
            "amount": 3000,
            "transaction_type": "deposit",
            "memo": ""
        }

        response_deposit = self.client.put(
            "/api/accounts/" + account_info["account_number"],
            json=transaction_data,
            headers=headers
        )
        assert_that(response_deposit.status_code).is_equal_to(status.HTTP_200_OK)

        transaction_data = {
            "amount": 2000,
            "transaction_type": "withdraw",
            "memo": ""
        }

        response_withdraw = self.client.put(
            "/api/accounts/" + account_info["account_number"],
            json=transaction_data,
            headers=headers
        )
        assert_that(response_withdraw.status_code).is_equal_to(status.HTTP_200_OK)

    def test_withdraw_from_insufficient_balance(self):
        headers = {"authorization": self.access_token}
        data = {"value": "account-password"}
        response = self.client.post(
            "/api/accounts",
            json=data,
            headers=headers
        )
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        response_list = self.client.get(
            "/api/accounts",
            headers=headers
        )
        account_info = response_list.json()[0]

        transaction_data = {
            "amount": 3000,
            "transaction_type": "deposit",
            "memo": ""
        }

        response_deposit = self.client.put(
            "/api/accounts/" + account_info["account_number"],
            json=transaction_data,
            headers=headers
        )
        assert_that(response_deposit.status_code).is_equal_to(status.HTTP_200_OK)

        transaction_data = {
            "amount": 5000,
            "transaction_type": "withdraw",
            "memo": ""
        }

        response_withdraw = self.client.put(
            "/api/accounts/" + account_info["account_number"],
            json=transaction_data,
            headers=headers
        )
        assert_that(response_withdraw.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)
