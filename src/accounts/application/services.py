from datetime import datetime

from src.accounts.application.unit_of_work import AbstractAccountUnitOfWork
from src.accounts.domain.models import Account, Balance, TransactionEvent
from src.accounts.dto import CreateAccountInfo, TransactionInfo, HistoryParams
from src.accounts.exceptions import InvalidTransactionTypeException, InvalidAccessException, AccountNotFoundException
from src.utils.id_generator import IdGenerator


class AccountService:
    def __init__(self, id_gen: IdGenerator, uow: AbstractAccountUnitOfWork):
        self.id_gen = id_gen
        self.uow = uow

    def __publish_transaction_event(self, account: Account, transaction_info: TransactionInfo):
        return TransactionEvent(
            account_number=account.account_number,
            transaction_datatime=datetime.utcnow(),
            transaction_amount=transaction_info.amount,
            balance=account.balance.amount,
            transaction_type=transaction_info.transaction_type,
            memo=transaction_info.memo
        )

    def create_account_with(self, info: CreateAccountInfo):
        new_account = Account(
            account_number=self.id_gen.generate(),
            owner_id=info.owner_id,
            account_password=info.account_password,
            balance=Balance(amount=0)
        )
        with self.uow:
            self.uow.accounts.add(new_account)
            self.uow.commit()

    def retrieve_account_with(self, user_id: str, account_number: str):
        with self.uow:
            account = self.uow.accounts.get_by_account_number(account_number)
            if account.owner_id != user_id:
                raise InvalidAccessException("only an owner can access the account of the owner")
            return account

    def list_accounts_with(self, owner_id: str):
        with self.uow:
            return self.uow.accounts.list(owner_id)

    def modify_balance(self, account_number: str, user_id: str, transaction_info: TransactionInfo):
        with self.uow:
            account = self.uow.accounts.get_by_account_number(account_number)
            if account.owner_id != user_id:
                raise InvalidAccessException("only an owner can access the account of the owner")

            if transaction_info.transaction_type == "deposit":
                account.deposit(Balance(amount=transaction_info.amount))
            elif transaction_info.transaction_type == "withdraw":
                account.withdraw(Balance(amount=transaction_info.amount))
            else:
                raise InvalidTransactionTypeException("invalid transaction type")
            self.uow.accounts.update_balance(account)
            self.uow.transaction_events.add(
                self.__publish_transaction_event(account, transaction_info)
            )
            self.uow.commit()

    def get_transaction_history(self, account_number: str, user_id: str, params: HistoryParams):
        with self.uow:
            account = self.uow.accounts.get_by_account_number(account_number)
            if account:
                if account.owner_id == user_id:
                    history = self.uow.transaction_events.history_by_account_number(account_number, params)
                    return history
                else:
                    raise InvalidAccessException(
                        "only the owner of an account can access the transaction history of the account"
                    )
            else:
                raise AccountNotFoundException(f"account {account_number} is not found")

