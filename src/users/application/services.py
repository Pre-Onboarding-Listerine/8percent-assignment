from src.users.application.unit_of_work import AbstractUserUnitOfWork
from src.users.domain import models
from src.users.dto import RegisterUserInfo
from src.utils.id_generator import IdGenerator


class UserService:
    def __init__(self, id_gen: IdGenerator, uow: AbstractUserUnitOfWork):
        self.id_gen = id_gen
        self.uow = uow

    def register(self, info: RegisterUserInfo):
        new_user = models.User(user_id=self.id_gen.generate(), **info.dict())
        with self.uow:
            self.uow.users.add(new_user)
            self.uow.commit()

