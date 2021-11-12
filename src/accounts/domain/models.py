from pydantic import BaseModel, Field

from src.accounts.exceptions import LackOfBalanceException


class Balance(BaseModel):
    amount: int = Field(..., ge=0)

    def __init__(self, amount: int):
        super().__init__(amount=amount)

    def __composite_values__(self):
        return [self.amount]

    def __add__(self, other):
        new_amount = self.amount + other.amount
        return Balance(amount=new_amount)

    def __sub__(self, other):
        new_amount = self.amount - other.amount
        if new_amount < 0:
            raise LackOfBalanceException("balance is insufficient")
        return Balance(amount=new_amount)

    def __eq__(self, other):
        return isinstance(other, Balance) and\
               other.amount == self.amount

    def __ne__(self, other):
        return not self.__eq__(other)


class Account(BaseModel):
    account_number: str
    owner_id: str
    account_password: str
    balance: Balance

    class Config:
        orm_mode = True

    def validate_password(self, password: str):
        if self.account_password == password:
            return True
        else:
            return False

    def deposit(self, amount: Balance):
        self.balance += amount

    def withdraw(self, amount: Balance):
        self.balance -= amount
