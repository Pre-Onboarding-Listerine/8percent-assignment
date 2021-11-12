import abc
import uuid


class IdGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self) -> str:
        raise NotImplementedError


class UserIdGenerator(IdGenerator):
    def generate(self) -> str:
        return "user-" + str(uuid.uuid4())


class AccountNumberGenerator(IdGenerator):
    def generate(self) -> str:
        return "account-" + str(uuid.uuid4())
