import hashlib

from django.conf import settings

HEADER_KEY_PREFIX = "RESIGNER"

add_prefix = lambda key : "{0}{1}{2}".format(HEADER_KEY_PREFIX, "-", key)
to_server_key = lambda key : "{0}{1}{2}".format("HTTP", "-", key).replace("-", "_")

CLIENT_TIME_STAMP_KEY = add_prefix("TIME-STAMP")
CLIENT_API_SIGNATURE_KEY = add_prefix("API-SIGNATURE")

SERVER_TIME_STAMP_KEY = to_server_key(CLIENT_TIME_STAMP_KEY)
SERVER_API_SIGNATURE_KEY = to_server_key(CLIENT_API_SIGNATURE_KEY)

def data_hash(req_body, time_stamp, url):
    hash = hashlib.sha1()
    hash.update(req_body + time_stamp + url)
    return hash.hexdigest()[:10]

def get_settings_param(name, default=0):
    if hasattr(settings, name):
        return getattr(settings, name)
    else:
        return default