from src.accounts.application.unit_of_work import AbstractAccountUnitOfWork
from src.accounts.domain.models import Account, Balance
from src.accounts.dto import CreateAccountInfo
from src.utils.id_generator import IdGenerator


class AccountService:
    def __init__(self, id_gen: IdGenerator, uow: AbstractAccountUnitOfWork):
        self.id_gen = id_gen
        self.uow = uow

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

    def retrieve_account_with(self, account_number: str):
        with self.uow:
            return self.uow.accounts.get_by_account_number(account_number)

    def list_accounts_with(self, owner_id: str):
        with self.uow:
            return self.uow.accounts.list(owner_id)
