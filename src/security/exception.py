class EmptyPropertyException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class IncorrectPasswordException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class EmptyAccessTokenException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidAccessTokenException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
