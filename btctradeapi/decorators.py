from exceptions import UnknownDeal
from deals import DEALS


def dealsfilter(func):

    def wrapper(classinstance, deal, *args, **kwargs):
        if deal not in DEALS.getitems():
            raise UnknownDeal
        return func(classinstance, deal, *args, **kwargs)
    return wrapper