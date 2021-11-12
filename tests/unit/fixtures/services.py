from typing import List

import pytest
from sqlalchemy.orm import Query

from src.accounts.application.services import AccountService
from src.accounts.application.unit_of_work import AbstractAccountUnitOfWork
from src.accounts.domain import models
from src.accounts.domain.models import Account
from src.accounts.exceptions import AccountNotFoundException
from src.accounts.infra.repository import AbstractAccountRepository, AbstractTransactionRepository
from src.security.application.services import AuthenticationService
from src.users.application.unit_of_work import AbstractUserUnitOfWork
from src.users.application.services import UserService
from src.users.domain.models import User
from src.users.exceptions import UserNotFoundException
from src.users.infra.repository import AbstractUserRepository
from src.utils.id_generator import IdGenerator


class FakeUserRepository(AbstractUserRepository):
    def __init__(self, users):
        self._users = users

    def exists(self, name: str) -> bool:
        if self._users.get_by_name(name, None):
            return True
        else:
            return False

    def add(self, user: User):
        self._users[user.user_id] = user

    def get_by_id(self, user_id: str) -> User:
        return self._users[user_id]

    def get_by_name(self, name: str) -> User:
        for key, value in self._users.items():
            if value.name == name:
                return self._users[key]
        raise UserNotFoundException("user not found")


class FakeUserUnitOfWork(AbstractUserUnitOfWork):
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


class FakeAccountRepository(AbstractAccountRepository):
    def __init__(self, accounts):
        self._accounts = accounts

    def exists(self, account_number: str):
        if self._accounts.get_by_account_number(account_number):
            return True
        else:
            return False

    def get_by_account_number(self, account_number: str) -> Account:
        try:
            return self._accounts[account_number]
        except KeyError:
            raise AccountNotFoundException("account not found")

    def add(self, account: Account):
        self._accounts[account.account_number] = account

    def list(self, owner_id: str) -> List[Account]:
        return list(filter(lambda account: account.owner_id == owner_id, self._accounts.values()))

    def update_balance(self, account: Account):
        self._accounts[account.account_number] = account


class FakeTransactionRepository(AbstractTransactionRepository):
    def __init__(self, transaction_events):
        self._transaction_events = transaction_events

    def list_by_account_number(self, account_number: str) -> List[models.TransactionEvent]:
        return list(filter(lambda event: event.account_number == account_number, self._transaction_events))

    def add(self, transaction: models.TransactionEvent):
        self._transaction_events.append(transaction)

    def history_by_account_number(self, account_number: str) -> Query:
        pass


class FakeAccountUnitOfWork(AbstractAccountUnitOfWork):
    def __init__(self):
        self.accounts = FakeAccountRepository(dict())
        self.transaction_events = FakeTransactionRepository(list())
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeAccountNumberGenerator(IdGenerator):
    def __init__(self):
        self.index = 0

    def generate(self) -> str:
        new_account_number = str(self.index)
        self.index += 1
        return new_account_number


@pytest.fixture
def account_service():
    return AccountService(FakeAccountNumberGenerator(), FakeAccountUnitOfWork())
