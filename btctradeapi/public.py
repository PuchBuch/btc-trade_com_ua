# -*- coding: utf-8 -*-

from requestmaker import RequestMaker
from exceptions import UnknownDeal
from deals import DEALS
from decorators import dealsfilter


class PublicAPI(RequestMaker):

    @dealsfilter
    def deals(self, deal):
        """
        Результатом данного запроса будет  список сделок
        купли/продажи BitCoin за гривну между участниками биржи в формате
        JSON. Например:
        :param deal: one of the DEALS (btc_uah e.g.)
        :return: [{"amnt_base": "6.3938515000", "amnt_trade": "0.0013320524", "price": "4800.0000000000",
        "pub_date": "2014­06­01 22:34:52", "user": "abolt", "type": "buy"}, {"amnt_base": "6.3938513300",
        "amnt_trade": "0.0013320524", "price": "4800.0000000000", "pub_date": "2014­06­01 22:34:52", "user":
        "baobab", "type": "sell"}]
        Две записи массива выше показывают, что пользователь ​abolt ​купил у пользователя ​baobab 0.0013320524​ BTC, заплатив за них ​6.3938515000 ​гривны, из расчета ​4800​ гривны за один BitCoin.
        массив  объектов, состоящих из
            amnt_base​ ­ сумма сделки в базовой валюте,
            amnt_trade ­ сумма сделки в валюте торга
            price ​ ­ цена
            pub_date ​ ­ дата сделки
            user​ ­ участник сделки
            type​ ­ тип операции sell/buy ­
                1) sell​ ­ продажа валюты торга
                2) buy​ ­ покупка валюты торга
        """
        return self.makeget('/deals/%s' % deal)

    @dealsfilter
    def sells(self, deal):
        """
        Результатом работы данного запроса будет объект,содержащий
        информацию о  заявках на продажу валюты торга( в данном случае
        валютной пары BitCoin/ Гривна) в формате JSON:
        :param deal: one of the DEALS (btc_uah e.g.)
        :return: {"min_price": "4910.0000000000", "list": [{"currency_trade": "0.0092000000", "price": "4910.0000000000",
        "currency_base": "45.1720000000"}, {"currency_trade": "0.0323484400", "price": "5000.0000000000",
        "currency_base": "161.7422000000"}, {"currency_trade": "0.0400000000", "price": "5400.0000000000",
        "currency_base": "216.0000000000"}, {"currency_trade": "2.0797893000", "price": "5500.0000000000",
        "currency_base": "11438.8410000000"}, {"currency_trade": "1.5000000000", "price": "5678.0000000000",
        "currency_base": "8517.0000000000"}, {"currency_trade": "0.0023348400", "price": "6100.0000000000",
        "currency_base": "14.2425240000"}, {"currency_trade": "0.2029538324", "price": "6400.0000000000",
        "currency_base": "1298.9045270000"}, {"currency_trade": "3.4808297160", "price": "6600.0000000000",
        "currency_base": "22973.4761300000"}, {"currency_trade": "0.2431990000", "price": "7000.0000000000",
        "currency_base": "1702.3930000000"}, {"currency_trade": "0.1000000000", "price": "7400.0000000000",
        "currency_base": "740.0000000000"}, {"currency_trade": "0.1500000000", "price": "7600.0000000000",
        "currency_base": "1140.0000000000"}, {"currency_trade": "0.0700000000", "price": "9999.0000000000",
        "currency_base": "699.9300000000"}, {"currency_trade": "0.0020000000", "price": "40100.0000000000",
        "currency_base": "80.2000000000"}], "orders_sum": "7.9126550000", "max_price": "40100.0000000000"}
        min_price ­ ​минимальная цена в списке заявок
        list ​­ список заявок на продажу содежащий объекты заявок.
        orders_sum ­ ​сумма всех заявок на продажу в валюте торга
        max_price​ ­ максимальная  цена в списке заявок


        Объект заявок состоит из:
        currency_trade​ ­ сумма на продажу в валюте торга
        price​ ­ цена из расчета за одну целую единицу валюты торга
        currency_base ­ ​сумма  сделки в базовой валюте
        """
        return self.makeget('/trades/sell/%s' % deal)

    @dealsfilter
    def buyies(self, deal):
        """
        Результатом работы данного запроса будет объект, содержащий
        информацию о  заявках на покупку валюты торга( в данном случае
        валютной пары BitCoin/ Гривна) в формате JSON:
        :param deal: one of the DEALS (btc_uah e.g.)
        :return: {"min_price": "4910.0000000000", "list": [{"currency_trade": "0.0092000000", "price": "4910.0000000000",
        "currency_base": "45.1720000000"}, {"currency_trade": "0.0323484400", "price": "5000.0000000000",
        "currency_base": "161.7422000000"}, {"currency_trade": "0.0400000000", "price": "5400.0000000000",
        "currency_base": "216.0000000000"}, {"currency_trade": "2.0797893000", "price": "5500.0000000000",
        "currency_base": "11438.8410000000"}, {"currency_trade": "1.5000000000", "price": "5678.0000000000",
        "currency_base": "8517.0000000000"}, {"currency_trade": "0.0023348400", "price": "6100.0000000000",
        "currency_base": "14.2425240000"}, {"currency_trade": "0.2029538324", "price": "6400.0000000000",
        "currency_base": "1298.9045270000"}, {"currency_trade": "3.4808297160", "price": "6600.0000000000",
        "currency_base": "22973.4761300000"}, {"currency_trade": "0.2431990000", "price": "7000.0000000000",
        "currency_base": "1702.3930000000"}, {"currency_trade": "0.1000000000", "price": "7400.0000000000",
        "currency_base": "740.0000000000"}, {"currency_trade": "0.1500000000", "price": "7600.0000000000",
        "currency_base": "1140.0000000000"}, {"currency_trade": "0.0700000000", "price": "9999.0000000000",
        "currency_base": "699.9300000000"}, {"currency_trade": "0.0020000000", "price": "40100.0000000000",
        "currency_base": "80.2000000000"}], "orders_sum": "7.9126550000", "max_price": "40100.0000000000"}
        min_price ­ ​минимальная цена в списке заявок на покупку
        list ​­ список заявок на покупку содежащий объекты заявок.
        orders_sum ­ ​сумма всех заявок на покупку в базовой  валюте ( в данном случае
        Гривна)
        max_price​ ­ максимальная  цена в списке заявок на покупку

        list ​­ список заявок на продажу содежащий объекты заявок.
        Объект заявок состоит из:
            currency_trade​ ­ сумма покупки  в валюте торга
            price​ ­ цена из расчета за одну целую единицу валюты торга
            currency_base ­ ​сумма  сделки в базовой валюте
        """
        return self.makeget('/trades/buy/%s' % deal)
