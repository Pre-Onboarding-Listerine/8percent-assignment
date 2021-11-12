import abc
from typing import List

from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import parse_obj_as
from sqlalchemy.orm import Query

from src.accounts.domain import models
from src.accounts.dto import HistoryParams
from src.accounts.exceptions import AccountNotFoundException, DuplicatedAccountException
from src.accounts.infra import orm


class AbstractAccountRepository(abc.ABC):
    @abc.abstractmethod
    def exists(self, account_number: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_account_number(self, account_number: str) -> models.Account:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, account: models.Account):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, owner_id: str) -> List[models.Account]:
        raise NotImplementedError

    @abc.abstractmethod
    def update_balance(self, account: models.Account):
        raise NotImplementedError


class SqlAccountRepository(AbstractAccountRepository):
    def __init__(self, session):
        self.session = session

    def exists(self, account_number: str):
        q = self.session.query(orm.Account).filter(orm.Account.account_number == account_number)
        return self.session.query(q.exists()).scalar()

    def get_by_account_number(self, account_number: str) -> models.Account:
        account = self.session.query(orm.Account).filter(orm.Account.account_number == account_number).first()
        if not account:
            raise AccountNotFoundException(f"account {account_number} is not found")
        return models.Account.from_orm(account)

    def add(self, account: models.Account):
        if self.exists(account.account_number):
            raise DuplicatedAccountException(f"account {account.account_number} already exists")
        account_orm = orm.Account(
            account_number=account.account_number,
            owner_id=account.owner_id,
            account_password=account.account_password,
            balance=account.balance
        )
        self.session.add(account_orm)

    def list(self, owner_id: str) -> List[models.Account]:
        accounts = self.session.query(orm.Account).filter(orm.Account.owner_id == owner_id).all()
        return parse_obj_as(List[models.Account], accounts)

    def update_balance(self, account: models.Account):
        account_orm = self.session.query(orm.Account)\
            .filter(orm.Account.account_number == account.account_number).first()
        account_orm.balance_amount = account.balance.amount


class AbstractTransactionRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, transaction: models.TransactionEvent):
        raise NotImplementedError

    @abc.abstractmethod
    def list_by_account_number(self, account_number: str) -> List[models.TransactionEvent]:
        raise NotImplementedError

    @abc.abstractmethod
    def history_by_account_number(self, account_number: str, params: HistoryParams):
        raise NotImplementedError


class SqlTransactionRepository(AbstractTransactionRepository):
    def __init__(self, session):
        self.session = session

    def add(self, transaction_event: models.TransactionEvent):
        transaction_event_orm = orm.TransactionEvent(**transaction_event.dict())
        self.session.add(transaction_event_orm)

    def list_by_account_number(self, account_number: str) -> List[models.TransactionEvent]:
        transaction_history = self.session.query(orm.TransactionEvent) \
            .filter(orm.TransactionEvent.account_number == account_number).all()
        return parse_obj_as(List[models.TransactionEvent], transaction_history)

    def history_by_account_number(self, account_number: str, params: HistoryParams):
        query = self.session.query(orm.TransactionEvent).filter(orm.TransactionEvent.account_number == account_number)
        if params.start:
            query = query.filter(orm.TransactionEvent.transaction_datatime >= params.start)
        if params.end:
            query = query.filter(orm.TransactionEvent.transaction_datatime < params.end)
        if params.transaction_type:
            query = query.filter(orm.TransactionEvent.transaction_type == params.transaction_type)
        return paginate(query)
