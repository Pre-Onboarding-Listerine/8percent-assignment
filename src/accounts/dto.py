from pydantic import BaseModel, validator

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
