from assertpy import assert_that

from src.accounts.application.unit_of_work import SqlAccountUnitOfWork
from src.accounts.domain import models
from src.accounts.domain.models import Balance
from src.accounts.exceptions import AccountNotFoundException, DuplicatedAccountException


def insert_account(session, account):
    session.execute(
        "INSERT INTO accounts (account_number, owner_id, account_password, balance_amount)"
        " VALUES (:account_number, :owner_id, :account_password, :balance_amount)",
        dict(
            account_number=account.account_number,
            owner_id=account.owner_id,
            account_password=account.account_password,
            balance_amount=account.balance.amount
        ),
    )


def insert_accounts(session, owner_id):
    session.execute(
        "INSERT INTO accounts (account_number, owner_id, account_password, balance_amount) VALUES "
        f"('123-123-123123', '{owner_id}', '123qwe', '12000'),"
        f"('123-456-123123', '{owner_id}', '123qwe', '0'),"
        f"('123-123-456123', '{owner_id}', '123qwe', '10000'),"
        f"('123-123-897876', '{owner_id}', '123qwe', '120')"
    )


def test_check_exists_with_exist_account(session_factory):
    account = models.Account(
        account_number="123-1234-123123",
        owner_id="user-1",
        account_password="123qwe123",
        balance=Balance(amount=10000)
    )
    session = session_factory()
    insert_account(session, account)
    session.commit()

    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        assert_that(uow.accounts.exists(account.account_number)).is_equal_to(True)


def test_check_exists_with_not_exist_account(session_factory):
    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        assert_that(uow.accounts.exists("asd")).is_equal_to(False)


def test_retrieve_account_with_exist_account(session_factory):
    account = models.Account(
        account_number="123-1234-123123",
        owner_id="user-1",
        account_password="123qwe123",
        balance=Balance(amount=10000)
    )
    session = session_factory()
    insert_account(session, account)
    session.commit()

    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        actual = uow.accounts.get_by_account_number(account.account_number)
        assert_that(actual).is_equal_to(account)


def test_retrieve_account_with_not_exist_account(session_factory):
    not_exist_account_number = "123qwe123-123-123123"
    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        assert_that(uow.accounts.get_by_account_number)\
            .raises(AccountNotFoundException)\
            .when_called_with(not_exist_account_number)


def test_add_account_with_valid_account(session_factory):
    valid_account = models.Account(
        account_number="123-1234-123123",
        owner_id="user-1",
        account_password="123qwe123",
        balance=Balance(amount=10000)
    )
    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(valid_account)
        actual = uow.accounts.get_by_account_number(valid_account.account_number)
        assert_that(actual).is_equal_to(valid_account)


def test_add_account_with_duplicated_account_number(session_factory):
    duplicated_account = models.Account(
        account_number="123-1234-123123",
        owner_id="user-1",
        account_password="123qwe123",
        balance=Balance(amount=10000)
    )
    session = session_factory()
    insert_account(session, duplicated_account)
    session.commit()

    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        assert_that(uow.accounts.add)\
            .raises(DuplicatedAccountException)\
            .when_called_with(duplicated_account)


def test_get_account_list_with_valid_owner_id(session_factory):
    owner_id = "user-1"
    session = session_factory()
    insert_accounts(session, owner_id)
    session.commit()

    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        accounts = uow.accounts.list(owner_id=owner_id)
        assert_that(len(accounts)).is_equal_to(4)


def test_get_account_list_without_accounts(session_factory):
    owner_id = "user-1"
    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        accounts = uow.accounts.list(owner_id=owner_id)
        assert_that(accounts).is_equal_to([])
