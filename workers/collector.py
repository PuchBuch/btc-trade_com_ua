from btctradeapi import config
from btctradeapi.deals import DEALS
from btctradeapi.exceptions import UnknownDeal
from btctradeapi.worker import Worker
from btctradeapi.public import PublicAPI
from app.storage import Storage


class InfoCollector(Worker):

    def __init__(self, deal):
        if deal not in DEALS.getitems():
            raise UnknownDeal(deal)

        super(InfoCollector, self).__init__(
            PublicAPI(),
            Storage()
        )
        self.deal = deal


    def jobcycle(self):

        deals = self.api.deals(self.deal)
        self.storage.put_object()
