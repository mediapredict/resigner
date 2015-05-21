from requests import Request, Session
import requests

from django.core import signing

from .utils import data_hash

def get_security_headers(req_body, x_api_key, api_secret_key,
                         header_api_key="X-API-SIGNATURE"):

    value = signing.dumps(x_api_key, key=api_secret_key+data_hash(req_body))
    return {header_api_key: value}

def _send_req_signed(method, url, data, x_api_key, api_secret_key):
    s = Session()
    req = Request(method, url, data=data)

    prepped = req.prepare()
    prepped.headers.update(get_security_headers(prepped.body, x_api_key, api_secret_key))

    return s.send(prepped)


def post_signed(url, data, x_api_key, api_secret_key):
    return _send_req_signed(
        "POST", url, data, x_api_key, api_secret_key
    )

def get_signed(url, data, x_api_key, api_secret_key):
    return _send_req_signed(
        "GET", url, data, x_api_key, api_secret_key
    )