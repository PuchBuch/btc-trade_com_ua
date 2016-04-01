from abc import abstractmethod
import datetime

import peewee

from btctradeapi import config
from btctradeapi import types
from btctradeapi.decorators import internaltypechecker


class Convertable(object):

    @abstractmethod
    #@classmethod
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


class Deals(BaseModel):

    deal = peewee.CharField(max_length=10)


class Deal(BaseModel, Convertable):
    deals = peewee.ForeignKeyField(Deals, null=True)
    user = peewee.ForeignKeyField(User)

    amnt_base = peewee.FloatField()
    amnt_trade = peewee.FloatField()

    price = peewee.FloatField()
    pub_date = peewee.DateTimeField()
    type = peewee.IntegerField()

    @internaltypechecker(types.Deal)
    def from_type(cls, btc_object):

        return cls.create(
            user=User.get_or_create(name=btc_object.user)[0],
            amnt_base=btc_object.amnt_base,
            amnt_trade=btc_object.amnt_trade,
            price=btc_object.price,
            pub_date=btc_object.pub_date,
            type=btc_object.type['int']
        )


class Buy(BaseModel, Convertable):
    min_price = peewee.FloatField()
    max_price = peewee.FloatField()
    orders_sum = peewee.FloatField()

    @internaltypechecker(types.Buyies)
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
    def from_type(cls, btc_object):
        instance = cls.create(
            min_price=btc_object.min_price,
            max_price=btc_object.max_price,
            orders_sum=btc_object.orders_sum,
        )
        for item in btc_object.list:
            list_item = SellItem.from_type(item)
            list_item.sell = instance
            list_item.save()
        return instance


class SellItem(BaseModel, Convertable):
    currency_base = peewee.FloatField()
    currency_trade = peewee.FloatField()
    price = peewee.FloatField()
    sell = peewee.ForeignKeyField(Sell, related_name="list", null=True)

    @internaltypechecker(types.basetuple("SellItem"))
    def from_type(cls, btc_object):
        return cls.create(
            currency_base=btc_object.currency_base,
            currency_trade=btc_object.currency_trade,
            price=btc_object.price
        )


class CycleIterationStateSnapshot(BaseModel):

    sells = peewee.ForeignKeyField(Sell, null=True)
    buyies = peewee.ForeignKeyField(Buy, null=True)
    deals = peewee.ForeignKeyField(Deal, null=True)

    deal = peewee.CharField()
    timestamp = peewee.DateTimeField(default=datetime.datetime.now)
