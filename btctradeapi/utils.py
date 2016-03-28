from deals import DEALS


def getdeal(currency1, currency2):
    possible_deal = "_".join((currency1.lower(), currency2.lower()))
    if possible_deal in DEALS.getitems():
        return possible_deal
    else:
        possible_deal = "_".join((currency2.lower(), currency1.lower()))
        if possible_deal in DEALS.getitems():
            return possible_deal
    return None
