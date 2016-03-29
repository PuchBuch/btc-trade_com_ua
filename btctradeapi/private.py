# -*- coding: utf-8 -*-

import json
import hashlib
import time

import requests

from requestmaker import RequestMaker
from exceptions import ConnectionError, ImpossibleDeal, UnknownDeal
from decorators import autoordered, dealsfilter
from deals import DEALS
from utils import getdeal


class PrivateAPI(RequestMaker):

    def __init__(self, pubkey, privkey):
        super(PrivateAPI, self).__init__()
        self.pubkey = pubkey
        self.privkey = privkey
        self.session = requests.Session()
        #TODO: fix multithreading resources race
        self.nonce = 1
        self.order = 1
        self.timespace = 5

    def makepost(self, url, **params):
        params.update(nonce=self.nonce, out_order_id=self.order)
        self.nonce += 1
        self.order += 1
        req = requests.Request('POST', url=self.base_api_url+url, data=params)
        req = req.prepare()
        req.headers['api-sign'] = hashlib.sha256(
            "%s%s" % (req.body, self.privkey)).hexdigest()
        req.headers['public-key'] = self.pubkey
        time.sleep(self.timespace)
        response = self.session.send(req)
        #import ipdb; ipdb.set_trace()
        print "url = '%s'\nPOST body='%s'\nHeaders = '%s'\nResponse: '%s'" % (req.url, req.body, req.headers, response.content)
        if response.status_code != 200:
            import ipdb; ipdb.set_trace()
            raise ConnectionError
        return json.loads(response.content)

    def auth(self):
        """
        Первый запрос для начала работы с торговым апи должен быть на url :

        https://btc-trade.com.ua/api/auth

            С POST параметром out_order_id равным произвольному значению и nonce равный целому произвольному числу. Воспользуемся командой curl :
            curl -k   -i -H "api-sign: 9925916858e6361ffb88fc0b71d763355ea979e3ac62a6acaa8fe4a8ba548abf" -H "public-key: 9e6ea26cc7314d6dea8359f8ed5de68b2b5f0ec8daa0d5eac96b86d2b44ada38"  --data "out_order_id=2&nonce=1" -v https://btc-trade.com.ua/api/auth

        :return:
        """
        return self.makepost('/auth', out_order_id=1)

    def balance(self):
        """
        После старта сессии, первый  запрос, который вам захочеться сделать - это наверняка проверить состояние вашего счета . Для этого необходимо cформировать POST запрос на url:
        https://btc-trade.com.ua/api/balance
        С POST параметром out_order_id равным произвольному значению и параметром nonce равный любому целочисленному числу, большем, чем число использованное в предыдущем запросе.
        Авторизация происходит путем добавление HTTP загаловков public-key и api-sign, где public-key - это публичный ключ из вашего личного кабинета, а api-sign подпись сформированная путем конкатенация вашего post запроса  и вашего  private_key, и получением хеш-функции SHA256 от полученной строки.
        Типовый запрос из командной строки при помощи команды curl :

        curl -k   -i -H "api-sign: 9925916858e6361ffb88fc0b71d763355ea979e3ac62a6acaa8fe4a8ba548abf" -H "public-key: 9e6ea26cc7314d6dea8359f8ed5de68b2b5f0ec8daa0d5eac96b86d2b44ada38"  --data "out_order_id=2&nonce=1" -v  https://btc-trade.com.ua/api/balance

        Результатом запроса будет :

            {"msg_count": 0, "accounts": [{"currency": "UAH", "balance": "1744.2104180000"}, {"currency": "BTC", "balance": "0.1205538600"}, {"currency": "LTC", "balance": "1.0266850207"}, {"currency": "NVC", "balance": "0.0000000000"}, {"currency": "DRK", "balance": "0.0000000000"}, {"currency": "VTC", "balance": "0.0000000000"}, {"currency": "PPC", "balance": "0.0000000000"}, {"currency": "HIRO", "balance": "999.5000000000"}], "use_f2a": false, "notify_count": 0}

            JSON - объект с полем accounts, содержащим список счетов по каждой ваюте.
            Внимание! Параметр out_order_id является обязательным и должен быть добавлен  к каждому POST запросу. Желательно его каждый раз изменять.


        :return:
        """

        return self.makepost('/balance', out_order_id=1)

    def sell(self, currency_from, currency_to, count, price, order=None):
        """
         Для этого необходимо cформировать POST запрос на url по выбранной вами валютной паре в данном случае LiteCoin/Гривна

        https://btc-trade.com.ua/api/sell/ltc_uah

        С POST параметрами
        count: 0.8851641964
        price:  55
        out_order_id:  55
        currency1: UAH
        currency: LTC
        nonce : 10

        Где :
            nonce - целочисленней инкремент
        Count - количество монет для продажи
        Price - цена из расчета за одну монету
        Currency1 - базовая валюта
        Currency - валюта торга
        Out_order_id - внешний идентификатор, принимающий произвольное значение

        И HTTP загаловками :
        public-key - публичный ключ
            api-sign - хеш сумма SHA256, сформированная от тела POST запроса с добавлением приватного ключа в конце, например:
        count=0.8851641964&nonce=10&price=55&out_order_id=55&currency1=UAH&currency=LTC$privat_key
            $privat_key - ваш приватный ключ

        Запрос при помощи команды curl:

        curl -k   -i -H "api-sign: 652167fcdc3d0f55cacd4f2eea27e2f2512669126b2ddf5b5cbdbd8e18c23592" -H "public-key: 9e6ea26cc7314d6dea8359f8ed5de68b2b5f0ec8daa0d5eac96b86d2b44ada38"
        --data "currency1=UAH&currency=BTC&count=0.003&price=6200&out_order_id=4&nonce=4" -v https://btc-trade.com.ua/api/sell/btc_uah

        В случае успеха ответом будет JSON объект вида :

            {"status": true, "description": "The order has been created", "oder_id": 1 }

            order_id - будет содержать внутренний идентификатор в системе, по которому можно будет проверить состояние вашей заявки

        :param deal:
        :param amount:
        :param order:
        :return:
        """
        deal = getdeal(currency_to, currency_from)
        if not deal:
            raise ImpossibleDeal()
        if not order:
            order = self.order
        #time.sleep(self.timespace)
        return self.makepost('/sell/%s' % deal, currency1=currency_from, currency=currency_to, price=price, count=count)

    def buy(self, currency_from, currency_to, count, price, order=None):
        """
         Заявка покупки формируется подобным образом, только на другой  url, для пары LiteCoin/Гривна:
        https://btc-trade.com.ua/api/buy/ltc_uah

        С POST параметрами
        count: 0.8851641964
        price:  55
        out_order_id:  57
        currency1: UAH
        currency: LTC
        nonce: 11

        Где :
        nonce - целочисленней инкремент
        Count - количество монет для покупки
        Price - цена из расчета за одну монету
        Currency1 - базовая валюта
        Currency - валюта торга
        Out_order_id - внешний идентификатор, принимающий произвольное значение

        И HTTP загаловками :
            api-sign - хеш сумма SHA256, сформированная от тела POST запроса с tpдобавлением приватного ключа в конце, например:
        count=0.8851641964&price=55&nonce=11&out_order_id=55&currency1=UAH&currency=LTC$privat_key
            $privat_key - ваш публичный ключ
            public-key - публичный ключ


        В случае успеха ответом будет JSON объект вида :
            {"status": true, "description": "The order has been created", "oder_id": 1 }

            order_id - будет содержать внутренний идентификатор в системе, по которому можно будет проверить состояние вашей заявки

              Сразу же после выполнения заявки, начинается поиск обратного предложения для нее. Если система находит предложение удовлетворяющее вашим условиям - система проводит сделку купли/продажи.


        :param currency_from:
        :param currency_to:
        :param count:
        :param price:
        :param order:
        :return:
        """

        deal = getdeal(currency_from, currency_to)
        if not deal:
            raise ImpossibleDeal()
        if not order:
            order = self.order
        #time.sleep(self.timespace)
        return self.makepost('/buy/%s' % deal, currency1=currency_from, currency=currency_to, price=price, count=count)
