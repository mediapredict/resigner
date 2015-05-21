from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client

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

    def test_update_api(self):
        from django.conf import settings

        data = {u"MY_TEST_DATA": "hello from test script!"}
        url = reverse("my_test_api")

        headers = get_security_headers(
            data, settings.X_API_KEY, self.api_key_secret_value, "HTTP_X_API_SIGNATURE"
        )
        res = self.client.get(url, data=data, **headers)
        self.assertEqual(res.status_code, 200)