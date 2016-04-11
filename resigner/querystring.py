import time
import json
import urlparse
from urllib import urlencode
from django.core.signing import Signer

from resigner.models import ApiKey


class ValidationError(Exception):
    pass

def _generate_signature(params, secret, timestamp):
    signer = Signer(key=secret)
    encoded_params = json.dumps(params, sort_keys=True)
    return signer.signature(":".join([timestamp, encoded_params]))


def sign(params, key, secret):
    timestamp = str(int(time.time()))

    params["signature"] = _generate_signature(params, secret, timestamp)
    params["key"] = key
    params["timestamp"] = timestamp

    return urlencode(params)

def validate(querystring, max_age=60*60):
    params = dict(urlparse.parse_qsl(querystring))
    timestamp = int(params["timestamp"])
    time_stamp_expired = timestamp + max_age

    for key in ["timestamp", "key", "signature",]:
        if key not in params:
            raise ValidationError("{0} must exist".format(key))

    if time.time() > time_stamp_expired:
        raise ValidationError("Timestamp Expired")

    try:
        key = ApiKey.objects.get(key=params["key"])
    except ApiKey.DoesNotExist:
        raise ValidationError("Key does not exist")

    signature = _generate_signature(params, key.secret, timestamp)

    if signature != params["signature"]:
        raise ValidationError("Your signature was invalid")

    return True







