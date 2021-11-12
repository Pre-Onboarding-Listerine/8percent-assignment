import abc

from src.users.domain import models
from src.users.exceptions import UserNotFoundException, DuplicatedUserException
from src.users.infra import orm


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    def exists(self, name: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, user: models.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user_id: str) -> models.User:
        raise NotImplementedError


class SqlUserRepository(AbstractUserRepository):
    def __init__(self, session):
        self.session = session

    def exists(self, name: str) -> bool:
        q = self.session.query(orm.User).filter(orm.User.name == name)
        return self.session.query(q.exists()).scalar()

    def add(self, user: models.User):
        if self.exists(user.name):
            raise DuplicatedUserException(f"user {user.name} already exists")
        user_orm = orm.User(**user.dict())
        self.session.add(user_orm)

    def get(self, user_id: str) -> models.User:
        user_orm = self.session.query(orm.User).filter(orm.User.user_id == user_id).first()
        if not user_orm:
            raise UserNotFoundException(f"{user_id} is not found")
        return models.User.from_orm(user_orm)
