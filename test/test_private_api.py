import unittest2
import json

import btctradeapi
from btctradeapi.private import PrivateAPI


class TestPrivateAPI(unittest2.TestCase):

    def setUp(self):
        json_data = json.load(open('test/keys.sec'))
        self.api = PrivateAPI(json_data['pubkey'], json_data['privkey'])

    def test_auth(self):
        auth_result = self.api.auth()
        self.assertEqual(auth_result['status'], True)
        self.assertEqual(auth_result['public_key'], self.api.pubkey)

