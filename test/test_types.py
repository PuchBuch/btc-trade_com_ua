import unittest2
import json


from btctradeapi import types


class TestTypesParsing(unittest2.TestCase):

    def test_Deals(self):
        data = json.load(open('test/data/deals.json'))

        result = types.Deals.parse_json(data)
        #print result
        self.assertIsInstance(result, types.Deals)