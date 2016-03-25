import unittest2
import json

import btctradeapi
from btctradeapi.public import PublicAPI


class TestPublicAPI(unittest2.TestCase):

    def setUp(self):
        self.api = PublicAPI()

    def test_deals(self):
        deals_btc_uah = self.api.deals('btc_uah')
        self.assertIsInstance(deals_btc_uah, list)