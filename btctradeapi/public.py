from requestmaker import RequestMaker
from exceptions import UnknownDeal
from deals import DEALS


class PublicAPI(RequestMaker):

    def deals(self, deal):
        if deal not in DEALS.getitems():
            raise UnknownDeal(deal)

        return self.makeget('/deals/%s' % deal)