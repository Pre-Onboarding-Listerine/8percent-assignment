class LackOfBalanceException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class AccountNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class DuplicatedAccountException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidTransactionTypeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidAccessException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
