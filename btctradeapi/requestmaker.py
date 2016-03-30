# -*- coding: utf-8 -*-

import time
import json

import requests

from exceptions import ConnectionError


class RequestMaker(object):

    base_api_url = 'https://btc-trade.com.ua/api'
    timebase = 3

    def __init__(self):
        self.session = requests.Session()
        self.proxies = {}

    def sendrequest(self, prepared):
        time.sleep(self.timebase)
        if len(self.proxies) != 0:
            response = self.session.send(prepared, proxies=self.proxies)
        else:
            response = self.session.send(prepared)
        return response

    def set_proxy(self, proxy):
        """
        Sets the proxy...
        :param proxy: proxy url (like https://212.23.31.21:333)
        :return: NoneType
        """
        self.proxies.update(https=proxy)

    def cleanup_proxy(self):
        """
        Cleans proxy
        :return: NoneType
        """
        del self.proxies['https']

    def makeget(self, url, **params):
        """
        Makes GET request
        :param url: url for request
        :param params: additional params
        :return: dict-base object
        """
        req = requests.Request('GET', self.base_api_url+url, data=params)
        prepared = req.prepare()

        response = self.sendrequest(prepared)

        if response.status_code != 200:
            raise ConnectionError
        return json.loads(response.content)

    def makepost(self, url, **params):
        """
        Makes POST request
        :param url: url for request
        :param params: additional params
        :return: dict-base object
        """
        req = requests.Request('POST', self.base_api_url+url, data=params)
        prepared = req.prepare()

        response = self.sendrequest(prepared)

        if response.status_code != 200:
            raise ConnectionError
        return json.loads(response.content)
