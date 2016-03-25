class DEALS:
    drk_ltc='drk_ltc'
    hiro_ltc='hiro_ltc'
    vtc_btc='vtc_btc'
    ltc_btc='ltc_btc'
    clr_btc='clr_btc'
    hiro_btc='hiro_btc'
    vtc_ltc='vtc_ltc'
    ppc_btc='ppc_btc'
    nvc_ltc='nvc_ltc'
    ltc_uah='ltc_uah'
    nvc_btc='nvc_btc'
    btc_uah='btc_uah'
    drk_btc='drk_btc'
    doge_uah='doge_uah'
    clr_uah='clr_uah'
    ppc_ltc='ppc_ltc'
    nvc_uah='nvc_uah'

    @classmethod
    def getitems(cls):
        result = []
        items = cls.__dict__.keys()
        for item in items:
            if callable(getattr(cls, item)):
                continue
            if item.startswith('_'):
                continue
            result.append(item)
        return result
