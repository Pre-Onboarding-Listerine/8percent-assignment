from pydantic import BaseModel, Field, validator

from src.users.exceptions import EmptyNameException


class RegisterUserInfo(BaseModel):
    name: str = Field(max_length=30)
    password: str

    @validator('name')
    def not_empty(cls, v: str) -> str:
        if not v:
            raise EmptyNameException("user name cannot be empty")
        return v
