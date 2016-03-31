import unittest2
import json


from btctradeapi import types


def parse_file_as_Type(filename, Type):
    return Type.parse_json(json.load(open(filename)))


class TestTypesParsing(unittest2.TestCase):

    def test_Deals(self):
        result = parse_file_as_Type(
            'test/data/deals.json', types.Deals)
        self.assertIsInstance(result, types.Deals)

    def test_Buyies(self):
        result = parse_file_as_Type(
            'test/data/buyies.json', types.Buyies)

        self.assertIsInstance(result, types.Buyies)

    def test_Sells(self):
        result = parse_file_as_Type(
            'test/data/sells.json', types.Sells)

        self.assertIsInstance(result, types.Sells)

    def test_Balance(self):
        result = parse_file_as_Type(
            'test/data/balance.json', types.Balance)
        #print result
        self.assertIsInstance(result, types.Balance)

    def test_RequestBuy(self):
        result = parse_file_as_Type(
            'test/data/requestbuy.json', types.RequestBuy)
        #print result
        self.assertIsInstance(result, types.RequestBuy)

    def test_Ask(self):
        result = parse_file_as_Type(
            'test/data/ask.json', types.Ask)
        #print result
        self.assertIsInstance(result, types.Ask)

    def test_Bid(self):
        result = parse_file_as_Type(
            'test/data/bid.json', types.Bid)
        #print result
        self.assertIsInstance(result, types.Bid)

    def test_OpenedOrders(self):
        result = parse_file_as_Type(
            'test/data/openedorders.json', types.OpenedOrders)
        #print result
        self.assertIsInstance(result, types.OpenedOrders)

    def test_OrderStatus(self):
        result = parse_file_as_Type(
            'test/data/orderstatus.json', types.OrderStatus)
        #print result
        #import ipdb; ipdb.set_trace()
        self.assertIsInstance(result, types.OrderStatus)

    def test_RemoveOrderStatus(self):
        result = parse_file_as_Type(
            'test/data/removeorderstatus.json', types.RemoveOrderStatus)
        #print result
        #import ipdb; ipdb.set_trace()
        self.assertIsInstance(result, types.RemoveOrderStatus)

    def test_RequestSell(self):
        result = parse_file_as_Type(
            'test/data/requestsell.json', types.RequestSell)
        #print result
        #import ipdb; ipdb.set_trace()
        self.assertIsInstance(result, types.RequestSell)
