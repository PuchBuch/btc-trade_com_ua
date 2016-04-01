from btctradeapi import config
from btctradeapi.deals import DEALS
from btctradeapi.exceptions import UnknownDeal
from btctradeapi.worker import Worker
from btctradeapi.public import PublicAPI
from app.models import CycleIterationStateSnapshot, Sell, Buy, Deal, Deals
from btctradeapi.config import DB

class InfoCollector(Worker):

    def __init__(self, deal):
        if deal not in DEALS.getitems():
            raise UnknownDeal(deal)

        super(InfoCollector, self).__init__(
            PublicAPI(),
        )
        self.deal = deal

    class States:
        NewState = "NewState"

    def getinitial(self):
        return self.States.NewState

    def transitions(self):
        pass

    def jobcycle(self):

        print "getting new data..."

        try:

            btc_deals = self.api.deals(self.deal)
            btc_sells = self.api.sells(self.deal)
            btc_buyies = self.api.buyies(self.deal)
        except:
            return

        print "new data was gotten..."
        with DB.transaction():
            deals = Deals.create(deal=self.deal)

            snaphost=CycleIterationStateSnapshot.create(
                deal=self.deal,
                sells=Sell.from_type(btc_sells),
                buyies=Buy.from_type(btc_buyies),
                deals=deals
            )

            for index, deal in enumerate(btc_deals.items):
                deal = Deal.from_type(deal)
                deal.deals = deals
                deal.save()

        print "snapshot saved with timestamp %s" % snaphost.timestamp