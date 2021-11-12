class EmptyNameException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UserNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class DuplicatedUserException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
