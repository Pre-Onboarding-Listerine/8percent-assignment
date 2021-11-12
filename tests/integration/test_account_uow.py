from datetime import datetime

from assertpy import assert_that

from src.accounts.application.unit_of_work import SqlAccountUnitOfWork
from src.accounts.domain import models
from src.accounts.domain.models import Balance, TransactionEvent
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


def insert_transaction_events(session):
    session.execute(
        "INSERT INTO transaction_events "
        "(account_number, transaction_datatime, transaction_amount, balance, transaction_type, memo) VALUES "
        f"('123-123-123123', '{datetime(2021, 10, 11, 9, 19, 32)}', '3000', '12000', 'withdraw', 'sadf'),"
        f"('123-123-123123', '{datetime(2021, 10, 12, 9, 19, 32)}', '5000', '7000', 'withdraw', 'sadf'),"
        f"('123-123-456456', '{datetime(2021, 10, 16, 9, 19, 32)}', '30000', '40000', 'deposit', 'sadf'),"
        f"('123-123-123123', '{datetime(2021, 10, 23, 9, 19, 32)}', '3000', '10000', 'deposit', 'sadf'),"
        f"('123-123-123123', '{datetime(2021, 11, 11, 9, 19, 32)}', '3000', '13000', 'withdraw', 'sadf'),"
        f"('123-123-456456', '{datetime(2021, 11, 11, 9, 19, 32)}', '3000', '37000', 'withdraw', 'sadf'),"
        f"('123-123-123123', '{datetime(2021, 12, 11, 9, 19, 32)}', '3000', '16000', 'deposit', 'sadf'),"
        f"('123-123-456456', '{datetime(2021, 12, 15, 9, 19, 32)}', '3000', '34000', 'withdraw', 'sadf'),"
        f"('123-123-123123', '{datetime(2021, 12, 16, 9, 19, 32)}', '3000', '13000', 'withdraw', 'sadf'),"
        f"('123-123-123123', '{datetime(2021, 12, 17, 9, 19, 32)}', '3000', '10000', 'withdraw', 'sadf')"
    )


def test_list_transactions_with_transactions(session_factory):
    session = session_factory()
    insert_transaction_events(session)
    session.commit()

    uow = SqlAccountUnitOfWork(session_factory)
    account_number = "123-123-123123"
    with uow:
        transactions = uow.transaction_events.list_by_account_number(account_number)
        assert_that(len(transactions)).is_equal_to(7)


def test_list_transactions_with_not_exist_account_number(session_factory):
    uow = SqlAccountUnitOfWork(session_factory)
    account_number = "123-123-123123"
    with uow:
        transactions = uow.transaction_events.list_by_account_number(account_number)
        assert_that(transactions).is_equal_to([])


def test_add_transaction_with_transaction_event(session_factory):
    transaction_event = TransactionEvent(
        account_number="123-123-123123",
        transaction_datatime=datetime(2021, 10, 16, 9, 19, 32),
        transaction_amount=30000,
        balance=40000,
        transaction_type="deposit",
        memo="asdfasdfaf"
    )
    uow = SqlAccountUnitOfWork(session_factory)
    with uow:
        uow.transaction_events.add(transaction_event)
        transaction_events = uow.transaction_events.list_by_account_number(transaction_event.account_number)
        assert_that(transaction_events[0].memo).is_equal_to(transaction_event.memo)


