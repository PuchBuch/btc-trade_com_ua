class BaseException(Exception):
    pass


class UnknownDeal(BaseException):
    pass


class ImpossibleDeal(BaseException):
    pass


class ConnectionError(BaseException):
    pass