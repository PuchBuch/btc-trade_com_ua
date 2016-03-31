from abc import abstractmethod
import datetime

import peewee

from btctradeapi import config
from btctradeapi import types
from btctradeapi.decorators import internaltypechecker


class OperationType(peewee.Field):

    def db_value(self, value):
        return int(value)

    def python_value(self, value):
        return int(value)


class Convertable(object):

    @abstractmethod
    @staticmethod
    def from_type(cls, btc_object):
        """
        Creates Model from BTC internal type object
        :param cls:
        :param btc_object:
        :return:
        """


class BaseModel(peewee.Model):

    class Meta:
        db = config.DB


class User(BaseModel):
    name = peewee.CharField(max_length=64)


class Deal(BaseModel, Convertable):
    user = peewee.ForeignKeyField(User)

    amnt_base = peewee.FloatField()
    amnt_trade = peewee.FloatField()

    price = peewee.FloatField()
    pub_date = peewee.DateTimeField()
    type = OperationType()

    @internaltypechecker(types.Deal)
    @staticmethod
    def from_type(cls, btc_object):

        return cls.create(
            user=User.get_or_create(name=btc_object.name),
            amnt_base=btc_object.amnt_base,
            amnt_trade=btc_object.amnt_trade,
            price=btc_object.price,
            pub_date=btc_object.pub_date,
            type=btc_object.type
        )


class Buy(BaseModel, Convertable):
    min_price = peewee.FloatField()
    max_price = peewee.FloatField()
    orders_sum = peewee.FloatField()

    @internaltypechecker(types.Buyies)
    @staticmethod
    def from_type(cls, btc_object):
        instance = cls.create(
            min_price=btc_object.min_price,
            max_price=btc_object.max_price,
            orders_sum=btc_object.orders_sum,
        )
        for item in btc_object.list:
            list_item = BuyItem.from_type(item)
            list_item.buy = instance
            list_item.save()
        return instance


class BuyItem(BaseModel, Convertable):
    currency_base = peewee.FloatField()
    currency_trade = peewee.FloatField()
    price = peewee.FloatField()
    buy = peewee.ForeignKeyField(Buy, related_name="list", null=True)

    @internaltypechecker(types.basetuple("BuyItem"))
    @staticmethod
    def from_type(cls, btc_object):
        return cls.create(
            currency_base=btc_object.currency_base,
            currency_trade=btc_object.currency_trade,
            price=btc_object.price
        )


class SellItem(BaseModel, Convertable):
    currency_base = peewee.FloatField()
    currency_trade = peewee.FloatField()
    price = peewee.FloatField()
    buy = peewee.ForeignKeyField(Buy, related_name="list", null=True)

    @internaltypechecker(types.basetuple("SellItem"))
    @staticmethod
    def from_type(cls, btc_object):
        return cls.create(
            currency_base=btc_object.currency_base,
            currency_trade=btc_object.currency_trade,
            price=btc_object.price
        )


class Sell(BaseModel, Convertable):
    min_price = peewee.FloatField()
    max_price = peewee.FloatField()
    orders_sum = peewee.FloatField()

    @internaltypechecker(types.Sells)
    @staticmethod
    def from_type(cls, btc_object):
        instance = cls.create(
            min_price=btc_object.min_price,
            max_price=btc_object.max_price,
            orders_sum=btc_object.orders_sum,
        )
        for item in btc_object.list:
            list_item = SellItem.from_type(item)
            list_item.buy = instance
            list_item.save()
        return instance


class CycleIterationStateSnapshot(BaseModel):

    sells = peewee.ForeignKeyField(Sell)
    buyies = peewee.ForeignKeyField(Buy)
    deals = peewee.ForeignKeyField(Deal)

    deal = peewee.CharField()
    timestamp = peewee.DateTimeField(default=datetime.datetime.now)
