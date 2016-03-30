import unittest2
import json


from btctradeapi import types


class TestTypesParsing(unittest2.TestCase):

    def test_Deals(self):
        data = json.load(open('test/data/deals.json'))

        result = types.Deals.parse_json(data)
        #print result
        self.assertIsInstance(result, types.Deals)

    def test_Buyies(self):
        data = json.load(open('test/data/buyies.json'))

        result = types.Buyies.parse_json(data)
        #print result
        self.assertIsInstance(result, types.Buyies)

    def test_Sells(self):
        data = json.load(open('test/data/sells.json'))

        result = types.Sells.parse_json(data)
        print result
        self.assertIsInstance(result, types.Sells)
