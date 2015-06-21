import json
import time

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.conf import settings

from resigner.models import ApiKey
from resigner.client import post_signed, get_signed, _send_req, _create_signed_req
from resigner.utils import CLIENT_TIME_STAMP_KEY, CLIENT_API_SIGNATURE_KEY


class TestSignedApiBase(object):
    def setUpBase(self):
        self.client = Client()

        api_key_obj = ApiKey.objects.create()
        self.api_key = api_key_obj.key
        self.api_secret = api_key_obj.secret

        self.url = self.live_server_url + reverse("my_test_api")

    def assertApiResult(self, res, result):
        self.assertEqual(json.loads(res.content)["result"], result)

    def assert_200_res_ok(self, res):
        self.assertEqual(res.status_code, 200)
        self.assertApiResult(res, "test ok")

    def get_api_params(self, data=None,
                 api_key=None,
                 api_secret=None):


        if data == None:
            data = {u"MY_TEST_DATA": u"hello from test script!"}

        if api_key == None:
            api_key = self.api_key

        if api_secret == None:
            api_secret = self.api_secret

        return {
            "url": self.url,
            "data": data,
            "x_api_key": api_key,
            "api_secret_key": api_secret,
        }

    def call_api(self, data=None, key=None, secret=None):

        kwargs = self.get_api_params(data, key, secret)

        return self.api_func()(**kwargs)


    def test_api_result_ok(self):
        self.assert_200_res_ok(
            self.call_api()
        )

    def test_api_result_ok_dummy_param(self):
        self.url = self.url + "?dummy_param=33"
        self.assert_200_res_ok(
            self.call_api()
        )

    def test_wrong_x_api_key(self):
        res = self.call_api(key="some_wrong_x_api_key")
        self.assertEqual(res.status_code, 400)

    def test_wrong_secret(self):
        res = self.call_api(secret="wrong_secret")
        self.assertEqual(res.status_code, 404)


    def deconstructed_client_api_call(self, callback_func=None):
        params = self.get_api_params()

        req = _create_signed_req(self.method_name, **params)
        if callback_func:
            callback_func(req)

        return _send_req(req)

    def test_deconstructed_client_api_OK(self):
        self.assert_200_res_ok(
            self.deconstructed_client_api_call()
        )

    def test_deconstructed_client_api_max_timeout(self):
        def simulate_delay(req):
            time.sleep(1.1)
        res = self.deconstructed_client_api_call(simulate_delay)

        self.assertEqual(res.status_code, 404)

    def test_signature_missing(self):
        def simulate_missing_header(req):
            del req.headers[CLIENT_API_SIGNATURE_KEY]
        res = self.deconstructed_client_api_call(simulate_missing_header)

        self.assertEqual(res.status_code, 404)


    def selfAssertTimeStampDiff(self, diff, result):
        def simulate_outdated_timestamp(req):
            key = CLIENT_TIME_STAMP_KEY
            ts = req.headers[key.lower()]
            req.headers.update(
                {key: str( int(ts) + diff )}
            )

        res = self.deconstructed_client_api_call(simulate_outdated_timestamp)
        self.assertEqual(res.status_code, 404)

    def test_timestamp_a_bit_outdated(self):
        self.selfAssertTimeStampDiff(-25, 200)

    def test_timestamp_really_outdated(self):
        self.selfAssertTimeStampDiff(-6*60, 404)

    def test_timestamp_in_the_near_future(self):
        self.selfAssertTimeStampDiff(+20, 200)

    def test_timestamp_in_the_distant_future(self):
        self.selfAssertTimeStampDiff(10*60, 404)

    def test_time_stamp_missing(self):
        def simulate_missing_header(req):
            del req.headers[CLIENT_TIME_STAMP_KEY]
        res = self.deconstructed_client_api_call(simulate_missing_header)

        self.assertEqual(res.status_code, 404)


    def test_signature_changes_each_second(self):
        signatures = []
        def collect_signatures(req):
            signatures.append(req.headers[CLIENT_API_SIGNATURE_KEY])

        send = lambda : self.assert_200_res_ok(
                self.deconstructed_client_api_call(callback_func=collect_signatures)
        )
        sleep = lambda : time.sleep(1)

        [func() for func in [send, sleep, send, sleep, send]]

        # all signatures are different
        self.assertEqual(len(set(signatures)), 3)


class TestSignedApiGet(LiveServerTestCase, TestSignedApiBase):
    method_name = "GET"

    def setUp(self):
        self.setUpBase()

    def api_func(self):
        return get_signed


class TestSignedApiPost(LiveServerTestCase, TestSignedApiBase):
    method_name = "POST"

    def setUp(self):
        self.setUpBase()

    def api_func(self):
        return post_signed

    def test_api_result_ok_answer_not_ok(self):
        res = self.call_api({u"SOMETHING_UNEXPECTED": u"some_val"})

        self.assertEqual(res.status_code, 200)
        self.assertApiResult(res, "no data received")