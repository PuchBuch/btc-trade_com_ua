# -*- coding: utf-8 -*-

class DEALS:
    """
    1) btc_uah ­ BitCoin к гривне
    2) ltc_uah ­ LitCoin к гривне
    3) nvc_uah ­ NovaCoin к гривне
    4) clr_uah ­ CoperLark к гривне
    5) doge_uah ­ Doge к гривне
    6) ltc_btc ­ LiteCoin к BitCoin
    7) drk_btc ­ DarkCoin к BitCoin
    8) nvc_btc ­ NovaCoin к BitCoin
    9) vtc_btc ­ VertCoin к BitCoin
    10) clr_btc ­ CoperLark к BitCoin
    11) ppc_btc ­ Peercoin к BitCoin
    12) hiro_btc ­ HiroCoin к BitCoin
    13) ppc_ltc ­ Peercoin к LiteCoin
    14) drk_ltc ­ DarkCoin к LiteCoin
    15) nvc_ltc ­ NovaCoin к LiteCoin
    16) hiro_ltc ­ HiroCoin к LiteCoin
    17) vtc_ltc ­ VertCoin к LiteCoin
    """
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
