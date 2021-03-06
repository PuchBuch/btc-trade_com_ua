from functools import wraps

from exceptions import UnknownDeal
from deals import DEALS


def dealsfilter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        deal = args[1]
        if deal not in DEALS.getitems():
            raise UnknownDeal
        return func(*args, **kwargs)
    return wrapper

def autoordered(func):
    @wraps(func)
    def wrapper(classinstance, deal, *args, **kwargs):
        if 'order' not in kwargs:
            kwargs.update(order=1)
        return func(classinstance, deal, *args, **kwargs)
    return wrapper

def checknonce(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        classinstance = args[0]
        if classinstance.nonce == 1:
            classinstance.auth()
        return func(*args, **kwargs)
    return wrapper
