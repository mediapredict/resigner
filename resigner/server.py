from functools import wraps

from django.conf import settings
from django.core import signing
from django.http import Http404

from .models import ApiKey
from .utils import data_hash


def signed_req_required(api_secret_key_name):

    def _signed_req_required(view_func):

        def check_signature(request, *args, **kwargs):

            def is_signature_ok():
                api_signature = request.META["HTTP_X_API_SIGNATURE"]
                if hasattr(settings, 'RESIGNER_API_MAX_DELAY'):
                    max_delay = settings.RESIGNER_API_MAX_DELAY
                else:
                    max_delay = 10

                try:
                    api_secret_key = ApiKey.objects.get(key=api_secret_key_name).secret
                    x_api_key_args = {
                        "s": api_signature,
                        "key": api_secret_key + data_hash(request.body),
                        "max_age": max_delay,
                        }
                    if settings.RESIGNER_X_API_KEY == signing.loads(**x_api_key_args):
                        return True

                except:
                    pass

                return False

            if "HTTP_X_API_SIGNATURE" in request.META.keys() and is_signature_ok():
                return view_func(request, *args, **kwargs)
            else:
                raise Http404

        return wraps(view_func)(check_signature)

    return _signed_req_required