import pytest

from src.security.application.services import AuthenticationService
from src.users.application import unit_of_work
from src.users.application.services import UserService
from src.users.domain import models
from src.users.exceptions import UserNotFoundException
from src.users.infra import repository
from src.utils.id_generator import IdGenerator


class FakeUserRepository(repository.AbstractUserRepository):
    def __init__(self, users):
        self._users = users

    def exists(self, name: str) -> bool:
        if self._users.get_by_id(name, None):
            return True
        else:
            return False

    def add(self, user: models.User):
        self._users[user.user_id] = user

    def get_by_id(self, user_id: str) -> models.User:
        return self._users[user_id]

    def get_by_name(self, name: str) -> models.User:
        for key, value in self._users.items():
            if value.name == name:
                return self._users[key]
        raise UserNotFoundException("user not found")


class FakeUserUnitOfWork(unit_of_work.AbstractUserUnitOfWork):
    def __init__(self):
        self.users = FakeUserRepository(dict())
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeUserIdGenerator(IdGenerator):
    def __init__(self):
        self.index = 0

    def generate(self):
        new_id = str(self.index)
        self.index += 1
        return new_id


@pytest.fixture
def user_service():
    return UserService(FakeUserIdGenerator(), FakeUserUnitOfWork())


@pytest.fixture
def authentication_service():
    return AuthenticationService(FakeUserUnitOfWork())
