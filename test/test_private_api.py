import unittest2
import json

import btctradeapi
from btctradeapi.private import PrivateAPI
from btctradeapi.deals import DEALS


class TestPrivateAPI(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        json_data = json.load(open('test/keys.sec'))
        cls.api = PrivateAPI(json_data['pubkey'], json_data['privkey'])

    def test_auth(self):
        auth_result = self.api.auth()
        self.assertEqual(auth_result['status'], True)
        self.assertEqual(auth_result['public_key'], self.api.pubkey)

    def test_balance(self):
        balance_result = self.api.balance()
        self.assertIn('msg_count', balance_result.keys())
        self.assertIn('accounts', balance_result.keys())

    def test_sell(self):
        sell_uah_to_doge = self.api.sell(currency_from='DOGE', currency_to='UAH', count=10, price=0.0051)
        self.assertEquals(sell_uah_to_doge['status'], True)

    def test_buy(self):
        buy_doge_with_uah = self.api.buy(currency_from='UAH', currency_to='DOGE', count=10, price=0.0056)
        self.assertEqual(buy_doge_with_uah['status'], "processed")

    def test_opened_orders(self):
        doge_uah_opened_orders_list = self.api.opened_orders('doge_uah')
        self.assertIsInstance(doge_uah_opened_orders_list['your_open_orders'], list)

