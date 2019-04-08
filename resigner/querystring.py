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


class ValidationError(Exception):
    pass


def _generate_signature(params, secret, timestamp):
    signer = Signer(key=secret)
    encoded_params = json.dumps(params, sort_keys=True)
    return signer.signature(":".join([timestamp, encoded_params]))


def sign(params, key, secret):
    params = {str(k): str(v) for (k, v) in params.items()}
    timestamp = str(int(time.time()))

    params[SIGNATURE_TAG] = _generate_signature(params, secret, timestamp)
    params[KEY_TAG] = key
    params[TIMESTAMP_TAG] = timestamp

    return "{}".format(urlencode(params))


def validate(querystring, max_age=60*60):
    params = dict(parse_qsl(querystring))

    for key in [TIMESTAMP_TAG, KEY_TAG, SIGNATURE_TAG, ]:
        if key not in params:
            raise ValidationError("{0} must exist".format(key))

    key = params.pop(KEY_TAG)
    signature = params.pop(SIGNATURE_TAG)

    timestamp = params.pop(TIMESTAMP_TAG)
    time_stamp_expired = int(timestamp) + max_age


    if time.time() > time_stamp_expired:
        raise ValidationError("Timestamp Expired")

    try:
        api_key = ApiKey.objects.get(key=key)
    except ApiKey.DoesNotExist:
        raise ValidationError("Key does not exist")

    new_signature = _generate_signature(params, api_key.secret, timestamp)

    if new_signature != signature:
        raise ValidationError("Your signature was invalid")

    return True
