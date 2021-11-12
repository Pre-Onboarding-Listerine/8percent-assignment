from assertpy import assert_that

from src.users.dto import RegisterUserInfo


def test_register_with_valid_name(user_service):
    info = RegisterUserInfo(name="asd", password="123qqwe")
    user_service.register(info)
    actual = user_service.uow.users.get_by_name(info.name)
    assert_that(actual.name).is_equal_to(info.name)
    assert_that(user_service.uow.committed).is_equal_to(True)
