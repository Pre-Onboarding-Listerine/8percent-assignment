from assertpy import assert_that

from src.users.dto import RegisterUserInfo


def test_register_with_valid_name(user_service):
    info = RegisterUserInfo(name="asd", password="123qqwe")
    user_service.register(info)
    assert_that(user_service.uow.users.get(str(0))).is_not_none()
    assert_that(user_service.uow.committed).is_equal_to(True)
