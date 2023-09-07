from django.conf import settings
from django.core.signing import Signer

HEADER_KEY_PREFIX = "RESIGNER"


def add_prefix(key):
    return f"{HEADER_KEY_PREFIX}-{key}"


def to_server_key(key):
    return f"HTTP_{key}".replace("-", "_")


CLIENT_TIME_STAMP_KEY = add_prefix("TIME-STAMP")
CLIENT_API_SIGNATURE_KEY = add_prefix("API-SIGNATURE")
CLIENT_API_KEY = add_prefix("X-API-KEY")

SERVER_TIME_STAMP_KEY = to_server_key(CLIENT_TIME_STAMP_KEY)
SERVER_API_SIGNATURE_KEY = to_server_key(CLIENT_API_SIGNATURE_KEY)
SERVER_API_KEY = to_server_key(CLIENT_API_KEY)


def get_signature(secret, body, timestamp, url):
    if not body:
        body = ""

    # fallback_keys="" prevents fetching from django config
    # Our Analytics package is meant for use outside of django
    signer = Signer(key=secret, fallback_keys="")
    return signer.signature(f"{body}:{timestamp}:{url}")


def get_settings_param(name, default=0):
    return getattr(settings, name, default)
