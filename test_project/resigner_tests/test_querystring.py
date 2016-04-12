import time
from urllib import urlencode

from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from resigner.models import ApiKey
from resigner.querystring import sign, validate


class TestQueryString(TestCase):
    def setUp(self):
        self.factory = RequestFactory
        self.timestamp = str(int(time.time()))
        self.params = {"kfid": 1, "next":"/"}
        self.api_key_obj = ApiKey.objects.create()
        self.api_key = self.api_key_obj.key
        self.api_secret = self.api_key_obj.secret
        self.signature = sign(self.params, self.api_key, self.api_secret)
        self.params["key"] = self.api_key
        self.params["timestamp"] = self.timestamp
        self.querystring = urlencode(self.params)

    def test_sign(self):
        self.assertEquals(self.signature, self.querystring)

    # def test_validate(self):
    #     req = self.factory.get('/my_test_api_url/')
    #     print(req)
    #     self.assertEquals(validate(self.querystring), True)