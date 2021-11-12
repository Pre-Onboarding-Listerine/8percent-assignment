from pydantic import BaseModel, validator, Field

from src.security.exception import EmptyPropertyException


class LoginInfo(BaseModel):
    name: str = Field(max_length=30)
    password: str

    @validator('name', 'password')
    def not_empty(cls, v: str) -> str:
        if not v:
            raise EmptyPropertyException("properties cannot be empty")
        return v


class AccessToken(BaseModel):
    access_token: str
