import time
from requests import Request, Session

from django.core.signing import Signer

from .utils import data_hash
from .utils import data_hash, get_settings_param, \
    CLIENT_TIME_STAMP_KEY, CLIENT_API_SIGNATURE_KEY, CLIENT_API_KEY


def _get_security_headers(req_body, x_api_key, api_secret_key, url,
                         header_api_key=CLIENT_API_SIGNATURE_KEY):
    time_stamp = str(int(time.time()))

    value = Signer(key=api_secret_key).sign(
        data_hash(req_body, time_stamp, url)
    )

    return {
        CLIENT_API_KEY: x_api_key, # uniquely identifies client
        header_api_key: value,
        CLIENT_TIME_STAMP_KEY: time_stamp
    }

def _create_signed_req(method, url, data, x_api_key, api_secret_key):
    req = Request(method, url, data=data)

    prepped = req.prepare()
    prepped.headers.update(
        _get_security_headers(prepped.body, x_api_key, api_secret_key, url)
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