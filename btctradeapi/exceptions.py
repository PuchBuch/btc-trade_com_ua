class BaseException(Exception):
    pass


class UnknownDeal(BaseException):
    pass


class ConnectionError(BaseException):
    pass