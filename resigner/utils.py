import hashlib

from django.conf import settings

def data_hash(req_body, time_stamp, url):
    hash = hashlib.sha1()
    hash.update(req_body + time_stamp + url)
    return hash.hexdigest()[:10]

def get_settings_param(name, default=0):
    if hasattr(settings, name):
        return getattr(settings, name)
    else:
        return default