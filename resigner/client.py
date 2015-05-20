import requests
import hashlib

from django.core import signing


def get_security_headers(req_body, x_api_key, api_secret_key,
                         header_api_key="X-API-SIGNATURE"):
    def data_hash():
        hash = hashlib.sha1()
        hash.update(str(req_body))
        print "*"*10, "SENDING", "*"*10, "[" , str(req_body), "]"
        return hash.hexdigest()[:10]

    value = signing.dumps(x_api_key, key=api_secret_key+data_hash())
    return {header_api_key: value}

def _send_req_signed(method, url, data, x_api_key, api_secret_key):
    headers = get_security_headers(data, x_api_key, api_secret_key)

    return method(url, data=data, headers=headers)

def post_signed(url, data, x_api_key, api_secret_key):
    return _send_req_signed(
        requests.post, url, data, x_api_key, api_secret_key
    )

def get_signed(url, data, x_api_key, api_secret_key):
    return _send_req_signed(
        requests.get, url, data, x_api_key, api_secret_key
    )