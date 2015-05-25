import json
import time

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.conf import settings

from resigner.models import ApiKey
from resigner.client import post_signed, _send_req, _create_signed_req

class TestSignedApi(LiveServerTestCase):
    def setUp(self):
        self.client = Client()
        self.api_key_secret_value = "some_test_secret_value"

        ApiKey.objects.create(
            key="MY_API_KEY",
            secret=self.api_key_secret_value,
        )

        self.url = self.live_server_url + reverse("my_test_api")

    def assertApiResult(self, res, result):
        self.assertEqual(json.loads(res.content)["result"], result)

    def assert_200_res_ok(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertApiResult(res, "test ok")

    def get_api_params(self, data=None,
                 x_api_key=settings.RESIGNER_X_API_KEY,
                 api_key_secret_value=None):

        if data == None:
            data = {u"MY_TEST_DATA": u"hello from test script!"}

        if api_key_secret_value == None:
            api_key_secret_value = self.api_key_secret_value

        return {
            "url": self.url,
            "data": data,
            "x_api_key": x_api_key,
            "api_secret_key": api_key_secret_value,
        }

    def call_api(self, data=None,
                 x_api_key=settings.RESIGNER_X_API_KEY,
                 api_key_secret_value=None):

        kwargs = self.get_api_params(data, x_api_key, api_key_secret_value)

        return post_signed(**kwargs)

    def test_api_result_ok(self):
        self.assert_200_res_ok(
            self.call_api()
        )

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


    def deconstructed_client_api_call(self, callback_func=None, method="POST"):
        params = self.get_api_params()

        req = _create_signed_req(method, **params)
        if callback_func:
            callback_func(req)

        return _send_req(req)

    def test_deconstructed_client_api_OK(self):
        self.assert_200_res_ok(
            self.deconstructed_client_api_call()
        )

    def test_deconstructed_client_api_max_timeout(self):
        def simulate_delay(req):
            time.sleep(1)
        res = self.deconstructed_client_api_call(simulate_delay)

        self.assertEqual(res.status_code, 404)

    def test_deconstructed_client_signature_missing(self):
        def simulate_missing_header(req):
            del req.headers["X-API-SIGNATURE"]
        res = self.deconstructed_client_api_call(simulate_missing_header)

        self.assertEqual(res.status_code, 404)

    def test_deconstructed_client_time_stamp_missing(self):
        def simulate_missing_header(req):
            del req.headers["TIME-STAMP"]
        res = self.deconstructed_client_api_call(simulate_missing_header)

        self.assertEqual(res.status_code, 404)

    def assert_signature_each_second_different(self, method):
        signatures = []
        def collect_signatures(req):
            signatures.append(req.headers["X-API-SIGNATURE"])

        def send_api_req():
            self.assert_200_res_ok(
                self.deconstructed_client_api_call(
                    callback_func=collect_signatures, method=method
                )
            )

        send_api_req()

        time.sleep(1)
        send_api_req()

        time.sleep(1)
        send_api_req()

        self.assertEqual(len(set(signatures)), 3)

    def test_post_req_signature_each_second_different(self):
        self.assert_signature_each_second_different("POST")

    def test_get_req_signature_each_second_different(self):
        self.assert_signature_each_second_different("GET")
