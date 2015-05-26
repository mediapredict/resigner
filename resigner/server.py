from functools import wraps
import time

from django.conf import settings
from django.core import signing
from django.http import Http404

from .models import ApiKey
from .utils import data_hash, get_settings_param, SERVER_TIME_STAMP_KEY, SERVER_API_SIGNATURE_KEY

def signed_req_required(api_secret_key_name):

    def _signed_req_required(view_func):

        def check_signature(request, *args, **kwargs):

            def is_time_stamp_valid():
                if not SERVER_TIME_STAMP_KEY in request.META.keys():
                    return False
                received_times_stamp = request.META[SERVER_TIME_STAMP_KEY]

                max_delay = get_settings_param("RESIGNER_TIME_STAMP_MAX_DELAY", 5*60)
                time_stamp_now = time.time()

                return (
                    abs(int(time_stamp_now) - int(received_times_stamp)) < max_delay
                )

            def is_signature_ok():
                if not SERVER_API_SIGNATURE_KEY in request.META.keys():
                    return False
                api_signature = request.META[SERVER_API_SIGNATURE_KEY]

                try:
                    api_secret_key = ApiKey.objects.get(key=api_secret_key_name).secret
                    time_stamp = request.META[SERVER_TIME_STAMP_KEY]
                    url = request.build_absolute_uri()
                    max_delay = get_settings_param("RESIGNER_API_MAX_DELAY", 10)

                    x_api_key_args = {
                        "s": api_signature,
                        "key": api_secret_key + data_hash(request.body, time_stamp, url),
                        "max_age": max_delay,
                        }
                    if settings.RESIGNER_X_API_KEY == signing.loads(**x_api_key_args):
                        return True

                except:
                    pass

                return False

            if is_time_stamp_valid() and is_signature_ok():
                return view_func(request, *args, **kwargs)
            else:
                raise Http404

        return wraps(view_func)(check_signature)

    return _signed_req_required