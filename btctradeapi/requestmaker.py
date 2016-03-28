# -*- coding: utf-8 -*-

import json

import requests

from exceptions import ConnectionError


class RequestMaker(object):

    base_api_url = 'https://btc-trade.com.ua/api'

    def makeget(self, url, **params):
        """
        Makes GET request
        :param url: url for request
        :param params: additional params
        :return: dict-base object
        """
        response = requests.get(self.base_api_url+url, params=params)
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
        response = requests.post(self.base_api_url+url, data=params)
        if response.status_code != 200:
            raise ConnectionError
        return json.loads(response.content)
