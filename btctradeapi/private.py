import json
import hashlib

import requests

from requestmaker import RequestMaker
from exceptions import ConnectionError


class PrivateAPI(RequestMaker):

    def __init__(self, pubkey, privkey):
        super(PrivateAPI, self).__init__()
        self.pubkey = pubkey
        self.privkey = privkey
        self.session = requests.Session()

    def makepost(self, url, **params):
        req = requests.Request('POST', url=self.base_api_url+url, data=params)
        req = req.prepare()
        req.headers['api-sign'] = hashlib.sha256(
            "%s%s" % (req.body, self.privkey)).hexdigest()
        req.headers['public-key'] = self.pubkey
        response = self.session.send(req)
        #import ipdb; ipdb.set_trace()
        if response.status_code != 200:
            raise ConnectionError
        return json.loads(response.content)

    def auth(self):
        return self.makepost('/auth', out_order_id=1, nonce=1)