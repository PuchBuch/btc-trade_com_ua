from requestmaker import RequestMaker


class PrivateAPI(RequestMaker):

    def __init__(self, pubkey, privkey):
        super(PrivateAPI, self).__init__()
        self.pubkey = pubkey
        self.privkey = privkey