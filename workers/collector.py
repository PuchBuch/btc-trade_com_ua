from btctradeapi import config
from btctradeapi.deals import DEALS
from btctradeapi.exceptions import UnknownDeal
from btctradeapi.worker import Worker
from btctradeapi.public import PublicAPI
from app.models import CycleIterationStateSnapshot, Sell, Buy, Deal


class InfoCollector(Worker):

    def __init__(self, deal):
        if deal not in DEALS.getitems():
            raise UnknownDeal(deal)

        super(InfoCollector, self).__init__(
            PublicAPI(),
        )
        self.deal = deal


    def jobcycle(self):

        deals = self.api.deals(self.deal)

        sells = self.api.sells(self.deal)

        buyies = self.api.buyies(self.deal)

        snaphost=CycleIterationStateSnapshot.create(
            deal=self.deal,
        )

