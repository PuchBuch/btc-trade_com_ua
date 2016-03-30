from abc import abstractmethod

from btctradeapi.config import DB


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Storage(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.db = DB

    @abstractmethod
    def put_object(self, table, _object):
        """
        Saves object to table
        :param table: str - table name
        :param _object: serializable object
        :return:
        """

    @abstractmethod
    def get_objects(self, table):
        """
        Returns all the objects from table
        :param table: str - table name
        :return:
        """
