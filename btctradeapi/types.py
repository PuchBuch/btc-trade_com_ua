import sys

from abc import abstractmethod
from collections import namedtuple
import datetime
import dateparser
from btctradeapi.exceptions import UnknownOperationType


def to_model_func_setter(instance, func):
    setattr(instance, 'to_model', func)


def parse_DateTime(str_datetime):
    #import ipdb; ipdb.set_trace()
    try:
        return datetime.datetime.strptime(
                str_datetime, "%Y%m%d %H:%M:%S")
    except (Exception):
        e = sys.exc_info()[1]
        #print e
        try:
            return datetime.datetime.strptime(
                str_datetime, "%Y-%m-%d %H:%M:%S")
        except (Exception):
            e = sys.exc_info()[1]
            #print e
            try:
                return dateparser.parse(str_datetime)
            except (Exception):
                e = sys.exc_info()[1]
                #print e
                import ipdb; ipdb.set_trace()
                return dateparser.parse(unicode(str_datetime))


def basetuple_proxy(dealname):
    return basetuple(dealname)


class ParseFuncs:
    pass
ParseFuncs = ParseFuncs()


def parse_Status(data):
    return data


class Operations:
    SELL = dict(int=0, str="sell")
    BUY = dict(int=1, str="buy")


class OrderStatuses:
    PROCESSING = dict(int=0, str="processing")
    PROCESSED = dict(int=1, str="processed")
    CANCELED = dict(int=2, str="canceled")


def parse_Operation(operation):
    got_operation = None
    for key in Operations.__dict__.keys():
        #import ipdb; ipdb.set_trace()
        if key.isupper() and not key.startswith('_'):
            item = getattr(Operations, key)
            if isinstance(operation, int):
                if item['int'] == operation:
                    got_operation = item
            if isinstance(operation, (str, unicode)):
                if item['str'] == operation:
                    got_operation = item
    return got_operation


def parse_OrderStatusString(data):
    #import ipdb; ipdb.set_trace()
    if isinstance(data, bool):
        return data
    if data.upper() in OrderStatuses.__dict__.keys():
        return getattr(OrderStatuses, data.upper())


def parse_ErrorDescription(json_data):
    return dict(status=json_data['status'], description=json_data['description'])


ParseFuncs.parse_Operation = parse_Operation


parse_AccountsList = lambda json_data: None
ParseFuncs.parse_AccountsList = staticmethod(parse_AccountsList)


reserved_words = [
    'and',
    'del',
    'from',
    'not',
    'while',
    'as',
    'elif',
    'global',
    'or',
    'with',
    'assert',
    'else',
    'if',
    'pass',
    'yield',
    'break',
    'except',
    'import',
    'print',
    'class',
    'exec',
    'in',
    'raise',
    'continue',
    'finally',
    'is',
    'return',
    'def',
    'for',
    'lambda',
    'try'
]


class Synonim:
    def __init__(self, of_what):
        self.of_what = of_what


fields = {
    'ErrorWithDescription': {
        'status': parse_Status,
        'description': str,
    },
    'Error': str,
    'DateTime': parse_DateTime,
    'Operation': parse_Operation,
    'Status': parse_Status,
    'CurrencyName': Synonim(str),

    'Deal': {
        'user': str,
        'amnt_base': float,
        'amnt_trade': float,
        'price': float,
        'pub_date': 'DateTime',
        'type': 'Operation',
    },
    'Deals': (list, 'Deal'),

    'Buyies': {
        'min_price': float,
        'max_price': float,
        'orders_sum': float,
        'list': 'BuyiesList',
    },
    'BuyItem': {
        'currency_base': float,
        'currency_trade': float,
        'price': float,
    },
    'SellItem': {
        'currency_base': float,
        'currency_trade': float,
        'price': float
    },
    'BuyiesList': (list, 'BuyItem'),
    'SellsList': (list, 'SellItem'),
    'Sells': {
        'min_price': float,
        'max_price': float,
        'orders_sum': float,
        'list': 'SellsList',
    },
    #'SellItem': Synonim('BuyItem'),

    'Balance': {
        'msg_count': int,
        "accounts": (ParseFuncs, 'parse_AccountsList'),
        'use_f2a': bool,
        'notify_count': int
    },
    'AccountsList': (list, 'AccountItem'),
    'AccountItem': {
        'currency': str,
        'balance': float
    },

    'RequestBuy': {
        'status': bool,
        'description': str,
        #'oder_id': int,                # NOT PRESENT IN SERVER ANSWER
    },

    'RequestSell': { #Synonim('RequestBuy'), # SERVER ANSWER DIFFERS
        'status': parse_Status,
        'start_sum_to_buy': float,
        'last_sum_to_buy': float,
        'description': str
    },

    'Ask': {
        'status': 'Status',
        #'avarage_price': float,        # NOT PRESENT IN SERVER ANSWER
        #'min_price': float,            # NOT PRESENT IN SERVER ANSWER
        'buy_sum': float,
        #'max_price': float,            # NOT PRESENT IN SERVER ANSWER
        #'amount2pay': float            # NOT PRESENT IN SERVER ANSWER
        'price': float                  # NOT PRESENT IN OFFICIAL DOCS !!!
    },

    'Bid': \
        # Synonim('Ask'),                # NOT SINNONYM AS IN OFFICIAL DOCS !!!
        # own describion
        {
            'status': 'Status',
            'price': float,
            'sell_sum': float
        },

    'OpenedOrders': {
        'your_open_orders': 'YourOpenedOrdersList',
        'balance_buy': float,
        'auth': bool,
        'balance_sell': float
    },
    'YourOpenedOrdersList': (list, 'OpenedOrderItem'),
    'OpenedOrderItem': {
        'amnt_base': float,
        'amnt_trade': float,
        'price': float,
        'pub_date': parse_DateTime,
        'type': parse_Operation,
        'id': int,
        'sum1': float,
        'sum2': float
    },

    'OrderStatus': {
        'status': parse_OrderStatusString,
        'sum2_history': float,
        'currency1': Synonim('CurrencyName'),
        'sum2': float,
        'currency2': str,
        'sum1_history': float,
        'pub_date': parse_DateTime,
        'id': int
    },

    'RemoveOrderStatus': {
        'status': bool,
    },
}

def parse_list(type_name, json_data):
    result = []
    parser = basetuple(type_name)
    for item in json_data:
        result.append(parser.parse_json(item))
    return result


def parse_synonym(typename, json_data, basetypename=None):
    result = {}
    if isinstance(typename, str) and typename in fields:
        if basetypename:
            class_ = basetuple_proxy(basetypename)
        else:
            class_ = basetuple_proxy(typename)
        presult = basetuple_proxy(typename).parse_json(json_data)

        for key in presult.keys():
            result.update({key: presult[key]})
        return class_(**result)

    elif callable(typename):
        return typename(json_data)


def basetuple(
        dealname, name_as=None
):
    tuple_fields = fields.get(dealname, None)
    #import ipdb; ipdb.set_trace()
    #if not tuple_fields or not isinstance(tuple_fields, dict):
    #    raise ValueError()
    if isinstance(tuple_fields, tuple) and fields.get(dealname)[0] is list:
        newtuple = namedtuple(name_as if name_as else dealname, 'items')
        def parser(cls, json_data):
            listitems = parse_list(tuple_fields[1], json_data)
            return cls(items=listitems)
        setattr(newtuple, 'parse_json', classmethod(parser))
    elif isinstance(tuple_fields, Synonim):
        if callable(tuple_fields.of_what):
            class newtuple:
                pass
            def parser(cls, json_data):
                result = {}
                return tuple_fields.of_what(json_data)
            setattr(newtuple, 'parse_json', classmethod(parser))
        elif tuple_fields.of_what in fields:
            return basetuple(tuple_fields.of_what, name_as=dealname)

    elif isinstance(tuple_fields, dict):
        newtuple = namedtuple(name_as if name_as else dealname, tuple_fields.keys())
        def parser(cls, json_data):
            items = {}
            try:
                for key in tuple_fields.keys():
                    #try:
                    rkey = key if key not in reserved_words else key+'_'
                    item = tuple_fields.get(key)
                    if isinstance(item, tuple) and item[0] is list:
                        listitems = []
                        for listitem in json_data[key]:
                            listitems.append(fields.get(item[1]).parse_json(listitem))
                        items.update({
                            rkey: listitems
                        })
                    elif isinstance(item, tuple) and item[0] is ParseFuncs and isinstance(item[1], str):
                        #import ipdb; ipdb.set_trace()
                        items.update({
                            rkey: getattr(item[0], item[1])(json_data[key])
                        })
                    elif callable(item):
                        #import ipdb; ipdb.set_trace()
                        items.update({
                            rkey: item(
                                json_data.get(key, None))
                        })
                    elif isinstance(item, str) and callable(fields.get(item, None)):
                        items.update({
                            rkey: fields.get(item)(json_data.get(key))
                        })
                    elif isinstance(item, str) and isinstance(fields.get(item, None), tuple):
                        #print key
                        items.update({
                            rkey: parse_list(fields.get(item)[1], json_data[key])
                        })
                    elif isinstance(item, Synonim):
                        #import ipdb; ipdb.set_trace()
                        items.update({
                            rkey: basetuple(item.of_what).parse_json(json_data[key])
                        })
                    #print key
                    #if key == "accounts":
                    #   print item
                    #   import ipdb; ipdb.set_trace()
                return cls(**items)
                #except:
                #    import ipdb; ipdb.set_trace()
            except (TypeError):
                e = sys.exc_info()[1]
                if 'status' in json_data.keys():
                    if 'description' in json_data.keys():
                        return basetuple("ErrorWithDescription").parse_json(json_data)
                    else:
                        return basetuple("Error").parse_json(json_data)
                else:
                    raise ValueError(str(json_data))
        setattr(newtuple, 'parse_json', classmethod(parser))
    else:
        #import ipdb; ipdb.set_trace()
        raise ValueError()
    #import ipdb; ipdb.set_trace()
    return newtuple


def parse_AccountsList(json_data):
    list_items = parse_list("AccountItem", json_data)
    result = {}
    for item in list_items:
        try:
            result.update({item.currency: item.balance})
        except (Exception):
            e = sys.exc_info()[1]
            print(e)
            import ipdb; ipdb.set_trace()
    result.update(accounts_list=list_items)
    Accounts = namedtuple("Accounts", " ".join(result.keys()))
    return Accounts(**result)


ParseFuncs.parse_AccountsList = parse_AccountsList


for item in ParseFuncs.__dict__.keys():
    if item.startswith('parse_'):
        class_func = getattr(ParseFuncs, item)
        #setattr(ParseFuncs, item, staticmethod(class_func))


Deal = basetuple("Deal")
Deals = basetuple("Deals")

Buyies = basetuple("Buyies")
Sells = basetuple("Sells")

Balance = basetuple("Balance")

RequestBuy = basetuple("RequestBuy")
RequestSell = basetuple("RequestSell")

OpenedOrders = basetuple("OpenedOrders")
YourOpenedOrdersList = basetuple("YourOpenedOrdersList")
OrderStatus = basetuple("OrderStatus")
RemoveOrderStatus = basetuple("RemoveOrderStatus")

Ask = basetuple("Ask")
Bid = basetuple("Bid")


