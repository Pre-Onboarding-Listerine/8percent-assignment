import pytest
from assertpy import assert_that
from jose import jwt

from src.configs.security import SECRET_KEY, ALGORITHM
from src.security.application.services import authenticate_token
from src.security.dto import LoginInfo
from src.security.exception import IncorrectPasswordException, EmptyAccessTokenException, InvalidAccessTokenException
from src.users.domain import models
from src.users.exceptions import UserNotFoundException


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


def test_authenticate_with_not_exist_user(authentication_service):
    not_exist_user_info = LoginInfo(
        name="asd",
        password="123qwe"
    )
    assert_that(authentication_service.authenticate)\
        .raises(UserNotFoundException)\
        .when_called_with(not_exist_user_info)


def test_authenticate_with_incorrect_password(valid_login_info, authentication_service):
    user_uow = authentication_service.uow
    user = models.User(user_id="user-1", **valid_login_info.dict())
    with user_uow:
        user_uow.users.add(user)
        user_uow.commit()

    incorrect_login_info = LoginInfo(
        name=valid_login_info.name,
        password="zxc"
    )
    assert_that(authentication_service.authenticate) \
        .raises(IncorrectPasswordException) \
        .when_called_with(incorrect_login_info)


def test_authenticate_token_with_valid_token():
    valid_token = "Bearer " + jwt.encode(
        claims={"user_id": "user-1"},
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )
    actual = authenticate_token(valid_token)
    expected = "user-1"
    assert_that(actual).is_equal_to(expected)


def test_authenticate_token_with_empty_string_token():
    empty_string_token = ""
    assert_that(authenticate_token)\
        .raises(EmptyAccessTokenException)\
        .when_called_with(empty_string_token)


def test_authenticate_token_with_invalid_token():
    invalid_token = "Bearer asdasfasdfasf"
    assert_that(authenticate_token)\
        .raises(InvalidAccessTokenException)\
        .when_called_with(invalid_token)
