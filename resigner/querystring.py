import time
import json

from future import standard_library
standard_library.install_aliases()

from urllib.parse import urlencode, parse_qsl

from django.core.signing import Signer

from resigner.models import ApiKey


TIMESTAMP_TAG = "_timestamp"
KEY_TAG = "key"
SIGNATURE_TAG = "signature"
EXPIRY_TAG = "_expiry"


class ValidationError(Exception):
    pass


def _generate_signature(params, secret, timestamp, expiry):
    signer = Signer(key=secret)
    encoded_params = json.dumps(params, sort_keys=True)

    timestamp = str(timestamp)
    expiry = str(expiry)

    return signer.signature(":".join([timestamp, expiry, encoded_params]))


def sign(params, key, secret, expiry=60*60):
    params = {str(k): str(v) for (k, v) in params.items()}
    timestamp = int(time.time())

    params[SIGNATURE_TAG] = _generate_signature(params, secret, timestamp, expiry)
    params[KEY_TAG] = key
    params[TIMESTAMP_TAG] = timestamp
    params[EXPIRY_TAG] = expiry

    return "{}".format(urlencode(params))


def validate(querystring):
    params = dict(parse_qsl(querystring))

    for key in [TIMESTAMP_TAG, KEY_TAG, SIGNATURE_TAG, ]:
        if key not in params:
            raise ValidationError("{0} must exist".format(key))

    key = params.pop(KEY_TAG)
    signature = params.pop(SIGNATURE_TAG)

    try:
        timestamp = int(params.pop(TIMESTAMP_TAG))
        expiry = int(params.pop(EXPIRY_TAG))
    except ValueError:
        raise ValidationError("Incorrect parameters")

    time_stamp_expired = int(timestamp) + int(expiry)
    if time.time() > time_stamp_expired:
        raise ValidationError("Timestamp Expired")

    try:
        api_key = ApiKey.objects.get(key=key)
    except ApiKey.DoesNotExist:
        raise ValidationError("Key does not exist")

    new_signature = _generate_signature(params, api_key.secret, timestamp, expiry)
    if new_signature != signature:
        raise ValidationError("Your signature was invalid")

    return True
