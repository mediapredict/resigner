import time
from requests import Request, Session

from django.core.signing import Signer

from .utils import data_hash
from .utils import data_hash, get_settings_param, \
    CLIENT_TIME_STAMP_KEY, CLIENT_API_SIGNATURE_KEY, CLIENT_API_KEY


def _get_security_headers(req_body, key, secret, url,
                         header_api_key=CLIENT_API_SIGNATURE_KEY):
    time_stamp = str(int(time.time()))

    value = Signer(key=secret).sign(
        data_hash(req_body, time_stamp, url)
    )

    return {
        CLIENT_API_KEY: key, # uniquely identifies client
        header_api_key: value,
        CLIENT_TIME_STAMP_KEY: time_stamp
    }

def _create_signed_req(method, url, data, key, secret):
    req = Request(method, url, data=data)

    prepped = req.prepare()
    prepped.headers.update(
        _get_security_headers(prepped.body, key, secret, url)
    )

    return prepped

def _send_req(req):
    return Session().send(req)

def _send_signed_req(method, url, data, key, secret):
    return _send_req(
        _create_signed_req(method, url, data, key, secret)
    )

def post_signed(url, data, key, secret):
    return _send_signed_req(
        "POST", url, data, key, secret
    )

def get_signed(url, data, key, secret):
    return _send_signed_req(
        "GET", url, data, key, secret
    )