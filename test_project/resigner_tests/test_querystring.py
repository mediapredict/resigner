from urllib.parse import parse_qsl

from django.test import TestCase

from resigner.models import ApiKey
from resigner import querystring


class TestQueryString(TestCase):
    def setUp(self):
        self.apikey = ApiKey.objects.create()

    def test_keys_present_in_querystring(self):
        one_day_expiration = 24 * 60 * 60
        signed_qs = querystring.sign(
            {"kfid": 1}, self.apikey.key, self.apikey.secret, one_day_expiration
        )

        self.assertTrue("kfid=1" in signed_qs)
        self.assertTrue(f"key={self.apikey.key}" in signed_qs)
        self.assertTrue(f"_expiry={one_day_expiration}" in signed_qs)

        signature = dict(
            parse_qsl(signed_qs)
        )['signature']
        self.assertTrue(f"signature={signature}" in signed_qs)

    def test_validate(self):
        signed_qs = querystring.sign(
            {"kfid": 1, "next":"https://www.mediapredict.com"},
            key=self.apikey.key,
            secret=self.apikey.secret,
            expiry=60
        )
        self.assertTrue(querystring.validate(str(signed_qs)))

    def test_fail_if_signed_request_expired(self):
        signed_qs = querystring.sign(
            {"kfid": 1},
            key=self.apikey.key,
            secret=self.apikey.secret,
            expiry=0
        )
        self.assertRaises(querystring.LinkExpired, querystring.validate, signed_qs)

    def assertValidationError(self, querystring, signed_qs):
        self.assertRaises(
            querystring.ValidationError, querystring.validate, signed_qs
        )

    def test_fail_if_signed_request_has_wrong_key(self):
        signed_qs = querystring.sign({"kfid": 1}, key="cheese", secret=self.apikey.secret)
        self.assertValidationError(querystring, signed_qs)

    def test_fail_if_signed_request_has_wrong_signature(self):
        signed_qs = querystring.sign({"kfid": 1}, key=self.apikey.key, secret="cheese")
        self.assertValidationError(querystring, signed_qs)
