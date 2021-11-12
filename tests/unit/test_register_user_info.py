from assertpy import assert_that

from src.users.dto import RegisterUserInfo
from src.users.exceptions import EmptyNameException


def test_not_empty_with_empty_name():
    assert_that(RegisterUserInfo).raises(EmptyNameException).when_called_with(name="", password="123")
