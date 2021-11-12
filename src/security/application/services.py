from jose import jwt

from src.configs.security import SECRET_KEY, ALGORITHM
from src.security.dto import LoginInfo, AccessToken
from src.users.application.unit_of_work import AbstractUserUnitOfWork


class AuthenticationService:
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    @staticmethod
    def __publish_access_token(user_id: str) -> AccessToken:
        token = "Bearer " + jwt.encode(
            claims={"user_id": user_id},
            key=SECRET_KEY,
            algorithm=ALGORITHM
        )
        return AccessToken(access_token=token)

    def authenticate(self, info: LoginInfo):
        with self.uow:
            user = self.uow.users.get_by_name(info.name)
            if user.password == info.password:
                return self.__publish_access_token(user.user_id)


def authenticate_token():
    pass