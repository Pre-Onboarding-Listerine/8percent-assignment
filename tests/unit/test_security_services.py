import pytest
from assertpy import assert_that
from jose import jwt

from src.configs.security import SECRET_KEY, ALGORITHM
from src.security.dto import LoginInfo
from src.users.domain import models


@pytest.fixture
def valid_login_info():
    return LoginInfo(name="asd", password="123qwe")


def test_authenticate_with_valid_info(valid_login_info, authentication_service):
    user_uow = authentication_service.uow
    user = models.User(user_id="user-1", **valid_login_info.dict())
    with user_uow:
        user_uow.users.add(user)
        user_uow.commit()

    access_token = authentication_service.authenticate(valid_login_info)
    expected = "Bearer " + jwt.encode(
        claims={"user_id": user.user_id},
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    assert_that(access_token.access_token).is_equal_to(expected)
