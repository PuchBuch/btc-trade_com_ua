from abc import abstractmethod
import datetime

import peewee

from btctradeapi import config


class OperationType(peewee.Field):

    def db_value(self, value):
        return int(value)

    def python_value(self, value):
        return int(value)


class BaseModel(peewee.Model):

    class Meta:
        db = config.DB

    @abstractmethod
    def to_btcobject(self):
        """
        Converts Peewee Model to btctradeapi.types type
        :return: btctradeapi.types member
        """

    @abstractmethod
    @staticmethod
    def from_json(cls, json_object):
        """
        Creates Model from JSON object
        :param cls:
        :param json_object:
        :return:
        """

class User(BaseModel):
    name = peewee.CharField(max_length=64)


class Deal(BaseModel):
    user = peewee.ForeignKeyField(User)

    amnt_base = peewee.FloatField()
    amnt_trade = peewee.FloatField()

    price = peewee.FloatField()
    pub_date = peewee.DateTimeField()
    type_ = OperationType()


class Buy(BaseModel):
    pass


class Sell(BaseModel):
    pass
