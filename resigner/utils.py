import hashlib

from django.conf import settings
from django.core.signing import Signer

HEADER_KEY_PREFIX = "RESIGNER"

add_prefix = lambda key : "{0}{1}{2}".format(HEADER_KEY_PREFIX, "-", key)
to_server_key = lambda key : "{0}{1}{2}".format("HTTP", "-", key).replace("-", "_")

CLIENT_TIME_STAMP_KEY = add_prefix("TIME-STAMP")
CLIENT_API_SIGNATURE_KEY = add_prefix("API-SIGNATURE")
CLIENT_API_KEY = add_prefix("X-API-KEY")

SERVER_TIME_STAMP_KEY = to_server_key(CLIENT_TIME_STAMP_KEY)
SERVER_API_SIGNATURE_KEY = to_server_key(CLIENT_API_SIGNATURE_KEY)
SERVER_API_KEY = to_server_key(CLIENT_API_KEY)

def get_signature(secret, body, timestamp, url):
    if not body:
        body = ""

    signer = Signer(key=secret)
    return signer.signature( ":".join([body, timestamp, url]) )

def get_settings_param(name, default=0):
    if hasattr(settings, name):
        return getattr(settings, name)
    else:
        return default