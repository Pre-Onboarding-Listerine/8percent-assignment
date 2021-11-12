import pytest
from assertpy import assert_that

from src.accounts.domain.models import Account, Balance
from src.accounts.exceptions import LackOfBalanceException


@pytest.fixture
def default_account():
    return Account(
        account_number="123-1234-123412",
        owner_id="user-1",
        account_password="123qwe",
        balance=Balance(amount=10000)
    )


def test_deposit_money_with_default_account(default_account):
    input_money = Balance(amount=5000)
    default_account.deposit(input_money)
    expected = Balance(amount=15000)

    assert_that(default_account.balance).is_equal_to(expected)


def test_withdraw_money_with_default_account(default_account):
    taken_money = Balance(amount=5000)
    default_account.withdraw(taken_money)
    expected = Balance(amount=5000)

    assert_that(default_account.balance).is_equal_to(expected)


def test_withdraw_money_with_over_balanced_amount(default_account):
    taken_money = Balance(amount=12000)
    assert_that(default_account.withdraw)\
        .raises(LackOfBalanceException)\
        .when_called_with(taken_money)


def test_validate_password_with_correct_password(default_account):
    correct_password = "123qwe"
    actual = default_account.validate_password(correct_password)
    expected = True

    assert_that(actual).is_equal_to(expected)


def test_validate_password_with_incorrect_password(default_account):
    incorrect_password = "zxczxc"
    actual = default_account.validate_password(incorrect_password)
    expected = False

    assert_that(actual).is_equal_to(expected)
