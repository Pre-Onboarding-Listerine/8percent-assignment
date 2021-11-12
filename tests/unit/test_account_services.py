from assertpy import assert_that

from src.accounts.domain.models import Balance
from src.accounts.dto import CreateAccountInfo, TransactionInfo
from src.accounts.exceptions import AccountNotFoundException, LackOfBalanceException, InvalidTransactionTypeException


def test_create_account_with_valid_info(account_service):
    info = CreateAccountInfo(owner_id="user-1", account_password="123qwe")
    account_service.create_account_with(info)

    assert_that(account_service.uow.committed).is_equal_to(True)


def test_get_account_list_with_owner_id(account_service):
    info = CreateAccountInfo(owner_id="user-1", account_password="123qwe")
    account_service.create_account_with(info)
    owner_id = "user-1"
    accounts = account_service.list_accounts_with(owner_id=owner_id)

    assert_that(len(accounts)).is_equal_to(1)


def test_get_account_list_with_not_exist_owner_id(account_service):
    not_exist_owner_id = "user-1"
    accounts = account_service.list_accounts_with(owner_id=not_exist_owner_id)

    assert_that(accounts).is_equal_to([])


def test_get_account_with_exist_account_number(account_service):
    info = CreateAccountInfo(owner_id="user-1", account_password="123qwe")
    account_service.create_account_with(info)
    accounts = account_service.list_accounts_with(owner_id=info.owner_id)
    account = account_service.retrieve_account_with(info.owner_id, accounts[0].account_number)

    assert_that(account.owner_id).is_equal_to(info.owner_id)
    assert_that(account.account_password).is_equal_to(info.account_password)


def test_get_account_with_not_exist_account_number(account_service):
    not_exist_account_number = "123-123-123123"
    assert_that(account_service.retrieve_account_with)\
        .raises(AccountNotFoundException)\
        .when_called_with("user-1", not_exist_account_number)


def test_withdraw_with_insufficient_balance(account_service):
    info = CreateAccountInfo(owner_id="user-1", account_password="123qwe")
    account_service.create_account_with(info)

    account = account_service.list_accounts_with(owner_id=info.owner_id)[0]

    account_number = account.account_number
    user_id = account.owner_id
    transaction_info = TransactionInfo(amount=3000, transaction_type="withdraw", memo="")

    assert_that(account_service.modify_balance)\
        .raises(LackOfBalanceException).\
        when_called_with(account_number, user_id, transaction_info)


def test_modify_balance_with_invalid_transaction_type(account_service):
    info = CreateAccountInfo(owner_id="user-1", account_password="123qwe")
    account_service.create_account_with(info)

    account = account_service.list_accounts_with(owner_id=info.owner_id)[0]

    account_number = account.account_number
    user_id = account.owner_id
    invalid_transaction_info = TransactionInfo(amount=3000, transaction_type="invalid", memo="")

    assert_that(account_service.modify_balance) \
        .raises(InvalidTransactionTypeException). \
        when_called_with(account_number, user_id, invalid_transaction_info)


def test_withdraw_balance_with_sufficient_balance(account_service):
    info = CreateAccountInfo(owner_id="user-1", account_password="123qwe")
    account_service.create_account_with(info)

    account = account_service.list_accounts_with(owner_id=info.owner_id)[0]

    account_number = account.account_number
    user_id = account.owner_id
    transaction_info = TransactionInfo(amount=30000, transaction_type="deposit", memo="")
    account_service.modify_balance(account_number, user_id, transaction_info)

    withdraw_transaction_info = TransactionInfo(amount=2000, transaction_type="withdraw", memo="")
    account_service.modify_balance(account_number, user_id, withdraw_transaction_info)

    actual = account_service.list_accounts_with(owner_id=info.owner_id)[0]
    assert_that(actual.balance).is_equal_to(Balance(amount=28000))

    uow = account_service.uow
    with uow:
        transaction_events = uow.transaction_events.list_by_account_number(account.account_number)
        assert_that(transaction_events).does_not_contain(None)
        assert_that(len(transaction_events)).is_equal_to(2)
