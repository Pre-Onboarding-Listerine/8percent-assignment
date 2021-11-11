import abc
import uuid


class IdGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self) -> str:
        raise NotImplementedError


class UserIdGenerator(IdGenerator):
    def generate(self):
        return "user-" + str(uuid.uuid4())
