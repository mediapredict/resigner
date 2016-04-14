import time
import urlparse
from urllib import urlencode

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from resigner.models import ApiKey
from resigner import querystring


class TestQueryString(TestCase):

    def setUp(self):
        self.apikey = ApiKey.objects.create()

    def test_kfid_in_querystring(self):
        signed_qs = querystring.sign({"kfid": 1}, key=self.apikey.key, secret=self.apikey.secret)
        self.assertTrue("kfid=1" in signed_qs)

    def test_key_in_querystring(self):
        signed_qs = querystring.sign({"kfid": 1}, key=self.apikey.key, secret=self.apikey.secret)
        self.assertTrue("key={0}".format(self.apikey.key) in signed_qs)

    def test_signature_in_querystring(self):
        signed_qs = querystring.sign({"kfid": 1}, key=self.apikey.key, secret=self.apikey.secret)
        params = dict(urlparse.parse_qsl(signed_qs))
        self.assertTrue("signature={0}".format(params["signature"]) in signed_qs)

    def test_validate(self):
        signed_qs = querystring.sign(
            {"kfid": 1, "next":"https://www.mediapredict.com"},
            key=self.apikey.key,
            secret=self.apikey.secret,
        )
        self.assertTrue(querystring.validate(str(signed_qs)))

    def test_fail_if_signed_request_expired(self):
        signed_qs = querystring.sign({"kfid": 1}, key=self.apikey.key, secret=self.apikey.secret)
        time.sleep(1)
        self.assertRaises(querystring.ValidationError, querystring.validate, signed_qs, max_age=0)

    def test_fail_if_signed_request_has_wrong_key(self):
        signed_qs = querystring.sign({"kfid": 1}, key="cheese", secret=self.apikey.secret)
        self.assertRaises(querystring.ValidationError, querystring.validate, signed_qs)

    def test_fail_if_signed_request_has_wrong_signature(self):
        signed_qs = querystring.sign({"kfid": 1}, key=self.apikey.key, secret="cheese")
        self.assertRaises(querystring.ValidationError, querystring.validate, signed_qs)
