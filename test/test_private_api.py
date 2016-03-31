import unittest2
from unittest2 import SkipTest
import json

import btctradeapi
from btctradeapi.private import PrivateAPI
from btctradeapi.deals import DEALS
from btctradeapi import types


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
        self.assertTrue(hasattr(balance_result, 'msg_count'))
        self.assertTrue(hasattr(balance_result, 'accounts'))

    #@unittest2.skip('waiting for answer in support')
    def test_sell(self):
        sell_uah_to_doge = self.api.sell(currency_from='UAH', currency_to='DOGE', count=10, price=0.0051)
        self.assertTrue((sell_uah_to_doge.status == "processed") or (sell_uah_to_doge.status is True))

    def test_buy(self):
        buy_doge_with_uah = self.api.buy(currency_from='UAH', currency_to='DOGE', count=10, price=0.0056)
        self.assertTrue((buy_doge_with_uah.status == "processed") or (buy_doge_with_uah.status is True))

    def test_opened_orders(self):
        doge_uah_opened_orders_list = self.api.opened_orders('doge_uah')
        print doge_uah_opened_orders_list
        self.assertIsInstance(doge_uah_opened_orders_list.your_open_orders, list)

    @unittest2.skip('waiting for answer in support')
    def test_order_status(self):
        order_status = self.api.order_status(1)
        self.assertIsInstance(order_status, types.OrderStatus)

    @unittest2.skip('waiting for answer in support')
    def test_remove_order(self):
        remove_order = self.api.remove_order(1)
        self.assertIsInstance(remove_order, types.RemoveOrderStatus)

    def test_get_cost_of_buying(self):
        cost_of_buying_btc = self.api.get_cost_of_buying(DEALS.btc_uah, amount=1)
        self.assertIsInstance(cost_of_buying_btc, types.Ask)

    def test_get_cost_of_selling(self):
        cost_of_selling_btc = self.api.get_cost_of_selling(DEALS.btc_uah, amount=1)
        #print cost_of_selling_btc
        self.assertIsInstance(cost_of_selling_btc, types.Bid)

