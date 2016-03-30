import unittest2
import json

import btctradeapi
from btctradeapi.public import PublicAPI
from btctradeapi.deals import DEALS
from btctradeapi.types import Deals, Sells, Buyies


class TestPublicAPI(unittest2.TestCase):

    def setUp(self):
        self.api = PublicAPI()

    def test_deals(self):
        deals_btc_uah = self.api.deals(DEALS.btc_uah)
        self.assertIsInstance(deals_btc_uah, Deals)

    def test_sells(self):
        sells_doge_uah = self.api.sells(DEALS.doge_uah)
        self.assertIsInstance(sells_doge_uah, Sells)

    def test_buyies(self):
        buyies_btc_uah = self.api.buyies(DEALS.btc_uah)
        self.assertIsInstance(buyies_btc_uah, Buyies)
