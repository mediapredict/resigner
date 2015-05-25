import time
from requests import Request, Session

from django.core import signing

from .utils import data_hash


def _get_security_headers(req_body, x_api_key, api_secret_key,
                         header_api_key="X-API-SIGNATURE"):
    time_stamp = str(int(time.time()))
    value = signing.dumps(x_api_key, key=api_secret_key+data_hash(req_body, time_stamp))

    return {header_api_key: value, "TIME-STAMP": time_stamp}

def _create_signed_req(method, url, data, x_api_key, api_secret_key):
    req = Request(method, url, data=data)

    prepped = req.prepare()
    prepped.headers.update(
        _get_security_headers(prepped.body, x_api_key, api_secret_key)
    )

    return prepped

def _send_req(req):
    return Session().send(req)

def _send_signed_req(method, url, data, x_api_key, api_secret_key):
    return _send_req(
        _create_signed_req(method, url, data, x_api_key, api_secret_key)
    )

def post_signed(url, data, x_api_key, api_secret_key):
    return _send_signed_req(
        "POST", url, data, x_api_key, api_secret_key
    )

def get_signed(url, data, x_api_key, api_secret_key):
    return _send_signed_req(
        "GET", url, data, x_api_key, api_secret_key
    )