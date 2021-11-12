from assertpy import assert_that

from src.accounts.dto import CreateAccountInfo
from src.accounts.exceptions import AccountNotFoundException


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
    account = account_service.retrieve_account_with(accounts[0].account_number)

    assert_that(account.owner_id).is_equal_to(info.owner_id)
    assert_that(account.account_password).is_equal_to(info.account_password)


def test_get_account_with_not_exist_account_number(account_service):
    not_exist_account_number = "123-123-123123"
    assert_that(account_service.retrieve_account_with)\
        .raises(AccountNotFoundException)\
        .when_called_with(not_exist_account_number)
