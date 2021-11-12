from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator, Field

from src.security.exception import EmptyPropertyException


class AccountPassword(BaseModel):
    value: str

    @validator('value')
    def not_empty(cls, v):
        if not v:
            raise EmptyPropertyException("account password is required")
        return v


class CreateAccountInfo(BaseModel):
    owner_id: str
    account_password: str


class AccountNumber(BaseModel):
    value: str

    @validator('value')
    def not_empty(cls, v):
        if not v:
            raise EmptyPropertyException("account number is required")
        return v


class TransactionInfo(BaseModel):
    amount: int = Field(gt=0)
    transaction_type: str
    memo: Optional[str]


class HistoryParams(BaseModel):
    start: Optional[datetime]
    end: Optional[datetime]
    transaction_type: Optional[str]


