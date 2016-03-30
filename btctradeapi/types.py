from abc import abstractmethod
from collections import namedtuple
import datetime
import dateparser
from exceptions import UnknownOperationType


def to_model_func_setter(instance, func):
    setattr(instance, 'to_model', func)


def parse_DateTime(str_datetime):
    #import ipdb; ipdb.set_trace()
    try:
        return datetime.datetime.strptime(
                str_datetime, "%Y%m%d %H:%M:%S")
    except:
        return dateparser.parse(str_datetime)


class Operations:
    SELL = dict(int=0, str="sell")
    BUY = dict(int=1, str="buy")


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


fields = {
    'DateTime': parse_DateTime,
    'Operation': parse_Operation,

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
    'BuyiesList': (list, 'BuyItem'),
}


def parse_list(type_name, json_data):
    result = []
    parser = basetuple(type_name)
    for item in json_data:
        result.append(parser.parse_json(item))
    return result


def basetuple(
        dealname,
):
    tuple_fields = fields.get(dealname, None)
    #import ipdb; ipdb.set_trace()
    #if not tuple_fields or not isinstance(tuple_fields, dict):
    #    raise ValueError()
    if isinstance(tuple_fields, tuple):
        newtuple = namedtuple(dealname, 'items')
        def parser(cls, json_data):
            listitems = parse_list(tuple_fields[1], json_data)
            return cls(items=listitems)
        setattr(newtuple, 'parse_json', classmethod(parser))

    elif isinstance(tuple_fields, dict):
        newtuple = namedtuple(dealname, tuple_fields.keys())
        def parser(cls, json_data):
            items = {}
            for key in tuple_fields.keys():
                rkey = key if key not in reserved_words else key+'_'
                item = tuple_fields.get(key)
                #if key == "list":
                #   print item
                #   import ipdb; ipdb.set_trace()
                if isinstance(item, tuple) and item[0] is list:
                    listitems = []
                    for listitem in json_data[key]:
                        listitems.append(fields.get(item[1]).parse_json(listitem))
                    items.update({
                        rkey: listitems
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

            return cls(**items)
        setattr(newtuple, 'parse_json', classmethod(parser))
    else:
        raise ValueError()
    #import ipdb; ipdb.set_trace()
    return newtuple


Deal = basetuple("Deal")
Deals = basetuple("Deals")

Buyies = basetuple("Buyies")
Sells = basetuple("Buyies")
