# -*- coding: utf-8 -*-

import json
import hashlib

import requests

from requestmaker import RequestMaker
from exceptions import ConnectionError, ImpossibleDeal, UnknownDeal
from decorators import dealsfilter, checknonce
from utils import getdeal


class PrivateAPI(RequestMaker):

    def __init__(self, pubkey, privkey):
        super(PrivateAPI, self).__init__()
        self.pubkey = pubkey
        self.privkey = privkey
        #TODO: fix multithreading resources race
        self.nonce = 1
        self.order = 1

    def makepost(self, url, **params):
        if params.get('out_order_id', None) is None:
            params.update(out_order_id=self.order)
            self.order += 1
        if params.get('nonce', None) is None:
            params.update(nonce=self.nonce)
            self.nonce += 1

        req = requests.Request('POST', url=self.base_api_url+url, data=params)
        prepared = req.prepare()
        prepared.headers['api-sign'] = hashlib.sha256(
            "%s%s" % (prepared.body, self.privkey)).hexdigest()
        prepared.headers['public-key'] = self.pubkey
        try:
            response = self.sendrequest(prepared)
            #import ipdb; ipdb.set_trace()
            print "url = '%s'\nPOST body='%s'\nHeaders = '%s'\nResponse: '%s'" % (
                prepared.url, prepared.body, prepared.headers, response.content)
            try:
                return json.loads(response.content)
            except Exception, e:
                print e
                return dict(status=False) #### WRONG WAY! !!!! TEMPORRARY FIX!
        except Exception, e:
            print e
            #if response.status_code != 200:
            import ipdb; ipdb.set_trace()
            raise ConnectionError

    def auth(self, order=None, nonce=None):
        """
        :param order: order number
        :param nonce: nonce number
        :return:

        Первый запрос для начала работы с торговым апи должен быть на url :

            https://btc-trade.com.ua/api/auth

        С POST параметром out_order_id равным произвольному значению и nonce равный целому произвольному числу.
        Воспользуемся командой curl :

        .. code-block:: console

            $ curl -k -i \\
            -H "api-sign: 9925916858e6361ffb88fc0b71d763355ea979e3ac62a6acaa8fe4a8ba548abf" \\
            -H "public-key: 9e6ea26cc7314d6dea8359f8ed5de68b2b5f0ec8daa0d5eac96b86d2b44ada38" \\
            --data "out_order_id=2&nonce=1" \\
            -v https://btc-trade.com.ua/api/auth
        """
        return self.makepost('/auth', out_order_id=1, nonce=nonce)

    @checknonce
    def balance(self, order=None, nonce=None):
        """
        :param order:
        :param nonce:
        :return:

        После старта сессии, первый  запрос, который вам захочеться сделать -
        это наверняка проверить состояние вашего счета .
        Для этого необходимо cформировать POST запрос на url:

            https://btc-trade.com.ua/api/balance

        С POST параметром out_order_id равным произвольному значению и параметром nonce равный любому целочисленному
        числу, большем, чем число использованное в предыдущем запросе.
        Авторизация происходит путем добавление HTTP загаловков public-key и api-sign, где public-key - это публичный
        ключ из вашего личного кабинета, а api-sign подпись сформированная путем конкатенация вашего post запроса
        и вашего  private_key, и получением хеш-функции SHA256 от полученной строки.

        Типовый запрос из командной строки при помощи команды curl :

        .. code-block:: console

            $ curl -k   -i \\
            -H "api-sign: 9925916858e6361ffb88fc0b71d763355ea979e3ac62a6acaa8fe4a8ba548abf" \\
            -H "public-key: 9e6ea26cc7314d6dea8359f8ed5de68b2b5f0ec8daa0d5eac96b86d2b44ada38" \\
            --data "out_order_id=2&nonce=1" \\
            -v  https://btc-trade.com.ua/api/balance

        Результатом запроса будет :

        .. code-block:: javascript

            {
                "msg_count": 0,
                "accounts": [
                    {
                        "currency": "UAH", "balance": "1744.2104180000"
                    }, {
                        "currency": "BTC", "balance": "0.1205538600"
                    }, {
                        "currency": "LTC", "balance": "1.0266850207"
                    }, {
                        "currency": "NVC", "balance": "0.0000000000"
                    }, {
                        "currency": "DRK", "balance": "0.0000000000"
                    }, {
                        "currency": "VTC", "balance": "0.0000000000"
                    }, {
                        "currency": "PPC", "balance": "0.0000000000"
                    }, {
                        "currency": "HIRO", "balance": "999.5000000000"
                    }
                ],
                "use_f2a": false,
                "notify_count": 0
            }

        JSON - объект с полем accounts, содержащим список счетов по каждой ваюте.
        Внимание! Параметр out_order_id является обязательным и должен быть добавлен  к каждому POST запросу.
        Желательно его каждый раз изменять.
        """

        return self.makepost('/balance', out_order_id=order, nonce=nonce)

    @checknonce
    def sell(self, currency_from, currency_to, count, price, order=None, nonce=None):
        """
        :param currency_from:
        :param currency_to:
        :param count:
        :param price:
        :param order:
        :param nonce:
        :return:

        Для этого необходимо cформировать POST запрос на url по выбранной вами валютной паре в данном случае \
        LiteCoin/Гривна

            https://btc-trade.com.ua/api/sell/ltc_uah

        С POST параметрами:
            * count: 0.8851641964
            * price:  55
            * out_order_id:  55
            * currency1: UAH
            * currency: LTC
            * nonce : 10

        Где :
            * nonce - целочисленней инкремент
            * Count - количество монет для продажи
            * Price - цена из расчета за одну монету
            * Currency1 - базовая валюта
            * Currency - валюта торга
            * Out_order_id - внешний идентификатор, принимающий произвольное значение

        И HTTP загаловками :
            * public-key - публичный ключ
            * api-sign - хеш сумма SHA256, сформированная от тела POST запроса с добавлением приватного ключа в конце, \
            например: \

                count=0.8851641964&nonce=10&price=55&out_order_id=55&currency1=UAH&currency=LTC$privat_key
                $privat_key - ваш приватный ключ

        Запрос при помощи команды curl:

        .. code-block:: console

            $ curl -k \\
            -i -H "api-sign: 652167fcdc3d0f55cacd4f2eea27e2f2512669126b2ddf5b5cbdbd8e18c23592" \\
            -H "public-key: 9e6ea26cc7314d6dea8359f8ed5de68b2b5f0ec8daa0d5eac96b86d2b44ada38"\\
            --data "currency1=UAH&currency=BTC&count=0.003&price=6200&out_order_id=4&nonce=4" \\
            -v https://btc-trade.com.ua/api/sell/btc_uah

        В случае успеха ответом будет JSON объект вида :

        .. code-block:: javascript

            {
                "status": true,
                "description": "The order has been created",
                "oder_id": 1
            }

        * order_id - будет содержать внутренний идентификатор в системе, \
         по которому можно будет проверить состояние вашей заявки

        """
        deal = getdeal(currency_to, currency_from)
        if not deal:
            raise ImpossibleDeal()
        #time.sleep(self.timespace)
        return self.makepost('/sell/%s' % deal, currency1=currency_from, currency=currency_to, price=price, count=count, out_order_id=order, nonce=nonce)

    @checknonce
    def buy(self, currency_from, currency_to, count, price, order=None, nonce=None):
        """
        :param currency_from:
        :param currency_to:
        :param count:
        :param price:
        :param order:
        :param nonce:
        :return:

        Заявка покупки формируется подобным образом, только на другой  url, для пары LiteCoin/Гривна:

            https://btc-trade.com.ua/api/buy/ltc_uah

        С POST параметрами
            * count: 0.8851641964
            * price:  55
            * out_order_id:  57
            * currency1: UAH
            * currency: LTC
            * nonce: 11

        Где :
            * nonce - целочисленней инкремент
            * Count - количество монет для покупки
            * Price - цена из расчета за одну монету
            * Currency1 - базовая валюта
            * Currency - валюта торга
            * Out_order_id - внешний идентификатор, принимающий произвольное значение

        И HTTP загаловками :
            * public-key - публичный ключ
            * api-sign - хеш сумма SHA256, сформированная от тела POST запроса с добавлением приватного ключа в конце, \
            например:

                count=0.8851641964&price=55&nonce=11&out_order_id=55&currency1=UAH&currency=LTC$privat_key

                $privat_key - ваш публичный ключ

        В случае успеха ответом будет JSON объект вида :

        .. code-block:: javascript

            {
                "status": true,
                "description": "The order has been created",
                "oder_id": 1
            }

        * order_id - будет содержать внутренний идентификатор в системе, \
        по которому можно будет проверить состояние вашей заявки

        Сразу же после выполнения заявки, начинается поиск обратного предложения для нее. \
        Если система находит предложение удовлетворяющее вашим условиям - система проводит сделку купли/продажи.
        """

        deal = getdeal(currency_from, currency_to)
        if not deal:
            raise ImpossibleDeal()
        if not order:
            order = self.order
        #time.sleep(self.timespace)
        return self.makepost('/buy/%s' % deal, currency1=currency_from, currency=currency_to, price=price, count=count, out_order_id=order, nonce=nonce)

    @dealsfilter
    @checknonce
    def opened_orders(self, deal, order=None, nonce=None):
        """
        :param deal:
        :param order:
        :param nonce:
        :return:

        Получение списка открытых заявок

        Для провеки статуса выполнения заявок необходимо сформировать запрос на url, в данном случае по валютной паре BTC/UAH :

            https://btc-trade.com.ua/api/my_orders/btc_uah

        С POST параметрами
            * out_order_id:  58
            * nonce: 12

        Где :
            * nonce - целочисленней инкремент
            * Out_order_id - внешний идентификатор, принимающий произвольное значение

        И HTTP загаловками :
            * api-sign - хеш сумма SHA256, сформированная от тела POST запроса с добавлением приватного ключа в конце, \
            например:

                out_order_id=58&nonce=12$privat_key

                $privat_key - ваш приватный  ключ

            * public-key - публичный ключ

         В случае успеха ответом будет JSON объект вида :

         .. code-block: javascript

                {
                    "your_open_orders": [
                        {
                            "amnt_base": "1538.2358440000",
                            "pub_date": "Oct. 18, 2014, 7:40 p.m.",
                            "price": "5400.0000000000",
                            "sum2": "1538.2358440000",
                            "sum1": "0.2848584896",
                            "amnt_trade": "0.2848584896",
                            "type": "sell",
                            "id": 4624
                        },
                        {
                            "amnt_base": "1159.4200000000", "pub_date": "Oct. 14, 2014, 8:57 p.m.",
                            "price": "5800.0000000000", "sum2": "1159.4200000000", "sum1": "0.1999000000",
                            "amnt_trade": "0.1999000000", "type": "sell", "id": 4405
                        }, {
                            "amnt_base": "1258.3137610000", "pub_date": "Oct. 10, 2014, 9:18 p.m.",
                            "price": "6200.0000000000", "sum2": "1258.3137610000", "sum1": "0.2029538324",
                            "amnt_trade": "0.2029538324", "type": "sell", "id": 4052
                        }
                    ],
                    "balance_buy": "0.0000396100",
                    "auth": true,
                    "balance_sell": "0.0000000000"
                }

        Поле your_open_orders содержит  список ваших открытых заявок на покупку/продажу.

            * id - идентификатор заявки
            * type - типа
                * покупка - buy
                * продажа - sell
            * amnt_trade - сумма в валюте торга
            * amnt_base - сумма в базовой валюте
            * price - цена из расчета за одну единицу валюты торга
        """
        return self.makepost('/my_orders/%s' % deal, out_order_id=order, nonce=nonce)

    @checknonce
    def order_status(self, order_id, order=None, nonce=None):
        """
        :param order_id:
        :param order:
        :param nonce:
        :return:

        Проверка статуса выполнения  заявки

        Для провеки статуса выполнения заявок необходимо сформировать запрос на url:

            https://btc-trade.com.ua/api/order/status/$id

        С POST параметрами
            * out_order_id:  59
            * nonce: 13

        Где :
            * nonce - целочисленней инкремент
            * out_order_id - внешний идентификатор, принимающий произвольное значение
            * $id - идентификатор полученный при создании заявки

        И HTTP загаловками :
            * public-key - публичный ключ
            * api-sign - хеш сумма SHA256, сформированная от тела POST запроса с добавлением приватного ключа в конце, \
            например:

                nonce=13&out_order_id=58$privat_key

                $privat_key - ваш  приватный  ключ

        В случае успеха ответом будет JSON объект вида :

        .. code-block: javascript

            {
                "status": "processing",
                "sum2_history": "1538.2358440000",
                "currency1": "BTC",
                "sum2": "1538.2358440000",
                "sum1": "0.2848584896",
                "currency2": "BTC",
                "sum1_history": "0.2848584896",
                "pub_date": "2014-10-18 19:40:20",
                "id": "4624"
            }

        * status - принимает значение
            * processing - в работе,
            * processed - выполнена,
            * canceled - отменена
        * sum1_history - заявочная сумма продажи
        * sum2_history - заявочная сумма покупки
        * sum1 - оставшаяся сумма продажи
        * sum2 - оставшаяся сумма продажи
        * currency1 - валюта продажи
        * currency2 - валюта покупки
        * id - идентификатор заявки
        * pub_date - дата заявки
        """
        return self.makepost('/order/status/%s' % order_id, out_order_id=order, nonce=nonce)

    @checknonce
    def remove_order(self, order_id, order=None, nonce=None):
        """
        :param self:
        :param order_id:
        :param order:
        :param nonce:
        :return:

        Удаление  заявки:

        Для провеки статуса выполнения заявок необходимо сформировать запрос на url:

            https://btc-trade.com.ua/api/order/remove/$id

        С POST параметрами
            * out_order_id:  90
            * nonce: 14

        Где :
            * Out_order_id - внешний идентификатор, принимающий произвольное значение
            * $id - идентификатор полученный при создании заявки

        И HTTP загаловками :
            * public-key - публичный ключ
            * api-sign - хеш сумма SHA256, сформированная от тела POST запроса с добавлением приватного ключа в конце, \
            например:

                nonce=14&out_order_id=90$privat_key

                $privat_key - ваш приватный ключ

         В случае успеха ответом будет JSON объект вида :

         .. code-block:: javascript

            {
                "status": true
            }
        """
        return self.makepost('/remove/order/%s' % order_id, out_order_id=order, nonce=nonce)

    @dealsfilter
    @checknonce
    def get_cost_of_buying(self, deal, amount, order=None, nonce=None):
        """
        :param deal:
        :param amount:
        :param order:
        :param nonce:
        :return:

        Получение стоимости покупки 1 коина

        Этот поможет узнать сколько будет стоить покупка одного коина в базовой валюте.
        Возьмем для примера bitcoin

            https://btc-trade.com.ua/api/ask/btc_uah

        С POST параметрами
            * out_order_id:  59
            * amount:1.01
            * nonce: 17

        Где :
            * nonce - целочисленней инкремент
            * Out_order_id - внешний идентификатор, принимающий произвольное значение
            * Amount - количество монет желаемой покупки

        И HTTP загаловками :
            * public-key - публичный ключ
            * api-sign - хеш сумма SHA256, сформированная от тела POST запроса с добавлением приватного ключа в конце, \
            например :

                nonce=17&out_order_id=58&amount=1.01$privat_key

                $privat_key - ваш приватный ключ

         В случае успеха ответом будет JSON объект вида :

         .. code-block:: javascript

            {
                "status": true,
                "avarage_price": "6500.0000000000",
                "min_price": "6500.0000000000",
                "buy_sum": "1.0000000000",
                "max_price": "6500.0000000000",
                "amount2pay": "6500.0000000000"
            }

        * status - результат запроса true или false
        * avarage_price - средняя цена покупки
        * min_price - минимальная цена в выборке
        * max_price - максимальная цена в выборке
        * amount2pay - сумма к оплате в базовой валюте
        * buy_sum - сумма покупки
        """
        return self.makepost('/ask/%s' % deal, amount=amount, out_order_id=order, nonce=nonce)

    @dealsfilter
    @checknonce
    def get_cost_of_selling(self, deal, amount, order=None, nonce=None):
        """
        :param deal:
        :param amount:
        :param order:
        :param nonce:
        :return:

        Получение стоимости продажи 1 коина

        Этот поможет узнать сколько будет стоить продажа одного коина в базовой валюте.
        Возьмем для примера bitcoin:

            https://btc-trade.com.ua/api/bid/btc_uah

        С POST параметрами
        * out_order_id:  59
        * amount:1.01
        * nonce: 18

        Где :
            * nonce - целочисленней инкремент
            * Out_order_id - внешний идентификатор, принимающий произвольное значение
            * Amount - количество монет желаемой продажи

        И HTTP загаловками :
            * public-key - публичный ключ
            * api-sign - хеш сумма SHA256, сформированная от тела POST запроса с добавлением приватного ключа в конце, \
            например  :

                out_order_id=58&amount=1.01&nonce=18$privat_key

                $privat_key - ваш приватный ключ

         В случае успеха ответом будет JSON объект вида :

         .. code-block:: javascript

            {
                "status": true,
                "avarage_price": "6300.0000000000",
                "min_price": "6300.0000000000",
                "buy_sum": "6300.0000000000",
                "max_price": "6300.0000000000",
                "amount2pay": "1.0000000000"
            }

        * status - результат запроса true или false
        * avarage_price - средняя цена продажи из расчета за одну монету
        * min_price - минимальная цена в выборке заявок
        * max_price - максимальная цена в выборке заявок
        * amount2pay - сумма продажи в  валюте торга
        * buy_sum - сумма вырученная за сделку
        """
        return self.makepost('/bid/%s' % deal, amount=amount, out_order_id=order, nonce=nonce)
