import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.conf import settings

from resigner.models import ApiKey
from resigner.client import get_security_headers

class TestSignedApi(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_key_secret_value = "some_test_secret_value"

        ApiKey.objects.create(
            key="MY_API_KEY",
            secret=self.api_key_secret_value,
        )

    def assertApiResult(self, res, result):
        self.assertEqual(json.loads(res.content)["result"], result)


    def call_api(self, data=None,
                 x_api_key=settings.X_API_KEY,
                 api_key_secret_value=None,
                 callback_func=None):

        url = reverse("my_test_api")

        if data == None:
            data = {u"MY_TEST_DATA": u"hello from test script!"}

        if api_key_secret_value == None:
            api_key_secret_value = self.api_key_secret_value

        headers = get_security_headers(
            data, x_api_key, api_key_secret_value, "HTTP_X_API_SIGNATURE"
        )

        if callback_func:
            callback_func()

        return self.client.get(url, data=data, **headers)

    def test_api_result_ok(self):
        res = self.call_api()

        self.assertEqual(res.status_code, 200)
        self.assertApiResult(res, "test ok")

    def test_api_result_nok(self):
        res = self.call_api({u"SOMETHING_UNEXPECTED": u"some_val"})

        self.assertEqual(res.status_code, 200)
        self.assertApiResult(res, "no data received")

    def test_wrong_x_api_key(self):
        res = self.call_api(x_api_key="some_wrong_x_api_key")
        self.assertEqual(res.status_code, 404)

    def test_wrong_secret(self):
        res = self.call_api(api_key_secret_value="wrong_secret")
        self.assertEqual(res.status_code, 404)

    def test_timeout(self):
        def simulate_delay():
            import time
            time.sleep(2)
        res = self.call_api(callback_func=simulate_delay)
        self.assertEqual(res.status_code, 404)
