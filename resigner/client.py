import requests
import hashlib

from django.core import signing


def _get_security_headers(req_body, x_api_key, api_secret_key):
    def data_hash():
        hash = hashlib.sha1()
        hash.update(str(req_body))
        print "*"*10, "SENDING", "*"*10, "[" , str(req_body), "]"
        return hash.hexdigest()[:10]

    value = signing.dumps(x_api_key, key=api_secret_key+data_hash())
    return {"X-API-SIGNATURE": value}

def _signed_send_req(method, url, data, x_api_key, api_secret_key):
    return method(url,
                  data=data,
                  headers=_get_security_headers(data, x_api_key, api_secret_key)
    )

def post_signed(url, data, x_api_key, api_secret_key):
    return _signed_send_req(
        requests.post, url, data, x_api_key, api_secret_key
    )

def get_signed(url, data, x_api_key, api_secret_key):
    return _signed_send_req(
        requests.get, url, data, x_api_key, api_secret_key
    )