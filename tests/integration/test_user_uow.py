from assertpy import assert_that

from src.users.application.unit_of_work import SqlUserUnitOfWork
from src.users.domain import models
from src.users.exceptions import UserNotFoundException, DuplicatedUserException


def insert_user(session, user):
    session.execute(
        "INSERT INTO users (user_id, name, password)"
        " VALUES (:user_id, :name, :password)",
        dict(user_id=user.user_id, name=user.name, password=user.password),
    )


def test_retrieve_user_with_user_id(session_factory):
    user = models.User(user_id="user-1", name="asd", password="123qwe")
    session = session_factory()
    insert_user(session, user)
    session.commit()

    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        actual = uow.users.get(user_id="user-1")
        assert_that(actual).is_equal_to(user)


def test_retrieve_user_with_not_exist_user(session_factory):
    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        assert_that(uow.users.get).raises(UserNotFoundException).when_called_with(user_id="user-1")


def test_add_user_with_valid_user(session_factory):
    user = models.User(user_id="user-1", name="asd", password="123qwe")
    uow = SqlUserUnitOfWork(session_factory)

    with uow:
        uow.users.add(user)
        actual = uow.users.get(user.user_id)
        assert_that(actual).is_equal_to(user)


def test_add_with_duplicated_user(session_factory):
    user = models.User(user_id="user-1", name="asd", password="123qwe")
    session = session_factory()
    insert_user(session, user)
    session.commit()

    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        assert_that(uow.users.add).raises(DuplicatedUserException).when_called_with(user)


def test_check_exists_with_exist_user(session_factory):
    user = models.User(user_id="user-1", name="asd", password="123qwe")
    session = session_factory()
    insert_user(session, user)
    session.commit()

    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        assert_that(uow.users.exists(user.name)).is_equal_to(True)


def test_check_exists_with_not_exist_user(session_factory):
    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        assert_that(uow.users.exists("asd")).is_equal_to(False)
