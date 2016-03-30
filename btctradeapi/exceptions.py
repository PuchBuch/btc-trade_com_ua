# -*- coding: utf-8 -*-


class BaseException(Exception):
    pass


class UnknownDeal(BaseException):
    """
    неизвестное значение deal
    """
    pass


class ImpossibleDeal(BaseException):
    """
    С двух валют нельзя получить deal - его нету в списке возможных
    """
    pass


class ConnectionError(BaseException):
    """
    Ошибка соединения либо внутренняя ошибка сервера
    """
    pass


class UnknownOperationType(BaseException):
    """

    """
